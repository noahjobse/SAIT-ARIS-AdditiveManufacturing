import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center">
      <div className="text-center max-w-2xl px-6">
        <h1 className="text-5xl font-bold text-white mb-4">
          ABB Robot Simulation Platform
        </h1>
        <p className="text-xl text-slate-300 mb-8">
          Welcome to the Digital Twin simulator
        </p>

        <button
          onClick={() => setCount((count) => count + 1)}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200"
        >
          Count is {count}
        </button>
      </div>
    </div>
  )
}

export default App
