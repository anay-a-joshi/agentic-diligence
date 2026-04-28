"use client";

import { AnalysisResult } from "@/lib/api";

export default function LBOReturns({ result }: { result: AnalysisResult }) {
  const lbo = result.lbo_full;
  if (!lbo || lbo.status !== "ok" || !lbo.base) return null;

  const scenarios = [
    { name: "Bull", color: "bg-green-50 border-green-200", scenario: lbo.bull },
    { name: "Base", color: "bg-amber-50 border-amber-200", scenario: lbo.base },
    { name: "Bear", color: "bg-red-50 border-red-200", scenario: lbo.bear },
  ];

  return (
    <div>
      <h2 className="text-2xl font-bold text-slate-900 mb-4">LBO Returns</h2>
      {lbo.size_prohibitive && (
        <div className="mb-4 px-4 py-3 rounded-xl bg-amber-50 border border-amber-300 text-sm text-amber-900">
          <strong>Size Note:</strong> {lbo.size_prohibitive_note}
        </div>
      )}
      <div className="grid md:grid-cols-3 gap-4">
        {scenarios.map(({ name, color, scenario }) => {
          if (!scenario) return null;
          const irr = scenario.returns.irr_pct;
          const moic = scenario.returns.moic;
          const exit_eq = scenario.exit.exit_equity_value_usd_millions;
          return (
            <div key={name} className={`rounded-2xl border-2 ${color} p-6`}>
              <div className="text-sm font-semibold uppercase tracking-wider text-slate-600 mb-3">
                {name} Case
              </div>
              <div className="space-y-3">
                <div>
                  <div className="text-xs text-slate-500">IRR (5-year)</div>
                  <div className="text-3xl font-bold text-slate-900 tabular-nums">{irr.toFixed(1)}%</div>
                </div>
                <div>
                  <div className="text-xs text-slate-500">MOIC</div>
                  <div className="text-2xl font-bold text-slate-900 tabular-nums">{moic.toFixed(2)}x</div>
                </div>
                <div>
                  <div className="text-xs text-slate-500">Exit Equity</div>
                  <div className="text-lg font-semibold text-slate-700 tabular-nums">
                    ${(exit_eq / 1000).toFixed(1)}B
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
