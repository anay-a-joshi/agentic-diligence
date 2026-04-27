export interface AnalysisResult {
  ticker: string;
  company_name: string;
  feasibility_score: number;
  lbo_irr_base: number;
  lbo_irr_bull: number;
  lbo_irr_bear: number;
  red_flags: string[];
  ic_memo_url: string;
  lbo_excel_url: string;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}
