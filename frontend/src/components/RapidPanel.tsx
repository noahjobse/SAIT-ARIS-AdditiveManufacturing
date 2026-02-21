import { useState, ChangeEvent } from 'react';

type RapidPanelProps = {
  onFileUploaded: (fileName: string) => void;
  onAddLog: (message: string, type?: 'info' | 'success' | 'error' | 'warning') => void;
};

const RapidPanel = ({ onFileUploaded, onAddLog }: RapidPanelProps) => {
  const [fileContent, setFileContent] = useState<string>("");
  const [fileName, setFileName] = useState<string>("");

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

  const handleExecute = () => {
    console.log('Execute RAPID: Not implemented');
    onAddLog('Execution of RAPID code is not yet implemented.', 'warning');
  };

  return (
    <div className="flex flex-col p-3 bg-zinc-300 rounded-lg h-full overflow-hidden">
      {/* Upload Section */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-zinc-700 mb-2">
          Upload RAPID File (.txt, .mod)
        </label>
        <div className="flex flex-col gap-2">
          <input 
            type="file" 
            accept=".txt,.mod" 
            onChange={handleFileUpload}
            className="block w-full text-sm text-zinc-500
              file:mr-4 file:py-2 file:px-4
              file:rounded-md file:border-0
              file:text-sm file:font-semibold
              file:bg-violet-950 file:text-white
              hover:file:bg-violet-900
              cursor-pointer"
          />
          {fileName && (
            <span className="text-xs text-zinc-600 truncate italic">
              Loaded: {fileName}
            </span>
          )}
        </div>
      </div>

      {/* Editor Section */}
      <div className="flex-1 flex flex-col min-h-0">
        <label className="block text-sm font-medium text-zinc-700 mb-1">
          Code Viewer
        </label>
        <textarea
          value={fileContent}
          onChange={(e) => setFileContent(e.target.value)}
          placeholder="File content will appear here..."
          className="flex-1 w-full p-3 bg-zinc-800 text-emerald-400 font-mono text-sm rounded-md border-0 focus:ring-2 focus:ring-violet-950 resize-none outline-none min-h-100"
        />
      </div>

      <button 
        onClick={handleExecute}
        className="mt-4 px-4 py-2 bg-violet-950 text-white rounded-md hover:bg-violet-900 transition-colors shadow-sm active:transform active:scale-95"
      >
        Execute RAPID
      </button>
    </div>
  );
};

export default RapidPanel;