"use client";

import { useState } from "react";

export function useChatStream(ticker: string) {
  const [messages, setMessages] = useState<Array<{ role: string; content: string }>>([]);

  const send = async (text: string) => {
    setMessages((m) => [...m, { role: "user", content: text }]);
    // TODO: implement streaming via fetch + ReadableStream
  };

  return { messages, send };
}
