'use client'

import { useState, useEffect, useRef } from 'react';

type LogEntry = {
    id: number;
    timestamp: string;
    message: string;
    type: 'info' | 'error' | 'success' | 'warning';
};

type StatusPanelProps = {
    lastLog?: { message: string, type: 'info' | 'success' | 'error' | 'warning' };
};

const logTypeColours = {
    'info': 'text-blue-300',
    'success': 'text-green-400',
    'error': 'text-red-400',
    'warning': 'text-yellow-400'
};


const StatusPanel = ({ lastLog }: StatusPanelProps) => {
const nextId = useRef(2);
const [logs, setLogs] = useState<LogEntry[]>([
    { id: 1, timestamp: new Date().toLocaleTimeString(), message: "Robot Models Ready", type: 'success' },
    { id: 0, timestamp: new Date().toLocaleTimeString(), message: "System Initialized", type: 'info' }
]);

// Update logs when a new one comes in via props
useEffect(() => {
    if (lastLog) {
    setLogs(prev => [{
        id: nextId.current++,
        timestamp: new Date().toLocaleTimeString(),
        message: lastLog.message,
        type: lastLog.type
    }, ...prev].slice(0, 100));
    }
}, [lastLog]);

return (
    <div className="h-full  flex flex-col z-40">
    {/* Panel Header */}
    <div className=" px-4 py-1 flex items-center justify-between border-b border-gray-700">
        <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
            <span className="text-[10px] uppercase tracking-widest font-bold text-gray-300">System Status & Logs</span>
        </div>
        <button 
        onClick={() => setLogs([])}
        className="text-[10px] uppercase font-bold text-gray-500 hover:text-gray-300 transition-colors"
        >
        Clear Logs
        </button>
    </div>

    {/* Log Container */}
    <div className="flex-1 overflow-y-auto p-2 font-mono text-xs scrollbar-thin scrollbar-thumb-gray-700">
        {logs.length === 0 ? (
        <div className="text-gray-600 italic p-2">No active logs...</div>
        ) : (
            logs.map((log) => (
                <div key={log.id} className="flex gap-3 mb-1 border-l-2 border-transparent hover:bg-gray-800/50 px-2 transition-colors">
                    <span className="text-gray-500 min-w-17.5">[{log.timestamp}]</span>
                    <span className={logTypeColours[log.type]}>
                        {log.type.toUpperCase()}: {log.message}
                    </span>
                </div>
            ))
        )}
    </div>
    
    {/* Quick Status Bar */}
    <div className="bg-purple-600/50 px-4 py-0.5 flex items-center gap-4 text-[10px] font-bold text-purple-200">
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
