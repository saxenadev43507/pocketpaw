<!-- EduPocket.svelte — Mock Education/Learning Pocket for PocketPaw Agent OS.
     Created: 2026-03-26 — Dark terminal-style student dashboard with gamified XP,
     knowledge map, AI tutor notes, performance KPIs, deadlines, and study group strip.
     Uses Tailwind CSS 4, Lucide icons, all mock data.
-->
<script lang="ts">
  import GraduationCap from "@lucide/svelte/icons/graduation-cap";
  import Flame from "@lucide/svelte/icons/flame";
  import Zap from "@lucide/svelte/icons/zap";
  import Clock from "@lucide/svelte/icons/clock";
  import BookOpen from "@lucide/svelte/icons/book-open";
  import Code from "@lucide/svelte/icons/code";
  import FileText from "@lucide/svelte/icons/file-text";
  import Brain from "@lucide/svelte/icons/brain";
  import Target from "@lucide/svelte/icons/target";
  import TrendingUp from "@lucide/svelte/icons/trending-up";
  import Trophy from "@lucide/svelte/icons/trophy";
  import Timer from "@lucide/svelte/icons/timer";
  import AlertTriangle from "@lucide/svelte/icons/alert-triangle";
  import CalendarDays from "@lucide/svelte/icons/calendar-days";
  import Sparkles from "@lucide/svelte/icons/sparkles";
  import Users from "@lucide/svelte/icons/users";

  // === STUDENT DATA ===
  const student = {
    name: "Aria Patel",
    course: "CS 301: Machine Learning",
    semester: "Spring 2026",
    gpa: 3.8,
    streak: 12,
    xp: 2450,
    xpMax: 3000,
  };

  // === TODAY'S FOCUS ===
  const todayFocus = [
    { title: "Neural Networks Quiz", due: "Due 4pm", progress: 70, status: "prepared", icon: Brain, color: "#FF9F0A" },
    { title: "Lab 5: CNN Implementation", due: "In progress", progress: 60, status: "3/5 tasks", icon: Code, color: "#0A84FF" },
    { title: "Read Chapter 8", due: "Not started", progress: 0, status: "~45 min", icon: BookOpen, color: "#FF453A" },
  ];

  // === KNOWLEDGE MAP ===
  const topics = [
    { name: "Linear Algebra", mastery: 95, color: "#30D158" },
    { name: "Probability", mastery: 82, color: "#30D158" },
    { name: "Gradient Descent", mastery: 71, color: "#FF9F0A" },
    { name: "CNNs", mastery: 45, color: "#FF9F0A" },
    { name: "Transformers", mastery: 20, color: "#FF453A" },
    { name: "RNNs", mastery: 60, color: "#FF9F0A" },
  ];

  // === PERFORMANCE KPIs ===
  const kpis = [
    { label: "Quiz Avg", value: "87%", trend: [72, 80, 85, 82, 90, 87], icon: Target, color: "#30D158" },
    { label: "Assignments", value: "94%", trend: [88, 90, 92, 95, 93, 94], icon: FileText, color: "#0A84FF" },
    { label: "Class Rank", value: "7/42", trend: [15, 12, 10, 9, 8, 7], icon: Trophy, color: "#BF5AF2" },
    { label: "Study Hrs", value: "14.2", trend: [10, 12, 11, 14, 13, 14.2], icon: Timer, color: "#64D2FF" },
  ];

  // === DEADLINES ===
  const deadlines = [
    { title: "Midterm Exam", days: 5, urgency: "#FF453A" },
    { title: "Group Project Proposal", days: 8, urgency: "#FF9F0A" },
    { title: "Lab 6: Transfer Learning", days: 12, urgency: "#0A84FF" },
    { title: "Paper Draft", days: 15, urgency: "#30D158" },
  ];

  // === AI TUTOR NOTES ===
  const tutorNotes = [
    "You struggle with backpropagation chain rule — try the visual walkthrough I prepared.",
    "Your quiz scores drop on Mondays — consider reviewing Sunday evening.",
    "You learn CNNs faster with code-first approach — I've prepared a notebook.",
  ];

  // === STUDY GROUP ===
  const studyGroup = [
    { name: "Aria", label: "You", online: true, color: "#64D2FF" },
    { name: "Marcus", label: "", online: true, color: "#30D158" },
    { name: "Priya", label: "", online: false, color: "#FF9F0A" },
    { name: "James", label: "", online: true, color: "#0A84FF" },
    { name: "AI Tutor", label: "", online: true, color: "#BF5AF2" },
  ];

  function trendPath(data: number[]): string {
    const max = Math.max(...data);
    const min = Math.min(...data);
    const range = max - min || 1;
    const w = 60;
    const h = 20;
    const step = w / (data.length - 1);
    return data.map((v, i) => {
      const x = i * step;
      const y = h - ((v - min) / range) * h;
      return `${i === 0 ? "M" : "L"}${x},${y}`;
    }).join(" ");
  }
