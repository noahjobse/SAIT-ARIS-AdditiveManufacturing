import { useState, useEffect } from "react";
import { Header } from "./components/Header";
import MainLayout from "./components/MainLayout";

export type TabType = "rapid" | "jog";
export type BottomPanelMode = "both" | "scrubber" | "logs";

export const ROBOT_MODELS = [
    { label: "ABB IRB 4600", path: "/models/robots/irb4600/Model_IRB_4600.glb" },
    { label: "ABB IRB 2600", path: "/models/robots/irb2600/Model_IRB_2600.glb" },
    { label: "ABB IRB 6700", path: "/models/robots/irb6700/Model_IRB_6700.glb" },
]

function App() {
    const [activeTab, setActiveTab] = useState<TabType>("jog");
    const [modelPath, setModelPath] = useState<string | null>(null);
    const [lastLog, setLastLog] = useState<{message: string, type: 'info' | 'success' | 'error' | 'warning'}>({
        message: "System Initialized",
        type: 'info'
    });

    // Log robot changes
    useEffect(() => {
        const robot = ROBOT_MODELS.find(r => r.path === modelPath);
        if (robot) {
            setLastLog({
                message: `Switched to robot: ${robot.label}`,
                type: 'success'
            });
        }
    }, [modelPath]);

    const handleFileUploaded = (fileName: string) => {
        setLastLog({
            message: `File uploaded: ${fileName}`,
            type: 'success'
        });
    };

    const handleLog = (message: string, type: 'info' | 'success' | 'error' | 'warning' = 'info') => {
        setLastLog({ message, type });
    };

    return (
        <div className="flex flex-col h-screen overflow-hidden bg-zinc-900">
            <Header 
                activeTab={activeTab} 
                setActiveTab={setActiveTab} 
                modelPath={modelPath}
                setModelPath={setModelPath}
            />
            
            <div className="flex-1 min-h-0 relative">
                <MainLayout 
                    activeTab={activeTab} 
                    setActiveTab={setActiveTab}
                    modelPath={modelPath} 
                    lastLog={lastLog}
                    onFileUploaded={handleFileUploaded}
                    onAddLog={handleLog}
                />
            </div>
        </div>
    )
}

export default App;