"use client";

const agents = [
  "Financial Agent",
  "Commercial Agent",
  "Risk Agent",
  "Governance Agent",
  "Market Agent",
  "Sentiment Agent",
  "Red Flag Agent",
  "Synthesis Agent",
];

export default function AgentProgressTracker() {
  return (
    <div className="bg-white rounded-lg border border-slate-200 p-4">
      <h3 className="font-semibold mb-3">Agent Pipeline</h3>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
        {agents.map((a) => (
          <div key={a} className="flex items-center gap-2 text-sm">
            <span className="w-2 h-2 rounded-full bg-slate-300" />
            <span className="text-slate-700">{a}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
