"use client";

import { AnalysisResult } from "@/lib/api";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";

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
    <div className="bg-white rounded-2xl border border-slate-200 p-6">
      <div className="flex items-baseline justify-between mb-4">
        <h3 className="text-xl font-bold text-slate-900">5-Year Projections (Base Case)</h3>
        <span className="text-sm text-slate-500">$B</span>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis dataKey="year" stroke="#64748b" />
          <YAxis stroke="#64748b" />
          <Tooltip formatter={(v: number) => `$${v.toFixed(1)}B`}
            contentStyle={{ borderRadius: 8, border: "1px solid #e2e8f0" }} />
          <Legend />
          <Line type="monotone" dataKey="Revenue" stroke="#3b82f6" strokeWidth={2.5} dot={{ r: 4 }} />
          <Line type="monotone" dataKey="EBITDA" stroke="#10b981" strokeWidth={2.5} dot={{ r: 4 }} />
          <Line type="monotone" dataKey="Debt Balance" stroke="#ef4444" strokeWidth={2.5} dot={{ r: 4 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
