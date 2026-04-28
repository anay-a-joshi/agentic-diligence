"use client";

import { AnalysisResult } from "@/lib/api";

export default function FeasibilityScore({ result }: { result: AnalysisResult }) {
  const score = result.feasibility_score ?? 0;
  const grade = result.feasibility_grade ?? "?";
  const verdict = result.feasibility_verdict ?? "";

  const color =
    score >= 70 ? "text-green-600" :
    score >= 50 ? "text-amber-500" : "text-red-600";
  const bgColor =
    score >= 70 ? "bg-green-50 border-green-200" :
    score >= 50 ? "bg-amber-50 border-amber-200" : "bg-red-50 border-red-200";
  const ringColor =
    score >= 70 ? "stroke-green-500" :
    score >= 50 ? "stroke-amber-500" : "stroke-red-500";

  const circumference = 2 * Math.PI * 80;
  const offset = circumference - (score / 100) * circumference;

  const components = result.feasibility_breakdown || {};
  const recommendation = result.synthesis?.recommendation || "—";
  const recColor =
    recommendation.includes("PROCEED TO IC") ? "bg-green-100 text-green-800" :
    recommendation.includes("CAVEATS") ? "bg-amber-100 text-amber-800" :
    "bg-red-100 text-red-800";

  return (
    <div className={`rounded-2xl border-2 ${bgColor} p-6 md:p-8`}>
      <div className="grid md:grid-cols-3 gap-6 items-center">
        <div className="flex flex-col items-center">
          <div className="relative w-48 h-48">
            <svg className="w-48 h-48 -rotate-90" viewBox="0 0 200 200">
              <circle cx="100" cy="100" r="80" strokeWidth="14" fill="none" className="stroke-slate-200" />
              <circle cx="100" cy="100" r="80" strokeWidth="14" fill="none"
                strokeLinecap="round"
                strokeDasharray={circumference}
                strokeDashoffset={offset}
                className={ringColor}
                style={{ transition: "stroke-dashoffset 1s ease-out" }}
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <div className={`text-5xl font-bold ${color}`}>{score}</div>
              <div className="text-sm text-slate-500">/ 100</div>
              <div className={`text-2xl font-bold ${color} mt-1`}>Grade {grade}</div>
            </div>
          </div>
        </div>

        <div className="md:col-span-2">
          <div className="text-xs font-semibold uppercase text-slate-500 tracking-wider mb-1">
            Take-Private Feasibility
          </div>
          <h2 className="text-2xl md:text-3xl font-bold text-slate-900 mb-3">{verdict}</h2>
          <div className={`inline-block px-4 py-2 rounded-lg font-bold text-sm ${recColor} mb-4`}>
            Recommendation: {recommendation}
          </div>
          <p className="text-slate-700 leading-relaxed">
            {result.synthesis?.recommendation_rationale || ""}
          </p>
        </div>
      </div>

      <div className="mt-6 pt-6 border-t border-slate-300/50 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {Object.entries(components).map(([key, comp]) => (
          <div key={key} className="text-center">
            <div className="text-xs text-slate-500 uppercase tracking-wider mb-1">
              {key.replace(/_/g, " ")}
            </div>
            <div className={`text-2xl font-bold ${
              comp.score >= 70 ? "text-green-600" :
              comp.score >= 50 ? "text-amber-500" : "text-red-600"
            }`}>
              {comp.score}
            </div>
            <div className="text-xs text-slate-400">{comp.weight_pct}% weight</div>
          </div>
        ))}
      </div>
    </div>
  );
}
