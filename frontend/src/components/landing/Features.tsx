const features = [
  { title: "Multi-Agent Analysis", desc: "7 specialized agents work in parallel across financials, governance, and risk." },
  { title: "SEC EDGAR Integration", desc: "Pulls 5 years of 10-Ks, 10-Qs, 8-Ks, and proxies automatically." },
  { title: "LBO + Monte Carlo", desc: "Full leveraged buyout model with sensitivity analysis on key drivers." },
  { title: "Partner-Ready Output", desc: "Downloadable IC memo PDF and linked Excel LBO model." },
];

export default function Features() {
  return (
    <section className="max-w-6xl mx-auto px-4 py-16">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {features.map((f) => (
          <div key={f.title} className="p-6 bg-white rounded-lg border border-slate-200">
            <h3 className="font-semibold text-slate-900 mb-2">{f.title}</h3>
            <p className="text-sm text-slate-600">{f.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
