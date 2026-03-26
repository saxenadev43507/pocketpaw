<!-- HealthPocket.svelte — Bloomberg Terminal-style Healthcare/Patient Care Pocket.
     Created: 2026-03-26 — Dark mode clinical dashboard with Apple Health-inspired vitals,
     medications panel, lab results, care timeline, AI agent notes, and team strip.
     All mock data, no real API calls. CSS-only sparklines for vital signs.
-->
<script lang="ts">
  import Heart from "@lucide/svelte/icons/heart";
  import Thermometer from "@lucide/svelte/icons/thermometer";
  import Wind from "@lucide/svelte/icons/wind";
  import Droplets from "@lucide/svelte/icons/droplets";
  import Activity from "@lucide/svelte/icons/activity";
  import Pill from "@lucide/svelte/icons/pill";
  import FlaskConical from "@lucide/svelte/icons/flask-conical";
  import Brain from "@lucide/svelte/icons/brain";
  import Clock from "@lucide/svelte/icons/clock";
  import ArrowUp from "@lucide/svelte/icons/arrow-up";
  import ArrowDown from "@lucide/svelte/icons/arrow-down";
  import Minus from "@lucide/svelte/icons/minus";
  import AlertTriangle from "@lucide/svelte/icons/alert-triangle";
  import CheckCircle from "@lucide/svelte/icons/check-circle-2";
  import User from "@lucide/svelte/icons/user";
  import Bot from "@lucide/svelte/icons/bot";
  import Stethoscope from "@lucide/svelte/icons/stethoscope";

  // === TEAM ===
  const team = [
    { name: "Dr. Patel", role: "Attending", color: "#0A84FF", initials: "SP" },
    { name: "Nurse Kim", role: "Primary RN", color: "#30D158", initials: "NK" },
    { name: "Nurse Alex", role: "RN", color: "#FF9F0A", initials: "NA" },
    { name: "AI Agent", role: "Monitor", color: "#BF5AF2", initials: "AI", isAI: true },
  ];

  // === VITALS ===
  const vitals = [
    { label: "Heart Rate", value: "72", unit: "bpm", icon: Heart, color: "#FF453A", status: "normal", bars: [60, 68, 72, 70, 65, 71, 72, 74, 70, 72] },
    { label: "Blood Pressure", value: "120/80", unit: "mmHg", icon: Activity, color: "#0A84FF", status: "normal", bars: [75, 78, 80, 82, 79, 80, 81, 78, 80, 80] },
    { label: "SpO2", value: "98", unit: "%", icon: Droplets, color: "#30D158", status: "normal", bars: [97, 98, 98, 97, 98, 99, 98, 98, 97, 98] },
    { label: "Temp", value: "98.6", unit: "°F", icon: Thermometer, color: "#FF9F0A", status: "normal", bars: [50, 52, 51, 53, 50, 52, 53, 51, 52, 52] },
    { label: "Resp Rate", value: "16", unit: "/min", icon: Wind, color: "#BF5AF2", status: "normal", bars: [14, 15, 16, 15, 16, 17, 16, 15, 16, 16] },
  ];

  // === MEDICATIONS ===
  const medications = [
    { name: "Metformin", dosage: "500mg", freq: "2x daily", next: "2:00 PM", status: "active" },
    { name: "Lisinopril", dosage: "10mg", freq: "1x daily", next: "8:00 AM", status: "active" },
    { name: "Aspirin", dosage: "81mg", freq: "1x daily", next: "8:00 AM", status: "active" },
    { name: "Atorvastatin", dosage: "20mg", freq: "1x daily", next: "10:00 PM", status: "active" },
    { name: "Prednisone", dosage: "5mg", freq: "taper", next: "—", status: "paused" },
  ];

  // === LAB RESULTS ===
  const labs = [
    { name: "Glucose", value: "105", unit: "mg/dL", range: "70-100", trend: "up", flag: "borderline" },
    { name: "Cholesterol", value: "195", unit: "mg/dL", range: "<200", trend: "down", flag: "normal" },
    { name: "WBC", value: "7.2", unit: "K/uL", range: "4.5-11.0", trend: "stable", flag: "normal" },
    { name: "Hemoglobin", value: "13.8", unit: "g/dL", range: "13.5-17.5", trend: "stable", flag: "normal" },
    { name: "Creatinine", value: "1.3", unit: "mg/dL", range: "0.7-1.3", trend: "up", flag: "borderline" },
  ];

  // === CARE TIMELINE ===
  const timeline = [
    { time: "06:00", event: "Admission", person: "Dr. Patel", type: "milestone" },
    { time: "06:30", event: "Initial assessment completed", person: "Nurse Kim", type: "assessment" },
    { time: "07:15", event: "Blood draw — CBC, BMP, Lipid panel", person: "Lab Tech", type: "lab" },
    { time: "08:00", event: "Metformin 500mg administered", person: "Nurse Kim", type: "medication" },
    { time: "09:30", event: "Doctor rounds — reviewed labs, adjusted plan", person: "Dr. Patel", type: "rounds" },
  ];

  // === AI AGENT NOTES ===
  const agentNotes = [
    { text: "Blood pressure trending up over 3 days — flagged for review", type: "warning" },
    { text: "Next lab draw due in 2 hours", type: "info" },
    { text: "Medication interaction check: clear", type: "success" },
  ];

  const flagColor = (flag: string) => {
    if (flag === "critical") return "#FF453A";
    if (flag === "borderline") return "#FF9F0A";
    return "#30D158";
  };
