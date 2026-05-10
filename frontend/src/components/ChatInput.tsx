// src/components/ChatInput.jsx

import { useState } from "react";

export default function ChatInput({ onSend, disabled }) {
    const [input, setInput] = useState("");

    function handleSubmit(e: { preventDefault: () => void; }) {
        e.preventDefault();
        const trimmed = input.trim();
        if (!trimmed || disabled) return;
        onSend(trimmed);
        setInput("");
    }

    function handleKeyDown(e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    }

    return (
        <form
            onSubmit={handleSubmit}
            className="flex items-center gap-3 px-4 py-4 border-t border-slate-800 bg-slate-950"
        >
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={disabled}
                placeholder={disabled ? "Upload a document first..." : "Ask something about your document..."}
                className="
          flex-1 px-4 py-3 rounded-xl text-sm
          bg-slate-800 border border-slate-700
          text-slate-100 placeholder-slate-500
          focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/30
          disabled:opacity-40 disabled:cursor-not-allowed
          transition-all duration-150
        "
            />
            <button
                type="submit"
                disabled={disabled || !input.trim()}
                className="
          p-3 rounded-xl bg-blue-600 text-white
          hover:bg-blue-500 active:bg-blue-700
          disabled:opacity-40 disabled:cursor-not-allowed
          transition-all duration-150
          flex items-center justify-center
        "
            >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                        d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
            </button>
        </form>
    );
}
