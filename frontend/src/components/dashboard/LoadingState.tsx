"use client";

import { useEffect, useState } from "react";

const AGENT_STAGES = [
  { name: "Fetching SEC filings", duration: 2000 },
  { name: "Financial Agent - extracting XBRL data", duration: 3000 },
  { name: "Commercial Agent - analyzing business model", duration: 8000 },
  { name: "Risk Agent - scoring risk factors", duration: 8000 },
  { name: "Governance Agent - assessing takeover defenses", duration: 8000 },
  { name: "Market Agent - pulling market data", duration: 2000 },
  { name: "Sentiment Agent - analyzing management tone", duration: 8000 },
  { name: "Red Flag Agent - scanning 8-Ks", duration: 8000 },
  { name: "LBO Engine - running Base/Bull/Bear scenarios", duration: 1000 },
  { name: "Computing feasibility score", duration: 1000 },
  { name: "Synthesis Agent - writing IC memo", duration: 5000 },
  { name: "Generating PDF + Excel deliverables", duration: 2000 },
];

export default function LoadingState({ ticker }: { ticker: string }) {
  const [stageIdx, setStageIdx] = useState(0);

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
    return () => { cancelled = true; };
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center px-6">
      <div className="max-w-2xl w-full">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-sm font-medium mb-4">
            <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
            Analyzing {ticker}
          </div>
          <h1 className="text-3xl font-bold text-slate-900 mb-2">
            8 Agents Running in Sequence
          </h1>
          <p className="text-slate-600">
            This typically takes 60-120 seconds. Each agent reads SEC filings and produces structured output.
          </p>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
          <div className="space-y-3">
            {AGENT_STAGES.map((stage, idx) => {
              const isDone = idx < stageIdx;
              const isActive = idx === stageIdx;
              return (
                <div
                  key={stage.name}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                    isActive ? "bg-blue-50 border border-blue-200" :
                    isDone ? "bg-green-50/50" : "bg-slate-50"
                  }`}
                >
                  <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 ${
                    isDone ? "bg-green-500 text-white" :
                    isActive ? "bg-blue-500 text-white" :
                    "bg-slate-200 text-slate-400"
                  }`}>
                    {isDone ? "X" : isActive ? "..." : idx + 1}
                  </div>
                  <span className={`text-sm ${
                    isActive ? "font-semibold text-slate-900" :
                    isDone ? "text-slate-600" : "text-slate-500"
                  }`}>
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
