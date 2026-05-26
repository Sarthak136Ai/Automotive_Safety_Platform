import React, { useState } from "react";
import { predictRecallSeverity } from "../api/api";
import { AlertCircle, ShieldAlert, Cpu, Sparkles, ChevronRight, Activity, ArrowRight, BookOpen, Layers } from "lucide-react";

function PredictionPanel() {
  const [formData, setFormData] = useState({
    manufacturer: "",
    component: "Brakes",
    model_year: 2021,
    summary: "",
    consequence: "",
    remedy: ""
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.manufacturer || !formData.summary) {
      setError("Please fill out the required fields: Manufacturer and Defect Summary.");
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const prediction = await predictRecallSeverity({
        manufacturer: formData.manufacturer,
        component: formData.component,
        summary: formData.summary,
        consequence: formData.consequence || null,
        remedy: formData.remedy || null,
        model_year: parseInt(formData.model_year)
      });
      setResult(prediction);
    } catch (err) {
      console.error("Recall prediction execution failure:", err);
      setError("Prediction failed. Make sure the ML artifacts are generated and the FastAPI backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const getRiskStyles = (tier) => {
    switch (tier?.toLowerCase()) {
      case "low":
        return { text: "text-risk-low", bg: "bg-risk-low/10 border-risk-low/20", progress: "bg-risk-low" };
      case "medium":
      case "moderate":
        return { text: "text-risk-medium", bg: "bg-risk-medium/10 border-risk-medium/20", progress: "bg-risk-medium" };
      case "high":
        return { text: "text-risk-high", bg: "bg-risk-high/10 border-risk-high/20", progress: "bg-risk-high" };
      case "critical":
        return { text: "text-risk-critical", bg: "bg-risk-critical/10 border-risk-critical/20", progress: "bg-risk-critical" };
      default:
        return { text: "text-zinc-400", bg: "bg-zinc-800/10 border-zinc-800/20", progress: "bg-zinc-500" };
    }
  };

  const componentsList = [
    "Brakes", "Airbags", "Electrical System", "Fuel System", 
    "Steering", "Engine", "Seat Belts", "Suspension", "Transmission", "Battery", "Other"
  ];

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Title */}
      <div>
        <h2 className="text-3xl font-extrabold title-outfit text-white">Safety Recall Threat Forecaster</h2>
        <p className="text-sm text-zinc-400 mt-1">
          Predict safety recall risk levels and receive Explainable AI (SHAP) word importance profiles.
        </p>
      </div>

      {/* Main Grid: Form Left, Results Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Prediction Form: 5 cols */}
        <form onSubmit={handleSubmit} className="glass-panel p-6 rounded-2xl lg:col-span-5 space-y-5">
          <h3 className="text-lg font-bold title-outfit text-white flex items-center gap-2 pb-2 border-b border-zinc-800/50">
            <Cpu className="w-4 h-4 text-indigo-400" />
            Safety Defect Parameters
          </h3>

          <div className="grid grid-cols-2 gap-4">
            {/* Manufacturer */}
            <div className="col-span-2">
              <label className="block text-xs font-semibold text-zinc-400 mb-1.5 uppercase tracking-wider">
                Manufacturer make *
              </label>
              <input
                type="text"
                required
                placeholder="e.g. Tesla, Ford, General Motors"
                value={formData.manufacturer}
                onChange={(e) => setFormData({ ...formData, manufacturer: e.target.value })}
                className="w-full bg-zinc-950/60 border border-zinc-800 rounded-xl py-2.5 px-4 text-sm text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-indigo-600 transition-colors"
              />
            </div>

            {/* Component */}
            <div>
              <label className="block text-xs font-semibold text-zinc-400 mb-1.5 uppercase tracking-wider">
                Component system
              </label>
              <select
                value={formData.component}
                onChange={(e) => setFormData({ ...formData, component: e.target.value })}
                className="w-full bg-zinc-950/60 border border-zinc-800 rounded-xl py-2.5 px-3 text-sm text-zinc-300 focus:outline-none focus:border-indigo-600 transition-colors"
              >
                {componentsList.map((comp) => (
                  <option key={comp} value={comp}>
                    {comp}
                  </option>
                ))}
              </select>
            </div>

            {/* Model Year */}
            <div>
              <label className="block text-xs font-semibold text-zinc-400 mb-1.5 uppercase tracking-wider">
                Model Year
              </label>
              <input
                type="number"
                min="1990"
                max="2027"
                required
                value={formData.model_year}
                onChange={(e) => setFormData({ ...formData, model_year: parseInt(e.target.value) })}
                className="w-full bg-zinc-950/60 border border-zinc-800 rounded-xl py-2.5 px-4 text-sm text-zinc-200 focus:outline-none focus:border-indigo-600 transition-colors"
              />
            </div>
          </div>

          {/* Defect Summary */}
          <div>
            <label className="block text-xs font-semibold text-zinc-400 mb-1.5 uppercase tracking-wider">
              Defect Summary Description *
            </label>
            <textarea
              required
              rows="3"
              placeholder="Describe the vehicle system defect details..."
              value={formData.summary}
              onChange={(e) => setFormData({ ...formData, summary: e.target.value })}
              className="w-full bg-zinc-950/60 border border-zinc-800 rounded-xl py-2.5 px-4 text-sm text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-indigo-600 transition-colors resize-none"
            />
          </div>

          {/* Consequence Summary */}
          <div>
            <label className="block text-xs font-semibold text-zinc-400 mb-1.5 uppercase tracking-wider">
              Consequence Summary
            </label>
            <textarea
              rows="2"
              placeholder="Describe the safety hazard consequences..."
              value={formData.consequence}
              onChange={(e) => setFormData({ ...formData, consequence: e.target.value })}
              className="w-full bg-zinc-950/60 border border-zinc-800 rounded-xl py-2.5 px-4 text-sm text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-indigo-600 transition-colors resize-none"
            />
          </div>

          {/* Remedy Action */}
          <div>
            <label className="block text-xs font-semibold text-zinc-400 mb-1.5 uppercase tracking-wider">
              Remedy Corrective Action
            </label>
            <textarea
              rows="2"
              placeholder="Describe how dealers will fix the issue..."
              value={formData.remedy}
              onChange={(e) => setFormData({ ...formData, remedy: e.target.value })}
              className="w-full bg-zinc-950/60 border border-zinc-800 rounded-xl py-2.5 px-4 text-sm text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-indigo-600 transition-colors resize-none"
            />
          </div>

          {error && (
            <div className="flex items-center gap-2 p-3 text-xs bg-red-950/30 text-risk-high rounded-xl border border-red-500/10">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-zinc-800 text-white py-3 rounded-xl text-sm font-semibold transition-all duration-200 flex items-center justify-center gap-2 shadow-lg shadow-indigo-600/15"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin -ml-1 mr-3 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Analyzing Defect...
              </span>
            ) : (
              <>
                Assess Recall Risk
                <ChevronRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Prediction Results: 7 cols */}
        <div className="lg:col-span-7 space-y-6">
          {result ? (
            <div className="space-y-6 animate-fadeIn">
              
              {/* Row: Severity Index Circular Visual & Probabilities */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                
                {/* Dial Widget */}
                <div className="glass-panel p-6 rounded-2xl flex flex-col items-center justify-between h-64 text-center">
                  <span className="text-xs font-bold uppercase tracking-wider text-zinc-400">Risk Assessment</span>
                  
                  {/* Gauge */}
                  <div className="relative flex items-center justify-center mt-3">
                    <svg className="w-32 h-32 transform -rotate-90">
                      <circle cx="64" cy="64" r="54" className="stroke-zinc-800" strokeWidth="10" fill="transparent" />
                      <circle 
                        cx="64" 
                        cy="64" 
                        r="54" 
                        className={`transition-all duration-1000 ${
                          result.predicted_risk_tier.toLowerCase() === "low" ? "stroke-risk-low" :
                          result.predicted_risk_tier.toLowerCase() === "medium" ? "stroke-risk-medium" :
                          result.predicted_risk_tier.toLowerCase() === "high" ? "stroke-risk-high" : "stroke-risk-critical"
                        }`}
                        strokeWidth="10" 
                        fill="transparent"
                        strokeDasharray={2 * Math.PI * 54}
                        strokeDashoffset={2 * Math.PI * 54 * (1 - result.probabilities[result.predicted_risk_tier])}
                        strokeLinecap="round"
                      />
                    </svg>
                    <div className="absolute flex flex-col items-center justify-center">
                      <span className={`text-2xl font-black title-outfit uppercase tracking-tight ${getRiskStyles(result.predicted_risk_tier).text}`}>
                        {result.predicted_risk_tier}
                      </span>
                      <span className="text-xs font-bold text-zinc-500 font-mono mt-0.5">
                        {Math.round(result.probabilities[result.predicted_risk_tier] * 100)}% Match
                      </span>
                    </div>
                  </div>

                  <span className="text-[10px] text-zinc-500 leading-normal max-w-[180px] mt-2">
                    XGBoost probability confidence score based on combined safety features.
                  </span>
                </div>

                {/* Probability List */}
                <div className="glass-panel p-6 rounded-2xl flex flex-col justify-between h-64">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-zinc-400 pb-2 border-b border-zinc-800/40">
                    Distribution Signatures
                  </h4>
                  <div className="space-y-3.5 my-auto">
                    {["Low", "Medium", "High", "Critical"].map((tier) => {
                      const prob = result.probabilities[tier] || 0.0;
                      return (
                        <div key={tier} className="space-y-1.5">
                          <div className="flex justify-between text-xs font-semibold">
                            <span className="text-zinc-300">{tier} Risk</span>
                            <span className="font-mono text-zinc-400">{Math.round(prob * 100)}%</span>
                          </div>
                          <div className="w-full bg-zinc-950 rounded-full h-2 overflow-hidden border border-zinc-800/40">
                            <div 
                              className={`h-full rounded-full transition-all duration-1000 ${getRiskStyles(tier).progress}`}
                              style={{ width: `${prob * 100}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

              </div>

              {/* AI Summary and Entities Card */}
              <div className="glass-panel p-6 rounded-2xl relative overflow-hidden border border-indigo-500/10">
                {/* Gradient Sparkle Glow */}
                <div className="absolute top-0 right-0 w-24 h-24 bg-indigo-500/5 rounded-full blur-xl pointer-events-none" />
                
                <h4 className="text-xs font-bold uppercase tracking-wider text-indigo-400 flex items-center gap-1.5 mb-3">
                  <Sparkles className="w-3.5 h-3.5 animate-pulse" />
                  AI Summary Headline (BART CNN)
                </h4>
                
                <p className="text-sm font-semibold text-white leading-relaxed italic border-l-2 border-indigo-500 pl-4 py-1">
                  "{result.ai_summary}"
                </p>

                {/* Extracted Entities badges */}
                <div className="mt-5 pt-4 border-t border-zinc-800/40 grid grid-cols-2 gap-4">
                  <div>
                    <span className="block text-[10px] uppercase font-bold text-zinc-500 tracking-wider mb-2">
                      Extracted Component Systems
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {result.entities.components.map((item) => (
                        <span key={item} className="text-[10px] font-semibold px-2 py-0.5 rounded bg-zinc-900 border border-zinc-800 text-zinc-300 capitalize">
                          {item}
                        </span>
                      ))}
                      {result.entities.components.length === 0 && (
                        <span className="text-[10px] text-zinc-600 italic">None identified</span>
                      )}
                    </div>
                  </div>

                  <div>
                    <span className="block text-[10px] uppercase font-bold text-zinc-500 tracking-wider mb-2">
                      Safety Hazard Indicators
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {result.entities.failures.map((item) => (
                        <span key={item} className="text-[10px] font-semibold px-2 py-0.5 rounded bg-zinc-900 border border-zinc-800 text-zinc-300 capitalize">
                          {item}
                        </span>
                      ))}
                      {result.entities.failures.length === 0 && (
                        <span className="text-[10px] text-zinc-600 italic">None identified</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Explainable AI: SHAP Explanations */}
              <div className="glass-panel p-6 rounded-2xl">
                <h4 className="text-xs font-bold uppercase tracking-wider text-zinc-400 mb-4 pb-2 border-b border-zinc-800/40 flex items-center justify-between">
                  <span>Explainable AI Model Trace (SHAP value contributions)</span>
                  <span className="text-[10px] font-normal text-zinc-500 uppercase font-sans">Feature Impact</span>
                </h4>

                <div className="space-y-3">
                  {result.shap_explanations.map((item, idx) => {
                    const isPositive = item.shap_value > 0;
                    // Max bound for plotting widths
                    const maxShap = Math.max(...result.shap_explanations.map(x => Math.abs(x.shap_value)), 0.1);
                    const widthPercent = Math.min((Math.abs(item.shap_value) / maxShap) * 100, 100);

                    return (
                      <div key={idx} className="grid grid-cols-12 gap-3 items-center text-xs">
                        {/* Feature Name */}
                        <div className="col-span-4 font-semibold text-zinc-300 truncate">
                          {item.feature}
                        </div>

                        {/* Chart bar */}
                        <div className="col-span-8 flex items-center gap-2">
                          <div className="flex-1 bg-zinc-950 h-5 rounded overflow-hidden relative border border-zinc-800/30 flex items-center">
                            {/* Directional Alignment */}
                            <div 
                              className={`h-full rounded ${isPositive ? "bg-red-500/20 border-r-2 border-red-500" : "bg-blue-500/20 border-l-2 border-blue-500"}`}
                              style={{ 
                                width: `${widthPercent}%`,
                                marginLeft: isPositive ? "0" : "auto"
                              }}
                            />
                            
                            {/* Indicator Badge inside bar */}
                            <span className={`absolute px-2 text-[9px] font-mono font-bold ${isPositive ? "right-2 text-red-400" : "left-2 text-blue-400"}`}>
                              {isPositive ? "+" : ""}{item.shap_value.toFixed(4)}
                            </span>
                          </div>
                          
                          <span className="text-[9px] font-bold text-zinc-500 w-8 text-right font-mono uppercase">
                            {isPositive ? "Risk+" : "Risk-"}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                  {result.shap_explanations.length === 0 && (
                    <div className="py-6 text-center text-zinc-600 italic text-xs">
                      No significant SHAP feature logs captured for this prediction.
                    </div>
                  )}
                </div>
              </div>

            </div>
          ) : (
            /* Idle Placeholder State */
            <div className="glass-panel p-12 rounded-2xl h-full flex flex-col items-center justify-center text-center space-y-4 border-dashed border-zinc-800/80">
              <div className="p-4 rounded-full bg-zinc-900 border border-zinc-800 text-zinc-500">
                <Activity className="w-8 h-8" />
              </div>
              <div>
                <h4 className="text-base font-bold title-outfit text-zinc-300">Awaiting Safety Assessment</h4>
                <p className="text-xs text-zinc-500 max-w-sm mx-auto mt-1">
                  Fill out the parameters form on the left to execute the live AutoSentinel AI safety recall risk models.
                </p>
              </div>
              <div className="pt-2 text-[10px] text-zinc-600 flex items-center gap-2">
                <span>FastAPI Predict Core</span>
                <ArrowRight className="w-3 h-3" />
                <span>TreeExplainer Log</span>
                <ArrowRight className="w-3 h-3" />
                <span>BART Summarizer</span>
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}

export default PredictionPanel;