</script>

<div class="health-pocket">
  <!-- Team Strip -->
  <div class="team-strip">
    {#each team as member}
      <div class="team-member" title={`${member.name} — ${member.role}`}>
        <div class="team-avatar" style="background:{member.color}20; border-color:{member.color}">
          {#if member.isAI}<Bot size={11} color={member.color} />{:else}<span style="color:{member.color}">{member.initials}</span>{/if}
        </div>
        <div class="team-dot" style="background:{member.color}"></div>
      </div>
    {/each}
    <div class="team-spacer"></div>
    <div class="team-label"><Stethoscope size={10} strokeWidth={1.5} /> Care Team</div>
  </div>

  <!-- Patient Header -->
  <div class="patient-header">
    <div class="patient-info">
      <div class="patient-avatar"><User size={16} color="rgba(255,255,255,0.6)" /></div>
      <div class="patient-details">
        <div class="patient-name">Eleanor Chen <span class="patient-age">68F</span></div>
        <div class="patient-meta">
          <span class="meta-tag">B+ Blood</span>
          <span class="meta-tag">Room 412-A</span>
          <span class="meta-tag">Dr. Patel</span>
        </div>
      </div>
    </div>
    <div class="status-badge status-stable">STABLE</div>
  </div>

  <!-- Vital Signs Row -->
  <div class="vitals-row">
    {#each vitals as vital}
      {@const Icon = vital.icon}
      <div class="vital-card">
        <div class="vital-top">
          <Icon size={12} color={vital.color} strokeWidth={1.8} />
          <span class="vital-label">{vital.label}</span>
        </div>
        <div class="vital-value" style="color:{vital.color}">{vital.value}<span class="vital-unit">{vital.unit}</span></div>
        <div class="vital-spark">
          {#each vital.bars as bar, i}
            <div class="spark-bar" style="height:{bar}%; background:{vital.color}; opacity:{0.3 + (i / vital.bars.length) * 0.7}"></div>
          {/each}
        </div>
      </div>
    {/each}
  </div>

  <!-- Content Grid: Medications + Labs -->
  <div class="content-grid">
    <!-- Medications Panel -->
    <div class="panel">
      <div class="panel-head">
        <Pill size={11} color="#0A84FF" strokeWidth={1.8} />
        <span class="panel-title">Medications</span>
        <span class="panel-count">{medications.filter(m => m.status === "active").length} active</span>
      </div>
      <div class="med-list">
        {#each medications as med}
          <div class="med-row">
            <div class="med-status-dot" class:med-active={med.status === "active"} class:med-paused={med.status === "paused"}></div>
            <div class="med-info">
              <span class="med-name">{med.name}</span>
              <span class="med-detail">{med.dosage} · {med.freq}</span>
            </div>
            <div class="med-next">
              {#if med.status === "active"}
                <Clock size={9} color="rgba(255,255,255,0.3)" /><span>{med.next}</span>
              {:else}
                <span class="med-paused-label">PAUSED</span>
              {/if}
            </div>
          </div>
        {/each}
      </div>
    </div>

    <!-- Lab Results Panel -->
    <div class="panel">
      <div class="panel-head">
        <FlaskConical size={11} color="#30D158" strokeWidth={1.8} />
        <span class="panel-title">Lab Results</span>
        <span class="panel-count">Today 07:15</span>
      </div>
      <div class="lab-table">
        <div class="lab-header-row">
          <span>Test</span><span>Value</span><span>Range</span><span></span>
        </div>
        {#each labs as lab}
          <div class="lab-row">
            <span class="lab-name">{lab.name}</span>
            <span class="lab-value" style="color:{flagColor(lab.flag)}">{lab.value}<span class="lab-unit">{lab.unit}</span></span>
            <span class="lab-range">{lab.range}</span>
            <span class="lab-trend">
              {#if lab.trend === "up"}<ArrowUp size={10} color="#FF9F0A" />
              {:else if lab.trend === "down"}<ArrowDown size={10} color="#30D158" />
              {:else}<Minus size={10} color="rgba(255,255,255,0.25)" />
              {/if}
            </span>
          </div>
        {/each}
      </div>
    </div>
  </div>

  <!-- Bottom Grid: Timeline + AI Notes -->
  <div class="content-grid">
    <!-- Care Timeline -->
    <div class="panel">
      <div class="panel-head">
        <Clock size={11} color="#FF9F0A" strokeWidth={1.8} />
        <span class="panel-title">Care Timeline</span>
        <span class="panel-count">Today</span>
      </div>
      <div class="timeline">
        {#each timeline as event, i}
          <div class="timeline-item">
            <div class="timeline-track">
              <div class="timeline-dot" class:tl-milestone={event.type === "milestone"} class:tl-lab={event.type === "lab"} class:tl-medication={event.type === "medication"} class:tl-rounds={event.type === "rounds"}></div>
              {#if i < timeline.length - 1}<div class="timeline-line"></div>{/if}
            </div>
            <div class="timeline-content">
              <div class="timeline-time">{event.time}</div>
              <div class="timeline-event">{event.event}</div>
              <div class="timeline-person">{event.person}</div>
            </div>
          </div>
        {/each}
      </div>
    </div>

    <!-- AI Agent Notes -->
    <div class="panel panel-ai">
      <div class="panel-head">
        <Brain size={11} color="#BF5AF2" strokeWidth={1.8} />
        <span class="panel-title" style="color:#BF5AF2">AI Agent</span>
        <div class="ai-live-dot"></div>
      </div>
      <div class="agent-notes">
        {#each agentNotes as note}
          <div class="agent-note">
            <div class="note-icon">
              {#if note.type === "warning"}<AlertTriangle size={11} color="#FF9F0A" />
              {:else if note.type === "success"}<CheckCircle size={11} color="#30D158" />
              {:else}<Clock size={11} color="#0A84FF" />
              {/if}
            </div>
            <span class="note-text">{note.text}</span>
          </div>
        {/each}
      </div>
      <div class="agent-footer">
        <Bot size={9} color="#BF5AF2" /> Monitoring · Last scan 2m ago
      </div>
    </div>
  </div>
</div>

<style>
  .health-pocket { width: 100%; height: 100%; display: flex; flex-direction: column; overflow-y: auto; padding: 8px; scrollbar-width: thin; scrollbar-color: rgba(255,255,255,0.06) transparent; gap: 6px; font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif; }
  /* Team */
  .team-strip { display: flex; align-items: center; gap: 8px; padding: 4px 6px; flex-shrink: 0; }
  .team-member { position: relative; }
  .team-avatar { width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 1.5px solid; font-size: 8px; font-weight: 700; }
  .team-dot { position: absolute; bottom: -1px; right: -1px; width: 7px; height: 7px; border-radius: 50%; border: 1.5px solid rgba(0,0,0,0.6); }
  .team-spacer { flex: 1; }
  .team-label { display: flex; align-items: center; gap: 4px; font-size: 9px; color: rgba(255,255,255,0.25); text-transform: uppercase; letter-spacing: 0.05em; }
  /* Patient */
  .patient-header { display: flex; align-items: center; justify-content: space-between; padding: 8px 10px; border-radius: 8px; background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.05); }
  .patient-info { display: flex; align-items: center; gap: 8px; }
  .patient-avatar { width: 32px; height: 32px; border-radius: 8px; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; }
  .patient-details { display: flex; flex-direction: column; gap: 2px; }
  .patient-name { font-size: 13px; font-weight: 700; color: rgba(255,255,255,0.90); }
  .patient-age { font-size: 10px; font-weight: 400; color: rgba(255,255,255,0.35); margin-left: 4px; }
  .patient-meta { display: flex; gap: 6px; }
  .meta-tag { font-size: 9px; color: rgba(255,255,255,0.30); padding: 1px 5px; border-radius: 3px; background: rgba(255,255,255,0.04); }
  .status-badge { font-size: 8px; font-weight: 700; letter-spacing: 0.08em; padding: 3px 8px; border-radius: 4px; }
  .status-stable { color: #30D158; background: rgba(48,209,88,0.12); }
  /* Vitals */
  .vitals-row { display: flex; gap: 5px; flex-shrink: 0; overflow-x: auto; scrollbar-width: none; }
  .vitals-row::-webkit-scrollbar { display: none; }
  .vital-card { flex: 1; min-width: 0; padding: 7px 8px; border-radius: 8px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); display: flex; flex-direction: column; gap: 2px; }
  .vital-top { display: flex; align-items: center; gap: 4px; }
  .vital-label { font-size: 8px; color: rgba(255,255,255,0.30); text-transform: uppercase; letter-spacing: 0.04em; }
  .vital-value { font-size: 18px; font-weight: 700; line-height: 1; }
  .vital-unit { font-size: 9px; font-weight: 400; opacity: 0.5; margin-left: 2px; }
  .vital-spark { display: flex; align-items: flex-end; gap: 2px; height: 18px; margin-top: 2px; }
  .spark-bar { flex: 1; border-radius: 1px; min-width: 0; transition: height 0.3s ease; }
  /* Grid & Panel */
  .content-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
  .panel { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); border-radius: 8px; padding: 8px; display: flex; flex-direction: column; overflow: hidden; }
  .panel-ai { border-color: rgba(191,90,242,0.12); }
  .panel-head { display: flex; align-items: center; gap: 5px; margin-bottom: 6px; }
  .panel-title { font-size: 10px; font-weight: 600; color: rgba(255,255,255,0.40); text-transform: uppercase; letter-spacing: 0.04em; }
  .panel-count { margin-left: auto; font-size: 8px; color: rgba(255,255,255,0.20); }
  /* Medications */
  .med-list { display: flex; flex-direction: column; gap: 4px; }
  .med-row { display: flex; align-items: center; gap: 6px; padding: 3px 0; }
  .med-status-dot { width: 5px; height: 5px; border-radius: 50%; flex-shrink: 0; }
  .med-active { background: #30D158; box-shadow: 0 0 4px rgba(48,209,88,0.4); }
  .med-paused { background: rgba(255,255,255,0.15); }
  .med-info { display: flex; flex-direction: column; flex: 1; min-width: 0; }
  .med-name { font-size: 10px; font-weight: 600; color: rgba(255,255,255,0.75); }
  .med-detail { font-size: 8px; color: rgba(255,255,255,0.25); }
  .med-next { display: flex; align-items: center; gap: 3px; font-size: 9px; color: rgba(255,255,255,0.30); flex-shrink: 0; }
  .med-paused-label { font-size: 7px; font-weight: 700; color: rgba(255,255,255,0.20); letter-spacing: 0.05em; }
  /* Labs */
  .lab-table { display: flex; flex-direction: column; gap: 2px; }
  .lab-header-row, .lab-row { display: grid; grid-template-columns: 1.2fr 1fr 1fr 20px; }
  .lab-header-row { font-size: 8px; color: rgba(255,255,255,0.18); text-transform: uppercase; letter-spacing: 0.04em; padding-bottom: 3px; border-bottom: 1px solid rgba(255,255,255,0.04); }
  .lab-row { align-items: center; padding: 3px 0; }
  .lab-name { font-size: 10px; color: rgba(255,255,255,0.55); }
  .lab-value { font-size: 10px; font-weight: 700; }
  .lab-unit { font-size: 8px; font-weight: 400; opacity: 0.5; margin-left: 1px; }
  .lab-range { font-size: 8px; color: rgba(255,255,255,0.20); }
  .lab-trend { display: flex; justify-content: center; }
  /* Timeline */
  .timeline { display: flex; flex-direction: column; }
  .timeline-item { display: flex; gap: 8px; }
  .timeline-track { display: flex; flex-direction: column; align-items: center; width: 10px; flex-shrink: 0; }
  .timeline-dot { width: 7px; height: 7px; border-radius: 50%; background: rgba(255,255,255,0.15); flex-shrink: 0; }
  .tl-milestone { background: #0A84FF; box-shadow: 0 0 4px rgba(10,132,255,0.4); }
  .tl-lab { background: #FF9F0A; }
  .tl-medication { background: #30D158; }
  .tl-rounds { background: #BF5AF2; }
  .timeline-line { width: 1px; flex: 1; min-height: 16px; background: rgba(255,255,255,0.06); }
  .timeline-content { padding-bottom: 8px; min-width: 0; }
  .timeline-time { font-size: 8px; color: rgba(255,255,255,0.25); font-variant-numeric: tabular-nums; }
  .timeline-event { font-size: 10px; color: rgba(255,255,255,0.65); line-height: 1.3; }
  .timeline-person { font-size: 8px; color: rgba(255,255,255,0.20); }
  /* AI Agent */
  .ai-live-dot { width: 6px; height: 6px; border-radius: 50%; background: #BF5AF2; margin-left: auto; box-shadow: 0 0 6px rgba(191,90,242,0.5); animation: pulse 2s ease-in-out infinite; }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
  .agent-notes { display: flex; flex-direction: column; gap: 6px; flex: 1; }
  .agent-note { display: flex; align-items: flex-start; gap: 6px; padding: 5px 6px; border-radius: 5px; background: rgba(191,90,242,0.04); border: 1px solid rgba(191,90,242,0.06); }
  .note-icon { flex-shrink: 0; margin-top: 1px; }
  .note-text { font-size: 9px; color: rgba(255,255,255,0.55); line-height: 1.4; }
  .agent-footer { display: flex; align-items: center; gap: 4px; font-size: 8px; color: rgba(191,90,242,0.35); margin-top: 6px; padding-top: 4px; border-top: 1px solid rgba(191,90,242,0.06); }
</style>
