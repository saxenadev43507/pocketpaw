<!-- ChatPanel.svelte — Full-viewport chat tab for the Agent OS.
     Updated: 2026-03-22 — No floating window, no traffic lights.
     Full viewport below top bar, glass background, native AI chat.
-->
<script lang="ts">
  import { onMount, tick } from "svelte";
  import ArrowUp from "@lucide/svelte/icons/arrow-up";
  import Mic from "@lucide/svelte/icons/mic";
  import Video from "@lucide/svelte/icons/video";
  import Phone from "@lucide/svelte/icons/phone";

  let { onClose }: { onClose: () => void } = $props();

  type Role = "user" | "agent";
  type Message = { id: string; role: Role; content: string; time: string };

  function nowTime() {
    return new Date().toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit", hour12: false });
  }

  let messages = $state<Message[]>([
    { id: "m1", role: "user", content: "Can you tell me something about you", time: "09:14" },
    { id: "m2", role: "agent", content: `The time required to learn genetics and biotechnology depends on several factors, including the desired level of understanding, prior knowledge, study habits, and resources. Here's a structured overview:\n\n1. Basic Understanding (1-3 months):\n  • Level: Foundational knowledge.\n  • Content: Covers DNA structure, genes, basic genetic principles, and an introduction to biotechnology applications.\n  • Study Habits: Consistent daily study sessions using textbooks, online courses, and educational videos.\n\n2. Intermediate Understanding (6-12 months):\n  • Level: Intermediate knowledge.\n  • Content: Includes genetic engineering, lab techniques, and biotechnology applications.\n  • Study Habits: Regular study sessions, participation in online forums, and practical experiments or simulations.\n\n3. Advanced Understanding (1-2 years):\n  • Level: Advanced knowledge.\n  • Content: Delves into CRISPR, gene editing, and the business aspects of biotechnology.\n  • Study Habits: Intensive study, possibly including formal courses or certifications, and hands-on lab experience.`, time: "09:14" },
  ]);

  let inputValue = $state("");
  let isTyping = $state(false);
  let messagesEl: HTMLDivElement | null = null;

  const MOCK_RESPONSES = [
    "Got it. I'm on it — I'll update you when this is done.",
    "Great idea. Let me research that and come back with a structured plan.",
    "Sure, I'll configure that right now. You should see the results in a few seconds.",
    "I've noted that. Want me to set a reminder or create a task in your Pockets?",
    "Interesting. I'll analyze that and give you a detailed breakdown shortly.",
  ];

  async function scrollToBottom() {
    await tick();
    if (messagesEl) messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  async function sendMessage() {
    const text = inputValue.trim();
    if (!text || isTyping) return;
    inputValue = "";
    messages = [...messages, { id: `m${Date.now()}`, role: "user", content: text, time: nowTime() }];
    await scrollToBottom();
    isTyping = true;
    await scrollToBottom();
    await new Promise((r) => setTimeout(r, 800));
    messages = [...messages, {
      id: `m${Date.now() + 1}`, role: "agent",
      content: MOCK_RESPONSES[Math.floor(Math.random() * MOCK_RESPONSES.length)],
      time: nowTime(),
    }];
    isTyping = false;
    await scrollToBottom();
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  }

  function renderMarkdown(text: string): string {
    const lines = text.split("\n");
    const out: string[] = [];
    for (const line of lines) {
      if (/^\s+[•·-]\s/.test(line)) { out.push(`<div class="md-bullet">${inlineMd(line.replace(/^\s+[•·-]\s/, ""))}</div>`); continue; }
      if (/^\d+\.\s/.test(line)) { out.push(`<div class="md-numbered">${inlineMd(line)}</div>`); continue; }
      if (line.trim() === "") { out.push('<div class="md-gap"></div>'); continue; }
      out.push(`<div class="md-line">${inlineMd(line)}</div>`);
    }
    return out.join("");
  }

  function inlineMd(text: string): string {
    return text.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  }

  let visible = $state(false);
  onMount(() => { scrollToBottom(); requestAnimationFrame(() => { visible = true; }); });
</script>

<!-- Full-viewport chat panel -->
<div class={visible ? "chat-panel chat-visible liquid-glass glass-noise" : "chat-panel liquid-glass glass-noise"}>
  <!-- Messages area — centered, max-width for readability -->
  <div class="messages-area" bind:this={messagesEl} aria-live="polite">
    <div class="messages-inner">
      {#each messages as msg (msg.id)}
        {#if msg.role === "user"}
          <div class="msg msg-user">
            <div class="user-bubble liquid-glass">{msg.content}</div>
          </div>
        {:else}
          <div class="msg msg-agent">
            <div class="agent-card liquid-glass">
              <div class="md-content">{@html renderMarkdown(msg.content)}</div>
            </div>
          </div>
        {/if}
      {/each}

      {#if isTyping}
        <div class="msg msg-agent">
          <div class="agent-card liquid-glass typing-card">
            <span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>
          </div>
        </div>
      {/if}
    </div>
  </div>

  <!-- Bottom input pill -->
  <footer class="input-footer">
    <div class="input-pill liquid-glass">
      <img class="input-avatar" src="/paw-avatar.png" alt="" aria-hidden="true" />
      <input
        class="chat-input" type="text" placeholder="Type your message..."
        bind:value={inputValue} onkeydown={handleKeydown}
        disabled={isTyping} autocomplete="off" spellcheck="false"
      />
      <span class="input-action"><Mic size={16} strokeWidth={1.8} /></span>
      <span class="input-action"><Video size={16} strokeWidth={1.8} /></span>
      <span class="input-action"><Phone size={16} strokeWidth={1.8} /></span>
      <button class="send-btn" onclick={sendMessage} disabled={!inputValue.trim() || isTyping}>
        <ArrowUp size={16} strokeWidth={2} />
      </button>
    </div>
  </footer>
</div>

<style>
  .chat-panel {
    position: fixed;
    top: 32px;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 50;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    opacity: 0;
    transition: opacity 200ms ease;
    border-top: 1px solid rgba(255,255,255,0.06);
  }
  .chat-visible { opacity: 1; }

  /* Messages */
  .messages-area {
    flex: 1; overflow-y: auto; padding: 24px 16px;
    display: flex; justify-content: center;
    scrollbar-width: thin; scrollbar-color: rgba(255,255,255,0.10) transparent;
  }
  .messages-area::-webkit-scrollbar { width: 4px; }
  .messages-area::-webkit-scrollbar-track { background: transparent; }
  .messages-area::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.10); border-radius: 2px; }

  .messages-inner {
    width: 100%;
    max-width: 720px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .msg { display: flex; flex-direction: column; }
  .msg-user { align-items: flex-end; }
  .msg-agent { align-items: flex-start; }

  .user-bubble {
    max-width: 70%;
    padding: 10px 16px;
    border-radius: 18px 18px 6px 18px;
    font-size: 14px; line-height: 1.55;
    color: rgba(255,255,255,0.88);
  }

  .agent-card {
    width: 100%;
    padding: 16px 20px;
    border-radius: 14px;
    font-size: 14px; line-height: 1.6;
    color: rgba(255,255,255,0.85);
  }

  :global(.md-content .md-line) { margin: 0; }
  :global(.md-content .md-gap) { height: 8px; }
  :global(.md-content .md-numbered) { margin: 2px 0; padding-left: 8px; }
  :global(.md-content .md-bullet) { margin: 1px 0; padding-left: 24px; position: relative; }
  :global(.md-content .md-bullet::before) { content: "•"; position: absolute; left: 12px; color: rgba(255,255,255,0.50); }
  :global(.md-content strong) { font-weight: 600; color: rgba(255,255,255,0.95); }

  .typing-card {
    display: flex; align-items: center; gap: 4px;
    padding: 14px 20px; width: auto;
  }
  .typing-dot {
    display: inline-block; width: 6px; height: 6px; border-radius: 50%;
    background: rgba(255,255,255,0.40);
    animation: typing-bounce 1.2s ease-in-out infinite;
  }
  .typing-dot:nth-child(2) { animation-delay: 0.18s; }
  .typing-dot:nth-child(3) { animation-delay: 0.36s; }
  @keyframes typing-bounce {
    0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
    40% { transform: translateY(-4px); opacity: 0.85; }
  }

  /* Input footer */
  .input-footer {
    flex-shrink: 0;
    padding: 12px 16px 20px;
    display: flex;
    justify-content: center;
  }

  .input-pill {
    display: flex; align-items: center; gap: 8px;
    height: 52px; padding: 0 10px 0 8px;
    border-radius: 100px;
    width: 100%; max-width: 720px;
  }

  .input-avatar {
    width: 34px; height: 34px; border-radius: 50%;
    border: 2px solid rgba(255,255,255,0.50);
    flex-shrink: 0;
    object-fit: cover;
  }

  .chat-input {
    flex: 1; background: none; border: none; outline: none;
    height: 100%; font-size: 14px; font-family: inherit;
    color: rgba(255,255,255,0.85); caret-color: #0A84FF;
  }
  .chat-input::placeholder { color: rgba(255,255,255,0.30); }
  .chat-input:disabled { opacity: 0.5; }

  .input-action {
    display: flex; align-items: center; justify-content: center;
    width: 28px; height: 28px; border-radius: 50%;
    color: rgba(255,255,255,0.40); cursor: pointer;
    transition: color 0.15s, background 0.15s;
  }
  .input-action:hover { color: rgba(255,255,255,0.75); background: rgba(255,255,255,0.08); }

  .send-btn {
    width: 32px; height: 32px; border-radius: 50%; border: none;
    background: rgba(255,255,255,0.20); color: white;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; flex-shrink: 0; transition: background 0.15s, opacity 0.15s;
  }
  .send-btn:hover:not(:disabled) { background: rgba(255,255,255,0.30); }
  .send-btn:disabled { opacity: 0.3; cursor: not-allowed; }
</style>
