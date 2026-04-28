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

  const examples = ["DELL", "HUBB", "NCR", "AAPL", "WBA"];

  return (
    <section className="relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-slate-50 via-white to-blue-50" />
      <div className="absolute -top-40 -right-40 w-96 h-96 bg-blue-100 rounded-full blur-3xl opacity-50" />
      <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-indigo-100 rounded-full blur-3xl opacity-50" />

      <div className="relative max-w-6xl mx-auto px-6 pt-20 pb-24">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-sm font-medium mb-6">
            <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
            Agentic AI for Private Equity Diligence
          </div>

          <h1 className="text-5xl md:text-6xl font-bold text-slate-900 tracking-tight mb-6 leading-tight">
            Take-Private Screening
            <br />
            <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              in Two Minutes, Not Two Months
            </span>
          </h1>

          <p className="text-xl text-slate-600 max-w-2xl mx-auto mb-12">
            Eight specialist AI agents analyze SEC filings, build a 5-year LBO model,
            and produce an investment-grade IC memo for any U.S. public company.
          </p>

          <form onSubmit={handleSubmit} className="max-w-xl mx-auto">
            <div className="flex flex-col sm:flex-row gap-3">
              <input
                type="text"
                value={ticker}
                onChange={(e) => setTicker(e.target.value)}
                placeholder="Enter ticker (e.g. DELL, HUBB, NCR)"
                className="flex-1 px-6 py-4 text-lg rounded-xl border-2 border-slate-200 focus:border-blue-500 focus:outline-none focus:ring-4 focus:ring-blue-100 transition-all bg-white"
                autoFocus
              />
              <button
                type="submit"
                className="px-8 py-4 text-lg font-semibold rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:shadow-lg hover:scale-[1.02] transition-all"
              >
                Analyze
              </button>
            </div>
            <div className="mt-4 flex flex-wrap justify-center gap-2 text-sm text-slate-600">
              <span>Try:</span>
              {examples.map((ex) => (
                <button
                  key={ex}
                  type="button"
                  onClick={() => router.push(`/analyze/${ex}`)}
                  className="px-3 py-1 rounded-full bg-white border border-slate-200 hover:border-blue-400 hover:text-blue-600 transition-colors"
                >
                  {ex}
                </button>
              ))}
            </div>
          </form>
        </div>
      </div>
    </section>
  );
}
