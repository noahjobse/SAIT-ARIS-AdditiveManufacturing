import React from "react";

type SidePanelHeaderProps = {
    title: string;
    description?: string;
};

function SidePanelHeader({ title, description }: SidePanelHeaderProps) {
    const words = title.split(" ");
    const firstWord = words[0];
    const rest = words.slice(1).join(" ");

    return (
        <>
            <h2 className="text-xl font-bold mb-2 tracking-tight w-48" style={{ fontFamily: "var(--font-geist-mono)" }}>
                <span className="text-white">{firstWord}</span>{" "}
                <span style={{ background: "linear-gradient(135deg,#f97316,#9333ea)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>{rest}</span>
            </h2>
            {description && (
                <p className="text-sm text-gray-400">{description}</p>
            )}
            <hr className="my-6 border-gray-400/50" />
        </>
    );
}

export default SidePanelHeader;
