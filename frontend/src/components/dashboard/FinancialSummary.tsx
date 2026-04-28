"use client";

import { AnalysisResult } from "@/lib/api";

function fmtMoney(v: number | null | undefined): string {
  if (v === null || v === undefined) return "-";
  if (Math.abs(v) >= 1000) return `$${(v / 1000).toFixed(1)}B`;
  return `$${v.toFixed(0)}M`;
}

function fmtPct(v: number | null | undefined): string {
  if (v === null || v === undefined) return "-";
  return `${v.toFixed(1)}%`;
}

function MetricCard({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-4">
      <div className="text-xs text-slate-500 uppercase tracking-wider mb-1">{label}</div>
      <div className="text-2xl font-bold text-slate-900 tabular-nums">{value}</div>
      {sub && <div className="text-xs text-slate-500 mt-1">{sub}</div>}
    </div>
  );
}

export default function FinancialSummary({ result }: { result: AnalysisResult }) {
  const f = result.financial;
  const m = result.raw_findings.market_agent?.data;
  if (!f) return null;
  const fy = f.fiscal_year ? `FY${f.fiscal_year}` : "Latest";

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-slate-900">Headline Metrics</h2>
        <span className="text-sm text-slate-500">{fy}</span>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
        <MetricCard label="Revenue" value={fmtMoney(f.revenue_usd_millions)} sub={fmtPct(f.revenue_growth_yoy_pct) + " YoY"} />
        <MetricCard label="EBITDA" value={fmtMoney(f.ebitda_usd_millions)} sub={fmtPct(f.ebitda_margin_pct) + " margin"} />
        <MetricCard label="Net Income" value={fmtMoney(f.net_income_usd_millions)} />
        <MetricCard label="Free Cash Flow" value={fmtMoney(f.free_cash_flow_usd_millions)} />
        <MetricCard label="Total Debt" value={fmtMoney(f.total_debt_usd_millions)} />
        <MetricCard label="Cash" value={fmtMoney(f.cash_and_equivalents_usd_millions)} />
        <MetricCard label="Market Cap" value={fmtMoney(m?.market_cap_usd_millions)} />
        <MetricCard label="Enterprise Value" value={fmtMoney(m?.ev_usd_millions)} />
        <MetricCard label="P/E Ratio" value={m?.pe_ratio ? `${m.pe_ratio.toFixed(1)}x` : "-"} />
        <MetricCard label="EV / EBITDA" value={m?.ev_to_ebitda ? `${m.ev_to_ebitda.toFixed(1)}x` : "-"} />
        <MetricCard label="Beta" value={m?.beta ? m.beta.toFixed(2) : "-"} />
        <MetricCard label="52W High" value={m?.["52_week_high"] ? `$${m["52_week_high"].toFixed(2)}` : "-"} />
      </div>
    </div>
  );
}
