import { useRobotContext } from '../context/RobotContext';

export const Sidebar = () => {
  const { currentRobot, setRobot } = useRobotContext();

  return (
    <aside className="w-80 bg-slate-50 border-r border-slate-200 flex flex-col h-full z-10">
      
      {/* 1. Robot Selection */}
      <div className="p-4 border-b border-slate-200">
        <h2 className="text-sm font-bold text-slate-700 uppercase mb-3">Robot Model</h2>
        <select 
          value={currentRobot}
          onChange={(e) => setRobot(e.target.value)}
          className="w-full p-2 border border-slate-300 rounded bg-white text-sm"
        >
          <option value="irb4600">ABB IRB 4600</option>
          <option value="irb2600" disabled>ABB IRB 2600 (Soon)</option>
          <option value="irb6700" disabled>ABB IRB 6700 (Soon)</option>
        </select>
      </div>

      {/* 2. File Upload Area */}
      <div className="p-4 border-b border-slate-200">
        <h2 className="text-sm font-bold text-slate-700 uppercase mb-3">File Manager</h2>
        
        <div className="border-2 border-dashed border-slate-300 rounded p-8 text-center hover:bg-blue-50 transition-colors cursor-pointer bg-white">
          <span className="text-sm text-slate-500 font-medium">
            Drag .mod or .stl files here
          </span>
        </div>
      </div>

      {/* 3. Object List Placeholder */}
      <div className="p-4 flex-1">
        <h2 className="text-sm font-bold text-slate-700 uppercase mb-3">Scene Objects</h2>
        <div className="text-xs text-slate-400 italic">
          No obstacles loaded yet.
        </div>
      </div>
      
    </aside>
  );
};