</script>

<div class="flex h-full w-full flex-col gap-3 overflow-y-auto p-4 font-sans text-white">

  <!-- HEADER -->
  <div class="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-white/5 bg-white/[0.03] px-4 py-3">
    <div class="flex items-center gap-3">
      <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-[#BF5AF2]/20">
        <GraduationCap class="h-5 w-5 text-[#BF5AF2]" />
      </div>
      <div>
        <p class="text-sm font-semibold text-white">{student.name}</p>
        <p class="text-xs text-white/50">{student.course} · {student.semester}</p>
      </div>
    </div>
    <div class="flex items-center gap-4 text-xs">
      <span class="rounded-md bg-white/5 px-2 py-1 text-white/60">GPA <span class="font-semibold text-[#30D158]">{student.gpa}</span></span>
      <span class="flex items-center gap-1 text-[#FF9F0A]"><Flame class="h-3.5 w-3.5" />{student.streak}d streak</span>
      <div class="flex items-center gap-2">
        <Zap class="h-3.5 w-3.5 text-[#64D2FF]" />
        <div class="h-1.5 w-24 overflow-hidden rounded-full bg-white/10">
          <div class="h-full rounded-full bg-[#64D2FF] transition-all" style="width: {(student.xp / student.xpMax) * 100}%"></div>
        </div>
        <span class="text-[10px] text-white/40">{student.xp}/{student.xpMax} XP</span>
      </div>
    </div>
  </div>

  <!-- TODAY'S FOCUS -->
  <div>
    <p class="mb-2 flex items-center gap-1.5 text-[11px] font-medium tracking-wider text-white/30 uppercase"><Clock class="h-3 w-3" />Today's Focus</p>
    <div class="grid grid-cols-3 gap-2">
      {#each todayFocus as item}
        {@const Icon = item.icon}
        <div class="rounded-lg border border-white/5 bg-white/[0.03] p-3">
          <div class="mb-2 flex items-center gap-2">
            <Icon class="h-4 w-4" style="color: {item.color}" />
            <span class="text-xs font-medium text-white/80">{item.title}</span>
          </div>
          <div class="mb-1 h-1 overflow-hidden rounded-full bg-white/10">
            <div class="h-full rounded-full transition-all" style="width: {item.progress}%; background: {item.color}"></div>
          </div>
          <div class="flex justify-between text-[10px] text-white/40">
            <span>{item.due}</span>
            <span>{item.status}</span>
          </div>
        </div>
      {/each}
    </div>
  </div>

  <!-- MIDDLE ROW: Knowledge Map + Performance -->
  <div class="grid grid-cols-2 gap-3">

    <!-- KNOWLEDGE MAP -->
    <div class="rounded-xl border border-white/5 bg-white/[0.03] p-3">
      <p class="mb-2 flex items-center gap-1.5 text-[11px] font-medium tracking-wider text-white/30 uppercase"><Brain class="h-3 w-3" />Knowledge Map</p>
      <div class="grid grid-cols-3 gap-2">
        {#each topics as t}
          <div class="flex flex-col items-center gap-1 rounded-lg border border-white/5 bg-white/[0.02] p-2">
            <div class="relative h-10 w-10 overflow-hidden rounded-md bg-white/5">
              <div class="absolute bottom-0 w-full transition-all" style="height: {t.mastery}%; background: {t.color}; opacity: 0.6"></div>
            </div>
            <span class="text-center text-[9px] leading-tight text-white/60">{t.name}</span>
            <span class="text-[10px] font-semibold" style="color: {t.color}">{t.mastery}%</span>
          </div>
        {/each}
      </div>
    </div>

    <!-- PERFORMANCE PANEL -->
    <div class="rounded-xl border border-white/5 bg-white/[0.03] p-3">
      <p class="mb-2 flex items-center gap-1.5 text-[11px] font-medium tracking-wider text-white/30 uppercase"><TrendingUp class="h-3 w-3" />Performance</p>
      <div class="grid grid-cols-2 gap-2">
        {#each kpis as kpi}
          {@const KpiIcon = kpi.icon}
          <div class="rounded-lg border border-white/5 bg-white/[0.02] p-2.5">
            <div class="mb-1 flex items-center gap-1.5">
              <KpiIcon class="h-3.5 w-3.5" style="color: {kpi.color}" />
              <span class="text-[10px] text-white/40">{kpi.label}</span>
            </div>
            <p class="mb-1 text-lg font-bold" style="color: {kpi.color}">{kpi.value}</p>
            <svg viewBox="0 0 60 20" class="h-4 w-full">
              <path d={trendPath(kpi.trend)} fill="none" stroke={kpi.color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.7" />
            </svg>
          </div>
        {/each}
      </div>
    </div>
  </div>

  <!-- BOTTOM ROW: Deadlines + AI Tutor -->
  <div class="grid grid-cols-2 gap-3">

    <!-- UPCOMING DEADLINES -->
    <div class="rounded-xl border border-white/5 bg-white/[0.03] p-3">
      <p class="mb-2 flex items-center gap-1.5 text-[11px] font-medium tracking-wider text-white/30 uppercase"><CalendarDays class="h-3 w-3" />Deadlines</p>
      <div class="flex flex-col gap-1.5">
        {#each deadlines as d}
          <div class="flex items-center justify-between rounded-md border border-white/5 bg-white/[0.02] px-3 py-2">
            <div class="flex items-center gap-2">
              <div class="h-2 w-2 rounded-full" style="background: {d.urgency}"></div>
              <span class="text-xs text-white/70">{d.title}</span>
            </div>
            <span class="text-[10px] font-medium" style="color: {d.urgency}">{d.days}d</span>
          </div>
        {/each}
      </div>
    </div>

    <!-- AI TUTOR NOTES -->
    <div class="rounded-xl border border-[#BF5AF2]/15 bg-[#BF5AF2]/[0.04] p-3">
      <p class="mb-2 flex items-center gap-1.5 text-[11px] font-medium tracking-wider text-[#BF5AF2]/60 uppercase"><Sparkles class="h-3 w-3" />AI Tutor Notes</p>
      <div class="flex flex-col gap-2">
        {#each tutorNotes as note}
          <div class="rounded-md border border-[#BF5AF2]/10 bg-[#BF5AF2]/[0.06] px-3 py-2 text-[11px] leading-relaxed text-white/60">
            {note}
          </div>
        {/each}
      </div>
    </div>
  </div>

  <!-- STUDY GROUP STRIP -->
  <div class="flex items-center gap-4 rounded-xl border border-white/5 bg-white/[0.03] px-4 py-2.5">
    <span class="flex items-center gap-1.5 text-[11px] font-medium tracking-wider text-white/30 uppercase"><Users class="h-3 w-3" />Study Group</span>
    <div class="flex items-center gap-3">
      {#each studyGroup as member}
        <div class="flex items-center gap-1.5">
          <div class="relative">
            <div class="flex h-7 w-7 items-center justify-center rounded-full text-[10px] font-semibold" style="background: {member.color}20; color: {member.color}">
              {member.name.slice(0, 2)}
            </div>
            <div class="absolute -bottom-0.5 -right-0.5 h-2.5 w-2.5 rounded-full border-2 border-black/60"
              style="background: {member.online ? '#30D158' : '#48484A'}"></div>
          </div>
          <span class="text-[10px] text-white/50">{member.label || member.name}</span>
        </div>
      {/each}
    </div>
  </div>
</div>
