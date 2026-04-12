'use client'

import type { TabType } from "@/types";
import { FileCode as RapidCodeIcon, Printer as PrinterIcon } from 'lucide-react';
import JointJogIcon from "@/assets/joint-jog-icon.svg";

type SidePanelTabsProps = {
    activeTab: TabType;
    setActiveTab: (tab: TabType) => void;
};

function SidePanelTabs({ activeTab, setActiveTab }: SidePanelTabsProps) {
    const tabs = [
        { id: "rapid" as TabType, label: "RAPID Code", icon: RapidCodeIcon },
        { id: "jog" as TabType, label: "Joint Jog", icon: JointJogIcon },
        { id: "print" as TabType, label: "3D Print", icon: PrinterIcon },
    ];

    return (
        <div className="flex flex-row px-3 py-1  justify-center items-center text-sm md:text-md font-medium h-full">
            {tabs.map((tab, i) => {
                const Icon = tab.icon;
                const isFirst = i === 0;
                const isLast = i === tabs.length - 1;

                return (
                    <button 
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`relative h-full w-28 py-2 px-4 transition-all duration-150 cursor-pointer flex flex-col  justify-center items-center ${
                            activeTab === tab.id 
                                ? "bg-gray-900 text-orange-500 border border-orange-500/50 transition-colors shadow-lg shadow-orange-500/30" 
                            : "bg-gray-900 text-gray-300 hover:bg-gray-800 border border-white/10 hover:text-orange-500 transition-colors"
                        }
                        ${isFirst ? "rounded-l-md" : ""}
                        ${isLast ? "rounded-r-md" : ""}
                    `}
                    >
                        {Icon && <Icon className="w-8 h-8 mb-1" />}
                        {tab.label}

                        {activeTab === tab.id && (
                            <div className="absolute left-1/2 -translate-x-1/2 -bottom-1 w-full h-1 bg-orange-500/10 -z-10 blur-md rounded-full pointer-events-none" />
                        )}
                    </button>
                );
        })}
        </div>
    );
}

export default SidePanelTabs;
