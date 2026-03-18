import React from "react";
import JointJogPanel from "./JointJogPanel";
import RapidPanel from "./RapidPanel";
import type { TabType } from "../App";
import type { TrajectoryWaypoint } from "../types";

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
};

function SidePanel({ activeTab, robotId, anglesDeg, jointLimits, setAnglesDeg, onFileUploaded, onAddLog, onTrajectoryReady }: SidePanelProps) {
    return (
        <div className="flex flex-col bg-linear-to-b from-gray-900 via-gray-950 via-85% to-black py-4 px-6 h-full ">
            {activeTab === "rapid" ? (
                <RapidPanel
                    robotId={robotId}
                    onFileUploaded={onFileUploaded}
                    onAddLog={onAddLog}
                    onTrajectoryReady={onTrajectoryReady}
                />
            ) : (
                <JointJogPanel anglesDeg={anglesDeg} setAnglesDeg={setAnglesDeg} jointLimits={jointLimits} />
            )}
        </div>
    );
}

export default SidePanel;
