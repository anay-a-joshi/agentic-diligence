"use client";

import { useParams } from "next/navigation";
import CompanyHeader from "@/components/dashboard/CompanyHeader";
import FeasibilityScore from "@/components/dashboard/FeasibilityScore";
import FinancialSummary from "@/components/dashboard/FinancialSummary";
import LBOReturns from "@/components/dashboard/LBOReturns";
import RiskDashboard from "@/components/dashboard/RiskDashboard";
import ICMemoViewer from "@/components/dashboard/ICMemoViewer";
import DownloadPanel from "@/components/dashboard/DownloadPanel";
import AgentProgressTracker from "@/components/shared/AgentProgressTracker";
import ChatWindow from "@/components/chatbot/ChatWindow";

export default function AnalyzePage() {
  const params = useParams();
  const ticker = params.ticker as string;

  return (
    <main className="min-h-screen bg-slate-50 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <CompanyHeader ticker={ticker} />
        <AgentProgressTracker />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <FeasibilityScore />
          <FinancialSummary />
          <LBOReturns />
        </div>
        <RiskDashboard />
        <ICMemoViewer />
        <DownloadPanel ticker={ticker} />
        <ChatWindow ticker={ticker} />
      </div>
    </main>
  );
}
