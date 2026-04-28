"use client";

import { AnalysisResult } from "@/lib/api";

function fmtMoney(v: number | null | undefined): string {
  if (v === null || v === undefined) return "—";
  if (Math.abs(v) >= 1000) return `$${(v / 1000).toFixed(1)}B`;
  return `$${v.toFixed(0)}M`;
}

function fmtPct(v: number | null | undefined): string {
  if (v === null || v === undefined) return "—";
  const sign = v > 0 ? "+" : "";
  return `${sign}${v.toFixed(1)}%`;
}

function MetricCard({
  label, value, sub, accent = "blue", delay = 0,
}: {
  label: string; value: string; sub?: string;
  accent?: "blue" | "violet" | "emerald" | "amber" | "rose" | "cyan";
  delay?: number;
}) {
  const accentColors = {
    blue: "rgba(59, 130, 246, 0.1)",
    violet: "rgba(139, 92, 246, 0.1)",
    emerald: "rgba(16, 185, 129, 0.1)",
    amber: "rgba(245, 158, 11, 0.1)",
    rose: "rgba(244, 63, 94, 0.1)",
    cyan: "rgba(6, 182, 212, 0.1)",
  };

  return (
    <div
      className="glass rounded-xl p-4 hover:bg-white/5 transition-all duration-300 hover:-translate-y-0.5 animate-fade-up relative overflow-hidden group"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div
        className="absolute top-0 right-0 w-32 h-32 rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
        style={{
          background: `radial-gradient(circle, ${accentColors[accent]} 0%, transparent 70%)`,
          transform: "translate(40%, -40%)",
        }}
      />
      <div className="relative">
        <div className="text-[10px] uppercase tracking-widest text-slate-500 font-medium mb-1.5">
          {label}
        </div>
        <div className="text-2xl md:text-3xl font-bold text-white tabular-nums">
          {value}
        </div>
        {sub && (
          <div className="text-xs text-slate-500 mt-1 tabular-nums">{sub}</div>
        )}
      </div>
    </div>
  );
}

export default function FinancialSummary({ result }: { result: AnalysisResult }) {
  const f = result.financial;
  const m = result.raw_findings.market_agent?.data;
  if (!f) return null;
  const fy = f.fiscal_year ? `FY${f.fiscal_year}` : "Latest";

  return (
    <section>
      <div className="flex items-baseline justify-between mb-6">
        <div>
          <div className="text-xs uppercase tracking-widest text-slate-500 mb-1 font-medium">
            Section 02
          </div>
          <h2 className="text-3xl font-bold text-white tracking-tight">
            Headline Metrics
          </h2>
        </div>
        <span className="text-sm text-slate-500 font-mono tabular-nums">{fy}</span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
        <MetricCard label="Revenue" value={fmtMoney(f.revenue_usd_millions)} sub={fmtPct(f.revenue_growth_yoy_pct) + " YoY"} accent="blue" delay={0} />
        <MetricCard label="EBITDA" value={fmtMoney(f.ebitda_usd_millions)} sub={fmtPct(f.ebitda_margin_pct) + " margin"} accent="emerald" delay={50} />
        <MetricCard label="Net Income" value={fmtMoney(f.net_income_usd_millions)} accent="violet" delay={100} />
        <MetricCard label="Free Cash Flow" value={fmtMoney(f.free_cash_flow_usd_millions)} accent="cyan" delay={150} />
        <MetricCard label="Total Debt" value={fmtMoney(f.total_debt_usd_millions)} accent="rose" delay={200} />
        <MetricCard label="Cash" value={fmtMoney(f.cash_and_equivalents_usd_millions)} accent="emerald" delay={250} />
        <MetricCard label="Market Cap" value={fmtMoney(m?.market_cap_usd_millions)} accent="blue" delay={300} />
        <MetricCard label="Enterprise Value" value={fmtMoney(m?.ev_usd_millions)} accent="violet" delay={350} />
        <MetricCard label="P/E Ratio" value={m?.pe_ratio ? `${m.pe_ratio.toFixed(1)}x` : "—"} accent="amber" delay={400} />
        <MetricCard label="EV / EBITDA" value={m?.ev_to_ebitda ? `${m.ev_to_ebitda.toFixed(1)}x` : "—"} accent="amber" delay={450} />
        <MetricCard label="Beta" value={m?.beta ? m.beta.toFixed(2) : "—"} accent="cyan" delay={500} />
        <MetricCard label="52W High" value={m?.["52_week_high"] ? `$${m["52_week_high"].toFixed(2)}` : "—"} accent="emerald" delay={550} />
      </div>
    </section>
  );
}
