import { createContext, useContext, useState, ReactNode } from 'react';

// Define what data is available globally
interface RobotContextType {
  currentRobot: string;
  setRobot: (name: string) => void;
  trajectory: any[]; 
  setTrajectory: (data: any[]) => void;
  playbackState: 'stopped' | 'playing' | 'paused';
  setPlaybackState: (state: 'stopped' | 'playing' | 'paused') => void;
}

const RobotContext = createContext<RobotContextType | undefined>(undefined);

export const RobotProvider = ({ children }: { children: ReactNode }) => {
  const [currentRobot, setRobot] = useState<string>('irb4600');
  const [trajectory, setTrajectory] = useState<any[]>([]);
  const [playbackState, setPlaybackState] = useState<'stopped' | 'playing' | 'paused'>('stopped');

  return (
    <RobotContext.Provider value={{ 
      currentRobot, setRobot, 
      trajectory, setTrajectory, 
      playbackState, setPlaybackState 
    }}>
      {children}
    </RobotContext.Provider>
  );
};

export const useRobotContext = () => {
  const context = useContext(RobotContext);
  if (!context) throw new Error("useRobotContext must be used within a RobotProvider");
  return context;
};