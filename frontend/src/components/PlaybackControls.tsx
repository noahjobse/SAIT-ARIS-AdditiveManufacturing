'use client'

import { useState, useEffect, useRef, useCallback } from 'react';
import type { TrajectoryWaypoint } from '@/types';

type PlaybackControlsProps = {
  trajectory: TrajectoryWaypoint[] | null;
  onJointAnglesUpdate: (angles: number[]) => void;
};

function interpolateJoints(traj: TrajectoryWaypoint[], t: number): number[] {
  if (t <= traj[0].timestamp) return [...traj[0].joints];
  const last = traj[traj.length - 1];
  if (t >= last.timestamp) return [...last.joints];

  let lo = 0, hi = traj.length - 2;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (traj[mid + 1].timestamp < t) lo = mid + 1;
    else hi = mid;
  }
  const a = traj[lo], b = traj[lo + 1];
  const alpha = (t - a.timestamp) / (b.timestamp - a.timestamp);
  return a.joints.map((j, k) => j + alpha * (b.joints[k] - j));
}

const PlaybackControls = ({ trajectory, onJointAnglesUpdate }: PlaybackControlsProps) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [playbackSpeed, setPlaybackSpeed] = useState(1.0);

  const rafRef = useRef<number | null>(null);
  const wallClockStartRef = useRef<number | null>(null);
  const simTimeAtStartRef = useRef<number>(0);

  const trajectoryRef = useRef(trajectory);
  trajectoryRef.current = trajectory;
  const speedRef = useRef(playbackSpeed);
  speedRef.current = playbackSpeed;

  const duration = trajectory ? trajectory[trajectory.length - 1].timestamp : 0;
  const durationRef = useRef(duration);
  durationRef.current = duration;

  const stopLoop = useCallback(() => {
    if (rafRef.current !== null) {
      cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
    }
    wallClockStartRef.current = null;
  }, []);

  const tick = useCallback((now: number) => {
    const traj = trajectoryRef.current;
    if (wallClockStartRef.current === null || !traj) return;

    const wallElapsed = (now - wallClockStartRef.current) / 1000;
    const simTime = simTimeAtStartRef.current + wallElapsed * speedRef.current;

    if (simTime >= durationRef.current) {
      setCurrentTime(durationRef.current);
      onJointAnglesUpdate(interpolateJoints(traj, durationRef.current));
      setIsPlaying(false);
      stopLoop();
      return;
    }

    setCurrentTime(simTime);
    onJointAnglesUpdate(interpolateJoints(traj, simTime));
    rafRef.current = requestAnimationFrame(tick);
  }, [onJointAnglesUpdate, stopLoop]);

  useEffect(() => {
    if (isPlaying && trajectory && trajectory.length > 0) {
      wallClockStartRef.current = performance.now();
      simTimeAtStartRef.current = currentTime >= duration ? 0 : currentTime;
      if (simTimeAtStartRef.current === 0) setCurrentTime(0);
      rafRef.current = requestAnimationFrame(tick);
    } else {
      stopLoop();
    }
    return stopLoop;
  // eslint-disable-next-line react-hooks/exhaustive-deps -- intentionally only re-run when isPlaying toggles; currentTime/duration are read via refs to avoid restarting the animation loop on every frame
  }, [isPlaying]);

  useEffect(() => {
    stopLoop();
    setIsPlaying(false);
    setCurrentTime(0);
    if (trajectory && trajectory.length > 0) {
      onJointAnglesUpdate([...trajectory[0].joints]);
    }
  }, [trajectory, stopLoop, onJointAnglesUpdate]);

  const handleScrub = (value: number) => {
    stopLoop();
    setIsPlaying(false);
    setCurrentTime(value);
    if (trajectory && trajectory.length > 0) {
      onJointAnglesUpdate(interpolateJoints(trajectory, value));
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const hasTrajectory = trajectory && trajectory.length > 0;

  return (
    <div className="px-4 flex flex-col justify-center gap-0.5 h-full z-50 relative">
      {!hasTrajectory && (
        <div className="absolute top-0 left-6 mb-2">
          <span className="text-[10px] font-bold text-gray-300 uppercase tracking-widest">
            No trajectory — execute RAPID code to animate
          </span>
        </div>
      )}

      <div className="flex items-center gap-6">
        {/* Play/Pause Button */}
        <button
          onClick={() => setIsPlaying(!isPlaying)}
          disabled={!hasTrajectory}
          className="w-8 h-8 bg-linear-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 disabled:from-gray-600 disabled:to-gray-600 disabled:cursor-not-allowed text-white text-sm sm:text-md font-medium rounded-lg transition-all outline-none cursor-pointer border-none flex flex-row justify-center items-center shadow-lg shadow-orange-500/20 active:scale-90 group shrink-0"
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
          value={playbackSpeed.toFixed(1)}
          onChange={(e) => setPlaybackSpeed(parseFloat(e.target.value))}
          className="bg-gray-700 text-gray-300 text-[10px] font-bold px-2 py-1 rounded border-none outline-none focus:ring-1 focus:ring-purple-500 uppercase tracking-widest cursor-pointer ml-auto"
        >
          <option value="0.5">0.5x</option>
          <option value="1.0">1.0x</option>
          <option value="1.5">1.5x</option>
          <option value="2.0">2.0x</option>
        </select>
      </div>

      {/* Scrubber */}
      <div className="w-full flex flex-col gap-0.5 relative pt-1">
        <input
          type="range"
          min="0"
          max={duration || 1}
          step="0.01"
          value={currentTime}
          onChange={(e) => handleScrub(parseFloat(e.target.value))}
          disabled={!hasTrajectory}
          className="w-full h-1.5 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-500 hover:accent-purple-400 transition-all disabled:cursor-not-allowed"
        />
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
