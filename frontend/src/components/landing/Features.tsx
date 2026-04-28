"use client";

const features = [
  {
    title: "Multi-Agent Pipeline",
    desc: "Eight specialists analyze in sequence: Financial, Commercial, Risk, Governance, Market, Sentiment, Red Flag, and Synthesis.",
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="3" width="7" height="7" rx="1" />
        <rect x="14" y="3" width="7" height="7" rx="1" />
        <rect x="3" y="14" width="7" height="7" rx="1" />
        <rect x="14" y="14" width="7" height="7" rx="1" />
      </svg>
    ),
    gradient: "from-blue-500 to-cyan-500",
  },
  {
    title: "Live SEC EDGAR",
    desc: "Direct ingestion from XBRL companyfacts API plus 10-K, 10-Q, 8-K, and DEF 14A filings — no caching, no staleness.",
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <line x1="16" y1="13" x2="8" y2="13" />
        <line x1="16" y1="17" x2="8" y2="17" />
      </svg>
    ),
    gradient: "from-violet-500 to-fuchsia-500",
  },
  {
    title: "5-Year LBO Model",
    desc: "Bull, Base, and Bear scenarios with full debt paydown schedule, IRR, MOIC, and 5×5 sensitivity tables.",
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <line x1="12" y1="20" x2="12" y2="10" />
        <line x1="18" y1="20" x2="18" y2="4" />
        <line x1="6" y1="20" x2="6" y2="16" />
      </svg>
    ),
    gradient: "from-emerald-500 to-teal-500",
  },
  {
    title: "Feasibility Score",
    desc: "Single 0–100 score with letter grade, weighted across financial quality, returns, governance, risk, red flags, and sentiment.",
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="10" />
        <polyline points="12 6 12 12 16 14" />
      </svg>
    ),
    gradient: "from-amber-500 to-orange-500",
  },
  {
    title: "IC Memo PDF",
    desc: "Five-page Investment Committee memo with cover, thesis, LBO returns, risks, governance — formatted exactly like Apollo or KKR produces.",
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
        <polyline points="7 10 12 15 17 10" />
        <line x1="12" y1="15" x2="12" y2="3" />
      </svg>
    ),
    gradient: "from-pink-500 to-rose-500",
  },
  {
    title: "LBO Excel Model",
    desc: "Five-tab workbook: Summary, Base/Bull/Bear projections, color-coded sensitivity heatmap, and inputs reference for handoff to associates.",
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
        <line x1="3" y1="9" x2="21" y2="9" />
        <line x1="9" y1="21" x2="9" y2="9" />
      </svg>
    ),
    gradient: "from-cyan-500 to-blue-500",
  },
];

export default function Features() {
  return (
    <section className="relative py-32 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-20">
          <div className="text-sm uppercase tracking-widest text-slate-500 mb-4 font-medium">
            What you get
          </div>
          <h2 className="text-5xl md:text-6xl font-bold tracking-tight mb-6">
            <span className="text-gradient">A complete diligence package,</span>
            <br />
            <span className="text-gradient-blue">in two minutes.</span>
          </h2>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto">
            The kind of work that costs $300K–$800K and takes a junior PE associate
            four to eight weeks to produce — generated live, on demand.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((f, i) => (
            <div
              key={f.title}
              className="group relative animate-fade-up"
              style={{ animationDelay: `${i * 80}ms` }}
            >
              <div
                className="absolute -inset-px rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"
                style={{
                  background: `linear-gradient(135deg, ${
                    f.gradient.includes("blue") ? "#3b82f6" :
                    f.gradient.includes("violet") ? "#8b5cf6" :
                    f.gradient.includes("emerald") ? "#10b981" :
                    f.gradient.includes("amber") ? "#f59e0b" :
                    f.gradient.includes("pink") ? "#ec4899" : "#06b6d4"
                  } 0%, transparent 100%)`,
                  filter: "blur(8px)",
                }}
              />
              <div className="relative h-full glass rounded-2xl p-7 hover:bg-card-hover transition-all duration-300 hover:-translate-y-1">
                <div
                  className={`inline-flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-br ${f.gradient} text-white mb-5 shadow-lg`}
                  style={{
                    boxShadow: `0 8px 32px ${
                      f.gradient.includes("blue") ? "rgba(59,130,246,0.3)" :
                      f.gradient.includes("violet") ? "rgba(139,92,246,0.3)" :
                      f.gradient.includes("emerald") ? "rgba(16,185,129,0.3)" :
                      f.gradient.includes("amber") ? "rgba(245,158,11,0.3)" :
                      f.gradient.includes("pink") ? "rgba(236,72,153,0.3)" : "rgba(6,182,212,0.3)"
                    }`,
                  }}
                >
                  {f.icon}
                </div>
                <h3 className="text-xl font-semibold text-white mb-2">{f.title}</h3>
                <p className="text-slate-400 leading-relaxed">{f.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
