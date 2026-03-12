import { useState, ChangeEvent } from 'react';
import { Upload as UploadIcon } from 'lucide-react';
import { CodeXml as CodeIcon } from 'lucide-react';
import PrimaryButton from './ui/PrimaryButton';
import SidePanelHeader from './ui/SidePanelHeader';

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
                className="flex w-full py-2 px-3 bg-gray-900 text-white/70 placeholder:text-white/50 font-mono text-sm rounded-lg focus:ring-1 hover:border-purple-500/40 focus:ring-purple-500/40 resize-none outline-none h-full border border-white/10 shadow-lg shadow-white/5 "
                />
            </div>

            <PrimaryButton 
                onClick={handleExecute}
                className="mb-2 mt-10 self-center"
            >
                Execute RAPID
            </PrimaryButton>

    </div>
);
};

export default RapidPanel;