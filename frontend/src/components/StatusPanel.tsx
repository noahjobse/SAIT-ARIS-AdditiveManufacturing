import { useState, useEffect } from 'react';

type LogEntry = {
  timestamp: string;
  message: string;
  type: 'info' | 'error' | 'success' | 'warning';
};

type StatusPanelProps = {
  lastLog?: { message: string, type: 'info' | 'success' | 'error' | 'warning' };
};

const StatusPanel = ({ lastLog }: StatusPanelProps) => {
  const [logs, setLogs] = useState<LogEntry[]>([
    { timestamp: new Date().toLocaleTimeString(), message: "System Initialized", type: 'info' },
    { timestamp: new Date().toLocaleTimeString(), message: "Robot Models Ready", type: 'success' }
  ]);

  // Update logs when a new one comes in via props
  useEffect(() => {
    if (lastLog) {
      setLogs(prev => [{
        timestamp: new Date().toLocaleTimeString(),
        message: lastLog.message,
        type: lastLog.type
      }, ...prev]);
    }
  }, [lastLog]);

  return (
    <div className="h-full bg-zinc-900 flex flex-col z-40">
      {/* Panel Header */}
      <div className="bg-zinc-800 px-4 py-1 flex items-center justify-between border-b border-zinc-700">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
          <span className="text-[10px] uppercase tracking-widest font-bold text-zinc-400">System Status & Logs</span>
        </div>
        <button 
          onClick={() => setLogs([])}
          className="text-[10px] uppercase font-bold text-zinc-500 hover:text-zinc-300 transition-colors"
        >
          Clear Logs
        </button>
      </div>

      {/* Log Container */}
      <div className="flex-1 overflow-y-auto p-2 font-mono text-xs scrollbar-thin scrollbar-thumb-zinc-700">
        {logs.length === 0 ? (
          <div className="text-zinc-600 italic p-2">No active logs...</div>
        ) : (
          logs.map((log, i) => (
            <div key={i} className="flex gap-3 mb-1 border-l-2 border-transparent hover:bg-zinc-800/50 px-2 transition-colors">
              <span className="text-zinc-500 min-w-17.5">[{log.timestamp}]</span>
              <span className={`
                ${log.type === 'error' ? 'text-red-400' : ''}
                ${log.type === 'success' ? 'text-green-400' : ''}
                ${log.type === 'warning' ? 'text-yellow-400' : ''}
                ${log.type === 'info' ? 'text-blue-300' : ''}
              `}>
                {log.type.toUpperCase()}: {log.message}
              </span>
            </div>
          ))
        )}
      </div>
      
      {/* Quick Status Bar */}
      <div className="bg-violet-950 px-4 py-0.5 flex items-center gap-4 text-[10px] font-bold text-violet-200">
        <span>READY</span>
        <span className="opacity-50">|</span>
        <span>WEBGL 2.0 ACTIVE</span>
        <span className="opacity-50">|</span>
        <span className="ml-auto">LATENCY: 12ms</span>
      </div>
    </div>
  );
};

export default StatusPanel;