"use client";

import { AnalysisResult } from "@/lib/api";

export default function FeasibilityScore({ result }: { result: AnalysisResult }) {
  const score = result.feasibility_score ?? 0;
  const grade = result.feasibility_grade ?? "?";
  const verdict = result.feasibility_verdict ?? "";

  const isGood = score >= 70;
  const isMid = score >= 50 && score < 70;

  const scoreColor = isGood ? "#10b981" : isMid ? "#f59e0b" : "#ef4444";
  const glowClass = isGood ? "glow-green" : isMid ? "glow-amber" : "glow-red";
  const textGradient = isGood ? "text-gradient-success" : isMid ? "text-gradient-warn" : "text-gradient-danger";

  const circumference = 2 * Math.PI * 90;
  const offset = circumference - (score / 100) * circumference;

  const components = result.feasibility_breakdown || {};
  const recommendation = result.synthesis?.recommendation || "—";

  const recBg =
    recommendation.includes("PROCEED TO IC") ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-300" :
    recommendation.includes("CAVEATS") ? "bg-amber-500/10 border-amber-500/30 text-amber-300" :
    "bg-red-500/10 border-red-500/30 text-red-300";

  return (
    <div className={`glass-strong rounded-3xl p-8 md:p-10 ${glowClass} animate-fade-up relative overflow-hidden`}>
      <div className="absolute top-0 left-0 w-full h-1" style={{ background: `linear-gradient(90deg, transparent, ${scoreColor}, transparent)` }} />

      <div className="grid lg:grid-cols-3 gap-10 items-center">
        <div className="flex justify-center">
          <div className="relative w-56 h-56">
            <div
              className="absolute inset-0 rounded-full"
              style={{
                background: `radial-gradient(circle, ${scoreColor}30 0%, transparent 70%)`,
                filter: "blur(30px)",
              }}
            />
            <svg className="relative w-56 h-56 -rotate-90" viewBox="0 0 220 220">
              <circle cx="110" cy="110" r="90" strokeWidth="14" fill="none" className="stroke-white/5" />
              <circle
                cx="110" cy="110" r="90" strokeWidth="14" fill="none"
                strokeLinecap="round"
                strokeDasharray={circumference}
                strokeDashoffset={offset}
                stroke={scoreColor}
                style={{
                  transition: "stroke-dashoffset 1.5s cubic-bezier(0.34, 1.56, 0.64, 1)",
                  filter: `drop-shadow(0 0 12px ${scoreColor}80)`,
                }}
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <div className={`text-7xl font-bold tabular-nums ${textGradient}`}>
                {score}
              </div>
              <div className="text-sm text-slate-500 tracking-wider tabular-nums">/ 100</div>
              <div
                className="mt-1 text-2xl font-bold tabular-nums"
                style={{ color: scoreColor }}
              >
                Grade {grade}
              </div>
            </div>
          </div>
        </div>

        <div className="lg:col-span-2">
          <div className="text-xs uppercase tracking-widest text-slate-500 mb-2 font-medium">
            Take-Private Feasibility
          </div>
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-5 tracking-tight">
            {verdict}
          </h2>

          <div
            className={`inline-flex items-center gap-2 px-4 py-2 rounded-full border ${recBg} mb-5`}
          >
            <span className="relative flex h-2 w-2">
              <span className="relative inline-flex rounded-full h-2 w-2 bg-current" />
            </span>
            <span className="font-bold text-sm tracking-wide">
              Recommendation · {recommendation}
            </span>
          </div>

          <p className="text-slate-300 leading-relaxed text-lg">
            {result.synthesis?.recommendation_rationale || ""}
          </p>
        </div>
      </div>

      <div className="mt-10 pt-8 border-t border-white/5">
        <div className="text-xs uppercase tracking-widest text-slate-500 mb-4 font-medium">
          Score Breakdown
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          {Object.entries(components).map(([key, comp]) => {
            const compGood = comp.score >= 70;
            const compMid = comp.score >= 50 && comp.score < 70;
            const compColor = compGood ? "#10b981" : compMid ? "#f59e0b" : "#ef4444";
            return (
              <div
                key={key}
                className="glass rounded-xl p-3 hover:bg-white/5 transition-colors"
              >
                <div className="text-[10px] uppercase tracking-widest text-slate-500 mb-1.5 font-medium truncate">
                  {key.replace(/_/g, " ")}
                </div>
                <div
                  className="text-3xl font-bold tabular-nums"
                  style={{ color: compColor }}
                >
                  {comp.score}
                </div>
                <div className="mt-2 h-1 bg-white/5 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-1000"
                    style={{ width: `${comp.score}%`, background: compColor }}
                  />
                </div>
                <div className="text-[10px] text-slate-600 mt-1.5 tabular-nums">
                  {comp.weight_pct}% weight
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
