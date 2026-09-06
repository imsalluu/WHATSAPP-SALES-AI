"use client";

import React, { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import { apiRequest } from "@/lib/api";
import { BarChart3, TrendingUp, Sparkles, MessageSquare, Bot, ShieldCheck, Zap } from "lucide-react";

export default function AnalyticsPage() {
  const [overview, setOverview] = useState<any>(null);
  const [funnel, setFunnel] = useState<any[]>([]);
  const [objections, setObjections] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [ov, fn, obj] = await Promise.all([
          apiRequest("/analytics/overview"),
          apiRequest("/analytics/sales-funnel"),
          apiRequest("/analytics/objections"),
        ]);
        setOverview(ov);
        setFunnel(fn);
        setObjections(obj);
      } catch (e) {
        console.error(e);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Header
          title="AI Sales Intelligence & Funnel Analytics"
          subtitle="Customer objection breakdowns, conversion rates, and sales agent performance"
        />

        <main className="p-8 space-y-8 flex-1 overflow-y-auto">
          {/* Key Metric Gauges */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
            <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl backdrop-blur-sm">
              <span className="text-xs text-slate-400 font-medium">Average Response Latency</span>
              <div className="mt-2 text-3xl font-black text-white font-mono">1.2s</div>
              <p className="mt-1 text-[11px] text-emerald-400">⚡ 10x faster than manual human response</p>
            </div>

            <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl backdrop-blur-sm">
              <span className="text-xs text-slate-400 font-medium">AI Autonomous Resolution</span>
              <div className="mt-2 text-3xl font-black text-emerald-400 font-mono">94.2%</div>
              <p className="mt-1 text-[11px] text-slate-400">Only 5.8% requires human agent takeover</p>
            </div>

            <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl backdrop-blur-sm">
              <span className="text-xs text-slate-400 font-medium">Average Order Value (AOV)</span>
              <div className="mt-2 text-3xl font-black text-teal-300 font-mono">৳1,856</div>
              <p className="mt-1 text-[11px] text-emerald-400">+15% lift via cross-selling & upselling</p>
            </div>
          </div>

          {/* Customer Objections Analysis */}
          <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl backdrop-blur-sm">
            <h3 className="text-sm font-bold text-white flex items-center gap-2 mb-1">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>Customer Objections & Resolution Rates</span>
            </h3>
            <p className="text-xs text-slate-400 mb-5">
              Identified friction points during customer purchase journeys and how effectively the AI salesperson resolved them.
            </p>

            <div className="space-y-4">
              {(objections.length > 0 ? objections : [
                { objection: "Delivery time & charge outside Dhaka", count: 34, resolved_percentage: 88.2 },
                { objection: "Price discount request / budget negotiation", count: 29, resolved_percentage: 75.8 },
                { objection: "Fabric / quality / sizing assurance", count: 22, resolved_percentage: 90.9 },
                { objection: "Return / exchange policy guarantee", count: 16, resolved_percentage: 93.7 },
              ]).map((item, idx) => (
                <div key={idx} className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800/80 space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-slate-200">{item.objection}</span>
                    <div className="flex items-center gap-3 font-mono">
                      <span className="text-slate-400">{item.count} occurrences</span>
                      <span className="text-emerald-400 font-bold">{item.resolved_percentage}% Resolved</span>
                    </div>
                  </div>
                  <div className="w-full h-2 bg-slate-900 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-teal-400 to-emerald-500 rounded-full"
                      style={{ width: `${item.resolved_percentage}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
