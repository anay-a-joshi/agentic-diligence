const features = [
  {
    title: "8 Specialist Agents",
    desc: "Financial, Commercial, Risk, Governance, Market, Sentiment, Red Flag, and Synthesis agents working in parallel like a junior PE team.",
    icon: "AI",
  },
  {
    title: "5-Year LBO Model",
    desc: "Base, Bull, and Bear scenarios with full debt paydown schedule, IRR, MOIC, and 5x5 sensitivity tables.",
    icon: "$$",
  },
  {
    title: "SEC EDGAR + XBRL",
    desc: "Pulls structured financials from XBRL companyfacts API plus 10-K, 10-Q, 8-K, and DEF 14A filings.",
    icon: "10K",
  },
  {
    title: "Feasibility Score",
    desc: "0-100 weighted score across 6 dimensions: Financial, LBO Returns, Governance, Risk, Red Flags, Sentiment.",
    icon: "/100",
  },
  {
    title: "IC Memo PDF",
    desc: "Downloadable, multi-page Investment Committee memo formatted like a real PE associate would produce.",
    icon: "PDF",
  },
  {
    title: "LBO Excel Workbook",
    desc: "Five-tab Excel: Summary, Base/Bull/Bear projections, color-coded sensitivity heatmap, inputs reference.",
    icon: "XLS",
  },
];

export default function Features() {
  return (
    <section className="max-w-6xl mx-auto px-6 py-20">
      <div className="text-center mb-16">
        <h2 className="text-4xl font-bold text-slate-900 mb-4">
          What you get in 2 minutes
        </h2>
        <p className="text-lg text-slate-600 max-w-2xl mx-auto">
          A complete take-private screening package — the kind that costs $300K-$800K and
          takes a junior PE associate 4-8 weeks to produce.
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {features.map((f) => (
          <div
            key={f.title}
            className="p-6 rounded-2xl bg-white border border-slate-200 hover:border-blue-300 hover:shadow-lg transition-all"
          >
            <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-blue-50 text-blue-700 font-bold mb-4">
              {f.icon}
            </div>
            <h3 className="text-xl font-semibold text-slate-900 mb-2">{f.title}</h3>
            <p className="text-slate-600 leading-relaxed">{f.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
