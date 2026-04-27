import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="border-b border-slate-200 bg-white px-6 py-4">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <Link href="/" className="text-xl font-bold">
          DiligenceAI
        </Link>
        <Link href="/about" className="text-slate-600 hover:text-slate-900">
          About
        </Link>
      </div>
    </nav>
  );
}
