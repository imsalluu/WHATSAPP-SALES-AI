"use client";

import React, { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import { apiRequest } from "@/lib/api";
import { BrainCircuit, Upload, Search, Trash2, Sparkles, FileText, CheckCircle2 } from "lucide-react";

export default function KnowledgePage() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [title, setTitle] = useState("");
  const [docType, setDocType] = useState("RETURN_REFUND");
  const [content, setContent] = useState("");
  const [testQuery, setTestQuery] = useState("");
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const fetchDocuments = async () => {
    try {
      const data = await apiRequest("/knowledge/documents");
      setDocuments(data);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleUploadDocument = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !content.trim()) return;

    try {
      await apiRequest("/knowledge/documents", {
        method: "POST",
        body: JSON.stringify({
          title,
          document_type: docType,
          content,
        }),
      });
      setTitle("");
      setContent("");
      fetchDocuments();
    } catch (e: any) {
      alert(e.message || "Failed to upload document");
    }
  };

  const handleDelete = async (docId: string) => {
    if (!confirm("Delete this document and vectorized embeddings?")) return;
    try {
      await apiRequest(`/knowledge/documents/${docId}`, { method: "DELETE" });
      fetchDocuments();
    } catch (e: any) {
      alert(e.message || "Failed to delete");
    }
  };

  const handleTestSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!testQuery.trim()) return;
    setIsSearching(true);
    try {
      const results = await apiRequest("/knowledge/search", {
        method: "POST",
        body: JSON.stringify({ query: testQuery, limit: 3 }),
      });
      setSearchResults(results);
    } catch (e: any) {
      alert(e.message || "Search failed");
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Header
          title="RAG Knowledge Base (pgvector)"
          subtitle="Upload store policies, FAQs, and guides so the AI Sales Agent can ground every reply in business facts"
        />

        <main className="p-8 space-y-8 flex-1 overflow-y-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Left: Document Upload & Ingestion Form */}
            <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl backdrop-blur-sm">
              <h3 className="text-sm font-bold text-white flex items-center gap-2 mb-1">
                <Upload className="w-4 h-4 text-emerald-400" />
                <span>Ingest Store Policy or FAQ</span>
              </h3>
              <p className="text-xs text-slate-400 mb-5">
                Automatically chunked into 400-char fragments with vector embeddings.
              </p>

              <form onSubmit={handleUploadDocument} className="space-y-4">
                <div>
                  <label className="text-xs font-semibold text-slate-300">Document Title</label>
                  <input
                    type="text"
                    required
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="w-full mt-1.5 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500"
                    placeholder="e.g. 7-Day Return & Exchange Policy 2026"
                  />
                </div>

                <div>
                  <label className="text-xs font-semibold text-slate-300">Category Type</label>
                  <select
                    value={docType}
                    onChange={(e) => setDocType(e.target.value)}
                    className="w-full mt-1.5 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                  >
                    <option value="RETURN_REFUND">RETURN & REFUND POLICY</option>
                    <option value="SHIPPING">SHIPPING & DELIVERY TIMELINES</option>
                    <option value="FAQ">STORE FREQUENTLY ASKED QUESTIONS</option>
                    <option value="POLICY">WARRANTY & AUTHENTICITY</option>
                    <option value="GENERAL">GENERAL BRAND INFORMATION</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs font-semibold text-slate-300">Document Content</label>
                  <textarea
                    rows={6}
                    required
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    className="w-full mt-1.5 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500"
                    placeholder="Paste full policy text here. For example: Customers can exchange items within 7 days..."
                  />
                </div>

                <button
                  type="submit"
                  className="w-full py-3 px-4 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/20 transition-all active:scale-95 flex items-center justify-center gap-2"
                >
                  <BrainCircuit className="w-4 h-4" />
                  <span>Index into Vector Database</span>
                </button>
              </form>
            </div>

            {/* Right: Interactive Semantic Search Playground */}
            <div className="space-y-6">
              <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl backdrop-blur-sm">
                <h3 className="text-sm font-bold text-white flex items-center gap-2 mb-1">
                  <Sparkles className="w-4 h-4 text-emerald-400" />
                  <span>RAG Vector Search Playground</span>
                </h3>
                <p className="text-xs text-slate-400 mb-4">
                  Test semantic query retrieval to preview exact context injected into AI prompts.
                </p>

                <form onSubmit={handleTestSearch} className="flex gap-2">
                  <input
                    type="text"
                    value={testQuery}
                    onChange={(e) => setTestQuery(e.target.value)}
                    placeholder="Ask policy question (e.g. How many days for return?)..."
                    className="flex-1 px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500"
                  />
                  <button
                    type="submit"
                    disabled={isSearching}
                    className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-emerald-400 text-xs font-bold rounded-xl border border-slate-700"
                  >
                    {isSearching ? "Searching..." : "Retrieve"}
                  </button>
                </form>

                {/* Retrieved Chunks Display */}
                {searchResults.length > 0 && (
                  <div className="mt-4 space-y-2.5">
                    <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                      Retrieved Grounding Chunks
                    </p>
                    {searchResults.map((res, i) => (
                      <div
                        key={i}
                        className="p-3.5 rounded-2xl bg-slate-950 border border-emerald-500/30 text-xs space-y-1"
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-semibold text-emerald-300">{res.document_title}</span>
                          <span className="font-mono text-[10px] text-emerald-400 font-bold">
                            Match Score: {(res.score * 100).toFixed(1)}%
                          </span>
                        </div>
                        <p className="text-slate-300 text-[11px] leading-relaxed mt-1">{res.content}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Uploaded Documents List */}
          <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl backdrop-blur-sm">
            <h3 className="text-sm font-bold text-white mb-4">Indexed Knowledge Documents</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {documents.length === 0 ? (
                <div className="col-span-2 text-center py-8 text-xs text-slate-500">
                  No knowledge documents indexed yet. Ingest your first store policy above!
                </div>
              ) : (
                documents.map((doc) => (
                  <div
                    key={doc.id}
                    className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800 flex items-start justify-between"
                  >
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <FileText className="w-4 h-4 text-emerald-400" />
                        <h4 className="font-bold text-xs text-white">{doc.title}</h4>
                      </div>
                      <p className="text-[10px] text-slate-400">
                        Type: <span className="text-slate-300 font-mono">{doc.document_type}</span> • Chunks:{" "}
                        <strong className="text-emerald-400">{doc.total_chunks}</strong>
                      </p>
                    </div>
                    <button
                      onClick={() => handleDelete(doc.id)}
                      className="p-1.5 text-slate-500 hover:text-rose-400 transition-colors"
                      title="Delete"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
