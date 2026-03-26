"use client";

import { useState } from "react";
// Note: You will need to copy Header and MainLayout into src/components/ next
import { Header } from "@/components/Header";
import MainLayout from "@/components/MainLayout";

// Export TabType so other components can import it, just like the old App.tsx
export type TabType = "rapid" | "jog";

export const ROBOT_MODELS = [
  { path: "/models/robots/irb4600/Model_IRB_4600.glb", label: "ABB IRB 4600" },
  { path: "/models/robots/irb2600/Model_IRB_2600.glb", label: "ABB IRB 2600" },
  { path: "/models/robots/irb6700/Model_IRB_6700.glb", label: "ABB IRB 6700" },
];

export default function Home() {
  // Lifted global state
  const [activeTab, setActiveTab] = useState<TabType>("rapid");
  const [modelPath, setModelPath] = useState<string | null>(null);
  const [lastLog, setLastLog] = useState<{ message: string; type: "info" | "success" | "error" | "warning" }>({
    message: "System Initialized",
    type: "info",
  });

  const handleAddLog = (message: string, type: "info" | "success" | "error" | "warning" = "info") => {
    setLastLog({ message, type });
  };

  const handleFileUploaded = (fileName: string) => {
    handleAddLog(`Loaded file: ${fileName}`, "info");
  };

  return (
    <main className="flex flex-col h-screen w-screen bg-black overflow-hidden">
      <Header 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        modelPath={modelPath} 
        setModelPath={setModelPath} 
      />
      
      <div className="flex-1 relative min-h-0">
        <MainLayout 
          activeTab={activeTab}
          modelPath={modelPath}
          lastLog={lastLog}
          setActiveTab={setActiveTab}
          onFileUploaded={handleFileUploaded}
          onAddLog={handleAddLog}
        />
      </div>
    </main>
  );
}
