// src/components/ChatWindow.jsx

import { useEffect, useRef } from "react";

export default function ChatWindow({ messages, loading }) {
  const bottomRef = useRef(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  if (messages.length === 0 && !loading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center gap-3 text-slate-600">
        <svg className="w-12 h-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1}
            d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
        <p className="text-sm">Upload a document and start asking questions</p>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto px-6 py-4 flex flex-col gap-4">
      {messages.map((msg, i) => (
        <div
          key={i}
          className={`flex flex-col gap-1 max-w-[80%] ${
            msg.role === "user" ? "self-end items-end" : "self-start items-start"
          }`}
        >
          <span className="text-[10px] uppercase tracking-widest font-medium text-slate-500 px-1">
            {msg.role === "user" ? "You" : "Assistant"}
          </span>
          <div className={`px-4 py-3 rounded-2xl text-sm leading-relaxed ${
            msg.role === "user"
              ? "bg-blue-600 text-white rounded-br-sm"
              : "bg-slate-800 text-slate-200 border border-slate-700/50 rounded-bl-sm"
          }`}>
            {msg.content}
          </div>
        </div>
      ))}

      {/* Loading bubble */}
      {loading && (
        <div className="flex flex-col gap-1 max-w-[80%] self-start items-start">
          <span className="text-[10px] uppercase tracking-widest font-medium text-slate-500 px-1">
            Assistant
          </span>
          <div className="px-4 py-3 rounded-2xl rounded-bl-sm bg-slate-800 border border-slate-700/50">
            <div className="flex gap-1 items-center h-4">
              {[0, 1, 2].map((i) => (
                <span
                  key={i}
                  className="w-1.5 h-1.5 rounded-full bg-slate-400 typing-indicator"
                  style={{ animationDelay: `${i * 0.2}s` }}
                />
              ))}
            </div>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}
