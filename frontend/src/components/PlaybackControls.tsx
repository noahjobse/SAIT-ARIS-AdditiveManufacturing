import { useState, useEffect } from 'react';

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
    <div className="bg-zinc-800 px-6 py-2 flex flex-col justify-center gap-2 h-full z-50">
      
      <div className="flex items-center gap-6">
        {/* Play/Pause Button */}
        <button 
          onClick={() => setIsPlaying(!isPlaying)}
          className="w-10 h-10 rounded-full bg-violet-600 hover:bg-violet-500 flex items-center justify-center text-white transition-all active:scale-90 shadow-lg group shrink-0"
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
        <div className="text-zinc-300 font-mono text-xs tabular-nums w-24 shrink-0">
          <span className="text-violet-400 font-bold">{formatTime(currentTime)}</span>
          <span className="mx-1 text-zinc-600">/</span>
          <span>{formatTime(duration)}</span>
        </div>

        {/* Speed Selector */}
        <select 
          value={playbackSpeed}
          onChange={(e) => setPlaybackSpeed(parseFloat(e.target.value))}
          className="bg-zinc-700 text-zinc-300 text-[10px] font-bold px-2 py-1 rounded border-none outline-none focus:ring-1 focus:ring-violet-500 uppercase tracking-widest cursor-pointer ml-auto"
        >
          <option value="1.0">1.0x</option>
          <option value="1.5">1.5x</option>
          <option value="2.0">2.0x</option>
          <option value="0.5">0.5x</option>
        </select>
      </div>

      {/* Scrubber Container */}
      <div className="w-full flex flex-col gap-1 relative pt-2">
        <input 
          type="range" 
          min="0" 
          max={duration} 
          step="0.1"
          value={currentTime}
          onChange={(e) => setCurrentTime(parseFloat(e.target.value))}
          className="w-full h-1.5 bg-zinc-700 rounded-lg appearance-none cursor-pointer accent-violet-500 hover:accent-violet-400 transition-all"
        />
        
        {/* Tick marks */}
        <div className="flex justify-between px-0.5">
          {[...Array(11)].map((_, i) => (
            <div key={i} className="w-px h-1 bg-zinc-600"></div>
          ))}
        </div>
      </div>

    </div>
  );
};

export default PlaybackControls;