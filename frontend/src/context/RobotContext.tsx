import { createContext, useContext, useState, ReactNode } from 'react';

interface RobotContextType {
  currentRobot: string;
  setRobot: (name: string) => void;
  jointAngles: number[];
  setJointAngles: (angles: number[]) => void;
  // NEW: Store list of files to load
  uploadedFiles: File[];
  addUploadedFile: (file: File) => void;
}

const RobotContext = createContext<RobotContextType | undefined>(undefined);

export const RobotProvider = ({ children }: { children: ReactNode }) => {
  const [currentRobot, setRobot] = useState<string>('irb4600');
  const [jointAngles, setJointAngles] = useState<number[]>([0, 0, 0, 0, 0, 0]);
  
  // New State for files
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);

  const addUploadedFile = (file: File) => {
    setUploadedFiles((prev) => [...prev, file]);
  };

  return (
    <RobotContext.Provider value={{ 
      currentRobot, setRobot, 
      jointAngles, setJointAngles,
      uploadedFiles, addUploadedFile
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