"use client";

import { AnalysisResult, downloadUrl } from "@/lib/api";

export default function DownloadPanel({ result }: { result: AnalysisResult }) {
  const pdfUrl = downloadUrl(result.ic_memo_url);
  const xlsxUrl = downloadUrl(result.lbo_excel_url);

  return (
    <section className="relative animate-fade-up">
      <div className="absolute -inset-1 rounded-3xl opacity-50 blur-2xl"
        style={{ background: "linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #06b6d4 100%)" }}
      />

      <div className="relative glass-strong rounded-3xl p-6 md:p-8 overflow-hidden border border-white/10">
        <div className="absolute top-0 left-0 w-full h-full bg-grid opacity-20" />

        <div className="relative flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
          <div className="flex-1">
            <div className="text-xs uppercase tracking-widest text-blue-400 mb-1 font-bold">
              Deliverables Ready
            </div>
            <h2 className="text-2xl md:text-3xl font-bold text-white mb-2 tracking-tight">
              Download your IC package
            </h2>
            <p className="text-slate-400">
              Investment-grade PDF memo and full LBO model — ready to send to your team.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-3">
            {pdfUrl && (
              <a
                href={pdfUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="group/btn relative flex items-center gap-3 px-6 py-4 rounded-2xl font-semibold text-white overflow-hidden transition-all hover:-translate-y-0.5"
                style={{
                  background: "linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)",
                  boxShadow: "0 8px 32px rgba(59, 130, 246, 0.4)",
                }}
              >
                <div className="w-10 h-10 rounded-xl bg-white/15 flex items-center justify-center">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                    <polyline points="14 2 14 8 20 8" />
                  </svg>
                </div>
                <div className="text-left">
                  <div className="text-xs opacity-80 uppercase tracking-wider font-medium">PDF</div>
                  <div className="font-bold">IC Memo</div>
                </div>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="group-hover/btn:translate-y-0.5 transition-transform">
                  <line x1="12" y1="5" x2="12" y2="19" />
                  <polyline points="19 12 12 19 5 12" />
                </svg>
              </a>
            )}

            {xlsxUrl && (
              <a
                href={xlsxUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="group/btn flex items-center gap-3 px-6 py-4 rounded-2xl font-semibold text-white overflow-hidden glass-strong border border-white/10 hover:bg-white/5 transition-all hover:-translate-y-0.5"
              >
                <div className="w-10 h-10 rounded-xl bg-emerald-500/20 flex items-center justify-center">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                    <line x1="3" y1="9" x2="21" y2="9" />
                    <line x1="9" y1="21" x2="9" y2="9" />
                  </svg>
                </div>
                <div className="text-left">
                  <div className="text-xs text-slate-400 uppercase tracking-wider font-medium">XLSX</div>
                  <div className="font-bold">LBO Model</div>
                </div>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="group-hover/btn:translate-y-0.5 transition-transform">
                  <line x1="12" y1="5" x2="12" y2="19" />
                  <polyline points="19 12 12 19 5 12" />
                </svg>
              </a>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
