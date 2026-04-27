import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DiligenceAI — Agentic Take-Private Screening",
  description: "Compress PE due diligence from weeks to hours.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
