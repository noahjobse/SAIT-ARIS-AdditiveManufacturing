import { useState } from 'react';
import PlaybackControls from './PlaybackControls';
import StatusPanel from './StatusPanel';
import type { BottomPanelMode } from '../App';

type BottomPanelProps = {
    lastLog: { message: string, type: 'info' | 'success' | 'error' | 'warning' };
};

function BottomPanel({ lastLog }: BottomPanelProps) {
    const [bottomPanelMode, setBottomPanelMode] = useState<BottomPanelMode>("both");
    const modes: { id: BottomPanelMode, label: string }[] = [
        { id: "scrubber", label: "SCRUBBER" },
        { id: "both", label: "BOTH" },
        { id: "logs", label: "LOGS" }
    ];

    return (
        <div className="flex flex-col border-t border-zinc-700 bg-zinc-900 shadow-2xl relative">
            {/* View Switcher Tabs */}
            <div className="absolute top-[-24px] right-4 flex gap-1 z-50">
                {modes.map(mode => (
                    <button
                        key={mode.id}
                        onClick={() => setBottomPanelMode(mode.id)}
                        className={`text-[10px] px-3 py-1 rounded-t-md transition-all font-bold tracking-tight border-x border-t border-zinc-700 ${bottomPanelMode === mode.id ? "bg-zinc-800 text-white" : "bg-zinc-900 text-zinc-500 hover:text-zinc-300"}`}
                    >
                        {mode.label}
                    </button>
                ))}
            </div>

            {/* Panel Content */}
            <div className="flex flex-row h-28">
                {(bottomPanelMode === "both" || bottomPanelMode === "scrubber") && (
                    <div className={`flex-1 ${bottomPanelMode === "both" ? "border-r border-zinc-700" : ""}`}>
                        <PlaybackControls />
                    </div>
                )}
                
                {(bottomPanelMode === "both" || bottomPanelMode === "logs") && (
                    <div className="flex-1 overflow-hidden">
                        <StatusPanel lastLog={lastLog} />
                    </div>
                )}
            </div>
        </div>
    );

} 

export default BottomPanel;