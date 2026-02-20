import JointJogPanel from "./JointJogPanel";
import RapidPanel from "./RapidPanel";
import type { TabType } from "../App";

type SidePanelProps = {
    activeTab: TabType;
    anglesDeg: number[];
    setAnglesDeg: React.Dispatch<React.SetStateAction<number[]>>;
    onFileUploaded: (fileName: string) => void;
};

function SidePanel({ activeTab, anglesDeg, setAnglesDeg, onFileUploaded }: SidePanelProps) {
    return (
        <div className="flex flex-col bg-zinc-400 p-2 h-full">
            {activeTab === "rapid" ? (
                <RapidPanel onFileUploaded={onFileUploaded} />
            ) : (
                <JointJogPanel anglesDeg={anglesDeg} setAnglesDeg={setAnglesDeg} />
            )}
        </div>
    );
}

export default SidePanel;