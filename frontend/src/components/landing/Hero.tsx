"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function Hero() {
  const [ticker, setTicker] = useState("");
  const router = useRouter();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const t = ticker.trim().toUpperCase();
    if (t) router.push(`/analyze/${t}`);
  };

  const examples = [
    { ticker: "DELL", label: "Dell", note: "$60B" },
    { ticker: "HUBB", label: "Hubbell", note: "$25B" },
    { ticker: "NCR", label: "NCR Voyix", note: "$1B" },
    { ticker: "AAPL", label: "Apple", note: "$3.9T" },
    { ticker: "WBA", label: "Walgreens", note: "$8B" },
  ];

  return (
    <section className="relative min-h-screen flex items-center justify-center px-6 py-20">
      <div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[1200px] h-[1200px] pointer-events-none animate-pulse-glow"
        style={{
          background: "radial-gradient(circle, rgba(59, 130, 246, 0.15) 0%, transparent 60%)",
          filter: "blur(60px)",
        }}
      />

      <div className="relative max-w-5xl mx-auto text-center w-full">
        <div
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-8 animate-fade-up"
          style={{ animationDelay: "0ms" }}
        >
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-400" />
          </span>
          <span className="text-sm text-slate-300 font-medium">
            Live · 8 specialist AI agents · SEC EDGAR data
          </span>
        </div>

        <h1
          className="text-6xl md:text-8xl font-bold tracking-tight mb-6 animate-fade-up leading-[1.05]"
          style={{ animationDelay: "100ms" }}
        >
          <span className="text-gradient">Take-Private</span>
          <br />
          <span className="text-gradient-blue">Screening, Reimagined.</span>
        </h1>

        <p
          className="text-xl md:text-2xl text-slate-400 max-w-3xl mx-auto mb-12 animate-fade-up font-light leading-relaxed"
          style={{ animationDelay: "200ms" }}
        >
          Eight agents read SEC filings. One synthesis writes the IC memo.
          <br className="hidden md:block" />
          What used to take 4–8 weeks now takes <span className="text-white font-medium">2 minutes</span>.
        </p>

        <form
          onSubmit={handleSubmit}
          className="max-w-2xl mx-auto animate-fade-up"
          style={{ animationDelay: "300ms" }}
        >
          <div className="relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 via-violet-600 to-cyan-500 rounded-2xl opacity-50 group-hover:opacity-100 blur-lg transition-opacity duration-500" />
            <div className="relative glass-strong rounded-2xl p-2 flex items-center gap-2">
              <div className="pl-4 pr-2 text-slate-400">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="11" cy="11" r="8" />
                  <line x1="21" y1="21" x2="16.65" y2="16.65" />
                </svg>
              </div>
              <input
                type="text"
                value={ticker}
                onChange={(e) => setTicker(e.target.value.toUpperCase())}
                placeholder="Enter any U.S. ticker..."
                className="flex-1 bg-transparent text-white text-lg placeholder:text-slate-500 focus:outline-none py-3 tabular-nums tracking-wide"
                autoFocus
              />
              <button
                type="submit"
                className="relative px-6 py-3 rounded-xl font-semibold text-white overflow-hidden group/btn transition-transform active:scale-95"
                style={{
                  background: "linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)",
                  boxShadow: "0 8px 32px rgba(59, 130, 246, 0.4)",
                }}
              >
                <span className="relative flex items-center gap-2">
                  Analyze
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="5" y1="12" x2="19" y2="12" />
                    <polyline points="12 5 19 12 12 19" />
                  </svg>
                </span>
              </button>
            </div>
          </div>

          <div
            className="mt-8 animate-fade-up"
            style={{ animationDelay: "500ms" }}
          >
            <div className="text-xs uppercase tracking-widest text-slate-500 mb-3">
              Try a real LBO target
            </div>
            <div className="flex flex-wrap justify-center gap-2">
              {examples.map((ex) => (
                <button
                  key={ex.ticker}
                  type="button"
                  onClick={() => router.push(`/analyze/${ex.ticker}`)}
                  className="group/chip flex items-center gap-2 px-4 py-2 rounded-xl glass hover:glass-strong transition-all hover:-translate-y-0.5"
                >
                  <span className="font-mono font-bold text-blue-400 group-hover/chip:text-blue-300">
                    {ex.ticker}
                  </span>
                  <span className="text-slate-400 text-sm">{ex.label}</span>
                  <span className="text-xs text-slate-500 tabular-nums">{ex.note}</span>
                </button>
              ))}
            </div>
          </div>
        </form>

        <div
          className="mt-20 grid grid-cols-3 gap-8 max-w-2xl mx-auto animate-fade-up"
          style={{ animationDelay: "700ms" }}
        >
          {[
            { val: "2 min", label: "vs 4–8 weeks" },
            { val: "$300K", label: "of work, free" },
            { val: "8", label: "AI agents" },
          ].map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-gradient-blue tabular-nums">
                {stat.val}
              </div>
              <div className="text-xs uppercase tracking-widest text-slate-500 mt-1">
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
