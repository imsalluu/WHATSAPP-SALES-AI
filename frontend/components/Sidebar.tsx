"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import {
  MessageSquare,
  LayoutDashboard,
  ShoppingBag,
  PackageCheck,
  Users,
  BrainCircuit,
  Bot,
  BarChart3,
  Smartphone,
  Settings,
  LogOut,
  Sparkles,
  Zap,
} from "lucide-react";

export default function Sidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  const navItems = [
    { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { href: "/conversations", label: "Conversations", icon: MessageSquare, badge: "AI Live" },
    { href: "/products", label: "Product Catalog", icon: ShoppingBag },
    { href: "/orders", label: "Orders", icon: PackageCheck },
    { href: "/leads", label: "Leads & CRM", icon: Users },
    { href: "/knowledge", label: "RAG Knowledge", icon: BrainCircuit },
    { href: "/agent", label: "AI Agent Config", icon: Bot },
    { href: "/analytics", label: "AI Intelligence", icon: BarChart3 },
    { href: "/whatsapp", label: "WhatsApp Setup", icon: Smartphone },
    { href: "/settings", label: "Settings & Team", icon: Settings },
  ];

  return (
    <aside className="w-64 bg-slate-950/80 backdrop-blur-xl border-r border-slate-800/80 flex flex-col h-screen sticky top-0 select-none z-30">
      {/* Brand Header */}
      <div className="p-5 border-b border-slate-800/80 flex items-center justify-between">
        <Link href="/dashboard" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center text-white shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition-transform">
            <Sparkles className="w-5 h-5 text-emerald-100" />
          </div>
          <div>
            <div className="font-bold text-base tracking-tight text-white flex items-center gap-1.5">
              <span>SALES AI</span>
              <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-semibold">
                PRO
              </span>
            </div>
            <p className="text-xs text-slate-400 font-medium">WhatsApp SaaS</p>
          </div>
        </Link>
      </div>

      {/* Organization Badge */}
      <div className="px-4 py-3 mx-3 mt-3 rounded-xl bg-slate-900/90 border border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-2.5 overflow-hidden">
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse shrink-0" />
          <div className="overflow-hidden">
            <p className="text-xs font-semibold text-slate-200 truncate">
              {user?.organization_name || "Demo Business"}
            </p>
            <p className="text-[10px] text-slate-400 uppercase font-mono">
              {user?.role || "OWNER"}
            </p>
          </div>
        </div>
        <span className="text-[10px] px-2 py-0.5 bg-teal-500/10 text-teal-400 rounded-full font-medium border border-teal-500/20">
          Online
        </span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
        {navItems.map((item) => {
          const isActive = pathname === item.href || (item.href !== "/dashboard" && pathname.startsWith(item.href));
          const Icon = item.icon;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-medium transition-all ${
                isActive
                  ? "bg-gradient-to-r from-emerald-500/20 to-teal-500/10 text-emerald-300 border border-emerald-500/30 shadow-sm"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/60"
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`w-4 h-4 ${isActive ? "text-emerald-400" : "text-slate-400"}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className="text-[9px] font-semibold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                  {item.badge}
                </span>
              )}
            </Link>
          );
        })}
      </nav>

      {/* User Profile & Logout */}
      <div className="p-4 border-t border-slate-800/80 bg-slate-950/60 flex items-center justify-between">
        <div className="flex items-center gap-2.5 overflow-hidden">
          <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center font-bold text-xs text-emerald-400 shrink-0">
            {user?.full_name ? user.full_name[0].toUpperCase() : "U"}
          </div>
          <div className="overflow-hidden">
            <p className="text-xs font-medium text-slate-200 truncate">{user?.full_name || "Sales User"}</p>
            <p className="text-[10px] text-slate-500 truncate">{user?.email || "user@salesai.com"}</p>
          </div>
        </div>
        <button
          onClick={logout}
          title="Sign out"
          className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition-colors"
        >
          <LogOut className="w-4 h-4" />
        </button>
      </div>
    </aside>
  );
}
