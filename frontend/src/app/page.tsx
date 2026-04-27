import TickerSearch from "@/components/landing/TickerSearch";
import Hero from "@/components/landing/Hero";
import Features from "@/components/landing/Features";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 to-white">
      <Hero />
      <div className="max-w-2xl mx-auto px-4">
        <TickerSearch />
      </div>
      <Features />
    </main>
  );
}
