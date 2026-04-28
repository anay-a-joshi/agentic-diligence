"use client";

import { AnalysisResult } from "@/lib/api";

export default function LBOReturns({ result }: { result: AnalysisResult }) {
  const lbo = result.lbo_full;
  if (!lbo || lbo.status !== "ok" || !lbo.base) return null;

  const scenarios = [
    { name: "Bull", scenario: lbo.bull, color: "#10b981", glow: "glow-green" },
    { name: "Base", scenario: lbo.base, color: "#f59e0b", glow: "glow-amber" },
    { name: "Bear", scenario: lbo.bear, color: "#ef4444", glow: "glow-red" },
  ];

  return (
    <section>
      <div className="mb-6">
        <div className="text-xs uppercase tracking-widest text-slate-500 mb-1 font-medium">
          Section 03
        </div>
        <h2 className="text-3xl font-bold text-white tracking-tight">
          LBO Returns
        </h2>
      </div>

      {lbo.size_prohibitive && (
        <div className="mb-6 glass rounded-xl px-5 py-4 border border-amber-500/20 flex items-start gap-3 animate-fade-up">
          <div className="w-8 h-8 rounded-full bg-amber-500/20 flex items-center justify-center flex-shrink-0">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
              <line x1="12" y1="9" x2="12" y2="13" />
              <line x1="12" y1="17" x2="12.01" y2="17" />
            </svg>
          </div>
          <div className="flex-1">
            <div className="text-amber-300 font-semibold text-sm mb-1">Size-Prohibitive Deal</div>
            <div className="text-slate-300 text-sm">{lbo.size_prohibitive_note}</div>
          </div>
        </div>
      )}

      <div className="grid md:grid-cols-3 gap-4">
        {scenarios.map(({ name, scenario, color, glow }, i) => {
          if (!scenario) return null;
          const irr = scenario.returns.irr_pct;
          const moic = scenario.returns.moic;
          const exit_eq = scenario.exit.exit_equity_value_usd_millions;
          const irrIsGood = irr >= 15;

          return (
            <div
              key={name}
              className={`glass-strong rounded-2xl p-6 ${glow} animate-fade-up relative overflow-hidden`}
              style={{ animationDelay: `${i * 100}ms` }}
            >
              <div
                className="absolute top-0 right-0 w-40 h-40 rounded-full opacity-30"
                style={{
                  background: `radial-gradient(circle, ${color}40 0%, transparent 60%)`,
                  filter: "blur(30px)",
                  transform: "translate(40%, -40%)",
                }}
              />

              <div className="relative">
                <div className="flex items-center justify-between mb-6">
                  <div className="text-xs uppercase tracking-widest font-bold" style={{ color }}>
                    {name} Case
                  </div>
                  <div
                    className="px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tabular-nums"
                    style={{
                      background: `${color}20`,
                      color: color,
                    }}
                  >
                    5y hold
                  </div>
                </div>

                <div className="mb-6">
                  <div className="text-[10px] uppercase tracking-widest text-slate-500 font-medium mb-1">
                    IRR
                  </div>
                  <div
                    className="text-5xl font-bold tabular-nums"
                    style={{ color }}
                  >
                    {irr > 0 ? "+" : ""}{irr.toFixed(1)}%
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3 pt-5 border-t border-white/5">
                  <div>
                    <div className="text-[10px] uppercase tracking-widest text-slate-500 font-medium mb-1">
                      MOIC
                    </div>
                    <div className="text-xl font-bold tabular-nums text-white">
                      {moic.toFixed(2)}x
                    </div>
                  </div>
                  <div>
                    <div className="text-[10px] uppercase tracking-widest text-slate-500 font-medium mb-1">
                      Exit Equity
                    </div>
                    <div className="text-xl font-bold tabular-nums text-white">
                      ${(exit_eq / 1000).toFixed(1)}B
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
