"use client";

import { AnalysisResult } from "@/lib/api";

export default function CompanyHeader({ result }: { result: AnalysisResult }) {
  const market = result.raw_findings.market_agent?.data;
  const price = market?.current_price;
  const sector = market?.sector;
  const industry = market?.industry;
  const high52 = market?.["52_week_high"];
  const low52 = market?.["52_week_low"];

  const pricePosition = price && high52 && low52
    ? ((price - low52) / (high52 - low52)) * 100
    : 0;

  return (
    <header className="relative pt-12 pb-8 px-6">
      <div className="max-w-7xl mx-auto">
        <div className="glass-strong rounded-3xl p-8 md:p-10 relative overflow-hidden animate-fade-up">
          <div
            className="absolute top-0 right-0 w-96 h-96 rounded-full opacity-20"
            style={{
              background: "radial-gradient(circle, #3b82f6 0%, transparent 70%)",
              filter: "blur(40px)",
              transform: "translate(40%, -40%)",
            }}
          />

          <div className="relative flex flex-col md:flex-row md:items-end md:justify-between gap-6">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-3 mb-3 flex-wrap">
                <span className="px-3 py-1 rounded-lg bg-white/5 border border-white/10 text-sm font-mono font-bold text-blue-400 tabular-nums">
                  {result.ticker}
                </span>
                {sector && (
                  <span className="text-sm text-slate-400">
                    {sector} <span className="text-slate-600 mx-1">·</span> {industry}
                  </span>
                )}
                <span className="text-xs text-slate-600 tabular-nums">
                  CIK {result.cik}
                </span>
              </div>

              <h1 className="text-4xl md:text-6xl font-bold text-white mb-3 tracking-tight">
                {result.company_name}
              </h1>

              <div className="flex flex-wrap items-center gap-3 text-sm">
                <span className="text-slate-400">Take-Private Screening</span>
                <span className="text-slate-700">·</span>
                {Object.entries(result.filings_summary).map(([k, v], i, arr) => (
                  <span key={k} className="text-slate-400 tabular-nums">
                    <span className="font-medium text-slate-200">{v}</span> {k}
                    {i < arr.length - 1 && <span className="text-slate-700 ml-3">·</span>}
                  </span>
                ))}
              </div>
            </div>

            {price !== undefined && price !== null && (
              <div className="text-right flex-shrink-0">
                <div className="text-xs uppercase tracking-widest text-slate-500 mb-1 font-medium">
                  Last
                </div>
                <div className="text-5xl md:text-6xl font-bold tabular-nums text-gradient">
                  ${typeof price === "number" ? price.toFixed(2) : price}
                </div>
                {market?.market_cap_usd_millions && (
                  <div className="text-sm text-slate-400 mt-2 tabular-nums">
                    Market Cap{" "}
                    <span className="text-slate-200 font-medium">
                      ${(market.market_cap_usd_millions / 1000).toFixed(1)}B
                    </span>
                  </div>
                )}
                {high52 && low52 && (
                  <div className="mt-3 w-48 ml-auto">
                    <div className="flex justify-between text-xs text-slate-500 mb-1.5 tabular-nums">
                      <span>${low52?.toFixed(0)}</span>
                      <span>${high52?.toFixed(0)}</span>
                    </div>
                    <div className="relative h-1 bg-white/5 rounded-full">
                      <div
                        className="absolute inset-y-0 left-0 rounded-full"
                        style={{
                          width: `${Math.min(100, Math.max(0, pricePosition))}%`,
                          background: "linear-gradient(90deg, #3b82f6, #8b5cf6)",
                        }}
                      />
                      <div
                        className="absolute top-1/2 -translate-y-1/2 w-3 h-3 rounded-full bg-white border-2 border-blue-500 shadow-lg"
                        style={{ left: `calc(${Math.min(100, Math.max(0, pricePosition))}% - 6px)` }}
                      />
                    </div>
                    <div className="text-xs text-slate-500 mt-1.5 text-center">
                      52-week range
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
