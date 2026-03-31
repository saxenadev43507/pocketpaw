/**
 * soc-visualizer.js — Mini-SOC Audit Visualizer (v3 — REAL DATA)
 * Alpine.js feature module — PocketPaw.Loader pattern.
 *
 * Consumes REAL backend endpoints:
 *   GET  /api/self-audit/reports          → [{date, total, passed, issues}]
 *   GET  /api/self-audit/reports/{date}   → {timestamp, total_checks, passed, issues, results:[{check, passed, message}]}
 *   POST /api/self-audit/run              → full report
 *
 * The backend returns 12 real checks. The frontend classifies them into
 * Security / Health / Config categories and assigns severity levels.
 *
 * Zero mock data — every number comes from the API.
 */

(function () {
  'use strict';

  if (!window.PocketPaw) window.PocketPaw = {};

  /* ─── Check classification (applied on top of API results) ────────── */

  const CATEGORY_MAP = {
    'guardian agent':     'Security',
    'plaintext api keys': 'Security',
    'file jail':          'Security',
    'tool profile':       'Security',
    'bypass permissions': 'Security',
    'audit log':          'Security',
    'stale sessions':     'Health',
    'disk usage':         'Health',
    'audit log size':     'Health',
    'config permissions': 'Config',
    'config conflicts':   'Config',
    'oauth tokens':       'Config',
  };

  const SEVERITY_MAP = {
    'guardian agent':     'crit',
    'plaintext api keys': 'crit',
    'bypass permissions': 'crit',
    'file jail':          'high',
    'oauth tokens':       'high',
    'tool profile':       'med',
    'stale sessions':     'med',
    'config permissions': 'med',
    'config conflicts':   'med',
    'audit log':          'med',
    'disk usage':         'low',
    'audit log size':     'low',
  };

  const SEV_ORDER = { crit: 0, high: 1, med: 2, low: 3 };
  const SEV_LABEL = { crit: 'CRIT', high: 'HIGH', med: 'MED', low: 'LOW' };

  /* ─── Helpers ─────────────────────────────────────────────────────── */

  function _dateStr(d) {
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${y}-${m}-${day}`;
  }

  function _cellLevel(report) {
    if (!report) return 'empty';
    if (report.passed === report.total) return 'success';
    if (report.issues >= 3) return 'error';
    return 'warning';
  }

  function _classify(check) {
    const lower = (check || '').toLowerCase();
    for (const [kw, cat] of Object.entries(CATEGORY_MAP)) {
      if (lower.includes(kw)) return cat;
    }
    return 'Config';
  }

  function _severity(check) {
    const lower = (check || '').toLowerCase();
    for (const [kw, sev] of Object.entries(SEVERITY_MAP)) {
      if (lower.includes(kw)) return sev;
    }
    return 'low';
  }

  function _enrichResults(results) {
    return (results || []).map(r => ({
      ...r,
      category: _classify(r.check),
      severity: _severity(r.check),
    }));
  }

  function _categorize(enriched) {
    const cats = { Security: [], Health: [], Config: [] };
    for (const r of enriched) {
      (cats[r.category] || cats.Config).push(r);
    }
    for (const cat of Object.values(cats)) {
      cat.sort((a, b) => SEV_ORDER[a.severity] - SEV_ORDER[b.severity]);
    }
    return cats;
  }

  /* ─── Sparkline (smooth cubic bezier) ─────────────────────────────── */

  function _sparkPath(scores) {
    if (scores.length < 2) return '';
    const W = 148, H = 36, P = 4;
    const mn = Math.max(0, Math.min(...scores) - 10);
    const mx = Math.min(100, Math.max(...scores) + 10);
    const rng = mx - mn || 1;
    const pts = scores.map((s, i) => [
      +(P + i / (scores.length - 1) * (W - P * 2)).toFixed(1),
      +(H - P - (s - mn) / rng * (H - P * 2)).toFixed(1),
    ]);
    let d = `M${pts[0]}`;
    for (let i = 1; i < pts.length; i++) {
      const cx = ((pts[i - 1][0] + pts[i][0]) / 2).toFixed(1);
      d += ` C${cx},${pts[i - 1][1]} ${cx},${pts[i][1]} ${pts[i][0]},${pts[i][1]}`;
    }
    return d;
  }

  /* ─── Module ──────────────────────────────────────────────────────── */

  const CIRC = 2 * Math.PI * 44;

  window.PocketPaw.SOCVisualizer = {
    name: 'SOCVisualizer',

    getState() {
      return {
        showSOC:            false,
        socReports:         [],      // from GET /api/self-audit/reports
        socSelectedReport:  null,    // from GET /api/self-audit/reports/{date}
        socLoading:         false,
        socTimeline:        [],      // 30-day heatmap cells
        socTrend:           [],      // last 14 score values
        socExpandedCheck:   null,    // accordion toggle
      };
    },

    getMethods() {
      return {

        /* ── Open / Close ───────────────────────────────────────────── */

        async openSOC() {
          this.showSOC           = true;
          this.socLoading        = true;
          this.socSelectedReport = null;
          this.socExpandedCheck  = null;
          try {
            await this._socFetchReports();
            this._socBuildTimeline();
            this._socBuildTrend();
            if (this.socReports.length > 0) {
              await this.socSelectDate(this.socReports[0].date);
            }
          } catch (e) {
            console.error('[SOC] openSOC:', e);
          } finally {
            this.socLoading = false;
            this.$nextTick(() => { if (window.refreshIcons) window.refreshIcons(); });
          }
        },

        closeSOC() {
          this.showSOC           = false;
          this.socSelectedReport = null;
          this.socExpandedCheck  = null;
        },

        /* ── Data fetching (REAL API) ───────────────────────────────── */

        async _socFetchReports() {
          const res = await fetch('/api/self-audit/reports');
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          this.socReports = await res.json();
        },

        async socSelectDate(date) {
          if (!date) return;
          this.socLoading = true;
          try {
            const res = await fetch(`/api/self-audit/reports/${encodeURIComponent(date)}`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const report = await res.json();
            // Enrich results with category + severity (backend doesn't include them)
            report.results = _enrichResults(report.results);
            this.socSelectedReport = report;
            this.socExpandedCheck  = null;
          } catch (e) {
            console.error('[SOC] socSelectDate:', e);
          } finally {
            this.socLoading = false;
          }
        },

        async socRunAudit() {
          this.socLoading = true;
          try {
            const res = await fetch('/api/self-audit/run', { method: 'POST' });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            // Re-fetch everything after the new audit
            await this._socFetchReports();
            this._socBuildTimeline();
            this._socBuildTrend();
            if (this.socReports.length > 0) {
              await this.socSelectDate(this.socReports[0].date);
            }
            if (this.showToast) {
              const r = this.socSelectedReport;
              const p = r ? r.passed : 0, t = r ? r.total_checks : 0;
              this.showToast(`Audit complete: ${p}/${t} passed`, p === t ? 'success' : 'warning');
            }
          } catch (e) {
            console.error('[SOC] socRunAudit:', e);
            if (this.showToast) this.showToast('Audit run failed', 'error');
          } finally {
            this.socLoading = false;
          }
        },

        /* ── Timeline (30-day heatmap) ──────────────────────────────── */

        _socBuildTimeline() {
          const map = {};
          for (const r of this.socReports) map[r.date] = r;
          const cells = [];
          const today = new Date();
          for (let i = 29; i >= 0; i--) {
            const d = new Date(today);
            d.setDate(today.getDate() - i);
            const ds = _dateStr(d);
            const r  = map[ds] || null;
            cells.push({
              date:   ds,
              label:  d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
              dayNum: d.getDate(),
              report: r,
              score:  r ? Math.round((r.passed / r.total) * 100) : null,
              level:  _cellLevel(r),
            });
          }
          this.socTimeline = cells;
        },

        socCellSelected(cell) {
          if (!this.socSelectedReport || !cell.report) return false;
          return (this.socSelectedReport.timestamp || '').startsWith(cell.date);
        },

        /* ── Trend sparkline ────────────────────────────────────────── */

        _socBuildTrend() {
          this.socTrend = this.socReports
            .slice(0, 14)
            .reverse()
            .map(r => Math.round((r.passed / r.total) * 100));
        },

        socSparkPath() {
          return _sparkPath(this.socTrend);
        },

        /* ── Score ring ─────────────────────────────────────────────── */

        socPassRate() {
          const r = this.socSelectedReport;
          if (!r || !r.total_checks) return 0;
          return Math.round((r.passed / r.total_checks) * 100);
        },

        socDonutDash() {
          const fill = (this.socPassRate() / 100) * CIRC;
          return `${fill.toFixed(1)} ${(CIRC - fill).toFixed(1)}`;
        },

        socScoreColor() {
          const p = this.socPassRate();
          if (p === 100) return 'var(--paw-success, #30d158)';
          if (p >= 75)   return 'var(--paw-warning, #ffd60a)';
          return 'var(--paw-error, #ff453a)';
        },

        /* ── Check breakdown ────────────────────────────────────────── */

        socCategories() {
          if (!this.socSelectedReport) return {};
          return _categorize(this.socSelectedReport.results || []);
        },

        socSevLabel(sev) {
          return SEV_LABEL[sev] || 'LOW';
        },

        socToggleCheck(name) {
          this.socExpandedCheck = this.socExpandedCheck === name ? null : name;
        },

        /* ── Formatting ─────────────────────────────────────────────── */

        socFmtDate(ts) {
          if (!ts) return '';
          try {
            return new Date(ts).toLocaleDateString('en-US', {
              month: 'short', day: 'numeric', year: 'numeric',
            });
          } catch { return ts; }
        },
      };
    },
  };

  if (window.PocketPaw.Loader) {
    window.PocketPaw.Loader.register('SOCVisualizer', window.PocketPaw.SOCVisualizer);
  }

})();
