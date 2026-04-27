interface Props {
  role: string;
  content: string;
}

export default function ChatMessage({ role, content }: Props) {
  return (
    <div className={`p-3 rounded ${role === "user" ? "bg-blue-50 ml-12" : "bg-slate-50 mr-12"}`}>
      <p className="text-xs font-semibold text-slate-500 mb-1">{role.toUpperCase()}</p>
      <p className="text-sm">{content}</p>
    </div>
  );
}
