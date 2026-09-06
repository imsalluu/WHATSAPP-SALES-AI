"use client";

import React, { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import { apiRequest } from "@/lib/api";
import { Users, Phone, MapPin, Sparkles, Filter, CheckCircle2, Flame, Search } from "lucide-react";

export default function LeadsPage() {
  const [leads, setLeads] = useState<any[]>([]);
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  const fetchLeads = async () => {
    try {
      const data = await apiRequest("/leads/");
      setLeads(data);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchLeads();
  }, []);

  const handleUpdateStatus = async (leadId: string, newStatus: string) => {
    try {
      await apiRequest(`/leads/${leadId}`, {
        method: "PATCH",
        body: JSON.stringify({ status: newStatus }),
      });
      fetchLeads();
    } catch (e: any) {
      alert(e.message || "Failed to update lead");
    }
  };

  const filtered = leads.filter((l) => {
    if (statusFilter !== "ALL" && l.status !== statusFilter) return false;
    if (searchTerm) {
      const phone = l.phone || "";
      const name = (l.name || "").toLowerCase();
      const intent = (l.intent || "").toLowerCase();
      return phone.includes(searchTerm) || name.includes(searchTerm.toLowerCase()) || intent.includes(searchTerm.toLowerCase());
    }
    return true;
  });

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Header
          title="Lead Capture & CRM Intelligence"
          subtitle="AI-qualified leads automatically extracted from WhatsApp conversations with qualification scoring"
        />

        <main className="p-8 space-y-6 flex-1 overflow-y-auto">
          {/* Filter Bar */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-sm">
            <div className="relative w-full sm:w-80">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="text"
                placeholder="Search leads by phone, name, intent..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-4 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
              />
            </div>

            <div className="flex items-center gap-1.5 overflow-x-auto text-xs">
              {["ALL", "NEW", "QUALIFIED", "CONTACTED", "CONVERTED", "LOST"].map((st) => (
                <button
                  key={st}
                  onClick={() => setStatusFilter(st)}
                  className={`px-3 py-1.5 rounded-xl font-semibold transition-colors ${
                    statusFilter === st
                      ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                      : "text-slate-400 hover:text-white hover:bg-slate-800"
                  }`}
                >
                  {st}
                </button>
              ))}
            </div>
          </div>

          {/* Leads Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {filtered.length === 0 ? (
              <div className="col-span-3 p-12 text-center text-slate-500 bg-slate-900/40 rounded-3xl border border-slate-800">
                No captured leads yet. When customers chat with the AI salesperson on WhatsApp, high-intent buyers will automatically appear here!
              </div>
            ) : (
              filtered.map((lead) => (
                <div
                  key={lead.id}
                  className="p-5 rounded-3xl bg-slate-900/80 border border-slate-800 hover:border-slate-700 transition-all shadow-xl backdrop-blur-sm flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-1.5">
                        <Flame className="w-4 h-4 text-amber-400" />
                        <span className="font-mono font-bold text-xs text-emerald-400">
                          Score: {lead.lead_score}/100
                        </span>
                      </div>
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                          lead.status === "QUALIFIED"
                            ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                            : lead.status === "CONVERTED"
                            ? "bg-teal-500/20 text-teal-300 border-teal-500/30"
                            : "bg-slate-800 text-slate-300 border-slate-700"
                        }`}
                      >
                        {lead.status}
                      </span>
                    </div>

                    <div className="mt-3">
                      <h3 className="font-bold text-sm text-white">{lead.name || "WhatsApp Inquirer"}</h3>
                      <p className="text-xs text-emerald-400 font-mono mt-0.5 flex items-center gap-1">
                        <Phone className="w-3 h-3" /> {lead.phone}
                      </p>
                    </div>

                    <div className="mt-3 p-3 rounded-2xl bg-slate-950/70 border border-slate-800/80 space-y-1.5 text-xs">
                      <div className="flex justify-between">
                        <span className="text-slate-400">Detected Intent:</span>
                        <span className="font-semibold text-slate-200">{lead.intent || "General Inquiry"}</span>
                      </div>
                      {lead.budget && (
                        <div className="flex justify-between">
                          <span className="text-slate-400">Budget:</span>
                          <span className="font-mono font-bold text-white">৳{lead.budget}</span>
                        </div>
                      )}
                      {lead.location && (
                        <div className="flex justify-between">
                          <span className="text-slate-400">Location:</span>
                          <span className="text-slate-300">{lead.location}</span>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between">
                    <span className="text-[10px] text-slate-500">
                      {new Date(lead.created_at).toLocaleDateString()}
                    </span>
                    <select
                      value={lead.status}
                      onChange={(e) => handleUpdateStatus(lead.id, e.target.value)}
                      className="bg-slate-950 border border-slate-700 text-slate-200 text-xs px-2 py-1 rounded-xl focus:outline-none"
                    >
                      <option value="NEW">NEW</option>
                      <option value="QUALIFIED">QUALIFIED</option>
                      <option value="CONTACTED">CONTACTED</option>
                      <option value="CONVERTED">CONVERTED</option>
                      <option value="LOST">LOST</option>
                    </select>
                  </div>
                </div>
              ))
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
