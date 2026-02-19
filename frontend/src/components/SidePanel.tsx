import JointJogPanel from "./JointJogPanel";

type SidePanelProps = {
    anglesDeg: number[];
    setAnglesDeg: React.Dispatch<React.SetStateAction<number[]>>;
};

function SidePanel({ anglesDeg, setAnglesDeg }: SidePanelProps) {
    return (
        <div className="flex flex-col bg-slate-400 p-2 h-full">
            <JointJogPanel anglesDeg={anglesDeg} setAnglesDeg={setAnglesDeg} />
        </div>
    );
}

export default SidePanel;