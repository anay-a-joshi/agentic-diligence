"use client";

import { AnalysisResult } from "@/lib/api";

const sevColors: Record<string, string> = {
  high: "bg-red-100 text-red-800 border-red-300",
  medium: "bg-amber-100 text-amber-800 border-amber-300",
  low: "bg-green-100 text-green-800 border-green-300",
  critical: "bg-red-200 text-red-900 border-red-400",
};

export default function RiskPanel({ result }: { result: AnalysisResult }) {
  const risk = result.raw_findings.risk_agent?.data;
  if (!risk?.top_risks?.length) return null;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6">
      <div className="flex items-baseline justify-between mb-4 flex-wrap gap-2">
        <h2 className="text-2xl font-bold text-slate-900">Top Risks</h2>
        <span className="text-sm text-slate-500">
          {risk.high_severity_count ?? 0} high-severity - {risk.total_risks_disclosed ?? 0} total disclosed
        </span>
      </div>
      <div className="space-y-3">
        {risk.top_risks.map((r: any, i: number) => {
          const sev = String(r.severity || "").toLowerCase();
          return (
            <div key={i} className={`p-4 rounded-xl border ${sevColors[sev] || "bg-slate-50 border-slate-200"}`}>
              <div className="flex items-start gap-3 flex-wrap mb-1">
                <span className="font-semibold text-slate-900">{r.risk}</span>
                <span className={`px-2 py-0.5 rounded text-xs font-bold uppercase ${sevColors[sev] || "bg-slate-200 text-slate-700"}`}>
                  {r.severity}
                </span>
                <span className="text-xs text-slate-500 italic">{r.category}</span>
              </div>
              <p className="text-sm text-slate-700 leading-relaxed">{r.description}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
