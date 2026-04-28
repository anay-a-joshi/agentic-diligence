"use client";

import { AnalysisResult } from "@/lib/api";

const sevConfig: Record<string, { bg: string; text: string; glow: string }> = {
  high: { bg: "bg-red-500/10 border-red-500/30", text: "text-red-300", glow: "shadow-red-500/20" },
  medium: { bg: "bg-amber-500/10 border-amber-500/30", text: "text-amber-300", glow: "shadow-amber-500/20" },
  low: { bg: "bg-emerald-500/10 border-emerald-500/30", text: "text-emerald-300", glow: "shadow-emerald-500/20" },
  critical: { bg: "bg-red-600/20 border-red-600/40", text: "text-red-200", glow: "shadow-red-600/30" },
};

export default function RiskPanel({ result }: { result: AnalysisResult }) {
  const risk = result.raw_findings.risk_agent?.data;
  if (!risk?.top_risks?.length) return null;

  return (
    <section className="glass-strong rounded-2xl p-6 md:p-8 animate-fade-up">
      <div className="flex items-baseline justify-between mb-6 flex-wrap gap-2">
        <div>
          <div className="text-xs uppercase tracking-widest text-slate-500 mb-1 font-medium">
            Risk Analysis
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Top Risks</h2>
        </div>
        <div className="flex gap-3 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-red-400" />
            <span className="text-slate-400 tabular-nums">
              <span className="text-white font-bold">{risk.high_severity_count ?? 0}</span> high
            </span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-slate-500" />
            <span className="text-slate-400 tabular-nums">
              <span className="text-white font-bold">{risk.total_risks_disclosed ?? 0}</span> total
            </span>
          </div>
        </div>
      </div>

      <div className="space-y-3">
        {risk.top_risks.map((r: any, i: number) => {
          const sev = String(r.severity || "").toLowerCase();
          const cfg = sevConfig[sev] || { bg: "bg-white/5 border-white/10", text: "text-slate-300", glow: "" };
          return (
            <div
              key={i}
              className={`glass rounded-xl p-5 border ${cfg.bg} animate-fade-up`}
              style={{ animationDelay: `${i * 60}ms` }}
            >
              <div className="flex items-start justify-between gap-3 flex-wrap mb-2">
                <div className="flex items-center gap-3 flex-1 min-w-0">
                  <div className="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center flex-shrink-0 text-xs font-mono font-bold text-slate-400 tabular-nums">
                    {String(i + 1).padStart(2, "0")}
                  </div>
                  <div className="font-semibold text-white">{r.risk}</div>
                </div>
                <div className="flex gap-2 flex-shrink-0">
                  <span className={`px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wider ${cfg.text} ${cfg.bg}`}>
                    {r.severity}
                  </span>
                  <span className="px-2 py-0.5 rounded-md text-[10px] font-medium uppercase tracking-wider bg-white/5 text-slate-400 border border-white/10">
                    {r.category}
                  </span>
                </div>
              </div>
              <p className="text-sm text-slate-400 leading-relaxed pl-11">{r.description}</p>
            </div>
          );
        })}
      </div>
    </section>
  );
}
