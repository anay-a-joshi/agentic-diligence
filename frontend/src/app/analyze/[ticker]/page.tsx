"use client";

import { useEffect, useState, use } from "react";
import { useRouter } from "next/navigation";
import { analyzeTicker, AnalysisResult } from "@/lib/api";
import LoadingState from "@/components/dashboard/LoadingState";
import CompanyHeader from "@/components/dashboard/CompanyHeader";
import FeasibilityScore from "@/components/dashboard/FeasibilityScore";
import FinancialSummary from "@/components/dashboard/FinancialSummary";
import LBOReturns from "@/components/dashboard/LBOReturns";
import LBOChart from "@/components/dashboard/LBOChart";
import InvestmentThesis from "@/components/dashboard/InvestmentThesis";
import RiskPanel from "@/components/dashboard/RiskPanel";
import GovernancePanel from "@/components/dashboard/GovernancePanel";
import RedFlagsPanel from "@/components/dashboard/RedFlagsPanel";
import CommercialPanel from "@/components/dashboard/CommercialPanel";
import DownloadPanel from "@/components/dashboard/DownloadPanel";

export default function AnalyzePage({
  params,
}: {
  params: Promise<{ ticker: string }>;
}) {
  const { ticker } = use(params);
  const upper = ticker.toUpperCase();
  const router = useRouter();
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    analyzeTicker(upper)
      .then((r) => { if (!cancelled) setResult(r); })
      .catch((e) => { if (!cancelled) setError(e.message); });
    return () => { cancelled = true; };
  }, [upper]);

  if (error) {
    return (
      <main className="min-h-screen flex items-center justify-center px-6">
        <div className="glass-strong rounded-3xl p-10 max-w-lg text-center">
          <div className="w-14 h-14 mx-auto mb-4 rounded-full bg-red-500/20 flex items-center justify-center">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ef4444" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
          </div>
          <h1 className="text-2xl font-bold text-white mb-2">Analysis Failed</h1>
          <p className="text-slate-400 mb-6 break-all text-sm">{error}</p>
          <button
            onClick={() => router.push("/")}
            className="px-6 py-3 rounded-xl font-semibold text-white"
            style={{
              background: "linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)",
              boxShadow: "0 8px 32px rgba(59, 130, 246, 0.4)",
            }}
          >
            Back to home
          </button>
        </div>
      </main>
    );
  }

  if (!result) return <LoadingState ticker={upper} />;

  return (
    <main className="relative pb-20">
      <CompanyHeader result={result} />

      <div className="max-w-7xl mx-auto px-6 space-y-6">
        <button
          onClick={() => router.push("/")}
          className="flex items-center gap-2 text-sm text-slate-500 hover:text-white transition-colors group"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="group-hover:-translate-x-0.5 transition-transform">
            <line x1="19" y1="12" x2="5" y2="12" />
            <polyline points="12 19 5 12 12 5" />
          </svg>
          Analyze another ticker
        </button>

        <FeasibilityScore result={result} />
        <DownloadPanel result={result} />
        <InvestmentThesis result={result} />
        <FinancialSummary result={result} />
        <LBOReturns result={result} />
        <LBOChart result={result} />
        <CommercialPanel result={result} />
        <RiskPanel result={result} />
        <GovernancePanel result={result} />
        <RedFlagsPanel result={result} />
      </div>
    </main>
  );
}
