import { useState } from "react";
import FileUpload from "./components/FileUpload";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";
import SourceChunks from "./components/SourceChunks";
import { askQuestion } from "./services/api";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sourceChunks, setSourceChunks] = useState([]);
  const [ingested, setIngested] = useState(false);

  async function handleSend(query: any) {
    setMessages((prev) => [...prev, { role: "user", content: query }]);
    setLoading(true);
    setSourceChunks([]);

    try {
      const result = await askQuestion(query);
      setMessages((prev) => [...prev, { role: "assistant", content: result.answer }]);
      setSourceChunks(result.source_chunks);
    } catch (err) {
      const msg = err.response?.data?.detail || "Something went wrong.";
      setMessages((prev) => [...prev, { role: "assistant", content: `Error: ${msg}` }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="h-screen bg-slate-950 text-slate-100 flex flex-col overflow-hidden">

      {/* Header */}
      <header className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/80 backdrop-blur-sm">
        <div>
          <h1 className="text-lg font-bold bg-gradient-to-r from-blue-400 to-violet-400 bg-clip-text text-transparent">
            RAG Document Q&A
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Built from scratch by Captain24Tyagi
          </p>
        </div>
        <div className={`flex items-center gap-2 text-xs px-3 py-1.5 rounded-full border ${ingested
          ? "text-emerald-400 border-emerald-500/30 bg-emerald-500/10"
          : "text-slate-500 border-slate-700 bg-slate-800/50"
          }`}>
          <span className={`w-1.5 h-1.5 rounded-full ${ingested ? "bg-emerald-400" : "bg-slate-600"}`} />
          {ingested ? "Document loaded" : "No document"}
        </div>
      </header>

      {/* Main */}
      <div className="flex flex-1 overflow-hidden">

        {/* Left Panel */}
        <aside className="w-80 min-w-[280px] border-r border-slate-800 bg-slate-900/50 flex flex-col gap-5 p-5 overflow-y-auto">
          <FileUpload onIngested={() => setIngested(true)} />

          {/* Divider */}
          {sourceChunks.length > 0 && (
            <div className="border-t border-slate-800 pt-4">
              <SourceChunks chunks={sourceChunks} />
            </div>
          )}
        </aside>

        {/* Right Panel — Chat */}
        <main className="flex-1 flex flex-col overflow-hidden">
          <ChatWindow messages={messages} loading={loading} />
          <ChatInput onSend={handleSend} disabled={loading || !ingested} />
        </main>

      </div>
    </div>
  );
}
