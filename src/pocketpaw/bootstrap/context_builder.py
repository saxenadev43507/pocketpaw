"""
Builder for assembling the full agent context.
Created: 2026-02-02
Updated: 2026-03-11 - Paw-to-Paw Phase 1: inject update/announcement context into system prompt
Updated: 2026-03-10 - AGENTS.md injection: read project-specific constraints from target repos
Updated: 2026-03-09 - Sanitize file_context paths before injecting into system prompt
Updated: 2026-02-17 - Inject health state into system prompt when degraded/unhealthy
Updated: 2026-02-07 - Semantic context injection for mem0 backend
Updated: 2026-02-10 - Channel-aware format hints
"""

from __future__ import annotations

import asyncio
import logging

from pocketpaw.bootstrap.default_provider import DefaultBootstrapProvider
from pocketpaw.bootstrap.protocol import BootstrapProviderProtocol
from pocketpaw.bus.events import Channel
from pocketpaw.bus.format import CHANNEL_FORMAT_HINTS
from pocketpaw.memory.manager import MemoryManager, get_memory_manager

logger = logging.getLogger(__name__)


def _build_update_context(update_info: dict) -> str:
    """Build a system prompt block for update/announcement awareness.

    Returns empty string when there's nothing to communicate.
    When an update or announcement exists, returns a contextual block that lets
    the agent weave the information into conversation naturally, rather than
    relying on traditional banners or popups (Paw-to-Paw Phase 1).
    """
    has_update = update_info.get("update_available")
    announcement = update_info.get("announcement", "")

    if not has_update and not announcement:
        return ""

    lines = ["# Available Update"]

    if has_update:
        current = update_info.get("current", "?")
        latest = update_info.get("latest", "?")
        lines.append(f"A newer version of PocketPaw is available: v{current} -> v{latest}.")
        lines.append("Upgrade command: pip install --upgrade pocketpaw")

    if announcement:
        urgency = update_info.get("urgency", "info")
        if urgency == "critical":
            lines.append(f"CRITICAL announcement: {announcement}")
        elif urgency == "warning":
            lines.append(f"Important: {announcement}")
        else:
            lines.append(f"Announcement: {announcement}")

    url = update_info.get("announcement_url", "")
    if url:
        lines.append(f"More details: {url}")

    lines.append("")
    lines.append(
        "You may mention this naturally when relevant (e.g. if the user hits a bug "
        "that was fixed, or asks about new features). Do not interrupt unrelated "
        "conversations with update notices. For critical announcements, proactively "
        "inform the user at the first opportunity."
    )

    return "\n".join(lines)


