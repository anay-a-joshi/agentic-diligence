"use client";

import { AnalysisResult } from "@/lib/api";

function Cell({ label, value }: { label: string; value: any }) {
  let display = "-";
  if (value === true) display = "Yes";
  else if (value === false) display = "No";
  else if (value !== null && value !== undefined && value !== "") {
    display = typeof value === "number" ? value.toFixed(1) : String(value);
  }
  return (
    <div className="flex justify-between py-2 border-b border-slate-100 last:border-0">
      <span className="text-slate-600">{label}</span>
      <span className="font-semibold text-slate-900">{display}</span>
    </div>
  );
}

export default function GovernancePanel({ result }: { result: AnalysisResult }) {
  const g = result.raw_findings.governance_agent?.data;
  if (!g) return null;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6">
      <h2 className="text-2xl font-bold text-slate-900 mb-4">Governance Assessment</h2>
      <div className="grid md:grid-cols-2 gap-x-8 gap-y-1">
        <Cell label="Board Size" value={g.board_size} />
        <Cell label="Independent Directors %" value={g.independent_directors_pct ? g.independent_directors_pct + "%" : null} />
        <Cell label="CEO/Chair Combined" value={g.ceo_chair_combined} />
        <Cell label="Staggered Board" value={g.staggered_board} />
        <Cell label="Poison Pill" value={g.poison_pill} />
        <Cell label="Dual-Class Shares" value={g.dual_class_shares} />
        <Cell label="Largest Holder" value={g.largest_holder} />
        <Cell label="Defense Strength" value={g.takeover_defense_strength} />
      </div>
      <div className="mt-4 p-4 rounded-xl bg-slate-50 border border-slate-200">
        <div className="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-1">
          Take-Private Feasibility
        </div>
        <div className="text-lg font-bold text-slate-900 mb-2">{g.feasibility_assessment}</div>
        <p className="text-sm text-slate-700">{g.summary}</p>
      </div>
    </div>
  );
}
