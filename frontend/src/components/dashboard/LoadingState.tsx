"use client";

import { useEffect, useState } from "react";

const AGENT_STAGES = [
  { name: "Fetching SEC filings", duration: 2000 },
  { name: "Financial Agent — extracting XBRL data", duration: 3000 },
  { name: "Commercial Agent — analyzing business model", duration: 8000 },
  { name: "Risk Agent — scoring risk factors", duration: 8000 },
  { name: "Governance Agent — assessing takeover defenses", duration: 8000 },
  { name: "Market Agent — pulling live market data", duration: 2000 },
  { name: "Sentiment Agent — analyzing management tone", duration: 8000 },
  { name: "Red Flag Agent — scanning recent 8-Ks", duration: 8000 },
  { name: "LBO Engine — running Bull/Base/Bear scenarios", duration: 1000 },
  { name: "Computing feasibility score", duration: 1000 },
  { name: "Synthesis Agent — writing IC memo", duration: 5000 },
  { name: "Generating PDF + Excel deliverables", duration: 2000 },
];

export default function LoadingState({ ticker }: { ticker: string }) {
  const [stageIdx, setStageIdx] = useState(0);
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    let cancelled = false;
    let i = 0;
    const tick = () => {
      if (cancelled || i >= AGENT_STAGES.length) return;
      setStageIdx(i);
      const dur = AGENT_STAGES[i]?.duration ?? 3000;
      i += 1;
      setTimeout(tick, dur);
    };
    tick();

    const elapsedTimer = setInterval(() => setElapsed((e) => e + 1), 1000);
    return () => {
      cancelled = true;
      clearInterval(elapsedTimer);
    };
  }, []);

  const progress = ((stageIdx + 1) / AGENT_STAGES.length) * 100;

  return (
    <div className="min-h-screen flex items-center justify-center px-6 py-12">
      <div className="max-w-2xl w-full">
        <div className="text-center mb-10 animate-fade-up">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-6">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-400" />
            </span>
            <span className="text-sm text-slate-300 font-medium tabular-nums">
              Analyzing {ticker} · {elapsed}s
            </span>
          </div>

          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="text-gradient">Multi-agent pipeline</span>
            <br />
            <span className="text-gradient-blue">in flight</span>
          </h1>

          <p className="text-slate-400">
            Eight specialist agents working in sequence. Typical run: 60–120 seconds.
          </p>
        </div>

        <div className="glass-strong rounded-2xl p-6 mb-6 animate-fade-up" style={{ animationDelay: "100ms" }}>
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs uppercase tracking-widest text-slate-500 font-medium">
              Progress
            </span>
            <span className="text-sm tabular-nums text-slate-300 font-medium">
              {Math.round(progress)}%
            </span>
          </div>
          <div className="relative h-2 bg-white/5 rounded-full overflow-hidden">
            <div
              className="absolute inset-y-0 left-0 rounded-full transition-all duration-1000 ease-out"
              style={{
                width: `${progress}%`,
                background: "linear-gradient(90deg, #3b82f6 0%, #8b5cf6 50%, #06b6d4 100%)",
                boxShadow: "0 0 20px rgba(59, 130, 246, 0.6)",
              }}
            />
          </div>
        </div>

        <div className="glass-strong rounded-2xl p-3 animate-fade-up" style={{ animationDelay: "200ms" }}>
          <div className="space-y-1">
            {AGENT_STAGES.map((stage, idx) => {
              const isDone = idx < stageIdx;
              const isActive = idx === stageIdx;
              return (
                <div
                  key={stage.name}
                  className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 ${
                    isActive ? "bg-blue-500/10" : "bg-transparent"
                  }`}
                >
                  <div className="flex-shrink-0">
                    {isDone ? (
                      <div className="w-7 h-7 rounded-full bg-emerald-500 flex items-center justify-center" style={{ boxShadow: "0 0 16px rgba(16, 185, 129, 0.5)" }}>
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                          <polyline points="20 6 9 17 4 12" />
                        </svg>
                      </div>
                    ) : isActive ? (
                      <div className="w-7 h-7 rounded-full bg-blue-500 flex items-center justify-center relative" style={{ boxShadow: "0 0 16px rgba(59, 130, 246, 0.6)" }}>
                        <div className="absolute inset-0 rounded-full bg-blue-400 animate-ping opacity-75" />
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" className="relative animate-spin">
                          <line x1="12" y1="2" x2="12" y2="6" />
                          <line x1="12" y1="18" x2="12" y2="22" />
                          <line x1="4.93" y1="4.93" x2="7.76" y2="7.76" />
                          <line x1="16.24" y1="16.24" x2="19.07" y2="19.07" />
                          <line x1="2" y1="12" x2="6" y2="12" />
                          <line x1="18" y1="12" x2="22" y2="12" />
                        </svg>
                      </div>
                    ) : (
                      <div className="w-7 h-7 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-xs font-mono text-slate-500 tabular-nums">
                        {String(idx + 1).padStart(2, "0")}
                      </div>
                    )}
                  </div>
                  <span
                    className={`text-sm transition-colors ${
                      isActive ? "text-white font-medium" :
                      isDone ? "text-slate-400" : "text-slate-600"
                    }`}
                  >
                    {stage.name}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