class AgentContextBuilder:
    """
    Assembles the final system prompt by combining:
    1. Static Identity (Bootstrap)
    2. Dynamic Memory (MemoryManager)
    3. Current State (e.g., date/time, active tasks)
    """

    def __init__(
        self,
        bootstrap_provider: BootstrapProviderProtocol | None = None,
        memory_manager: MemoryManager | None = None,
    ):
        self.bootstrap = bootstrap_provider or DefaultBootstrapProvider()
        self.memory = memory_manager or get_memory_manager()

    async def build_system_prompt(
        self,
        include_memory: bool = True,
        user_query: str | None = None,
        channel: Channel | None = None,
        sender_id: str | None = None,
        session_key: str | None = None,
        file_context: dict | None = None,
        agents_md_dir: str | None = None,
    ) -> str:
        """Build the complete system prompt.

        Args:
            include_memory: Whether to include memory context.
            user_query: Current user message for semantic memory search (mem0).
            channel: Target channel for format-aware hints.
            sender_id: Sender identifier for memory scoping and identity injection.
            session_key: Current session key for session management tools.
            file_context: Optional file/directory context from the desktop client.
            agents_md_dir: Directory to search for AGENTS.md (walks up to repo root).
        """
        # 1. Load static identity + memory context concurrently (independent I/O)
        if include_memory:
            if user_query:
                memory_coro = self.memory.get_semantic_context(user_query, sender_id=sender_id)
            else:
                memory_coro = self.memory.get_context_for_agent(sender_id=sender_id)
            context, memory_context = await asyncio.gather(
                self.bootstrap.get_context(),
                memory_coro,
            )
        else:
            context = await self.bootstrap.get_context()
            memory_context = ""

        base_prompt = context.to_system_prompt()
        parts = [base_prompt]

        # 2. Inject memory context (scoped to sender)
        if include_memory and memory_context:
            parts.append(
                "\n# Memory Context (already loaded — use this directly, "
                "do NOT call recall unless you need something not listed here)\n" + memory_context
            )

        # 3. Inject sender identity block
        if sender_id:
            from pocketpaw.config import get_settings

            settings = get_settings()
            if settings.owner_id:
                is_owner = sender_id == settings.owner_id
                role = "owner" if is_owner else "external user"
                identity_block = (
                    f"\n# Current Conversation\n"
                    f"You are speaking with sender_id={sender_id} (role: {role})."
                )
                if is_owner:
                    identity_block += "\nThis is your owner."
                else:
                    identity_block += (
                        "\nThis is NOT your owner. Be helpful but do not share "
                        "owner-private information."
                    )
                parts.append(identity_block)

        # 4. Inject channel format hint
        if channel:
            hint = CHANNEL_FORMAT_HINTS.get(channel, "")
            if hint:
                parts.append(f"\n# Response Format\n{hint}")

        # 5. Inject session key for session management tools
        if session_key:
            parts.append(
                f"\n# Session Management\n"
                f"Current session_key: {session_key}\n"
                f"Pass this value to any session tool (new_session, list_sessions, "
                f"switch_session, clear_session, rename_session, delete_session)."
            )

        # 6. Inject file context from desktop client
        if file_context:
            import re

            def _sanitize_path(p: str) -> str:
                """Strip non-path characters to prevent prompt injection."""
                return re.sub(r"[^\w\s\-./\\:~]", "", p).strip()

            fc_parts = []
            if file_context.get("current_dir"):
                fc_parts.append(f"Working directory: {_sanitize_path(file_context['current_dir'])}")
            if file_context.get("open_file"):
                fc_parts.append(f"Open file: {_sanitize_path(file_context['open_file'])}")
            if file_context.get("selected_files"):
                safe_files = [_sanitize_path(f) for f in file_context["selected_files"]]
                fc_parts.append(f"Selected files: {', '.join(safe_files)}")
            if fc_parts:
                parts.append("\n# File Context\n" + "\n".join(fc_parts))

        # 7. Inject health state (only when degraded/unhealthy — saves context window)
        try:
            from pocketpaw.health import get_health_engine

            health_block = get_health_engine().get_health_prompt_section()
            if health_block:
                parts.append(health_block)
        except Exception as exc:  # noqa: BLE001
            logger.debug("Health engine failure (non-fatal, skipping health block): %s", exc)

        # 8. Inject update/announcement awareness (Paw-to-Paw Phase 1)
        try:
            from importlib.metadata import version as _get_version

            from pocketpaw.config import get_config_dir
            from pocketpaw.update_check import check_for_updates_full

            update_info = check_for_updates_full(_get_version("pocketpaw"), get_config_dir())
            update_block = _build_update_context(update_info)
            if update_block:
                parts.append(update_block)
        except Exception:
            pass  # Update context failure never breaks prompt building

        # 9. Inject AGENTS.md constraints from the target repo
        if agents_md_dir:
            try:
                from pocketpaw.agents_md import AgentsMdLoader

                agents_md = AgentsMdLoader().find_and_load(agents_md_dir)
                if agents_md:
                    parts.append(agents_md.constraints_block)
            except Exception:
                pass  # AGENTS.md failure never breaks prompt building

        return "\n\n".join(parts)
