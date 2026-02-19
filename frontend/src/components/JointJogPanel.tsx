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
        <div className="flex flex-col p-3 bg-slate-300 rounded-lg ">
            <h2 className="text-lg font-semibold mb-4">Joint Jog</h2>

            {anglesDeg.map((deg, i) => {
                const bubbleWidthPx = 43;  // Temp hardcoded
                const sliderWidthPx = 245; 

                let pos = (deg - minDeg) / (maxDeg - minDeg);

                // Clamp bubble positions so it stays within slider
                const minPos = bubbleWidthPx / 2 / sliderWidthPx;
                const maxPos = 1 - minPos;
                pos = Math.min(Math.max(pos, minPos), maxPos);

                const bubblePosition = pos * 100;
                
                return (
                <div key={i} className="mb-4">
                    
                    {/* Joint Number + Deg */}
                    <div className="mb-1 font-semibold">J{i + 1}: {deg}°</div>
                    
                    <div className="relative">
                        {/* Deg Bubble */}
                        <div 
                            className="absolute w-12 h-6 bg-purple-950 text-white text-xs rounded-md flex items-center justify-center mb-2 pointer-events-none"
                            style={{ left: `${bubblePosition}%`, transform: `translateX(-50%)` }}
                        >
                            {deg}°
                        </div>

                        {/* Slider */}
                        <input 
                            type="range" min={minDeg} max={maxDeg} value={deg} 
                            onChange={(e) => updateAngle(i, parseFloat(e.target.value))} 
                            className="w-full accent-purple-950" 
                        />

                        {/* Min/Max Labels */}
                        <div className="flex justify-between text-xs text-gray-600 ">
                            <span>-180°</span>
                            <span>180°</span>
                        </div>

                        {/* Break Line */}
                        {i < anglesDeg.length - 1 && <hr className="mt-3 border-slate-400" />}
                    </div>
                </div>
                );
            })}

            {/* Reset / Temp Jump to Home */}
            <button 
                onClick={resetAngles}
                className="mt-4 px-4 py-2 bg-purple-950 text-white rounded-md transition-colors hover:shadow-[0px_2px_6px_rgba(0,0,0,0.3)]"
            >
                Reset
            </button>
        </div>
    );
}

export default JointJogPanel;