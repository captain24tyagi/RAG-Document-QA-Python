// src/components/FileUpload.jsx

import { useState, useRef, type ChangeEvent, type DragEvent } from "react";
import { uploadDocument } from "../services/api";

interface FileUploadProps {
  onIngested: (result: any) => void;
}

export default function FileUpload({ onIngested }: FileUploadProps) {
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  async function handleFile(file: File | null | undefined) {
    if (!file) return;
    setLoading(true);
    setStatus("Processing document...");

    try {
      const result = await uploadDocument(file);
      setStatus(`✓ ${result.new_chunks} chunks ingested (${result.chunks_stored} total)`);
      if (onIngested) onIngested(result);
    } catch (err: any) {
      const msg = err.response?.data?.detail || "Upload failed.";
      setStatus(`✗ ${msg}`);
    } finally {
      setLoading(false);
    }
  }

  function handleChange(e: ChangeEvent<HTMLInputElement>) {
    handleFile(e.target.files?.[0]);
  }

  function handleDrop(e: DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setIsDragging(false);
    handleFile(e.dataTransfer.files?.[0]);
  }

  return (
    <div className="flex flex-col gap-3">
      <p className="text-xs font-semibold uppercase tracking-widest text-slate-500">
        Upload Document
      </p>

      {/* Drop Zone */}
      <div
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={`
          flex flex-col items-center justify-center gap-2 p-6 rounded-xl border-2 border-dashed cursor-pointer
          transition-all duration-200
          ${isDragging
            ? "border-blue-500 bg-blue-500/10"
            : "border-slate-700 bg-slate-800/50 hover:border-blue-500/60 hover:bg-slate-800"
          }
          ${loading ? "opacity-50 pointer-events-none" : ""}
        `}
      >
        {/* Icon */}
        <svg className="w-8 h-8 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
            d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p className="text-sm text-slate-400">
          {loading ? "Uploading..." : "Drop a file here or click to browse"}
        </p>
        <input
          ref={inputRef}
          type="file"
          // accept=".txt"
          onChange={handleChange}
          className="hidden"
        />
      </div>

      {/* Status */}
      {status && (
        <p className={`text-xs px-3 py-2 rounded-lg ${status.startsWith("✓")
          ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
          : status.startsWith("✗")
            ? "bg-red-500/10 text-red-400 border border-red-500/20"
            : "bg-slate-800 text-slate-400"
          }`}>
          {status}
        </p>
      )}
    </div>
  );
}
