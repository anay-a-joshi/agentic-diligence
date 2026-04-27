"use client";

interface Props {
  ticker?: string;
}

export default function CompanyHeader({ ticker }: Props) {
  return (
    <div className="p-6 bg-white rounded-lg border border-slate-200">
      <h2 className="text-xl font-semibold text-slate-900">CompanyHeader</h2>
      <p className="text-sm text-slate-500 mt-2">
        TODO: Wire to backend /analyze/{ticker || "TICKER"} endpoint
      </p>
    </div>
  );
}
