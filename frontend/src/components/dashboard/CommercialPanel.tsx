"use client";

import { AnalysisResult } from "@/lib/api";

function PillGroup({ items, color }: { items: string[]; color: "blue" | "violet" | "rose" }) {
  const colors = {
    blue: "bg-blue-500/10 border-blue-500/30 text-blue-300",
    violet: "bg-violet-500/10 border-violet-500/30 text-violet-300",
    rose: "bg-rose-500/10 border-rose-500/30 text-rose-300",
  };
  return (
    <div className="flex flex-wrap gap-2">
      {items.map((s, i) => (
        <span
          key={i}
          className={`px-3 py-1.5 rounded-lg text-sm font-medium border ${colors[color]}`}
        >
          {s}
        </span>
      ))}
    </div>
  );
}

export default function CommercialPanel({ result }: { result: AnalysisResult }) {
  const c = result.raw_findings.commercial_agent?.data;
  if (!c) return null;

  return (
    <section className="glass-strong rounded-2xl p-6 md:p-8 animate-fade-up">
      <div className="mb-6">
        <div className="text-xs uppercase tracking-widest text-slate-500 mb-1 font-medium">
          Commercial Diligence
        </div>
        <h2 className="text-2xl font-bold text-white tracking-tight">
          Business Model
        </h2>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {c.business_segments?.length > 0 && (
          <div>
            <div className="text-[10px] uppercase tracking-widest text-slate-500 font-bold mb-3">
              Business Segments
            </div>
            <PillGroup items={c.business_segments} color="blue" />
          </div>
        )}
        {c.primary_products?.length > 0 && (
          <div>
            <div className="text-[10px] uppercase tracking-widest text-slate-500 font-bold mb-3">
              Primary Products
            </div>
            <PillGroup items={c.primary_products} color="violet" />
          </div>
        )}
        {c.key_competitors?.length > 0 && (
          <div>
            <div className="text-[10px] uppercase tracking-widest text-slate-500 font-bold mb-3">
              Key Competitors
            </div>
            <PillGroup items={c.key_competitors} color="rose" />
          </div>
        )}
        {c.competitive_advantages?.length > 0 && (
          <div>
            <div className="text-[10px] uppercase tracking-widest text-slate-500 font-bold mb-3">
              Competitive Advantages
            </div>
            <ul className="space-y-2">
              {c.competitive_advantages.map((a: string, i: number) => (
                <li key={i} className="flex gap-2 text-sm text-slate-300">
                  <span className="flex-shrink-0 mt-1.5 w-1 h-1 rounded-full bg-emerald-400" />
                  <span>{a}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {c.growth_strategy && (
        <div className="mt-6 glass rounded-xl p-5 border-l-2 border-violet-500">
          <div className="text-[10px] uppercase tracking-widest text-violet-400 font-bold mb-2">
            Growth Strategy
          </div>
          <p className="text-sm text-slate-300 leading-relaxed">{c.growth_strategy}</p>
        </div>
      )}
    </section>
  );
}
