'use client'

import { useState, ChangeEvent } from 'react';
import { Upload as UploadIcon } from 'lucide-react';
import { CodeXml as CodeIcon } from 'lucide-react';
import PrimaryButton from './ui/PrimaryButton';
import SidePanelHeader from './ui/SidePanelHeader';
import type { TrajectoryWaypoint } from '@/types';

type RapidPanelProps = {
  robotId: string | null;
  onFileUploaded: (fileName: string) => void;
  onAddLog: (message: string, type?: 'info' | 'success' | 'error' | 'warning') => void;
  onTrajectoryReady: (trajectory: TrajectoryWaypoint[]) => void;
};

const RapidPanel = ({ robotId, onFileUploaded, onAddLog, onTrajectoryReady }: RapidPanelProps) => {
  const [fileContent, setFileContent] = useState<string>("");
  const [fileName, setFileName] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  const handleFileUpload = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    onFileUploaded(file.name);
    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target?.result as string;
      setFileContent(content);
    };
    reader.readAsText(file);
  };

  const handleExecute = async () => {
    if (!fileContent.trim()) {
      onAddLog('No RAPID code to execute.', 'warning');
      return;
    }
    if (!robotId) {
      onAddLog('Select a robot model before executing.', 'warning');
      return;
    }

    setIsLoading(true);
    onAddLog('Parsing RAPID code...', 'info');

    try {
      const parseRes = await fetch('/api/parse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: fileContent }),
      });

      if (!parseRes.ok) {
        const err = await parseRes.json().catch(() => ({ detail: parseRes.statusText }));
        throw new Error(`Parse error: ${err.detail ?? parseRes.statusText}`);
      }

      const parsed = await parseRes.json();
      const commandCount: number = parsed.command_count ?? 0;

      if (commandCount === 0) {
        onAddLog('No move commands found in RAPID code.', 'warning');
        setIsLoading(false);
        return;
      }

      onAddLog(`Parsed ${commandCount} commands — running simulation...`, 'info');

      // Step 2: Simulate — send full program dict so variable declarations are preserved
      const simRes = await fetch('/api/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ robot_id: robotId, program: parsed.program }),
      });

      if (!simRes.ok) {
        const err = await simRes.json().catch(() => ({ detail: simRes.statusText }));
        throw new Error(`Simulation error: ${err.detail ?? simRes.statusText}`);
      }

      const { trajectory, stats } = await simRes.json();
      onAddLog(
        `Simulation complete: ${stats.total_waypoints} waypoints, ${stats.duration_seconds.toFixed(2)}s duration`,
        'success'
      );
      onTrajectoryReady(trajectory);
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      onAddLog(msg, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className='flex flex-col flex-1'>
      <SidePanelHeader title="RAPID Code" description="Upload and execute your robot programs." />

      {/* Upload Section */}
      <div className="mb-4">
        <label className="inline-flex text-sm font-medium text-gray-300 items-center mb-3 gap-2 w-full whitespace-nowrap">
          <UploadIcon className="w-4 h-4 inline-block text-orange-500 shrink-0" strokeWidth={3} />
          <span className='overflow-hidden text-ellipsis'>Upload RAPID File (.txt, .mod)</span>
        </label>
        <div className="flex flex-col gap-2">
          <input
            type="file"
            accept=".txt,.mod"
            onChange={handleFileUpload}
            className="block w-full text-sm font-medium text-gray-400
              file:cursor-pointer
              file:mr-3 file:py-2 file:px-4
              file:rounded-md file:border-0
              file:text-sm file:font-semibold
              file:bg-linear-to-r file:from-orange-500 file:to-orange-600
              hover:from-orange-600 hover:to-orange-700 file:text-white
              cursor-pointer"
          />
          {fileName && (
            <span className="text-xs text-gray-500 truncate italic">
              Loaded: {fileName}
            </span>
          )}
        </div>
      </div>

      {/* Code Editor Section */}
      <div className="flex flex-col flex-1 min-h-0">
        <label className="inline-flex text-sm font-medium text-gray-300 mt-4.5 mb-3 items-center gap-2">
          <CodeIcon className="w-4 h-4 inline-block shrink-0 text-orange-500" strokeWidth={3} />
          Code Editor
        </label>
        <textarea
          value={fileContent}
          onChange={(e) => setFileContent(e.target.value)}
          placeholder="File content will appear here..."
          className="flex w-full py-2 px-3 bg-gray-900 text-white/70 placeholder:text-white/50 font-mono text-sm rounded-lg focus:ring-1 hover:border-purple-500/40 focus:ring-purple-500/40 resize-none outline-none h-full border border-white/10 shadow-lg shadow-white/5"
        />
      </div>

      <PrimaryButton
        onClick={handleExecute}
        className="mb-2 mt-4 self-center shrink-0"
        disabled={isLoading}
      >
        {isLoading ? 'Running...' : 'Execute RAPID'}
      </PrimaryButton>
    </div>
  );
};

export default RapidPanel;
