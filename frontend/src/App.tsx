import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';
import { RobotProvider } from './context/RobotContext';

function App() {
  return (
    <RobotProvider>
      <div className="h-screen w-screen flex flex-col bg-slate-100 overflow-hidden">
        
        {/* Top Bar */}
        <Header />

        {/* Main Workspace (Split View) */}
        <div className="flex flex-1 overflow-hidden">
          
          {/* Left Panel */}
          <Sidebar />

          {/* Right Panel (3D Canvas Placeholder) */}
          <main className="flex-1 relative bg-gray-900 flex items-center justify-center">
            
            <div className="text-center">
              <h2 className="text-2xl text-white font-light mb-2">3D Viewport</h2>
              <p className="text-slate-400 text-sm">Babylon.js Scene initializes here in Step 2</p>
              
              {/* Temporary Visual Grid */}
              <div className="absolute inset-0 opacity-10 pointer-events-none" 
                    style={{ 
                      backgroundImage: 'linear-gradient(#444 1px, transparent 1px), linear-gradient(90deg, #444 1px, transparent 1px)', 
                      backgroundSize: '40px 40px' 
                    }}>
              </div>
            </div>

          </main>

        </div>
      </div>
    </RobotProvider>
  );
}

export default App;