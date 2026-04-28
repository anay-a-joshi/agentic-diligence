"use client";

import { AnalysisResult } from "@/lib/api";

export default function CompanyHeader({ result }: { result: AnalysisResult }) {
  const market = result.raw_findings.market_agent?.data;
  const price = market?.current_price;
  const sector = market?.sector;
  const industry = market?.industry;

  return (
    <div className="bg-gradient-to-r from-slate-900 to-slate-800 text-white">
      <div className="max-w-7xl mx-auto px-6 py-10">
        <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 mb-2 flex-wrap">
              <span className="px-3 py-1 rounded-md bg-white/10 text-sm font-mono font-bold">
                {result.ticker}
              </span>
              {sector && (
                <span className="text-sm text-slate-300">
                  {sector} - {industry}
                </span>
              )}
              <span className="text-xs text-slate-400">
                CIK {result.cik}
              </span>
            </div>
            <h1 className="text-4xl font-bold mb-2">{result.company_name}</h1>
            <p className="text-slate-300">
              Take-Private Screening - {Object.entries(result.filings_summary)
                .map(([k, v]) => `${v} ${k}`).join(" - ")}
            </p>
          </div>
          {price !== undefined && price !== null && (
            <div className="text-right">
              <div className="text-sm text-slate-400 mb-1">Current Price</div>
              <div className="text-4xl font-bold tabular-nums">
                ${typeof price === "number" ? price.toFixed(2) : price}
              </div>
              {market?.market_cap_usd_millions && (
                <div className="text-sm text-slate-300 mt-1">
                  Market Cap: ${(market.market_cap_usd_millions / 1000).toFixed(1)}B
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
