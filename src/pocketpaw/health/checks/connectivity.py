"""Connectivity health checks -- LLM API reachability."""

from __future__ import annotations

from pocketpaw.health.checks.result import HealthCheckResult


async def check_llm_reachable() -> HealthCheckResult:
    """Check that the configured LLM API responds (5s timeout)."""
    from pocketpaw.config import get_settings

    settings = get_settings()
    backend = settings.agent_backend

    if backend == "claude_agent_sdk":
        return await _check_anthropic_reachable(settings)
    elif backend == "google_adk":
        return await _check_google_reachable(settings)
    elif backend == "openai_agents":
        return await _check_openai_reachable(settings)

    return HealthCheckResult(
        check_id="llm_reachable",
        name="LLM Reachable",
        category="connectivity",
        status="ok",
        message=f"Connectivity check not implemented for {backend}",
        fix_hint="",
    )


async def _check_anthropic_reachable(settings) -> HealthCheckResult:
    try:
        import os

        import httpx

        api_key = settings.anthropic_api_key
        if not api_key:
            api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            return HealthCheckResult(
                check_id="llm_reachable",
                name="LLM Reachable",
                category="connectivity",
                status="warning",
                message="No API key to test connectivity",
                fix_hint="Set your Anthropic API key first.",
            )

        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                "https://api.anthropic.com/v1/models",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                },
            )
        if resp.status_code == 200:
            return HealthCheckResult(
                check_id="llm_reachable",
                name="LLM Reachable",
                category="connectivity",
                status="ok",
                message="Anthropic API is reachable and key is valid",
                fix_hint="",
            )
        elif resp.status_code in (401, 403):
            return HealthCheckResult(
                check_id="llm_reachable",
                name="LLM Reachable",
                category="connectivity",
                status="critical",
                message=(f"Anthropic API reachable but key is invalid (HTTP {resp.status_code})"),
                fix_hint="Check your API key in Settings > API Keys.",
            )
        return HealthCheckResult(
            check_id="llm_reachable",
            name="LLM Reachable",
            category="connectivity",
            status="warning",
            message=f"Anthropic API returned HTTP {resp.status_code}",
            fix_hint="Check https://status.anthropic.com for outages.",
        )
    except Exception as e:
        return HealthCheckResult(
            check_id="llm_reachable",
            name="LLM Reachable",
            category="connectivity",
            status="critical",
            message=f"Cannot reach Anthropic API: {e}",
            fix_hint="Check your internet connection or https://status.anthropic.com",
        )


async def _check_google_reachable(settings) -> HealthCheckResult:
    try:
        import os

        import httpx

        api_key = settings.google_api_key or os.environ.get("GOOGLE_API_KEY", "")
        if not api_key:
            return HealthCheckResult(
                check_id="llm_reachable",
                name="LLM Reachable",
                category="connectivity",
                status="warning",
                message="No Google API key to test connectivity",
                fix_hint="Set your Google API key first.",
            )

        model = settings.google_adk_model or "gemini-2.5-flash"
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model}",
                params={"key": api_key},
            )
        if resp.status_code == 200:
            return HealthCheckResult(
                check_id="llm_reachable",
                name="LLM Reachable",
                category="connectivity",
                status="ok",
                message=f"Google AI API is reachable (model: {model})",
                fix_hint="",
            )
        elif resp.status_code in (401, 403):
            return HealthCheckResult(
                check_id="llm_reachable",
                name="LLM Reachable",
                category="connectivity",
                status="critical",
                message=f"Google AI API reachable but key is invalid (HTTP {resp.status_code})",
                fix_hint="Check your Google API key in Settings > API Keys.",
            )
        return HealthCheckResult(
            check_id="llm_reachable",
            name="LLM Reachable",
            category="connectivity",
            status="warning",
            message=f"Google AI API returned HTTP {resp.status_code}",
            fix_hint="Check your Google API key and model name.",
        )
    except Exception as e:
        return HealthCheckResult(
            check_id="llm_reachable",
            name="LLM Reachable",
            category="connectivity",
            status="critical",
            message=f"Cannot reach Google AI API: {e}",
            fix_hint="Check your internet connection.",
        )


async def _check_openai_reachable(settings) -> HealthCheckResult:
    try:
        import os

        import httpx

        api_key = settings.openai_api_key or os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            return HealthCheckResult(
                check_id="llm_reachable",
                name="LLM Reachable",
                category="connectivity",
                status="warning",
                message="No OpenAI API key to test connectivity",
                fix_hint="Set your OpenAI API key first.",
            )

        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                "https://api.openai.com/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
            )
        if resp.status_code == 200:
            return HealthCheckResult(
                check_id="llm_reachable",
                name="LLM Reachable",
                category="connectivity",
                status="ok",
                message="OpenAI API is reachable and key is valid",
                fix_hint="",
            )
        elif resp.status_code in (401, 403):
            return HealthCheckResult(
                check_id="llm_reachable",
                name="LLM Reachable",
                category="connectivity",
                status="critical",
                message=f"OpenAI API reachable but key is invalid (HTTP {resp.status_code})",
                fix_hint="Check your OpenAI API key in Settings > API Keys.",
            )
        else:
            return HealthCheckResult(
                check_id="llm_reachable",
                name="LLM Reachable",
                category="connectivity",
                status="warning",
                message=f"OpenAI API returned unexpected HTTP {resp.status_code}",
                fix_hint="Check https://status.openai.com for outages.",
            )
    except Exception as e:
        return HealthCheckResult(
            check_id="llm_reachable",
            name="LLM Reachable",
            category="connectivity",
            status="critical",
            message=f"Cannot reach OpenAI API: {e}",
            fix_hint="Check your internet connection.",
        )
