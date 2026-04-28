"use client";

import { AnalysisResult } from "@/lib/api";

const sevColors: Record<string, string> = {
  critical: "bg-red-200 text-red-900",
  high: "bg-red-100 text-red-800",
  medium: "bg-amber-100 text-amber-800",
  low: "bg-green-100 text-green-800",
};

export default function RedFlagsPanel({ result }: { result: AnalysisResult }) {
  const rf = result.raw_findings.red_flag_agent?.data;
  if (!rf) return null;

  if (!rf.red_flags?.length) {
    return (
      <div className="bg-white rounded-2xl border border-slate-200 p-6">
        <h2 className="text-2xl font-bold text-slate-900 mb-2">Red-Flag Scan (8-Ks)</h2>
        <p className="text-slate-600">No material red flags identified in recent 8-K filings.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6">
      <div className="flex items-baseline justify-between mb-4 flex-wrap gap-2">
        <h2 className="text-2xl font-bold text-slate-900">Red-Flag Scan (8-Ks)</h2>
        <span className="text-sm text-slate-500">
          {rf.deal_breakers_count ?? 0} critical - {rf.high_concern_count ?? 0} high concern
        </span>
      </div>
      <div className="space-y-3">
        {rf.red_flags.map((f: any, i: number) => {
          const sev = String(f.severity || "").toLowerCase();
          return (
            <div key={i} className="p-4 rounded-xl bg-slate-50 border border-slate-200">
              <div className="flex items-start gap-2 flex-wrap mb-1">
                <span className="font-semibold text-slate-900">{f.flag}</span>
                <span className={`px-2 py-0.5 rounded text-xs font-bold uppercase ${sevColors[sev] || "bg-slate-200 text-slate-700"}`}>
                  {f.severity}
                </span>
                <span className="text-xs text-slate-500">
                  {f.category} - {f.filing_date}
                </span>
              </div>
              <p className="text-sm text-slate-700 leading-relaxed">{f.description}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
