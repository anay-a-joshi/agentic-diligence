"use client";

import { AnalysisResult } from "@/lib/api";

const sevConfig: Record<string, { bg: string; text: string }> = {
  critical: { bg: "bg-red-600/20 border-red-600/40", text: "text-red-200" },
  high: { bg: "bg-red-500/10 border-red-500/30", text: "text-red-300" },
  medium: { bg: "bg-amber-500/10 border-amber-500/30", text: "text-amber-300" },
  low: { bg: "bg-emerald-500/10 border-emerald-500/30", text: "text-emerald-300" },
};

export default function RedFlagsPanel({ result }: { result: AnalysisResult }) {
  const rf = result.raw_findings.red_flag_agent?.data;
  if (!rf) return null;

  if (!rf.red_flags?.length) {
    return (
      <section className="glass-strong rounded-2xl p-6 md:p-8 animate-fade-up">
        <div className="mb-4">
          <div className="text-xs uppercase tracking-widest text-slate-500 mb-1 font-medium">
            8-K Scan
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Red Flags</h2>
        </div>
        <div className="flex items-center gap-3 text-emerald-300">
          <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          </div>
          <span>No material red flags identified in recent 8-K filings.</span>
        </div>
      </section>
    );
  }

  return (
    <section className="glass-strong rounded-2xl p-6 md:p-8 animate-fade-up">
      <div className="flex items-baseline justify-between mb-6 flex-wrap gap-2">
        <div>
          <div className="text-xs uppercase tracking-widest text-slate-500 mb-1 font-medium">
            8-K Scan
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Red Flags</h2>
        </div>
        <div className="flex gap-3 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-red-500" />
            <span className="text-slate-400 tabular-nums">
              <span className="text-white font-bold">{rf.deal_breakers_count ?? 0}</span> critical
            </span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-amber-500" />
            <span className="text-slate-400 tabular-nums">
              <span className="text-white font-bold">{rf.high_concern_count ?? 0}</span> high
            </span>
          </div>
        </div>
      </div>

      <div className="space-y-3">
        {rf.red_flags.map((f: any, i: number) => {
          const sev = String(f.severity || "").toLowerCase();
          const cfg = sevConfig[sev] || { bg: "bg-white/5 border-white/10", text: "text-slate-300" };
          return (
            <div key={i} className={`glass rounded-xl p-5 border ${cfg.bg} animate-fade-up`} style={{ animationDelay: `${i * 60}ms` }}>
              <div className="flex items-start justify-between gap-3 flex-wrap mb-2">
                <div className="font-semibold text-white">{f.flag}</div>
                <div className="flex gap-2 flex-shrink-0">
                  <span className={`px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wider ${cfg.text} ${cfg.bg}`}>
                    {f.severity}
                  </span>
                  <span className="px-2 py-0.5 rounded-md text-[10px] font-medium uppercase tracking-wider bg-white/5 text-slate-400 border border-white/10 tabular-nums">
                    {f.filing_date}
                  </span>
                </div>
              </div>
              <p className="text-sm text-slate-400 leading-relaxed">{f.description}</p>
            </div>
          );
        })}
      </div>
    </section>
  );
}
