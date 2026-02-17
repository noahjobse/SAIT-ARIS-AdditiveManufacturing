import { useRobotContext } from '../context/RobotContext';
import { useCallback } from 'react';

export const Sidebar = () => {
  const { currentRobot, setRobot, jointAngles, setJointAngles, addUploadedFile, uploadedFiles } = useRobotContext();

  const handleSliderChange = (index: number, value: string) => {
    const newAngles = [...jointAngles];
    newAngles[index] = parseFloat(value);
    setJointAngles(newAngles);
  };

  // Drag and Drop Handlers
  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    const files = Array.from(e.dataTransfer.files);
    
    files.forEach(file => {
      const ext = file.name.split('.').pop()?.toLowerCase();
      if (ext === 'stl' || ext === 'mod') {
        addUploadedFile(file);
      } else {
        alert("Only .stl and .mod files are allowed for Phase 1");
      }
    });
  }, [addUploadedFile]);

  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault(); // Necessary to allow dropping
  };

  return (
    <aside className="w-80 bg-slate-50 border-r border-slate-200 flex flex-col h-full z-10 overflow-y-auto">
      
      {/* 1. Robot Selector */}
      <div className="p-4 border-b border-slate-200">
        <h2 className="text-sm font-bold text-slate-700 uppercase mb-3">FR-1: Robot Model</h2>
        <select 
          value={currentRobot}
          onChange={(e) => setRobot(e.target.value)}
          className="w-full p-2 border border-slate-300 rounded bg-white text-sm"
        >
          <option value="irb4600">ABB IRB 4600</option>
          <option value="irb2600" disabled>ABB IRB 2600 (Soon)</option>
        </select>
      </div>

      {/* 2. Upload Zone (FR-2) */}
      <div className="p-4 border-b border-slate-200">
        <h2 className="text-sm font-bold text-slate-700 uppercase mb-3">FR-2: Environment</h2>
        
        <div 
          onDrop={onDrop}
          onDragOver={onDragOver}
          className="border-2 border-dashed border-slate-300 rounded p-6 text-center hover:bg-blue-50 hover:border-blue-400 transition-colors cursor-pointer bg-white"
        >
          <p className="text-xs text-slate-500 font-medium">
            Drag & Drop .STL Files
          </p>
        </div>

        {/* List of uploaded files */}
        <div className="mt-3 space-y-1">
          {uploadedFiles.map((f, i) => (
              <div key={i} className="text-xs text-slate-600 bg-slate-200 px-2 py-1 rounded flex justify-between">
                <span>{f.name}</span>
                <span className="text-[10px] text-slate-400">{(f.size / 1024).toFixed(1)}KB</span>
              </div>
          ))}
        </div>
      </div>

      {/* 3. Manual Controls */}
      <div className="p-4 border-b border-slate-200">
        <h2 className="text-sm font-bold text-slate-700 uppercase mb-4">Manual Joints</h2>
        <div className="flex flex-col gap-4">
          {jointAngles.map((angle, i) => (
            <div key={i}>
              <div className="flex justify-between text-xs font-semibold text-slate-600 mb-1">
                <span>J{i + 1}</span>
                <span>{angle}°</span>
              </div>
              <input
                type="range"
                min="-180"
                max="180"
                value={angle}
                onChange={(e) => handleSliderChange(i, e.target.value)}
                className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
            </div>
          ))}
        </div>
      </div>
      
    </aside>
  );
};