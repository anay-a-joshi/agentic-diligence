"use client";

import { useState } from "react";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";

interface Props {
  ticker: string;
}

export default function ChatWindow({ ticker }: Props) {
  const [messages, setMessages] = useState<Array<{ role: string; content: string }>>([
    { role: "assistant", content: `Ask me anything about ${ticker}'s filings.` },
  ]);

  const handleSend = async (text: string) => {
    setMessages((m) => [...m, { role: "user", content: text }]);
    // TODO: stream from /chat endpoint
  };

  return (
    <div className="bg-white rounded-lg border border-slate-200 p-4">
      <h3 className="font-semibold mb-3">Ask DiligenceAI</h3>
      <div className="space-y-2 max-h-96 overflow-y-auto mb-3">
        {messages.map((m, i) => (
          <ChatMessage key={i} role={m.role} content={m.content} />
        ))}
      </div>
      <ChatInput onSend={handleSend} />
    </div>
  );
}
