export const Header = () => {
  return (
    <header className="h-16 bg-slate-900 text-white flex items-center justify-between px-6 shadow-md z-10">
      
      {/* Title Area */}
      <div className="flex items-center gap-3">
        <div className="text-2xl">🤖</div>
        <h1 className="text-xl font-bold tracking-wide">
          ROBOT SIMULATOR <span className="text-xs font-normal text-slate-400 ml-2">v0.1</span>
        </h1>
      </div>

      {/* User / Theme Area */}
      <div className="flex items-center gap-4">
        <button className="text-xs bg-slate-800 px-3 py-1 rounded hover:bg-slate-700 border border-slate-700">
          Theme
        </button>
        <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-sm font-bold">
          UA
        </div>
      </div>
    </header>
  );
};