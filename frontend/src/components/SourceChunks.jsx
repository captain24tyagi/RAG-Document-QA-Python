
export default function SourceChunks({ chunks }) {
    if (!chunks || chunks.length === 0) return null;

    return (
        <div className="flex flex-col gap-3">
            <p className="text-xs font-semibold uppercase tracking-widest text-slate-500">
                Source Chunks
            </p>

            <div className="flex flex-col gap-2">
                {chunks.map((chunk, i) => (
                    <div
                        key={i}
                        className="rounded-xl border border-slate-700/60 bg-slate-800/40 p-3 flex flex-col gap-2"
                    >
                        <div className="flex items-center justify-between">
                            <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-500">
                                Chunk {i + 1}
                            </span>
                            <span className="text-[10px] font-mono font-semibold text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded-full">
                                {chunk.score.toFixed(4)}
                            </span>
                        </div>
                        <p className="text-xs text-slate-400 leading-relaxed line-clamp-4">
                            {chunk.text}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
}
