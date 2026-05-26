import React, { useState } from "react";
import { ShieldAlert, BarChart3, Binary, Search, HelpCircle, HardDrive } from "lucide-react";
import Dashboard from "./pages/Dashboard.jsx";
import PredictionPanel from "./pages/PredictionPanel.jsx";
import SemanticSearch from "./pages/SemanticSearch.jsx";

function App() {
  const [activeTab, setActiveTab] = useState("dashboard");

  const renderContent = () => {
    switch (activeTab) {
      case "dashboard":
        return <Dashboard />;
      case "prediction":
        return <PredictionPanel />;
      case "search":
        return <SemanticSearch />;
      default:
        return <Dashboard />;
    }
  };

  const navItems = [
    { id: "dashboard", label: "Executive Dashboard", icon: BarChart3 },
    { id: "prediction", label: "Recall Risk Predictor", icon: Binary },
    { id: "search", label: "Semantic Search Explorer", icon: Search },
  ];

  return (
    <div className="flex min-h-screen text-zinc-100 bg-[#09090b]">
      {/* Sidebar Navigation */}
      <aside className="w-64 border-r border-zinc-800/80 bg-zinc-950/80 backdrop-blur-md flex flex-col justify-between fixed h-full z-20">
        <div>
          {/* Brand Header */}
          <div className="p-6 border-b border-zinc-800/80 flex items-center gap-3">
            <div className="bg-indigo-600/20 p-2 rounded-xl border border-indigo-500/30 text-indigo-400">
              <ShieldAlert className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <h1 className="text-lg font-bold title-outfit text-white leading-tight">AutoSentinel AI</h1>
              <span className="text-[10px] uppercase font-bold tracking-wider text-zinc-400">Safety Intelligence</span>
            </div>
          </div>

          {/* Nav Items */}
          <nav className="p-4 space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 ${
                    isActive
                      ? "bg-indigo-600 text-white shadow-lg shadow-indigo-600/25 border border-indigo-500/20"
                      : "text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900/60"
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? "text-white" : "text-zinc-500"}`} />
                  {item.label}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Footer info */}
        <div className="p-4 border-t border-zinc-800/60 text-[11px] text-zinc-500 space-y-2">
          <div className="flex items-center gap-2">
            <HardDrive className="w-3.5 h-3.5 text-zinc-500" />
            <span>NHTSA Safety Recall DB</span>
          </div>
          <div className="flex items-center gap-2">
            <HelpCircle className="w-3.5 h-3.5 text-zinc-500" />
            <span>AI Risk Core: Active</span>
          </div>
          <p className="mt-2 text-[10px] text-zinc-600">&copy; 2026 AutoSentinel Inc. Production Grade v1.0</p>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 pl-64 min-h-screen flex flex-col">
        {/* Top Header */}
        <header className="h-16 border-b border-zinc-800/50 bg-zinc-950/40 backdrop-blur-md px-8 flex items-center justify-between sticky top-0 z-10">
          <div className="flex items-center gap-2">
            <span className="text-xs px-2.5 py-0.5 rounded-full font-semibold bg-emerald-950 text-emerald-400 border border-emerald-500/20">
              System Online
            </span>
            <span className="text-zinc-600">|</span>
            <span className="text-xs text-zinc-400">Model: XGBoost Classifier + live SHAP Explainer</span>
          </div>
          <div className="text-xs text-zinc-400 flex items-center gap-3">
            <span>Server: <strong className="text-indigo-400">FastAPI/Postgres</strong></span>
            <span>Client: <strong className="text-indigo-400">Vite/React/Tailwind</strong></span>
          </div>
        </header>

        {/* Dynamic Panel Content */}
        <div className="flex-1 p-8 bg-transparent max-w-7xl w-full mx-auto">
          {renderContent()}
        </div>
      </main>
    </div>
  );
}

export default App;
