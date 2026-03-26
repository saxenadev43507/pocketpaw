<!-- LegalPocket.svelte — Mock Legal Case Management Pocket for PocketPaw Agent OS.
     Created: 2026-03-26 — Dark terminal-style law firm dashboard with case header,
     deadline alerts, document repository, billable hours, case timeline, AI insights,
     and team strip. All mock data, no API calls.
-->
<script lang="ts">
  import Scale from "@lucide/svelte/icons/scale";
  import FileText from "@lucide/svelte/icons/file-text";
  import Clock from "@lucide/svelte/icons/clock";
  import AlertTriangle from "@lucide/svelte/icons/alert-triangle";
  import Brain from "@lucide/svelte/icons/brain";
  import Users from "@lucide/svelte/icons/users";
  import Gavel from "@lucide/svelte/icons/gavel";
  import Calendar from "@lucide/svelte/icons/calendar";
  import CircleDot from "@lucide/svelte/icons/circle-dot";
  import CheckCircle from "@lucide/svelte/icons/check-circle-2";
  import FileSearch from "@lucide/svelte/icons/file-search";
  import FilePen from "@lucide/svelte/icons/file-pen";
  import FileCheck from "@lucide/svelte/icons/file-check";
  import Send from "@lucide/svelte/icons/send";

  const deadlines = [
    { label: "Motion response due", days: 3, color: "#FF453A", bg: "rgba(255,69,58,0.12)" },
    { label: "Discovery deadline", days: 12, color: "#FF9F0A", bg: "rgba(255,159,10,0.12)" },
    { label: "Deposition scheduled", days: 18, color: "#30D158", bg: "rgba(48,209,88,0.12)" },
  ];

  const documents = [
    { name: "Complaint", type: "filing", date: "Jan 15", author: "J. Park", status: "Filed", statusColor: "#30D158" },
    { name: "Answer", type: "filing", date: "Feb 12", author: "Opp. Counsel", status: "Filed", statusColor: "#30D158" },
    { name: "Discovery Requests", type: "discovery", date: "Feb 28", author: "M. Chen", status: "Sent", statusColor: "#0A84FF" },
    { name: "Expert Report Draft", type: "draft", date: "Mar 18", author: "J. Park", status: "Draft", statusColor: "#FF9F0A" },
    { name: "Settlement Offer", type: "letter", date: "Mar 22", author: "J. Park", status: "Review", statusColor: "#BF5AF2" },
  ];

  const docIcons: Record<string, typeof FileText> = {
    filing: FileCheck,
    discovery: FileSearch,
    draft: FilePen,
    letter: Send,
  };

  const weeklyHours = [18, 22, 14, 20, 16, 12];
  const maxHours = Math.max(...weeklyHours);

  const timeline = [
    { label: "Filed", date: "Jan 15", done: true },
    { label: "Answer Received", date: "Feb 12", done: true },
    { label: "Discovery Phase", date: "Feb 28", done: true, current: true },
    { label: "Depositions", date: "Apr 10", done: false },
    { label: "Expert Reports", date: "May 5", done: false },
    { label: "Mediation", date: "Jun 2", done: false },
    { label: "Trial", date: "Jul 14", done: false },
  ];

  const insights = [
    "Opposing counsel cited <strong>Morrison v. National</strong> in their brief — this precedent was overturned in 2024. Flag for response.",
    "<strong>3 discovery requests</strong> unanswered past 5 days — deadline risk escalating.",
    "Similar case settled for <strong>$340K</strong> in 2025 — relevant data point for negotiation strategy.",
  ];

  const team = [
    { name: "Jane Park", role: "Lead Attorney", color: "#0A84FF", online: true },
    { name: "Mike Chen", role: "Associate", color: "#30D158", online: true },
    { name: "Sarah Lin", role: "Paralegal", color: "#FF9F0A", online: false },
    { name: "AI Legal Agent", role: "Analysis", color: "#BF5AF2", online: true },
  ];
</script>

