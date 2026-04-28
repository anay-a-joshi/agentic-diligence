"use client";

import { AnalysisResult, downloadUrl } from "@/lib/api";

export default function DownloadPanel({ result }: { result: AnalysisResult }) {
  const pdfUrl = downloadUrl(result.ic_memo_url);
  const xlsxUrl = downloadUrl(result.lbo_excel_url);

  return (
    <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-6 md:p-8 text-white">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold mb-1">Download Deliverables</h2>
          <p className="text-blue-100">
            Investment-grade IC memo and full LBO model — ready to send to your team.
          </p>
        </div>
        <div className="flex flex-col sm:flex-row gap-3">
          {pdfUrl && (
            <a href={pdfUrl} target="_blank" rel="noopener noreferrer"
              className="px-6 py-3 bg-white text-blue-700 font-semibold rounded-xl hover:bg-blue-50 transition flex items-center gap-2 justify-center">
              IC Memo PDF
            </a>
          )}
          {xlsxUrl && (
            <a href={xlsxUrl} target="_blank" rel="noopener noreferrer"
              className="px-6 py-3 bg-white text-blue-700 font-semibold rounded-xl hover:bg-blue-50 transition flex items-center gap-2 justify-center">
              LBO Excel
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
