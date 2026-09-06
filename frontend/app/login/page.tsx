"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import { apiRequest } from "@/lib/api";
import { Sparkles, Bot, ShieldCheck, ArrowRight, CheckCircle2 } from "lucide-react";

export default function LoginPage() {
  const [email, setEmail] = useState("owner@brandstore.com");
  const [password, setPassword] = useState("SecurePassword123!");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const { login } = useAuth();
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const data = await apiRequest("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });

      login(data.access_token, data);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Failed to sign in. Please verify your credentials.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickDemoLogin = async () => {
    // Attempt registration of demo account or login
    setIsLoading(true);
    setError("");
    try {
      try {
        await apiRequest("/auth/register", {
          method: "POST",
          body: JSON.stringify({
            email: "demo@whatsappsalesai.com",
            password: "DemoPassword123!",
            full_name: "Alex Rahman",
            organization_name: "Aura Apparel",
          }),
        });
      } catch (e) {
        // already exists, proceed to login
      }

      const loginData = await apiRequest("/auth/login", {
        method: "POST",
        body: JSON.stringify({
          email: "demo@whatsappsalesai.com",
          password: "DemoPassword123!",
        }),
      });

      login(loginData.access_token, loginData);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Demo login failed");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col md:flex-row">
      {/* Left: Value Proposition & Showcase */}
      <div className="flex-1 bg-gradient-to-br from-slate-900 via-slate-950 to-emerald-950/40 p-8 md:p-16 flex flex-col justify-between border-b md:border-b-0 md:border-r border-slate-800">
        <div>
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center text-white shadow-xl shadow-emerald-500/20">
              <Sparkles className="w-6 h-6 text-emerald-100" />
            </div>
            <div>
              <span className="font-bold text-lg tracking-tight text-white">WHATSAPP SALES AI</span>
              <p className="text-xs text-emerald-400 font-medium">B2B Autonomous Sales Engine</p>
            </div>
          </div>

          <div className="mt-16 max-w-lg">
            <h1 className="text-3xl md:text-4xl font-extrabold text-white tracking-tight leading-tight">
              Turn WhatsApp conversations into <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-200">automated sales orders.</span>
            </h1>
            <p className="mt-4 text-sm text-slate-400 leading-relaxed">
              Equip your e-commerce store with an AI digital salesperson that checks real stock, recommends products, answers policies via RAG, creates orders, and escalates to human agents.
            </p>

            <div className="mt-8 space-y-3">
              {[
                "Never hallucinates prices, stock counts, or delivery times",
                "12 integrated business database tools with LangGraph",
                "Official Meta WhatsApp Cloud API + Webhook architecture",
                "Multi-tenant isolation, human handoff, and live CRM pipeline",
              ].map((feat, idx) => (
                <div key={idx} className="flex items-center gap-3 text-xs text-slate-300">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                  <span>{feat}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="pt-8 border-t border-slate-800/80 text-xs text-slate-500 flex items-center justify-between">
          <span>Enterprise Grade SaaS • 2026</span>
          <span className="flex items-center gap-1.5 text-emerald-400">
            <ShieldCheck className="w-4 h-4" /> 100% Isolated Data
          </span>
        </div>
      </div>

      {/* Right: Auth Form */}
      <div className="flex-1 flex items-center justify-center p-8 md:p-16">
        <div className="w-full max-w-md bg-slate-900/90 border border-slate-800 p-8 rounded-3xl shadow-2xl backdrop-blur-xl">
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold text-white tracking-tight">Sign In to Dashboard</h2>
            <p className="text-xs text-slate-400 mt-1">Manage your WhatsApp sales team and conversations</p>
          </div>

          {error && (
            <div className="mb-6 p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
              {error}
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="text-xs font-semibold text-slate-300">Email Address</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full mt-1.5 px-4 py-3 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-emerald-500"
                placeholder="you@company.com"
              />
            </div>

            <div>
              <div className="flex items-center justify-between">
                <label className="text-xs font-semibold text-slate-300">Password</label>
                <a href="#" className="text-xs text-emerald-400 hover:underline">Forgot?</a>
              </div>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full mt-1.5 px-4 py-3 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-emerald-500"
                placeholder="••••••••••••"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full mt-2 py-3.5 px-4 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-sm shadow-lg shadow-emerald-500/20 transition-all flex items-center justify-center gap-2 active:scale-95 disabled:opacity-50"
            >
              {isLoading ? "Signing in..." : "Sign In to Workspace"}
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          <div className="mt-4 pt-4 border-t border-slate-800">
            <button
              type="button"
              onClick={handleQuickDemoLogin}
              disabled={isLoading}
              className="w-full py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-emerald-400 font-semibold text-xs border border-emerald-500/20 transition-colors"
            >
              ✨ Instant One-Click Demo Login
            </button>
          </div>

          <div className="mt-6 text-center text-xs text-slate-400">
            Don&apos;t have an organization?{" "}
            <Link href="/register" className="text-emerald-400 hover:underline font-semibold">
              Create Account
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
