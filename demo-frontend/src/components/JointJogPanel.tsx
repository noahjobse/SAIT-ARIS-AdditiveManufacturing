import React from 'react';
import * as Slider from '@radix-ui/react-slider';
import { RotateCcw as ResetIcon } from 'lucide-react';
import PrimaryButton from './ui/PrimaryButton';
import SidePanelHeader from './ui/SidePanelHeader';

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
        <div className='flex flex-col flex-1'>
            <SidePanelHeader title="Joint Jogging" description="Slide the sliders to adjust joint angles." />

            <div className='flex flex-col h-full justify-between '>
                <div className="flex flex-col gap-2">
                    {/* All joints in separate container */}
                    {anglesDeg.map((deg, i) => {
                        return (
                        <div key={i} className="flex flex-1 flex-col py-2 px-3 bg-black/40 rounded-lg overflow-y-auto justify-center border border-white/10 shadow-lg hover:border-purple-500/40 shadow-white/5">
                            
                            {/* Joint Number + Editable Deg */}
                            <div className="flex justify-between items-center px-1">
                                <span className="font-bold text-sm text-white tracking-tight">J{i + 1}</span>
                                <div className="relative group">
                                    <input
                                        type="text"
                                        min={minDeg}
                                        max={maxDeg}
                                        value={deg}
                                        onChange={(e) => {
                                            let val = parseFloat(e.target.value);
                                            if (isNaN(val)) val = 0;
                                            val = Math.min(maxDeg, Math.max(minDeg, val));
                                            updateAngle(i, val);
                                        }}
                                        className="w-12 pr-3 text-right text-sm -mr-0.5 font-bold hover:bg-gray-800 focus:bg-gray-800 text-orange-500 py-0.2 rounded shadow-sm outline-none focus:ring-1 focus:ring-gray-500/50 transition-all cursor-text "
                                    />
                                    <span className="absolute right-1 top-1/2 -translate-y-1/2 text-sm font-bold text-orange-500">°</span>
                                </div>
                            </div>
                            
                            <div className="relative h-8 flex items-center">
                                {/* Slider */}
                                <Slider.Root
                                    value={[deg]} 
                                    min={minDeg} 
                                    max={maxDeg} 
                                    step={1} 
                                    onValueChange={(val) => updateAngle(i, val[0])}
                                    className="relative flex w-full touch-none items-center select-none data-disabled:opacity-50 data-[orientation=vertical]:h-full data-[orientation=vertical]:min-h-44 data-[orientation=vertical]:w-auto data-[orientation=vertical]:flex-col"
                                >
                                    <Slider.Track className="bg-gray-600/75 relative grow overflow-hidden rounded-full data-[orientation=horizontal]:h-2 data-[orientation=horizontal]:w-full data-[orientation=vertical]:h-full data-[orientation=vertical]:w-1.5">
                                        <Slider.Range className="bg-linear-to-r from-purple-600 to-purple-700 absolute data-[orientation=horizontal]:h-full data-[orientation=vertical]:w-full shadow-lg shadow-purple-500/20" />
                                    </Slider.Track>

                                    <Slider.Thumb className="border-2 border-purple-600 bg-white ring-purple-500/50 block size-5 shrink-0 rounded-full shadow-lg transition-[color,box-shadow] hover:ring-4 hover:shadow-purple-500/30 focus-visible:ring-4 focus-visible:outline-hidden disabled:pointer-events-none disabled:opacity-50 cursor-grab active:cursor-grabbing" />
                                </Slider.Root>
                            </div>

                            {/* Min/Max Labels */}
                            <div className="flex justify-between text-[10px] text-gray-400 font-medium -mt-1 leading-none">
                                <span>-180°</span>
                                <span>180°</span>
                            </div>
                
                        </div>
                        );
                    })}

                </div>

                {/* Reset / Temp Jump to Home */}
                <PrimaryButton 
                    onClick={resetAngles}
                    className="mb-2 self-center"
                >
                    <ResetIcon className="w-4 h-4 mr-1 " strokeWidth={3} />
                    Reset Joints
                </PrimaryButton>
            </div>
        </div>
    );
}

export default JointJogPanel;