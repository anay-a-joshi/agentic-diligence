"use client";

import { useEffect, useState } from "react";
import { analyzeTicker } from "@/lib/api";
import type { AnalysisResult } from "@/lib/types";

export function useAnalysis(ticker: string) {
  const [data, setData] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!ticker) return;
    analyzeTicker(ticker)
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [ticker]);

  return { data, loading, error };
}
