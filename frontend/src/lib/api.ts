export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export async function analyzeTicker(ticker: string): Promise<AnalysisResult> {
  const url = `${API_BASE_URL}/analyze/${ticker.toUpperCase()}`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Backend error ${res.status}: ${text}`);
  }
  return await res.json();
}

export function downloadUrl(relativePath: string): string {
  if (!relativePath) return "";
  if (relativePath.startsWith("http")) return relativePath;
  return `${API_BASE_URL}${relativePath}`;
}

export interface FinancialData {
  fiscal_year: number | null;
  revenue_usd_millions: number | null;
  ebitda_usd_millions: number | null;
  net_income_usd_millions: number | null;
  free_cash_flow_usd_millions: number | null;
  total_debt_usd_millions: number | null;
  cash_and_equivalents_usd_millions: number | null;
  shares_outstanding_millions: number | null;
  revenue_growth_yoy_pct: number | null;
  ebitda_margin_pct: number | null;
  key_drivers: string[];
  key_risks: string[];
  non_recurring_items: string[];
  summary: string;
}

export interface FeasibilityComponent {
  score: number;
  reason: string;
  weight_pct: number;
}

export interface LBOScenario {
  inputs: Record<string, number>;
  projections: {
    year: number[];
    revenue_usd_millions: number[];
    ebitda_usd_millions: number[];
    fcf_usd_millions: number[];
    debt_balance_usd_millions: number[];
  };
  exit: {
    exit_ebitda_usd_millions: number;
    exit_ev_usd_millions: number;
    exit_equity_value_usd_millions: number;
    remaining_debt_usd_millions: number;
  };
  returns: {
    moic: number;
    irr_pct: number;
  };
}

export interface LBOFull {
  status: string;
  size_prohibitive?: boolean;
  size_prohibitive_note?: string;
  base?: LBOScenario;
  bull?: LBOScenario;
  bear?: LBOScenario;
  summary?: {
    irr_base_pct: number;
    irr_bull_pct: number;
    irr_bear_pct: number;
    moic_base: number;
    moic_bull: number;
    moic_bear: number;
  };
}

export interface SynthesisData {
  executive_summary: string;
  investment_thesis: string[];
  key_risks_to_thesis: string[];
  value_creation_levers: string[];
  recommendation: string;
  recommendation_rationale: string;
  next_steps: string[];
  _fallback_used?: boolean;
}

export interface AgentResult {
  status: string;
  data: any;
  error?: string;
}

export interface AnalysisResult {
  ticker: string;
  company_name: string;
  cik: string;
  filings_summary: Record<string, number>;
  financial: FinancialData | null;
  feasibility_score: number | null;
  feasibility_grade: string | null;
  feasibility_verdict: string | null;
  feasibility_breakdown: Record<string, FeasibilityComponent>;
  lbo_irr_base: number | null;
  lbo_irr_bull: number | null;
  lbo_irr_bear: number | null;
  lbo_moic_base: number | null;
  lbo_full: LBOFull;
  synthesis: SynthesisData;
  red_flags: string[];
  ic_memo_url: string;
  lbo_excel_url: string;
  raw_findings: Record<string, AgentResult>;
}
