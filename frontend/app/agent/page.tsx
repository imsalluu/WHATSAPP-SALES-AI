"use client";

import React, { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import { apiRequest } from "@/lib/api";
import { Bot, Save, Sparkles, Wrench, ShieldAlert, Clock, CheckCircle2 } from "lucide-react";

export default function AgentConfigPage() {
  const [agentName, setAgentName] = useState("Sara - Sales Specialist");
  const [personality, setPersonality] = useState("Friendly, consultative and concise");
  const [tone, setTone] = useState("Enthusiastic & Professional");
  const [language, setLanguage] = useState("English & Bengali (Banglish)");
  const [greetingMessage, setGreetingMessage] = useState("Hello! Welcome to our store. How can I help you today? 🛍️");
  const [businessDescription, setBusinessDescription] = useState("Premium retail clothing & lifestyle goods.");
  const [shippingRules, setShippingRules] = useState("Inside Dhaka: ৳60 (24-48h), Outside Dhaka: ৳120 (2-4 days).");
  const [returnPolicy, setReturnPolicy] = useState("7-day easy exchange and return policy on unworn items.");
  const [isSaving, setIsSaving] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const cfg = await apiRequest("/agent-config/");
        if (cfg) {
          setAgentName(cfg.agent_name || "Sara");
          setPersonality(cfg.personality || "");
          setTone(cfg.tone || "");
          setLanguage(cfg.language || "");
          setGreetingMessage(cfg.greeting_message || "");
          setBusinessDescription(cfg.business_description || "");
          setShippingRules(cfg.shipping_rules || "");
          setReturnPolicy(cfg.return_policy || "");
        }
      } catch (e) {
        console.error(e);
      }
    };
    fetchConfig();
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setSavedSuccess(false);

    try {
      await apiRequest("/agent-config/", {
        method: "PUT",
        body: JSON.stringify({
          agent_name: agentName,
          personality,
          tone,
          language,
          greeting_message: greetingMessage,
          business_description: businessDescription,
          shipping_rules: shippingRules,
          return_policy: returnPolicy,
        }),
      });
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (e: any) {
      alert(e.message || "Failed to update configuration");
    } finally {
      setIsSaving(false);
    }
  };

  const allTools = [
    { name: "search_products", desc: "Searches inventory catalog by keywords & price filters" },
    { name: "get_product", desc: "Retrieves complete product specs & gallery" },
    { name: "check_inventory", desc: "Checks live stock for exact sizes/colors" },
    { name: "get_product_variants", desc: "Lists all available variant combinations" },
    { name: "get_order", desc: "Tracks live order status and tracking info" },
    { name: "create_order", desc: "Places confirmed orders into PostgreSQL" },
    { name: "update_order", desc: "Updates order states and cancellations" },
    { name: "calculate_shipping", desc: "Calculates delivery rate based on city" },
    { name: "get_shipping_status", desc: "Fetches courier tracking details" },
    { name: "capture_lead", desc: "Scores leads & records CRM buyer intent" },
    { name: "create_support_ticket", desc: "Logs escalated customer service issues" },
    { name: "transfer_to_human", desc: "Transfers conversation to human agents" },
  ];

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Header
          title="AI Sales Agent Persona & Tool Toggles"
          subtitle="Configure system prompt rules, brand tone, languages, and enabled business database tools"
        />

        <main className="p-8 space-y-8 flex-1 overflow-y-auto">
          <form onSubmit={handleSave} className="space-y-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Left: Persona & Tone Settings */}
              <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-4 backdrop-blur-sm">
                <h3 className="text-sm font-bold text-white flex items-center gap-2 mb-4">
                  <Bot className="w-4 h-4 text-emerald-400" />
                  <span>Sales Representative Persona</span>
                </h3>

                <div>
                  <label className="text-xs font-semibold text-slate-300">Agent Display Name</label>
                  <input
                    type="text"
                    required
                    value={agentName}
                    onChange={(e) => setAgentName(e.target.value)}
                    className="w-full mt-1.5 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-xs font-semibold text-slate-300">Tone of Voice</label>
                    <input
                      type="text"
                      value={tone}
                      onChange={(e) => setTone(e.target.value)}
                      className="w-full mt-1.5 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500"
                    />
                  </div>
                  <div>
                    <label className="text-xs font-semibold text-slate-300">Languages Supported</label>
                    <input
                      type="text"
                      value={language}
                      onChange={(e) => setLanguage(e.target.value)}
                      className="w-full mt-1.5 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500"
                    />
                  </div>
                </div>

                <div>
                  <label className="text-xs font-semibold text-slate-300">Default Welcome Greeting</label>
                  <textarea
                    rows={2}
                    value={greetingMessage}
                    onChange={(e) => setGreetingMessage(e.target.value)}
                    className="w-full mt-1.5 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500"
                  />
                </div>

                <div>
                  <label className="text-xs font-semibold text-slate-300">Business & Store Description</label>
                  <textarea
                    rows={2}
                    value={businessDescription}
                    onChange={(e) => setBusinessDescription(e.target.value)}
                    className="w-full mt-1.5 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500"
                  />
                </div>
              </div>

              {/* Right: Policies & Guardrails */}
              <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-4 backdrop-blur-sm">
                <h3 className="text-sm font-bold text-white flex items-center gap-2 mb-4">
                  <ShieldAlert className="w-4 h-4 text-emerald-400" />
                  <span>Grounding Rules & Policies</span>
                </h3>

                <div>
                  <label className="text-xs font-semibold text-slate-300">Shipping Policy in Prompt</label>
                  <textarea
                    rows={3}
                    value={shippingRules}
                    onChange={(e) => setShippingRules(e.target.value)}
                    className="w-full mt-1.5 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500"
                  />
                </div>

                <div>
                  <label className="text-xs font-semibold text-slate-300">Return & Exchange Policy</label>
                  <textarea
                    rows={3}
                    value={returnPolicy}
                    onChange={(e) => setReturnPolicy(e.target.value)}
                    className="w-full mt-1.5 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500"
                  />
                </div>

                <div className="p-4 rounded-2xl bg-emerald-950/30 border border-emerald-500/20 text-xs text-emerald-300 space-y-1">
                  <p className="font-bold flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5" /> Anti-Hallucination Guardrail Active
                  </p>
                  <p className="text-[11px] text-slate-300">
                    The agent is constrained to never fabricate inventory counts or product prices.
                  </p>
                </div>
              </div>
            </div>

            {/* 12 Enabled Business Tools Matrix */}
            <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl backdrop-blur-sm">
              <h3 className="text-sm font-bold text-white flex items-center gap-2 mb-4">
                <Wrench className="w-4 h-4 text-emerald-400" />
                <span>12 Autonomous Sales Tools Enabled</span>
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
                {allTools.map((t, idx) => (
                  <div
                    key={idx}
                    className="p-3.5 rounded-2xl bg-slate-950/80 border border-slate-800 flex items-start gap-3"
                  >
                    <div className="w-2 h-2 rounded-full bg-emerald-400 mt-1 shrink-0" />
                    <div>
                      <p className="font-mono text-xs font-bold text-emerald-300">{t.name}()</p>
                      <p className="text-[11px] text-slate-400 mt-0.5">{t.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Save Button */}
            <div className="flex items-center justify-end gap-3">
              {savedSuccess && (
                <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1">
                  <CheckCircle2 className="w-4 h-4" /> Agent configuration saved!
                </span>
              )}
              <button
                type="submit"
                disabled={isSaving}
                className="px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/20 transition-all flex items-center gap-2 active:scale-95 disabled:opacity-50"
              >
                <Save className="w-4 h-4" />
                <span>{isSaving ? "Saving..." : "Save AI Configuration"}</span>
              </button>
            </div>
          </form>
        </main>
      </div>
    </div>
  );
}
