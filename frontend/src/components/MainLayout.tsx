'use client'

import { useState, useRef, useCallback } from "react";
import BottomPanel from "./BottomPanel";
import SidePanel from "./SidePanel";
import Viewport3D from "./babylon/Viewport3D";
import type { TabType } from "@/app/page";
import type { TrajectoryWaypoint } from "../types";
import { robotIdFromPath } from "../types";

type MainLayoutProps = {
    activeTab: TabType;
    modelPath: string | null;
    lastLog: { message: string, type: 'info' | 'success' | 'error' | 'warning' };
    setActiveTab: (tab: TabType) => void;
    onFileUploaded: (fileName: string) => void;
    onAddLog: (message: string, type?: 'info' | 'success' | 'error' | 'warning') => void;
};

function MainLayout({ activeTab, modelPath, lastLog, onFileUploaded, onAddLog }: MainLayoutProps) {
    const [anglesDeg, setAnglesDeg] = useState<number[]>([0, 0, 0, 0, 0, 0]);
    const [jointLimits, setJointLimits] = useState<{ min: number, max: number }[] | undefined>(undefined);
    const [trajectory, setTrajectory] = useState<TrajectoryWaypoint[] | null>(null);
    const prevModelPath = useRef(modelPath);

    // Reset joint angles and trajectory when robot model changes
    if (modelPath !== prevModelPath.current) {
        prevModelPath.current = modelPath;
        setAnglesDeg([0, 0, 0, 0, 0, 0]);
        setTrajectory(null);
    }

    const handleJointLimitsExtracted = useCallback((limits: { min: number; max: number }[] | undefined) => {
        setJointLimits(limits);

        if (limits) {
            setAnglesDeg((prev) =>
                limits.map((limit, i) => {
                    const current = prev[i] ?? 0;
                    return Math.min(limit.max, Math.max(limit.min, current));
                })
            );
        } else {
            setAnglesDeg([0, 0, 0, 0, 0, 0]);
        }
    }, []);

    const robotId = robotIdFromPath(modelPath);

    return (
        <div className="flex flex-row h-full w-full bg-black overflow-hidden ">
            {/* Side Panel */}
            <div className="flex flex-col basis-3/11 border-r border-orange-500/50 h-full shadow-xl overflow-hidden">
                <SidePanel
                    activeTab={activeTab}
                    robotId={robotId}
                    anglesDeg={anglesDeg}
                    jointLimits={jointLimits}
                    setAnglesDeg={setAnglesDeg}
                    onFileUploaded={onFileUploaded}
                    onAddLog={onAddLog}
                    onTrajectoryReady={setTrajectory}
                />
            </div>

            {/* Viewport + Bottom Panel */}
            <div className="flex-1 flex flex-col relative overflow-hidden h-full min-h-0">

                <div className="flex-1 relative min-h-0">
                    <Viewport3D anglesDeg={anglesDeg} modelPath={modelPath} onJointLimitsExtracted={handleJointLimitsExtracted} />
                </div>

                <BottomPanel
                    lastLog={lastLog}
                    trajectory={trajectory}
                    onJointAnglesUpdate={setAnglesDeg}
                />
            </div>

        </div>
    );
}

export default MainLayout;
