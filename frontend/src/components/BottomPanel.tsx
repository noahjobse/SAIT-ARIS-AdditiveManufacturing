'use client'

import { useState, useRef, useCallback } from 'react';
import PlaybackControls from './PlaybackControls';
import StatusPanel from './StatusPanel';
import type { TrajectoryWaypoint } from '@/types';
import type { HeatmapMode } from './babylon/ExtrusionTrail';

type BottomPanelMode = "scrubber" | "both" | "logs";

type BottomPanelProps = {
    lastLog: { message: string, type: 'info' | 'success' | 'error' | 'warning' };
    trajectory: TrajectoryWaypoint[] | null;
    onJointAnglesUpdate: (angles: number[]) => void;
    height?: number;
    addTrailPoint?: (pos: number[], penDown: boolean) => void;
    clearTrail?: () => void;
    addExtrusionPoint?: (pos: number[], cumulativeExtrusion: number) => void;
    clearExtrusion?: () => void;
    setHeatmapMode?: (mode: HeatmapMode) => void;
};

function BottomPanel({ lastLog, trajectory, onJointAnglesUpdate, height, addTrailPoint, clearTrail, addExtrusionPoint, clearExtrusion, setHeatmapMode }: BottomPanelProps) {
    const [bottomPanelMode, setBottomPanelMode] = useState<BottomPanelMode>("both");
    const [splitPercent, setSplitPercent] = useState(50);
    const containerRef = useRef<HTMLDivElement>(null);
    const dragging = useRef(false);

    const modes: { id: BottomPanelMode, label: string }[] = [
        { id: "scrubber", label: "SCRUBBER" },
        { id: "both", label: "BOTH" },
        { id: "logs", label: "LOGS" }
    ];

    const handleDrag = useCallback((e: MouseEvent) => {
        if (!containerRef.current) return;
        const rect = containerRef.current.getBoundingClientRect();
        const pct = ((e.clientX - rect.left) / rect.width) * 100;
        setSplitPercent(Math.min(85, Math.max(15, pct)));
    }, []);

    const stopDrag = useCallback(() => {
        dragging.current = false;
        document.body.style.userSelect = '';
        document.body.style.cursor = '';
        window.removeEventListener('mousemove', handleDrag);
        window.removeEventListener('mouseup', stopDrag);
    }, [handleDrag]);

    const startDrag = useCallback(() => {
        dragging.current = true;
        document.body.style.userSelect = 'none';
        document.body.style.cursor = 'col-resize';
        window.addEventListener('mousemove', handleDrag);
        window.addEventListener('mouseup', stopDrag);
    }, [handleDrag, stopDrag]);

    return (
        <div className="flex flex-col bg-linear-to-b from-black to-black shadow-2xl relative shrink-0" style={{ height: height ?? 130 }}>
            {/* View Switcher Tabs */}
            <div className="absolute top-[-24px] right-4 flex gap-1 z-50">
                {modes.map(mode => (
                    <button
                        key={mode.id}
                        onClick={() => setBottomPanelMode(mode.id)}
                        className={`text-[10px] px-3 py-1 rounded-t-md transition-all font-bold tracking-tight border-x border-t border-orange-500/50 ${bottomPanelMode === mode.id ? "bg-gray-900 text-white" : "bg-gray-950 text-gray-500 hover:text-gray-300 "}`}
                    >
                        {mode.label}
                    </button>
                ))}
            </div>

            {/* Panel Content */}
            <div ref={containerRef} className="flex flex-row h-full">
                {(bottomPanelMode === "both" || bottomPanelMode === "scrubber") && (
                    <div
                        className="overflow-hidden h-full"
                        style={bottomPanelMode === "both" ? { flexBasis: `${splitPercent}%`, flexShrink: 0, flexGrow: 0 } : { flex: 1 }}
                    >
                        <PlaybackControls
                            trajectory={trajectory}
                            onJointAnglesUpdate={onJointAnglesUpdate}
                            addTrailPoint={addTrailPoint}
                            clearTrail={clearTrail}
                            addExtrusionPoint={addExtrusionPoint}
                            clearExtrusion={clearExtrusion}
                            setHeatmapMode={setHeatmapMode}
                        />
                    </div>
                )}

                {/* Drag Handle — only visible in "both" mode */}
                {bottomPanelMode === "both" && (
                    <div
                        onMouseDown={startDrag}
                        className="w-1.5 cursor-col-resize bg-gray-700 hover:bg-purple-500 active:bg-purple-400 transition-colors shrink-0"
                    />
                )}

                {(bottomPanelMode === "both" || bottomPanelMode === "logs") && (
                    <div
                        className="overflow-hidden"
                        style={bottomPanelMode === "both" ? { flex: 1 } : { flex: 1 }}
                    >
                        <StatusPanel lastLog={lastLog} />
                    </div>
                )}
            </div>
        </div>
    );
}

export default BottomPanel;
