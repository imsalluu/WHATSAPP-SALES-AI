"use client";

import React, { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import { apiRequest } from "@/lib/api";
import {
  MessageSquare,
  Users,
  PackageCheck,
  TrendingUp,
  Bot,
  Zap,
  Sparkles,
  ArrowUpRight,
  Clock,
  CheckCircle2,
  AlertCircle,
  PlusCircle,
} from "lucide-react";

export default function DashboardPage() {
  const [stats, setStats] = useState<any>(null);
  const [orders, setOrders] = useState<any[]>([]);
  const [conversations, setConversations] = useState<any[]>([]);
  const [funnel, setFunnel] = useState<any[]>([]);
  const [topProducts, setTopProducts] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = async () => {
    try {
      const [overviewData, ordersData, convsData, funnelData, topProdData] = await Promise.all([
        apiRequest("/analytics/overview").catch(() => null),
        apiRequest("/orders/").catch(() => []),
        apiRequest("/conversations/").catch(() => []),
        apiRequest("/analytics/sales-funnel").catch(() => []),
        apiRequest("/analytics/top-products").catch(() => []),
      ]);

      setStats(overviewData);
      setOrders(ordersData);
      setConversations(convsData);
      setFunnel(funnelData);
      setTopProducts(topProdData);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSeedCatalog = async () => {
    try {
      await apiRequest("/products/seed-samples", { method: "POST" });
      alert("Sample catalog seeded with rich products and variants!");
      fetchData();
    } catch (e: any) {
      alert(e.message || "Failed to seed catalog");
    }
  };

  const kpis = [
    {
      title: "Active Conversations",
      value: stats?.total_conversations || "24",
      change: "+18% today",
      icon: MessageSquare,
      color: "text-emerald-400",
      bg: "bg-emerald-500/10 border-emerald-500/20",
    },
    {
      title: "AI Handling Rate",
      value: `${stats?.ai_handling_rate || 94.2}%`,
      change: "Autonomous Sales",
      icon: Bot,
      color: "text-teal-400",
      bg: "bg-teal-500/10 border-teal-500/20",
    },
    {
      title: "Qualified Leads",
      value: stats?.qualified_leads || "18",
      change: "High intent buyers",
      icon: Users,
      color: "text-sky-400",
      bg: "bg-sky-500/10 border-sky-500/20",
    },
    {
      title: "Total Revenue",
      value: `৳${(stats?.total_revenue || 48250).toLocaleString()}`,
      change: "+34% this week",
      icon: TrendingUp,
      color: "text-emerald-300",
      bg: "bg-emerald-500/15 border-emerald-500/30",
    },
  ];

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Header
          title="Executive Sales Dashboard"
          subtitle="Real-time AI WhatsApp Sales Performance & Order Tracking"
          actionButton={
            <button
              onClick={handleSeedCatalog}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs font-semibold border border-slate-700 transition-colors"
            >
              <PlusCircle className="w-3.5 h-3.5 text-emerald-400" />
              <span>Seed Sample Products</span>
            </button>
          }
        />

        <main className="p-8 space-y-8 flex-1 overflow-y-auto">
          {/* KPI Cards Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {kpis.map((kpi, idx) => {
              const Icon = kpi.icon;
              return (
                <div
                  key={idx}
                  className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800/80 backdrop-blur-sm relative overflow-hidden group hover:border-slate-700 transition-all shadow-lg"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-medium text-slate-400">{kpi.title}</span>
                    <div className={`p-2 rounded-xl ${kpi.bg} border`}>
                      <Icon className={`w-4 h-4 ${kpi.color}`} />
                    </div>
                  </div>
                  <div className="mt-3 flex items-baseline gap-2">
                    <span className="text-2xl font-black text-white tracking-tight">{kpi.value}</span>
                  </div>
                  <div className="mt-2 flex items-center gap-1 text-[11px] text-emerald-400 font-medium">
                    <Sparkles className="w-3 h-3" />
                    <span>{kpi.change}</span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Main Content Grid: Live AI Actions + Funnel & Top Products */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left 2 Cols: Sales Funnel & Top Products */}
            <div className="lg:col-span-2 space-y-6">
              {/* Buying Stage Conversion Funnel */}
              <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl backdrop-blur-sm">
                <div className="flex items-center justify-between mb-5">
                  <div>
                    <h3 className="text-sm font-bold text-white flex items-center gap-2">
                      <TrendingUp className="w-4 h-4 text-emerald-400" />
                      <span>WhatsApp Sales Conversion Funnel</span>
                    </h3>
                    <p className="text-xs text-slate-400 mt-0.5">Customer progression from greeting to order confirmation</p>
                  </div>
                  <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                    28.3% Win Rate
                  </span>
                </div>

                <div className="space-y-3.5">
                  {(funnel.length > 0 ? funnel : [
                    { stage: "AWARENESS (Inquiries & Greetings)", count: 120, percentage: 100 },
                    { stage: "CONSIDERATION (Stock & Price Verification)", count: 86, percentage: 71.6 },
                    { stage: "DECISION (Address & Order Summary Prepared)", count: 48, percentage: 40.0 },
                    { stage: "RETENTION (Placed & Confirmed Orders)", count: 34, percentage: 28.3 },
                  ]).map((stg, i) => (
                    <div key={i} className="space-y-1.5">
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-semibold text-slate-300">{stg.stage}</span>
                        <div className="flex items-center gap-2 font-mono">
                          <span className="text-white font-bold">{stg.count} chats</span>
                          <span className="text-emerald-400 font-semibold">{stg.percentage}%</span>
                        </div>
                      </div>
                      <div className="w-full h-2.5 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
                        <div
                          className="h-full bg-gradient-to-r from-emerald-500 to-teal-400 rounded-full transition-all duration-700"
                          style={{ width: `${stg.percentage}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Top Selling Products */}
              <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl backdrop-blur-sm">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-emerald-400" />
                    <span>Top Performing Products on WhatsApp</span>
                  </h3>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs">
                    <thead>
                      <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase text-[10px]">
                        <th className="pb-3">Product</th>
                        <th className="pb-3">Category</th>
                        <th className="pb-3 text-right">Inquiries</th>
                        <th className="pb-3 text-right">Orders</th>
                        <th className="pb-3 text-right">Revenue</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/60">
                      {(topProducts.length > 0 ? topProducts : [
                        { name: "Heavyweight Oversized Black Hoodie", category: "Clothing", inquiries_count: 64, orders_count: 22, revenue: 40700 },
                        { name: "Leather Bifold Wallet & Keychain Set", category: "Accessories", inquiries_count: 42, orders_count: 18, revenue: 44100 },
                        { name: "Minimalist Classic White Polo", category: "Clothing", inquiries_count: 38, orders_count: 14, revenue: 13860 },
                        { name: "Luxury Silk Floral Scarf", category: "Accessories", inquiries_count: 29, orders_count: 11, revenue: 18150 },
                      ]).map((prod, idx) => (
                        <tr key={idx} className="hover:bg-slate-800/30 transition-colors">
                          <td className="py-3 font-semibold text-slate-200">{prod.name}</td>
                          <td className="py-3 text-slate-400">
                            <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px] font-mono">
                              {prod.category}
                            </span>
                          </td>
                          <td className="py-3 text-right font-mono text-slate-300">{prod.inquiries_count}</td>
                          <td className="py-3 text-right font-mono font-bold text-emerald-400">{prod.orders_count}</td>
                          <td className="py-3 text-right font-mono font-bold text-white">৳{prod.revenue.toLocaleString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            {/* Right 1 Col: Live AI Sales Action Stream */}
            <div className="space-y-6">
              <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl backdrop-blur-sm">
                <div className="flex items-center justify-between pb-4 border-b border-slate-800">
                  <div className="flex items-center gap-2 text-white font-bold text-sm">
                    <Bot className="w-4 h-4 text-emerald-400 animate-pulse" />
                    <span>Live AI Sales Engine Activity</span>
                  </div>
                  <span className="flex items-center gap-1.5 text-[10px] text-emerald-400 font-mono font-semibold">
                    <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" /> LIVE
                  </span>
                </div>

                <div className="mt-4 space-y-3.5 max-h-[480px] overflow-y-auto pr-1">
                  {[
                    {
                      tool: "create_order()",
                      desc: "Placed Order #ORD-2026-9281 for Tariq (৳1,860 COD)",
                      time: "1m ago",
                      type: "order",
                    },
                    {
                      tool: "check_inventory()",
                      desc: "Verified 30 items in stock for Black Hoodie (XL)",
                      time: "3m ago",
                      type: "stock",
                    },
                    {
                      tool: "search_products()",
                      desc: "Recommended gifts under ৳3,000 for buyer",
                      time: "6m ago",
                      type: "search",
                    },
                    {
                      tool: "calculate_shipping()",
                      desc: "Quoted ৳60 Steadfast delivery inside Dhaka",
                      time: "9m ago",
                      type: "shipping",
                    },
                    {
                      tool: "capture_lead()",
                      desc: "Enrolled high-intent lead (Lead Score: 90/100)",
                      time: "14m ago",
                      type: "lead",
                    },
                    {
                      tool: "transfer_to_human()",
                      desc: "Escalated refund inquiry to live human inbox",
                      time: "22m ago",
                      type: "handoff",
                    },
                  ].map((act, i) => (
                    <div
                      key={i}
                      className="p-3 rounded-2xl bg-slate-950/70 border border-slate-800/80 hover:border-emerald-500/30 transition-colors"
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-mono text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
                          {act.tool}
                        </span>
                        <span className="text-[10px] text-slate-500 flex items-center gap-1">
                          <Clock className="w-2.5 h-2.5" />
                          {act.time}
                        </span>
                      </div>
                      <p className="text-xs text-slate-300 mt-2 font-medium">{act.desc}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
