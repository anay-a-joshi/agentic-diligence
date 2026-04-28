import Hero from "@/components/landing/Hero";
import Features from "@/components/landing/Features";

export default function Home() {
  return (
    <main className="relative">
      <Hero />
      <Features />
      <footer className="relative border-t border-white/5 py-12 px-6">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-slate-500">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-md bg-gradient-to-br from-blue-500 to-violet-500 flex items-center justify-center text-white font-bold text-xs">
              D
            </div>
            <span className="text-slate-300 font-medium">DiligenceAI</span>
            <span>·</span>
            <span>Built with Next.js, FastAPI, Llama 3.3 70B</span>
          </div>
          <div className="flex gap-6">
            <span>SEC EDGAR</span>
            <span>·</span>
            <span>Not investment advice</span>
          </div>
        </div>
      </footer>
    </main>
  );
}
