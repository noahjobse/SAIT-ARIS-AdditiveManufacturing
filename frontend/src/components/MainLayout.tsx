import { useState } from "react";
import SidePanel from "./SidePanel";
import Viewport3D from "./Viewport3D";
import StatusPanel from "./StatusPanel";
import PlaybackControls from "./PlaybackControls";
import type { TabType, BottomPanelMode } from "../App";

type MainLayoutProps = {
    activeTab: TabType;
    modelPath: string;
    lastLog: { message: string, type: 'info' | 'success' | 'error' | 'warning' };
    onFileUploaded: (fileName: string) => void;
    onAddLog: (message: string, type?: 'info' | 'success' | 'error' | 'warning') => void;
};

function MainLayout({ activeTab, modelPath, lastLog, onFileUploaded, onAddLog }: MainLayoutProps) {
    const [anglesDeg, setAnglesDeg] = useState<number[]>([0, 0, 0, 0, 0, 0]);
    const [bottomPanelMode, setBottomPanelMode] = useState<BottomPanelMode>("both");

    return (
        <div className="flex flex-row h-full w-full bg-zinc-800 overflow-hidden">
            {/* Side Panel (Spans full height) */}
            <div className="basis-1/4 border-r border-zinc-700 shadow-xl z-20 overflow-y-auto">
                <SidePanel 
                    activeTab={activeTab} 
                    anglesDeg={anglesDeg} 
                    setAnglesDeg={setAnglesDeg} 
                    onFileUploaded={onFileUploaded}
                    onAddLog={onAddLog}
                />
            </div>

            {/* Viewport Area + Bottom Bar */}
            <div className="flex-1 flex flex-col relative overflow-hidden h-full">
                {/* 3D Viewport */}
                <div className="flex-1 relative">
                    <Viewport3D anglesDeg={anglesDeg} modelPath={modelPath}/>
                </div>
                
                {/* Bottom Bar Container */}
                <div className="flex flex-col border-t border-zinc-700 bg-zinc-900 shadow-2xl relative">
                    {/* View Switcher Tabs (Sitting on the top edge of the panel) */}
                    <div className="absolute top-[-24px] right-4 flex gap-1 z-50">
                        <button 
                            onClick={() => setBottomPanelMode("scrubber")}
                            className={`text-[10px] px-3 py-1 rounded-t-md transition-all font-bold tracking-tight border-x border-t border-zinc-700 ${bottomPanelMode === "scrubber" ? "bg-zinc-800 text-white" : "bg-zinc-900 text-zinc-500 hover:text-zinc-300"}`}
                        >
                            SCRUBBER
                        </button>
                        <button 
                            onClick={() => setBottomPanelMode("both")}
                            className={`text-[10px] px-3 py-1 rounded-t-md transition-all font-bold tracking-tight border-x border-t border-zinc-700 ${bottomPanelMode === "both" ? "bg-zinc-800 text-white" : "bg-zinc-900 text-zinc-500 hover:text-zinc-300"}`}
                        >
                            BOTH
                        </button>
                        <button 
                            onClick={() => setBottomPanelMode("logs")}
                            className={`text-[10px] px-3 py-1 rounded-t-md transition-all font-bold tracking-tight border-x border-t border-zinc-700 ${bottomPanelMode === "logs" ? "bg-zinc-800 text-white" : "bg-zinc-900 text-zinc-500 hover:text-zinc-300"}`}
                        >
                            LOGS
                        </button>
                    </div>

                    {/* Panel Content (Height matches original h-28) */}
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
            </div>

        </div>
    );
}

export default MainLayout;