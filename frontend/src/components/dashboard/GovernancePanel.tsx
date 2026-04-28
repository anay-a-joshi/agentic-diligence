"use client";

import { AnalysisResult } from "@/lib/api";

function Cell({ label, value }: { label: string; value: any }) {
  let display = "—";
  let color = "text-slate-300";
  if (value === true) { display = "Yes"; color = "text-amber-300"; }
  else if (value === false) { display = "No"; color = "text-emerald-300"; }
  else if (value !== null && value !== undefined && value !== "") {
    display = typeof value === "number" ? value.toFixed(1) : String(value);
    color = "text-white";
  }
  return (
    <div className="flex justify-between py-3 border-b border-white/5 last:border-0">
      <span className="text-slate-500 text-sm">{label}</span>
      <span className={`font-medium tabular-nums ${color}`}>{display}</span>
    </div>
  );
}

export default function GovernancePanel({ result }: { result: AnalysisResult }) {
  const g = result.raw_findings.governance_agent?.data;
  if (!g) return null;

  const feasColor =
    String(g.feasibility_assessment).toLowerCase() === "easy" ? "#10b981" :
    String(g.feasibility_assessment).toLowerCase() === "moderate" ? "#f59e0b" :
    "#ef4444";

  return (
    <section className="glass-strong rounded-2xl p-6 md:p-8 animate-fade-up">
      <div className="mb-6">
        <div className="text-xs uppercase tracking-widest text-slate-500 mb-1 font-medium">
          Board & Defenses
        </div>
        <h2 className="text-2xl font-bold text-white tracking-tight">
          Governance Assessment
        </h2>
      </div>

      <div className="grid md:grid-cols-2 gap-x-8 gap-y-0">
        <Cell label="Board Size" value={g.board_size} />
        <Cell label="Independent Directors %" value={g.independent_directors_pct ? g.independent_directors_pct + "%" : null} />
        <Cell label="CEO/Chair Combined" value={g.ceo_chair_combined} />
        <Cell label="Staggered Board" value={g.staggered_board} />
        <Cell label="Poison Pill" value={g.poison_pill} />
        <Cell label="Dual-Class Shares" value={g.dual_class_shares} />
        <Cell label="Largest Holder" value={g.largest_holder} />
        <Cell label="Defense Strength" value={g.takeover_defense_strength} />
      </div>

      <div className="mt-6 pt-6 border-t border-white/5">
        <div className="flex items-center gap-3 mb-3">
          <div className="text-xs uppercase tracking-widest text-slate-500 font-medium">
            Take-Private Feasibility
          </div>
          <div
            className="px-3 py-1 rounded-full text-xs font-bold tracking-wider"
            style={{
              background: `${feasColor}20`,
              color: feasColor,
              border: `1px solid ${feasColor}40`,
            }}
          >
            {g.feasibility_assessment}
          </div>
        </div>
        <p className="text-sm text-slate-400 leading-relaxed">{g.summary}</p>
      </div>
    </section>
  );
}
