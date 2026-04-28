import Hero from "@/components/landing/Hero";
import Features from "@/components/landing/Features";

export default function Home() {
  return (
    <main className="min-h-screen bg-white">
      <Hero />
      <Features />
      <footer className="border-t border-slate-200 py-8 text-center text-sm text-slate-500">
        DiligenceAI - Built with Next.js + FastAPI + Llama 3.3 70B - SEC EDGAR data
      </footer>
    </main>
  );
}
