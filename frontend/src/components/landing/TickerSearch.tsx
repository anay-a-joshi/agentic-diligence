"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function TickerSearch() {
  const [ticker, setTicker] = useState("");
  const router = useRouter();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (ticker.trim()) {
      router.push(`/analyze/${ticker.trim().toUpperCase()}`);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 mb-12">
      <input
        type="text"
        value={ticker}
        onChange={(e) => setTicker(e.target.value)}
        placeholder="Enter ticker (e.g., DOCN, AAPL, MSFT)"
        className="flex-1 px-6 py-4 text-lg border-2 border-slate-200 rounded-lg focus:outline-none focus:border-blue-500"
      />
      <button
        type="submit"
        className="px-8 py-4 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition"
      >
        Analyze
      </button>
    </form>
  );
}