<div class="flex flex-col gap-3 p-4 min-h-full text-white font-sans text-sm">
  <!-- Case Header -->
  <div class="flex flex-wrap items-center gap-x-4 gap-y-2 rounded-lg bg-[#12121A] border border-white/[0.06] px-4 py-3">
    <div class="flex items-center gap-2">
      <Scale class="size-5 text-[#0A84FF]" />
      <h1 class="text-base font-semibold tracking-tight">Smith v. Jones Corp</h1>
    </div>
    <span class="text-xs text-white/40 font-mono">#2026-CV-4892</span>
    <span class="rounded-full bg-[#30D158]/15 text-[#30D158] px-2.5 py-0.5 text-[11px] font-medium">Active</span>
    <span class="text-xs text-white/50">NY Supreme Court</span>
    <span class="text-xs text-white/50 flex items-center gap-1">
      <Gavel class="size-3" /> Hon. Martinez
    </span>
    <span class="text-xs text-white/50 flex items-center gap-1">
      <Calendar class="size-3" /> Filed Jan 15, 2026
    </span>
    <span class="ml-auto rounded-md bg-[#0A84FF]/15 text-[#0A84FF] px-2.5 py-0.5 text-[11px] font-medium">
      Next hearing: Apr 2 — 7 days
    </span>
  </div>

  <!-- Deadline Alerts -->
  <div class="flex gap-2 overflow-x-auto">
    {#each deadlines as d}
      <div class="flex-1 min-w-[180px] flex items-center gap-2.5 rounded-lg px-3 py-2.5 border" style:background={d.bg} style:border-color="{d.color}33">
        <AlertTriangle class="size-4 shrink-0" style="color: {d.color}" />
        <div class="flex flex-col">
          <span class="text-xs text-white/70">{d.label}</span>
          <span class="text-sm font-bold" style:color={d.color}>{d.days} days</span>
        </div>
      </div>
    {/each}
  </div>

  <!-- Main Grid: Documents + Billable Hours -->
  <div class="grid grid-cols-1 lg:grid-cols-5 gap-3">
    <!-- Document Repository (3 cols) -->
    <div class="lg:col-span-3 rounded-lg bg-[#12121A] border border-white/[0.06] p-3">
      <div class="flex items-center gap-2 mb-2.5">
        <FileText class="size-4 text-[#0A84FF]" />
        <h2 class="text-xs font-semibold uppercase tracking-wider text-white/60">Documents</h2>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-xs">
          <thead>
            <tr class="text-white/30 border-b border-white/[0.06]">
              <th class="text-left py-1.5 font-medium pl-1">Document</th>
              <th class="text-left py-1.5 font-medium">Date</th>
              <th class="text-left py-1.5 font-medium">Author</th>
              <th class="text-left py-1.5 font-medium">Status</th>
            </tr>
          </thead>
          <tbody>
            {#each documents as doc}
              {@const Icon = docIcons[doc.type] ?? FileText}
              <tr class="border-b border-white/[0.04] hover:bg-white/[0.02] transition-colors">
                <td class="py-2 pl-1 flex items-center gap-2">
                  <Icon class="size-3.5 text-white/40" />
                  <span class="text-white/80">{doc.name}</span>
                </td>
                <td class="py-2 text-white/40">{doc.date}</td>
                <td class="py-2 text-white/40">{doc.author}</td>
                <td class="py-2">
                  <span class="text-[11px] font-medium" style:color={doc.statusColor}>{doc.status}</span>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Billable Hours (2 cols) -->
    <div class="lg:col-span-2 rounded-lg bg-[#12121A] border border-white/[0.06] p-3">
      <div class="flex items-center gap-2 mb-2.5">
        <Clock class="size-4 text-[#FF9F0A]" />
        <h2 class="text-xs font-semibold uppercase tracking-wider text-white/60">Billable Hours</h2>
      </div>
      <div class="grid grid-cols-2 gap-2 mb-3">
        <div class="rounded-md bg-white/[0.04] px-2.5 py-2">
          <span class="text-[10px] text-white/40 uppercase">Total</span>
          <p class="text-lg font-bold text-white">142.5<span class="text-xs text-white/30 ml-0.5">hrs</span></p>
        </div>
        <div class="rounded-md bg-white/[0.04] px-2.5 py-2">
          <span class="text-[10px] text-white/40 uppercase">Unbilled</span>
          <p class="text-lg font-bold text-[#FF9F0A]">$28,500</p>
        </div>
        <div class="rounded-md bg-white/[0.04] px-2.5 py-2">
          <span class="text-[10px] text-white/40 uppercase">This Week</span>
          <p class="text-lg font-bold text-white">12.3<span class="text-xs text-white/30 ml-0.5">hrs</span></p>
        </div>
        <div class="rounded-md bg-white/[0.04] px-2.5 py-2">
          <span class="text-[10px] text-white/40 uppercase">Budget Left</span>
          <p class="text-lg font-bold text-[#30D158]">68%</p>
        </div>
      </div>
      <!-- Mini bar chart -->
      <div class="flex items-end gap-1.5 h-16 px-1">
        {#each weeklyHours as h, i}
          <div class="flex-1 flex flex-col items-center gap-1">
            <div
              class="w-full rounded-sm transition-all"
              style:height="{(h / maxHours) * 100}%"
              style:background={i === weeklyHours.length - 1 ? "#0A84FF" : "rgba(255,255,255,0.12)"}
            ></div>
            <span class="text-[9px] text-white/25">W{i + 1}</span>
          </div>
        {/each}
      </div>
    </div>
  </div>

  <!-- Bottom Grid: Timeline + AI Insights -->
  <div class="grid grid-cols-1 lg:grid-cols-5 gap-3">
    <!-- Case Timeline (3 cols) -->
    <div class="lg:col-span-3 rounded-lg bg-[#12121A] border border-white/[0.06] p-3">
      <div class="flex items-center gap-2 mb-2.5">
        <CircleDot class="size-4 text-[#30D158]" />
        <h2 class="text-xs font-semibold uppercase tracking-wider text-white/60">Case Timeline</h2>
      </div>
      <div class="flex flex-col gap-0">
        {#each timeline as step, i}
          <div class="flex items-start gap-3">
            <!-- Vertical line + dot -->
            <div class="flex flex-col items-center">
              <div
                class="size-2.5 rounded-full shrink-0 mt-1 ring-2"
                style:background={step.current ? "#30D158" : step.done ? "#0A84FF" : "transparent"}
                style:ring-color={step.current ? "#30D158" : step.done ? "#0A84FF" : "rgba(255,255,255,0.15)"}
              ></div>
              {#if i < timeline.length - 1}
                <div
                  class="w-px h-5"
                  style:background={step.done ? "#0A84FF" : "rgba(255,255,255,0.08)"}
                ></div>
              {/if}
            </div>
            <div class="flex items-center gap-2 -mt-0.5 pb-1">
              <span class={step.current ? "text-[#30D158] font-semibold text-xs" : step.done ? "text-white/70 text-xs" : "text-white/30 text-xs"}>
                {step.label}
              </span>
              <span class="text-[10px] text-white/20">{step.date}</span>
              {#if step.current}
                <span class="text-[10px] bg-[#30D158]/15 text-[#30D158] rounded-full px-1.5 py-0.5 font-medium">CURRENT</span>
              {/if}
            </div>
          </div>
        {/each}
      </div>
    </div>

    <!-- AI Agent Insights (2 cols) -->
    <div class="lg:col-span-2 rounded-lg bg-[#12121A] border border-[#BF5AF2]/20 p-3">
      <div class="flex items-center gap-2 mb-2.5">
        <Brain class="size-4 text-[#BF5AF2]" />
        <h2 class="text-xs font-semibold uppercase tracking-wider text-[#BF5AF2]/70">AI Insights</h2>
      </div>
      <div class="flex flex-col gap-2">
        {#each insights as insight, i}
          <div class="rounded-md bg-[#BF5AF2]/[0.06] border border-[#BF5AF2]/10 px-3 py-2 text-xs text-white/70 leading-relaxed">
            <span class="text-[#BF5AF2] font-mono text-[10px] mr-1.5">#{i + 1}</span>
            {@html insight}
          </div>
        {/each}
      </div>
    </div>
  </div>

  <!-- Team Strip -->
  <div class="flex items-center gap-4 rounded-lg bg-[#12121A] border border-white/[0.06] px-4 py-2.5">
    <div class="flex items-center gap-2 mr-2">
      <Users class="size-4 text-white/40" />
      <span class="text-[10px] font-semibold uppercase tracking-wider text-white/40">Team</span>
    </div>
    {#each team as member}
      <div class="flex items-center gap-2">
        <div class="relative">
          <div class="size-7 rounded-full flex items-center justify-center text-[11px] font-bold" style:background="{member.color}22" style:color={member.color}>
            {member.name.split(" ").map(n => n[0]).join("")}
          </div>
          <div
            class="absolute -bottom-0.5 -right-0.5 size-2 rounded-full border border-black/60"
            style:background={member.online ? "#30D158" : "#48484A"}
          ></div>
        </div>
        <div class="flex flex-col">
          <span class="text-xs text-white/80 leading-tight">{member.name}</span>
          <span class="text-[10px] text-white/30 leading-tight">{member.role}</span>
        </div>
      </div>
    {/each}
  </div>
</div>
