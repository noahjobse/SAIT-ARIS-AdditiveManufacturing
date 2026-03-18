type SidePanelHeaderProps = {
    title: string;
    description?: string;
};
function SidePanelHeader({ title, description }: SidePanelHeaderProps) {
    return (
        <>
            <h2 className="text-xl font-bold bg-linear-to-r from-orange-500 to-purple-600 bg-clip-text text-transparent mb-2 tracking-tight w-48">
                {title}
            </h2>

            {description && (
                <p className="text-sm text-gray-400">{description}</p>
            )}

            <hr className="my-6 border-gray-400/50" />
        </>
    );
}

export default SidePanelHeader;