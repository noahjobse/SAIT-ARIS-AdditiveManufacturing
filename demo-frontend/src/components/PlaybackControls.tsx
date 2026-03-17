import { useState, useEffect, useRef, useCallback } from 'react';
import type { TrajectoryWaypoint } from '../types';

type PlaybackControlsProps = {
  trajectory: TrajectoryWaypoint[] | null;
  onJointAnglesUpdate: (angles: number[]) => void;
};

// TODO(human): Implement this function.
// Given a sorted trajectory and time t (seconds), binary-search for the two
// surrounding waypoints and linearly interpolate each joint angle between them.
// Return the interpolated joints array (degrees).
// Edge cases: t <= first.timestamp → return first.joints
//             t >= last.timestamp  → return last.joints
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

  // Use refs so the RAF tick always reads the latest values without re-creating the loop
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
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isPlaying]); // intentionally limited — tick/stopLoop/trajectory read via stable refs

  // Reset when a new trajectory arrives
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
    <div className="bg-zinc-800 px-6 py-2 flex flex-col justify-center gap-2 h-full z-50 relative">
      {!hasTrajectory && (
        <div className="absolute top-1 left-6">
          <span className="text-[8px] font-bold text-zinc-500 uppercase tracking-widest opacity-70">
            No trajectory — execute RAPID code to animate
          </span>
        </div>
      )}

      <div className="flex items-center gap-6 mt-2">
        {/* Play/Pause Button */}
        <button
          onClick={() => setIsPlaying(!isPlaying)}
          disabled={!hasTrajectory}
          className="w-10 h-10 rounded-full bg-violet-600 hover:bg-violet-500 disabled:bg-zinc-600 disabled:cursor-not-allowed flex items-center justify-center text-white transition-all active:scale-90 shadow-lg group shrink-0"
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
          <option value="0.5">0.5x</option>
          <option value="1.0">1.0x</option>
          <option value="1.5">1.5x</option>
          <option value="2.0">2.0x</option>
        </select>
      </div>

      {/* Scrubber */}
      <div className="w-full flex flex-col gap-1 relative pt-2">
        <input
          type="range"
          min="0"
          max={duration || 1}
          step="0.01"
          value={currentTime}
          onChange={(e) => handleScrub(parseFloat(e.target.value))}
          disabled={!hasTrajectory}
          className="w-full h-1.5 bg-zinc-700 rounded-lg appearance-none cursor-pointer accent-violet-500 hover:accent-violet-400 transition-all disabled:cursor-not-allowed"
        />
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
