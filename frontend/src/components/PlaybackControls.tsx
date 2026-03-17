import React from 'react';
import { useState, useEffect } from 'react';
import * as Slider from '@radix-ui/react-slider';

const PlaybackControls = () => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration] = useState(60); // Dummy duration of 60 seconds
  const [playbackSpeed, setPlaybackSpeed] = useState(1.0);

  // Dummy playback simulation
  useEffect(() => {
    let interval: ReturnType<typeof setInterval>;
    if (isPlaying) {
      // Calculate delay based on speed (100ms / speed)
      // e.g., 2.0x speed = 50ms interval, 0.5x speed = 200ms interval
      const delay = 100 / playbackSpeed;
      interval = setInterval(() => {
        setCurrentTime((prev) => (prev >= duration ? 0 : prev + 0.1));
      }, delay);
    }
    return () => clearInterval(interval);
  }, [isPlaying, duration, playbackSpeed]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className=" px-6 py-1 flex flex-col justify-center gap-2 h-full z-50 relative">
      {/* Stub Indicator */}
      <div className="absolute top-0 left-6 mb-2">
        <span className="text-[10px] font-bold text-gray-300 uppercase tracking-widest ">
          Playback Simulation (UI Stub)
        </span>
      </div>

      <div className="flex items-center gap-6 mt-2">
        {/* Play/Pause Button */}
        <button 
          onClick={() => setIsPlaying(!isPlaying)}
          className="w-8 h-8 bg-linear-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white text-sm sm:text-md font-medium rounded-lg transition-all outline-none cursor-pointer border-none flex flex-row justify-center items-center shadow-lg shadow-orange-500/20 active:scale-90 group shrink-0"
        >
          {isPlaying ? (
            <div className="flex gap-1">
              <div className="w-1.5 h-4 bg-white rounded-sm"></div>
              <div className="w-1.5 h-4 bg-white rounded-sm"></div>
            </div>
          ) : (
            <div className="ml-1 w-0 h-0 border-t-8 border-t-transparent border-l-14 border-l-white border-b-8 border-b-transparent"></div>
          )}
        </button>

        {/* Time Display */}
        <div className="text-gray-300 font-mono text-xs tabular-nums w-24 shrink-0">
          <span className="text-orange-500 font-bold">{formatTime(currentTime)}</span>
          <span className="mx-1 text-gray-600">/</span>
          <span>{formatTime(duration)}</span>
        </div>

        {/* Speed Selector */}
        <select 
          value={playbackSpeed}
          onChange={(e) => setPlaybackSpeed(parseFloat(e.target.value))}
          className="bg-gray-700 text-gray-300 text-[10px] font-bold px-2 py-1 rounded border-none outline-none focus:ring-1 focus:ring-purple-500 uppercase tracking-widest cursor-pointer ml-auto"
        >
          <option value="1.0">1.0x</option>
          <option value="1.5">1.5x</option>
          <option value="2.0">2.0x</option>
          <option value="0.5">0.5x</option>
        </select>
      </div>

      {/* Scrubber Container */}
      <div className="w-full flex flex-col gap-1 relative pt-2">
        {/* <input 
          type="range" 
          min="0" 
          max={duration} 
          step="0.1"
          value={currentTime}
          onChange={(e) => setCurrentTime(parseFloat(e.target.value))}
          className="w-full h-1.5 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-500 hover:accent-purple-400 transition-all"
        /> */}
        
        <Slider.Root
          value={[currentTime]} 
          min={0}
          max={duration}
          step={0.1}
          onValueChange={(value) => setCurrentTime(value[0])}
          className="relative flex w-full touch-none items-center select-none data-disabled:opacity-50 data-[orientation=vertical]:h-full data-[orientation=vertical]:min-h-44 data-[orientation=vertical]:w-auto data-[orientation=vertical]:flex-col"
        >
          <Slider.Track className="bg-gray-600/75 relative grow overflow-hidden rounded-full data-[orientation=horizontal]:h-2 data-[orientation=horizontal]:w-full data-[orientation=vertical]:h-full data-[orientation=vertical]:w-1.5">
                <Slider.Range className="bg-linear-to-r from-purple-600 to-purple-700 absolute data-[orientation=horizontal]:h-full data-[orientation=vertical]:w-full shadow-lg shadow-purple-500/20" />
            </Slider.Track>

            <Slider.Thumb className="border-2 border-purple-600 bg-white ring-purple-500/50 block size-5 shrink-0 rounded-full shadow-lg transition-[color,box-shadow] hover:ring-4 hover:shadow-purple-500/30 focus-visible:ring-4 focus-visible:outline-hidden disabled:pointer-events-none disabled:opacity-50 cursor-grab active:cursor-grabbing" />
        </Slider.Root>

        {/* Tick marks */}
        <div className="flex justify-between px-0.5">
          {[...Array(11)].map((_, i) => (
            <div key={i} className="w-px h-1 bg-gray-600"></div>
          ))}
        </div>
      </div>

    </div>
  );
};

export default PlaybackControls;