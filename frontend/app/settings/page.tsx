"use client";

import React, { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import { apiRequest } from "@/lib/api";
import { Settings, Users, Shield, CreditCard, Sparkles, Check, Key } from "lucide-react";

export default function SettingsPage() {
  const [org, setOrg] = useState<any>(null);
  const [members, setMembers] = useState<any[]>([]);
  const [orgName, setOrgName] = useState("");
  const [currency, setCurrency] = useState("BDT");
  const [timezone, setTimezone] = useState("Asia/Dhaka");
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    const fetchOrgData = async () => {
      try {
        const [orgData, membersData] = await Promise.all([
          apiRequest("/organizations/current"),
          apiRequest("/organizations/members"),
        ]);
        setOrg(orgData);
        setOrgName(orgData.name || "");
        setCurrency(orgData.currency || "BDT");
        setTimezone(orgData.timezone || "Asia/Dhaka");
        setMembers(membersData || []);
      } catch (e) {
        console.error(e);
      }
    };
    fetchOrgData();
  }, []);

  const handleSaveOrg = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    try {
      await apiRequest("/organizations/current", {
        method: "PATCH",
        body: JSON.stringify({ name: orgName, currency, timezone }),
      });
      alert("Organization profile updated!");
    } catch (e: any) {
      alert(e.message || "Failed to update organization");
    } finally {
      setIsSaving(false);
    }
  };

  const plans = [
    { name: "Free", price: "৳0", convs: "100 chats/mo", agents: "1 Agent", current: false },
    { name: "Starter", price: "৳2,500/mo", convs: "1,500 chats/mo", agents: "3 Agents", current: true },
    { name: "Business", price: "৳7,000/mo", convs: "10,000 chats/mo", agents: "10 Agents", current: false },
    { name: "Agency", price: "৳18,000/mo", convs: "Unlimited chats", agents: "Unlimited", current: false },
  ];

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Header
          title="Organization Settings & Team Members"
          subtitle="Manage workspace parameters, role-based access control (RBAC), and subscription tiers"
        />

        <main className="p-8 space-y-8 flex-1 overflow-y-auto">
          {/* Organization Profile */}
          <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl backdrop-blur-sm">
            <h3 className="text-sm font-bold text-white flex items-center gap-2 mb-4">
              <Settings className="w-4 h-4 text-emerald-400" />
              <span>Workspace Details</span>
            </h3>

            <form onSubmit={handleSaveOrg} className="space-y-4 max-w-2xl">
              <div>
                <label className="text-xs font-semibold text-slate-300">Organization / Store Name</label>
                <input
                  type="text"
                  required
                  value={orgName}
                  onChange={(e) => setOrgName(e.target.value)}
                  className="w-full mt-1.5 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-semibold text-slate-300">Base Currency</label>
                  <select
                    value={currency}
                    onChange={(e) => setCurrency(e.target.value)}
                    className="w-full mt-1.5 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                  >
                    <option value="BDT">BDT (৳) - Bangladeshi Taka</option>
                    <option value="USD">USD ($) - US Dollar</option>
                    <option value="EUR">EUR (€) - Euro</option>
                    <option value="GBP">GBP (£) - British Pound</option>
                  </select>
                </div>
                <div>
                  <label className="text-xs font-semibold text-slate-300">Timezone</label>
                  <select
                    value={timezone}
                    onChange={(e) => setTimezone(e.target.value)}
                    className="w-full mt-1.5 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                  >
                    <option value="Asia/Dhaka">Asia/Dhaka (GMT+6)</option>
                    <option value="Asia/Dubai">Asia/Dubai (GMT+4)</option>
                    <option value="UTC">UTC (GMT+0)</option>
                    <option value="America/New_York">America/New_York (EST)</option>
                  </select>
                </div>
              </div>

              <button
                type="submit"
                disabled={isSaving}
                className="px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow transition-all disabled:opacity-50"
              >
                {isSaving ? "Saving..." : "Save Workspace Changes"}
              </button>
            </form>
          </div>

          {/* Team Members & RBAC */}
          <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl backdrop-blur-sm">
            <h3 className="text-sm font-bold text-white flex items-center gap-2 mb-4">
              <Users className="w-4 h-4 text-emerald-400" />
              <span>Team Members & Role-Based Access Control</span>
            </h3>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase text-[10px]">
                    <th className="pb-3">Name</th>
                    <th className="pb-3">Email</th>
                    <th className="pb-3">Role</th>
                    <th className="pb-3">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {members.map((mem) => (
                    <tr key={mem.id} className="hover:bg-slate-800/30">
                      <td className="py-3 font-semibold text-white">{mem.user.full_name}</td>
                      <td className="py-3 text-slate-400 font-mono">{mem.user.email}</td>
                      <td className="py-3">
                        <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 font-mono text-[10px] font-bold border border-emerald-500/20">
                          {mem.role}
                        </span>
                      </td>
                      <td className="py-3 text-emerald-400 font-semibold">Active</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Subscription Tier Cards */}
          <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl backdrop-blur-sm">
            <h3 className="text-sm font-bold text-white flex items-center gap-2 mb-4">
              <CreditCard className="w-4 h-4 text-emerald-400" />
              <span>SaaS Subscription Plan</span>
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {plans.map((p, idx) => (
                <div
                  key={idx}
                  className={`p-5 rounded-2xl border flex flex-col justify-between ${
                    p.current
                      ? "bg-gradient-to-b from-emerald-950/40 to-slate-900 border-emerald-500 shadow-lg shadow-emerald-500/10"
                      : "bg-slate-950 border-slate-800"
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-sm text-white">{p.name}</span>
                      {p.current && (
                        <span className="text-[9px] px-2 py-0.5 rounded-full bg-emerald-500 text-slate-950 font-bold">
                          Active Plan
                        </span>
                      )}
                    </div>
                    <div className="mt-3 text-2xl font-black text-white font-mono">{p.price}</div>
                    <div className="mt-4 space-y-1.5 text-xs text-slate-300">
                      <div>• {p.convs}</div>
                      <div>• {p.agents}</div>
                      <div>• Full Tool Calling</div>
                      <div>• pgvector RAG</div>
                    </div>
                  </div>
                  <button
                    disabled={p.current}
                    className={`w-full mt-6 py-2 rounded-xl text-xs font-bold transition-all ${
                      p.current
                        ? "bg-slate-800 text-slate-400 cursor-default"
                        : "bg-emerald-500 hover:bg-emerald-400 text-slate-950"
                    }`}
                  >
                    {p.current ? "Current Plan" : "Upgrade Plan"}
                  </button>
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
