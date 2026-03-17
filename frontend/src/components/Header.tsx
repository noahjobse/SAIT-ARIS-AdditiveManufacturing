import type { TabType } from "../App";
import { ROBOT_MODELS } from "../App";
import SidePanelTabs from "./SidePanelTabs";

type HeaderProps = {
  activeTab: TabType;
  setActiveTab: (tab: TabType) => void;
  modelPath: string | null;
  setModelPath: (path: string | null) => void;
};

export const Header = ({ 
  activeTab, 
  setActiveTab,
  modelPath, 
  setModelPath
}: HeaderProps) => {
  return (
    <header className="relative h-20 bg-black/95 backdrop-blur-sm text-white flex justify-between items-center px-6 z-50 border-b border-white/10">

      <div className="flex flex-row flex-1 text-2xl font-bold tracking-tight justify-between items-center h-full">
        {/* Robot Selector */}
        <div className="flex flex-row items-center gap-2">
          <div className="flex flex-col">
            <label htmlFor="robot-select" className="text-[10px] uppercase tracking-wider text-gray-300 font-bold mb-0.5 ml-1">
              Robot Model:
            </label>
            <select 
              id="robot-select"
              value={modelPath ?? ""}
              onChange={(e) => setModelPath(e.target.value)}
              className="bg-linear-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white text-sm font-medium px-3 py-1.5 rounded-md transition-all outline-none cursor-pointer border-none shadow-lg shadow-orange-500/20"
            >
              <option value="" disabled className="bg-gray-600 text-gray-300">Select a model</option>

              {ROBOT_MODELS.map((robot) => (
                <option key={robot.path} value={robot.path} className="bg-gray-700">
                  {robot.label}
                </option>
              ))}
            </select>
          </div>
        </div>
        
        {/* Side Panel Tabs */}
        <div className="w-full mx-4 h-full">
          <SidePanelTabs activeTab={activeTab} setActiveTab={setActiveTab} />
        </div>

        <h1 className="drop-shadow-sm bg-linear-to-r from-orange-500 to-purple-600 bg-clip-text text-transparent text-3xl">ArmStudio</h1>
      </div>

    </header>
  );
};