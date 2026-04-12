"use client";

import { useState } from "react";
import { Header } from "@/components/Header";
import MainLayout from "@/components/MainLayout";
import type { TabType } from "@/types";

export default function Home() {
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
    <main
      className="flex flex-col w-full bg-black overflow-hidden"
      style={{ height: 'calc(100vh - var(--mrb-height, 0px))' }}
    >
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
