'use client'

import { useState, ChangeEvent } from 'react';
import { Upload as UploadIcon, Layers as LayersIcon } from 'lucide-react';
import PrimaryButton from './ui/PrimaryButton';
import SidePanelHeader from './ui/SidePanelHeader';
import type { TrajectoryWaypoint } from '@/types';

type PrintPanelProps = {
  robotId: string | null;
  onAddLog: (message: string, type?: 'info' | 'success' | 'error' | 'warning') => void;
  onTrajectoryReady: (trajectory: TrajectoryWaypoint[]) => void;
  onStlPreviewUrl: (url: string | null) => void;
};

type PrintStats = {
  layer_count: number;
  total_extrusion_mm: number;
  move_commands: number;
  print_height_mm: number;
  slice_time_ms: number;
};

type SliceStage = null | 'uploading' | 'slicing' | 'simulating';

const PrintPanel = ({ robotId, onAddLog, onTrajectoryReady, onStlPreviewUrl }: PrintPanelProps) => {
  const [fileName, setFileName] = useState('');
  const [fileId, setFileId] = useState<string | null>(null);
  const [stage, setStage] = useState<SliceStage>(null);
  const [printStats, setPrintStats] = useState<PrintStats | null>(null);

  const [layerHeight, setLayerHeight] = useState(0.2);
  const [nozzleDiameter, setNozzleDiameter] = useState(0.4);

  const handleFileSelect = async (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    setPrintStats(null);
    setFileId(null);

    // Create blob URL for 3D preview
    const blobUrl = URL.createObjectURL(file);
    onStlPreviewUrl(blobUrl);

    // Upload to backend
    setStage('uploading');
    onAddLog(`Uploading ${file.name}...`, 'info');

    try {
      const form = new FormData();
      form.append('file', file);

      const res = await fetch('/api/print/upload', { method: 'POST', body: form });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        throw new Error(err.detail ?? res.statusText);
      }

      const { file_id, size_bytes } = await res.json();
      setFileId(file_id);
      onAddLog(`Uploaded ${(size_bytes / 1024).toFixed(0)}KB — ready to slice`, 'success');
    } catch (err) {
      onAddLog(`Upload failed: ${err instanceof Error ? err.message : err}`, 'error');
    } finally {
      setStage(null);
    }
  };

  const handleSlice = async () => {
    if (!fileId) {
      onAddLog('Upload an STL file first.', 'warning');
      return;
    }
    if (!robotId) {
      onAddLog('Select a robot model before slicing.', 'warning');
      return;
    }

    setStage('slicing');
    onAddLog('Slicing STL...', 'info');
    onStlPreviewUrl(null); // clear preview during simulation

    try {
      setStage('simulating');
      onAddLog('Generating trajectory...', 'info');

      const res = await fetch('/api/print/slice', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          file_id: fileId,
          robot_id: robotId,
          layer_height: layerHeight,
          nozzle_diameter: nozzleDiameter,
        }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        throw new Error(err.detail ?? res.statusText);
      }

      const { trajectory, stats, print_stats } = await res.json();
      setPrintStats(print_stats);
      onAddLog(
        `Done: ${print_stats.layer_count} layers, ${stats.total_waypoints} waypoints, ${stats.duration_seconds.toFixed(1)}s duration`,
        'success',
      );
      onTrajectoryReady(trajectory);
    } catch (err) {
      onAddLog(`Slice failed: ${err instanceof Error ? err.message : err}`, 'error');
    } finally {
      setStage(null);
    }
  };

  const stageLabel: Record<string, string> = {
    uploading: 'Uploading...',
    slicing: 'Slicing STL...',
    simulating: 'Generating trajectory...',
  };

  return (
    <div className="flex flex-col flex-1">
      <SidePanelHeader title="3D Print" description="Upload an STL and simulate FDM printing." />

      {/* STL Upload */}
      <div className="mb-4">
        <label className="inline-flex text-sm font-medium text-gray-300 items-center mb-3 gap-2 w-full whitespace-nowrap">
          <UploadIcon className="w-4 h-4 inline-block text-orange-500 shrink-0" strokeWidth={3} />
          <span className="overflow-hidden text-ellipsis">Upload STL File</span>
        </label>
        <input
          type="file"
          accept=".stl"
          onChange={handleFileSelect}
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
          <span className="text-xs text-gray-500 truncate italic mt-1 block">
            Loaded: {fileName}
          </span>
        )}
      </div>

      {/* Print Settings */}
      <div className="mb-4">
        <label className="inline-flex text-sm font-medium text-gray-300 items-center mb-3 gap-2">
          <LayersIcon className="w-4 h-4 text-orange-500 shrink-0" strokeWidth={3} />
          Print Settings
        </label>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="text-xs text-gray-500 block mb-1">Layer Height (mm)</label>
            <input
              type="number"
              min={0.05}
              max={1.0}
              step={0.05}
              value={layerHeight}
              onChange={(e) => setLayerHeight(parseFloat(e.target.value) || 0.2)}
              className="w-full bg-gray-900 text-white text-sm px-2 py-1.5 rounded border border-white/10 outline-none focus:ring-1 focus:ring-purple-500/40"
            />
          </div>
          <div>
            <label className="text-xs text-gray-500 block mb-1">Nozzle (mm)</label>
            <input
              type="number"
              min={0.2}
              max={1.2}
              step={0.1}
              value={nozzleDiameter}
              onChange={(e) => setNozzleDiameter(parseFloat(e.target.value) || 0.4)}
              className="w-full bg-gray-900 text-white text-sm px-2 py-1.5 rounded border border-white/10 outline-none focus:ring-1 focus:ring-purple-500/40"
            />
          </div>
        </div>
      </div>

      {/* Print Stats */}
      {printStats && (
        <div className="mb-4 p-3 bg-gray-900/80 rounded-lg border border-white/5 text-xs text-gray-400 space-y-1">
          <div className="flex justify-between"><span>Layers</span><span className="text-white">{printStats.layer_count}</span></div>
          <div className="flex justify-between"><span>Height</span><span className="text-white">{printStats.print_height_mm} mm</span></div>
          <div className="flex justify-between"><span>Extrusion</span><span className="text-white">{printStats.total_extrusion_mm.toFixed(1)} mm</span></div>
          <div className="flex justify-between"><span>Commands</span><span className="text-white">{printStats.move_commands}</span></div>
          <div className="flex justify-between"><span>Slice Time</span><span className="text-white">{printStats.slice_time_ms.toFixed(0)} ms</span></div>
        </div>
      )}

      <PrimaryButton
        onClick={handleSlice}
        className="mb-2 mt-auto self-center shrink-0"
        disabled={!!stage || !fileId}
      >
        {stage ? stageLabel[stage] : 'Slice & Simulate'}
      </PrimaryButton>
    </div>
  );
};

export default PrintPanel;
