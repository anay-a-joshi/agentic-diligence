"use client";

import { AnalysisResult } from "@/lib/api";

function BulletList({ items, color, glowColor }: { items: string[]; color: string; glowColor: string }) {
  return (
    <ul className="space-y-3">
      {items.map((b, i) => (
        <li key={i} className="flex gap-3">
          <span className="flex-shrink-0 mt-2 w-1.5 h-1.5 rounded-full"
            style={{
              background: color,
              boxShadow: `0 0 8px ${glowColor}`,
            }}
          />
          <span className="text-slate-300 leading-relaxed">{b}</span>
        </li>
      ))}
    </ul>
  );
}

const sections = [
  { key: "investment_thesis", title: "Investment Thesis", color: "#3b82f6", glow: "rgba(59, 130, 246, 0.6)" },
  { key: "value_creation_levers", title: "Value Creation Levers", color: "#10b981", glow: "rgba(16, 185, 129, 0.6)" },
  { key: "key_risks_to_thesis", title: "Key Risks", color: "#f59e0b", glow: "rgba(245, 158, 11, 0.6)" },
  { key: "next_steps", title: "Next Steps", color: "#8b5cf6", glow: "rgba(139, 92, 246, 0.6)" },
];

export default function InvestmentThesis({ result }: { result: AnalysisResult }) {
  const s: any = result.synthesis;
  if (!s || !s.executive_summary) return null;

  return (
    <section className="glass-strong rounded-2xl p-6 md:p-10 animate-fade-up relative overflow-hidden">
      <div
        className="absolute top-0 right-0 w-96 h-96 rounded-full opacity-20"
        style={{
          background: "radial-gradient(circle, #8b5cf6 0%, transparent 70%)",
          filter: "blur(60px)",
          transform: "translate(40%, -40%)",
        }}
      />

      <div className="relative">
        <div className="mb-8">
          <div className="text-xs uppercase tracking-widest text-slate-500 mb-1 font-medium">
            Section 01
          </div>
          <h2 className="text-3xl font-bold text-white tracking-tight">
            Investment Memo
          </h2>
        </div>

        <div className="mb-10 glass rounded-xl p-6 border-l-2 border-blue-500">
          <div className="text-[10px] uppercase tracking-widest text-blue-400 font-bold mb-3">
            Executive Summary
          </div>
          <p className="text-slate-200 leading-relaxed text-lg font-light">
            {s.executive_summary}
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-x-10 gap-y-8">
          {sections.map(({ key, title, color, glow }) => {
            const items = s[key];
            if (!items?.length) return null;
            return (
              <div key={key}>
                <div className="flex items-center gap-2 mb-4">
                  <div className="w-1 h-5 rounded-full" style={{ background: color, boxShadow: `0 0 10px ${glow}` }} />
                  <h3 className="text-lg font-semibold text-white">{title}</h3>
                </div>
                <BulletList items={items} color={color} glowColor={glow} />
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
