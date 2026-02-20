import React from 'react';

type JointJogPanelProps = {
    anglesDeg: number[];
    setAnglesDeg: React.Dispatch<React.SetStateAction<number[]>>;
};

function JointJogPanel({ anglesDeg, setAnglesDeg }: JointJogPanelProps) {
    const updateAngle = (i: number, deg: number) => {
        setAnglesDeg((prev) => {
            const next = [...prev];
            next[i] = deg;
            return next;
        });
    };

    const minDeg = -180;
    const maxDeg = 180;

    const resetAngles = () => {
        setAnglesDeg(anglesDeg.map(() => 0));
    };

    return (
        <div className="flex flex-col p-3 bg-zinc-300 rounded-lg shadow-inner h-full overflow-y-auto">

            {/* All joints in a single container */}
            <div className="flex flex-col">
                {anglesDeg.map((deg, i) => {
                    return (
                    <div key={i} className="mb-4">
                        
                        {/* Joint Number + Editable Deg */}
                        <div className="flex justify-between items-center mb-1 px-1">
                            <span className="font-bold text-sm text-zinc-800 tracking-tight">JOINT {i + 1}</span>
                            <div className="flex items-center gap-1 group">
                                <input
                                    type="number"
                                    min={minDeg}
                                    max={maxDeg}
                                    value={deg}
                                    onChange={(e) => {
                                        let val = parseFloat(e.target.value);
                                        if (isNaN(val)) val = 0;
                                        val = Math.min(maxDeg, Math.max(minDeg, val));
                                        updateAngle(i, val);
                                    }}
                                    className="w-16 text-center text-sm font-bold bg-zinc-200 text-violet-950 py-1 rounded shadow-sm outline-none focus:ring-2 focus:ring-violet-600/50 transition-all cursor-text border border-zinc-300"
                                />
                                <span className="text-xs font-bold text-violet-950">°</span>
                            </div>
                        </div>
                        
                        <div className="relative h-8 flex items-center">
                            {/* Slider */}
                            <input 
                                type="range" min={minDeg} max={maxDeg} value={deg} 
                                onChange={(e) => updateAngle(i, parseFloat(e.target.value))} 
                                className="w-full accent-violet-900 h-2 cursor-pointer appearance-none bg-zinc-400/50 rounded-lg" 
                            />
                        </div>

                        {/* Min/Max Labels */}
                        <div className="flex justify-between text-[10px] text-zinc-600 font-medium -mt-1 leading-none">
                            <span>-180°</span>
                            <span>180°</span>
                        </div>
                        
                        {/* Thin separator between joints */}
                        {i < anglesDeg.length - 1 && <hr className="mt-2 border-zinc-400/50" />}
                    </div>
                    );
                })}
            </div>

            {/* Reset / Temp Jump to Home */}
            <button 
                onClick={resetAngles}
                className="mt-4 px-4 py-2 bg-violet-950 text-white rounded-md transition-all hover:bg-violet-900 active:scale-95 shadow-sm font-bold"
            >
                Reset Joints
            </button>
        </div>
    );
}

export default JointJogPanel;