"use client";

import { AnalysisResult } from "@/lib/api";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, Area, AreaChart } from "recharts";

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload || !payload.length) return null;
  return (
    <div className="glass-strong rounded-xl p-3 border border-white/10">
      <div className="text-xs uppercase tracking-widest text-slate-500 font-medium mb-2">
        {label}
      </div>
      {payload.map((entry: any) => (
        <div key={entry.name} className="flex items-center justify-between gap-4 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full" style={{ background: entry.color }} />
            <span className="text-slate-300">{entry.name}</span>
          </div>
          <span className="font-bold text-white tabular-nums">${entry.value.toFixed(1)}B</span>
        </div>
      ))}
    </div>
  );
};

export default function LBOChart({ result }: { result: AnalysisResult }) {
  const base = result.lbo_full?.base;
  if (!base) return null;

  const data = base.projections.year.map((yr, idx) => ({
    year: `Y${yr}`,
    Revenue: Math.round(base.projections.revenue_usd_millions[idx] / 1000),
    EBITDA: Math.round(base.projections.ebitda_usd_millions[idx] / 1000),
    "Debt Balance": Math.round(base.projections.debt_balance_usd_millions[idx] / 1000),
  }));

  return (
    <section className="glass-strong rounded-2xl p-6 md:p-8 animate-fade-up relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-blue-500 to-transparent opacity-50" />

      <div className="flex items-baseline justify-between mb-6">
        <div>
          <div className="text-xs uppercase tracking-widest text-slate-500 mb-1 font-medium">
            5-Year Projections
          </div>
          <h3 className="text-2xl font-bold text-white tracking-tight">
            Base Case
          </h3>
        </div>
        <span className="text-sm text-slate-500 font-mono tabular-nums">USD Billions</span>
      </div>

      <ResponsiveContainer width="100%" height={320}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="grad-rev" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#3b82f6" stopOpacity={0.4} />
              <stop offset="100%" stopColor="#3b82f6" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="grad-ebitda" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#10b981" stopOpacity={0.4} />
              <stop offset="100%" stopColor="#10b981" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="grad-debt" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#ef4444" stopOpacity={0.3} />
              <stop offset="100%" stopColor="#ef4444" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.08)" vertical={false} />
          <XAxis
            dataKey="year"
            stroke="#64748b"
            tick={{ fill: "#64748b", fontSize: 12 }}
            tickLine={false}
            axisLine={{ stroke: "rgba(148, 163, 184, 0.1)" }}
          />
          <YAxis
            stroke="#64748b"
            tick={{ fill: "#64748b", fontSize: 12 }}
            tickLine={false}
            axisLine={{ stroke: "rgba(148, 163, 184, 0.1)" }}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ stroke: "rgba(148, 163, 184, 0.2)" }} />
          <Legend
            iconType="circle"
            wrapperStyle={{ paddingTop: 10, fontSize: 12 }}
            formatter={(v) => <span className="text-slate-300">{v}</span>}
          />
          <Area type="monotone" dataKey="Revenue" stroke="#3b82f6" strokeWidth={2.5} fill="url(#grad-rev)" />
          <Area type="monotone" dataKey="EBITDA" stroke="#10b981" strokeWidth={2.5} fill="url(#grad-ebitda)" />
          <Area type="monotone" dataKey="Debt Balance" stroke="#ef4444" strokeWidth={2.5} fill="url(#grad-debt)" />
        </AreaChart>
      </ResponsiveContainer>
    </section>
  );
}
