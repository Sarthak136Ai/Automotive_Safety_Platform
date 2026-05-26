import React, { useState } from "react";
import { searchSemanticRecalls } from "../api/api";
import { Search, ShieldAlert, Cpu, Sparkles, Filter, ChevronDown, ChevronUp, AlertCircle, FileText } from "lucide-react";

function SemanticSearch() {
  const [query, setQuery] = useState("");
  const [topK, setTopK] = useState(5);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  
  // Track index of expanded safety cards
  const [expandedCards, setExpandedCards] = useState({});

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    try {
      setLoading(true);
      setError(null);
      setExpandedCards({}); // Reset expanded cards
      const response = await searchSemanticRecalls(query, parseInt(topK));
      setResults(response.results);
    } catch (err) {
      console.error("Semantic query failure:", err);
      setError("Semantic vector search failed. Make sure the embeddings have been compiled by running python src/run_pipeline.py first.");
    } finally {
      setLoading(false);
    }
  };

  const toggleCard = (id) => {
    setExpandedCards((prev) => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  const getRiskStyles = (tier) => {
    switch (tier?.toLowerCase()) {
      case "low":
        return "text-risk-low bg-risk-low/10 border-risk-low/20";
      case "medium":
      case "moderate":
        return "text-risk-medium bg-risk-medium/10 border-risk-medium/20";
      case "high":
        return "text-risk-high bg-risk-high/10 border-risk-high/20";
      case "critical":
        return "text-risk-critical bg-risk-critical/10 border-risk-critical/20";
      default:
        return "text-zinc-400 bg-zinc-800/20 border-zinc-800/10";
    }
  };

  const getSimilarityBadge = (score) => {
    const percentage = Math.round(score * 100);
    if (percentage > 85) {
      return "text-indigo-400 bg-indigo-950/40 border-indigo-500/20";
    } else if (percentage > 60) {
      return "text-cyan-400 bg-cyan-950/40 border-cyan-500/20";
    } else {
      return "text-zinc-500 bg-zinc-900 border-zinc-800/60";
    }
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Title */}
      <div>
        <h2 className="text-3xl font-extrabold title-outfit text-white">Semantic Safety Recall Explorer</h2>
        <p className="text-sm text-zinc-400 mt-1">
          Perform high-dimensional cosine similarity searches across safety recall indexes using dense vector embeddings.
        </p>
      </div>

      {/* Query Bar Form */}
      <form onSubmit={handleSearch} className="glass-panel p-5 rounded-2xl flex flex-col sm:flex-row gap-4 items-center border border-indigo-500/10">
        <div className="relative flex-1 w-full">
          <Search className="w-5 h-5 text-zinc-500 absolute left-4 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            required
            placeholder="Type vehicle safety concern (e.g. steering wheel vibration, airbags fail to deploy, battery overheat)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-zinc-950/60 border border-zinc-800/80 rounded-xl py-3 pl-12 pr-4 text-sm text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-indigo-600 transition-colors"
          />
        </div>

        <div className="flex gap-4 items-center w-full sm:w-auto shrink-0 justify-end">
          {/* TopK Selection */}
          <div className="flex items-center gap-2 bg-zinc-950/60 border border-zinc-800/80 rounded-xl px-3 py-2 text-sm text-zinc-400 shrink-0">
            <Filter className="w-4 h-4 text-zinc-500" />
            <select
              value={topK}
              onChange={(e) => setTopK(e.target.value)}
              className="bg-transparent border-none text-zinc-300 focus:outline-none text-xs font-semibold cursor-pointer"
            >
              {[3, 5, 8, 12, 15, 20].map((k) => (
                <option key={k} value={k}>
                  Top {k} Results
                </option>
              ))}
            </select>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-zinc-800 text-white font-semibold text-sm px-6 py-3 rounded-xl transition-colors shrink-0 flex items-center gap-2 shadow-lg shadow-indigo-600/15"
          >
            {loading ? "Searching Index..." : "Search Index"}
          </button>
        </div>
      </form>

      {/* Error State */}
      {error && (
        <div className="glass-panel p-6 rounded-2xl border border-red-500/20 text-center max-w-2xl mx-auto space-y-4">
          <AlertCircle className="w-10 h-10 text-risk-high mx-auto" />
          <h4 className="text-base font-bold title-outfit text-white">Embeddings Matrix Missing</h4>
          <p className="text-xs text-zinc-400">{error}</p>
        </div>
      )}

      {/* Loading Skeleton */}
      {loading && (
        <div className="space-y-4 animate-pulse">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="h-28 bg-zinc-900 rounded-2xl border border-zinc-800/40" />
          ))}
        </div>
      )}

      {/* Search Result List */}
      {results && !loading && (
        <div className="space-y-4 animate-fadeIn">
          <div className="flex justify-between items-center px-2">
            <span className="text-xs font-bold text-zinc-500 uppercase tracking-wider">
              Search Results Matrix for: <span className="text-indigo-400 lowercase font-mono">"{query}"</span>
            </span>
            <span className="text-xs text-zinc-500">
              Found {results.length} matched recall items
            </span>
          </div>

          {results.map((recall, index) => {
            const isExpanded = !!expandedCards[recall.id];
            return (
              <div 
                key={recall.id} 
                className={`glass-panel rounded-2xl overflow-hidden border transition-all duration-300 ${
                  isExpanded ? "border-indigo-500/25 bg-zinc-900/40" : "border-white/5 hover:border-zinc-800/80"
                }`}
              >
                {/* Visible Banner */}
                <div 
                  onClick={() => toggleCard(recall.id)}
                  className="p-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 cursor-pointer select-none"
                >
                  <div className="space-y-1.5 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      {/* Similarity Badge */}
                      <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${getSimilarityBadge(recall.similarity_score)}`}>
                        {Math.round(recall.similarity_score * 100)}% Match
                      </span>
                      
                      {/* Threat Class */}
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold border uppercase tracking-wider ${getRiskStyles(recall.risk_label)}`}>
                        {recall.risk_label} risk
                      </span>

                      <span className="text-xs text-zinc-400 font-semibold font-mono">
                        {recall.manufacturer} &bull; {recall.model_year}
                      </span>
                    </div>

                    <h4 className="text-sm font-semibold text-white leading-snug">
                      {recall.ai_summary}
                    </h4>
                  </div>

                  <div className="flex items-center gap-3 shrink-0 self-end md:self-auto">
                    <span className="text-xs font-medium text-zinc-500 capitalize bg-zinc-950/40 px-2.5 py-1 rounded-lg border border-zinc-800/40">
                      {recall.component}
                    </span>
                    <button className="p-1.5 rounded-lg bg-zinc-950/40 border border-zinc-800/40 text-zinc-400 hover:text-zinc-200">
                      {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {/* Expanded Details Panel */}
                {isExpanded && (
                  <div className="px-5 pb-5 pt-3 border-t border-zinc-800/40 bg-zinc-950/30 grid grid-cols-1 md:grid-cols-3 gap-6 animate-fadeIn">
                    
                    {/* Defect Description */}
                    <div className="space-y-1.5">
                      <div className="flex items-center gap-1.5 text-zinc-400 text-xs font-bold uppercase tracking-wider">
                        <FileText className="w-3.5 h-3.5 text-zinc-500" />
                        Defect summary
                      </div>
                      <p className="text-xs text-zinc-300 leading-relaxed font-sans bg-zinc-950/60 p-3.5 rounded-xl border border-zinc-800/40 min-h-[100px]">
                        {recall.summary}
                      </p>
                    </div>

                    {/* Safety Consequence */}
                    <div className="space-y-1.5">
                      <div className="flex items-center gap-1.5 text-zinc-400 text-xs font-bold uppercase tracking-wider">
                        <ShieldAlert className="w-3.5 h-3.5 text-zinc-500" />
                        Consequence hazard
                      </div>
                      <p className="text-xs text-zinc-300 leading-relaxed font-sans bg-zinc-950/60 p-3.5 rounded-xl border border-zinc-800/40 min-h-[100px]">
                        {recall.consequence}
                      </p>
                    </div>

                    {/* Dealer Remedy */}
                    <div className="space-y-1.5">
                      <div className="flex items-center gap-1.5 text-zinc-400 text-xs font-bold uppercase tracking-wider">
                        <Cpu className="w-3.5 h-3.5 text-zinc-500" />
                        Remedy Action
                      </div>
                      <p className="text-xs text-zinc-300 leading-relaxed font-sans bg-zinc-950/60 p-3.5 rounded-xl border border-zinc-800/40 min-h-[100px]">
                        {recall.remedy}
                      </p>
                    </div>

                  </div>
                )}
              </div>
            );
          })}
          {results.length === 0 && (
            <div className="glass-panel p-12 rounded-2xl text-center text-zinc-500">
              No matching automotive safety recalls found in index.
            </div>
          )}
        </div>
      )}

      {/* Idle placeholder */}
      {!results && !loading && (
        <div className="glass-panel p-16 rounded-2xl text-center space-y-4 border-dashed border-zinc-800">
          <div className="p-4 rounded-full bg-zinc-900 border border-zinc-800 text-zinc-600 max-w-fit mx-auto">
            <Search className="w-8 h-8" />
          </div>
          <div>
            <h4 className="text-base font-bold title-outfit text-zinc-400">Awaiting Semantic Search Query</h4>
            <p className="text-xs text-zinc-500 max-w-md mx-auto mt-1">
              Type vehicle defects in natural language to search, extract, and trace similarities across the historical recall database.
            </p>
          </div>
        </div>
      )}

    </div>
  );
}

export default SemanticSearch;
