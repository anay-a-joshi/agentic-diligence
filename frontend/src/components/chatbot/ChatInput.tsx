"use client";

import { useState } from "react";

interface Props {
  onSend: (text: string) => void;
}

export default function ChatInput({ onSend }: Props) {
  const [text, setText] = useState("");

  const handle = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim()) {
      onSend(text);
      setText("");
    }
  };

  return (
    <form onSubmit={handle} className="flex gap-2">
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="flex-1 px-3 py-2 border rounded"
        placeholder="What's the customer concentration risk?"
      />
      <button className="px-4 py-2 bg-blue-600 text-white rounded">Send</button>
    </form>
  );
}
