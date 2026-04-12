'use client'

import React from "react";
import JointJogPanel from "./JointJogPanel";
import RapidPanel from "./RapidPanel";
import PrintPanel from "./PrintPanel";
import type { TabType } from "@/types";
import type { TrajectoryWaypoint } from "@/types";

type JointLimit = {
    min: number;
    max: number;
};

type SidePanelProps = {
    activeTab: TabType;
    robotId: string | null;
    anglesDeg: number[];
    jointLimits?: JointLimit[];
    setAnglesDeg: React.Dispatch<React.SetStateAction<number[]>>;
    onFileUploaded: (fileName: string) => void;
    onAddLog: (message: string, type?: 'info' | 'success' | 'error' | 'warning') => void;
    onTrajectoryReady: (trajectory: TrajectoryWaypoint[]) => void;
    onStlPreviewUrl: (url: string | null) => void;
};

function SidePanel({ activeTab, robotId, anglesDeg, jointLimits, setAnglesDeg, onFileUploaded, onAddLog, onTrajectoryReady, onStlPreviewUrl }: SidePanelProps) {
    return (
        <div className="flex flex-col min-h-0 bg-linear-to-b from-gray-900 via-gray-950 via-85% to-black py-4 px-6 h-full overflow-y-auto">
            {activeTab === "rapid" ? (
                <RapidPanel
                    robotId={robotId}
                    onFileUploaded={onFileUploaded}
                    onAddLog={onAddLog}
                    onTrajectoryReady={onTrajectoryReady}
                />
            ) : activeTab === "print" ? (
                <PrintPanel
                    robotId={robotId}
                    onAddLog={onAddLog}
                    onTrajectoryReady={onTrajectoryReady}
                    onStlPreviewUrl={onStlPreviewUrl}
                />
            ) : (
                <JointJogPanel anglesDeg={anglesDeg} setAnglesDeg={setAnglesDeg} jointLimits={jointLimits} />
            )}
        </div>
    );
}

export default SidePanel;
