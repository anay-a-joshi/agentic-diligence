"use client";

import { AnalysisResult } from "@/lib/api";

function BulletList({ items, color }: { items: string[]; color: string }) {
  return (
    <ul className="space-y-2">
      {items.map((b, i) => (
        <li key={i} className="flex gap-3">
          <span className={`flex-shrink-0 mt-2 w-1.5 h-1.5 rounded-full ${color}`} />
          <span className="text-slate-700 leading-relaxed">{b}</span>
        </li>
      ))}
    </ul>
  );
}

export default function InvestmentThesis({ result }: { result: AnalysisResult }) {
  const s = result.synthesis;
  if (!s || !s.executive_summary) return null;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 md:p-8">
      <h2 className="text-2xl font-bold text-slate-900 mb-4">Investment Memo</h2>
      <div className="mb-6 p-4 rounded-xl bg-slate-50 border border-slate-200">
        <div className="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-2">
          Executive Summary
        </div>
        <p className="text-slate-800 leading-relaxed">{s.executive_summary}</p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {s.investment_thesis?.length > 0 && (
          <div>
            <h3 className="font-bold text-slate-900 mb-3">Investment Thesis</h3>
            <BulletList items={s.investment_thesis} color="bg-blue-500" />
          </div>
        )}
        {s.value_creation_levers?.length > 0 && (
          <div>
            <h3 className="font-bold text-slate-900 mb-3">Value Creation Levers</h3>
            <BulletList items={s.value_creation_levers} color="bg-green-500" />
          </div>
        )}
        {s.key_risks_to_thesis?.length > 0 && (
          <div>
            <h3 className="font-bold text-slate-900 mb-3">Key Risks to Thesis</h3>
            <BulletList items={s.key_risks_to_thesis} color="bg-amber-500" />
          </div>
        )}
        {s.next_steps?.length > 0 && (
          <div>
            <h3 className="font-bold text-slate-900 mb-3">Recommended Next Steps</h3>
            <BulletList items={s.next_steps} color="bg-indigo-500" />
          </div>
        )}
      </div>
    </div>
  );
}
