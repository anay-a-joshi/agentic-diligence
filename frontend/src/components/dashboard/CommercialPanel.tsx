"use client";

import { AnalysisResult } from "@/lib/api";

export default function CommercialPanel({ result }: { result: AnalysisResult }) {
  const c = result.raw_findings.commercial_agent?.data;
  if (!c) return null;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6">
      <h2 className="text-2xl font-bold text-slate-900 mb-4">Commercial Diligence</h2>
      <div className="grid md:grid-cols-2 gap-6">
        {c.business_segments?.length > 0 && (
          <div>
            <div className="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-2">Business Segments</div>
            <div className="flex flex-wrap gap-2">
              {c.business_segments.map((s: string, i: number) => (
                <span key={i} className="px-3 py-1 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-sm">{s}</span>
              ))}
            </div>
          </div>
        )}
        {c.primary_products?.length > 0 && (
          <div>
            <div className="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-2">Primary Products</div>
            <div className="flex flex-wrap gap-2">
              {c.primary_products.map((p: string, i: number) => (
                <span key={i} className="px-3 py-1 rounded-full bg-purple-50 border border-purple-200 text-purple-700 text-sm">{p}</span>
              ))}
            </div>
          </div>
        )}
        {c.key_competitors?.length > 0 && (
          <div>
            <div className="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-2">Key Competitors</div>
            <div className="flex flex-wrap gap-2">
              {c.key_competitors.map((k: string, i: number) => (
                <span key={i} className="px-3 py-1 rounded-full bg-red-50 border border-red-200 text-red-700 text-sm">{k}</span>
              ))}
            </div>
          </div>
        )}
        {c.competitive_advantages?.length > 0 && (
          <div>
            <div className="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-2">Competitive Advantages</div>
            <ul className="space-y-1">
              {c.competitive_advantages.map((a: string, i: number) => (
                <li key={i} className="text-sm text-slate-700">- {a}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
      {c.growth_strategy && (
        <div className="mt-4 p-4 rounded-xl bg-slate-50 border border-slate-200">
          <div className="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-1">Growth Strategy</div>
          <p className="text-sm text-slate-700 leading-relaxed">{c.growth_strategy}</p>
        </div>
      )}
    </div>
  );
}
