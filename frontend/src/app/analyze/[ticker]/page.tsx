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
      <main className="min-h-screen flex items-center justify-center bg-slate-50 px-6">
        <div className="max-w-lg text-center">
          <h1 className="text-2xl font-bold text-slate-900 mb-2">Analysis Failed</h1>
          <p className="text-slate-600 mb-6 break-all">{error}</p>
          <button onClick={() => router.push("/")}
            className="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700">
            Back to home
          </button>
        </div>
      </main>
    );
  }

  if (!result) return <LoadingState ticker={upper} />;

  return (
    <main className="min-h-screen bg-slate-50 pb-12">
      <CompanyHeader result={result} />
      <div className="max-w-7xl mx-auto px-6 py-8 space-y-6">
        <button onClick={() => router.push("/")}
          className="text-sm text-slate-600 hover:text-slate-900">
          ← Analyze another ticker
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
