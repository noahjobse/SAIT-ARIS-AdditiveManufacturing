import type { TabType } from "../App";
import { ROBOT_MODELS } from "../App";

type HeaderProps = {
  activeTab: TabType;
  setActiveTab: (tab: TabType) => void;
  modelPath: string;
  setModelPath: (path: string) => void;
};

export const Header = ({ 
  activeTab, 
  setActiveTab, 
  modelPath, 
  setModelPath
}: HeaderProps) => {
  return (
    <header className="h-16 bg-violet-950 text-white flex justify-between items-center px-6 z-30 border-b border-violet-900/50">
      
      <div className="flex flex-row gap-2 items-center text-lg h-full">
        <button 
          onClick={() => setActiveTab("rapid")}
          className={`h-12 mt-4 px-4 rounded-t-md transition-all duration-150 font-bold ${
            activeTab === "rapid" 
              ? "bg-zinc-400 text-violet-950" 
              : "hover:bg-violet-900/50 text-zinc-300"
          }`}
        >
          RAPID Code
        </button>
        <button 
          onClick={() => setActiveTab("jog")}
          className={`h-12 mt-4 px-4 rounded-t-md transition-all duration-150 font-bold ${
            activeTab === "jog" 
              ? "bg-zinc-400 text-violet-950" 
              : "hover:bg-violet-900/50 text-zinc-300"
          }`}
        >
          Joint Jogging
        </button>
      </div>

      <div className="flex flex-row text-2xl font-bold tracking-tight gap-8 items-center h-full">
        {/* Robot Selector */}
        <div className="flex flex-row items-center gap-2">
          <div className="flex flex-col">
            <label htmlFor="robot-select" className="text-[10px] uppercase tracking-wider text-violet-300 font-bold mb-0.5 ml-1">
              Robot:
            </label>
            <select 
              id="robot-select"
              value={modelPath}
              onChange={(e) => setModelPath(e.target.value)}
              className="bg-violet-900 hover:bg-violet-800 text-white text-sm px-3 py-1.5 rounded-md transition-all outline-none focus:ring-2 focus:ring-violet-400 cursor-pointer border-none shadow-inner"
            >
              {ROBOT_MODELS.map((robot) => (
                <option key={robot.path} value={robot.path} className="bg-zinc-800">
                  {robot.label}
                </option>
              ))}
            </select>
          </div>
        </div>
        <h1 className="ml-4 drop-shadow-sm text-3xl">ArmStudio</h1>
      </div>

    </header>
  );
};