"use client";

import React, { useState } from "react";
import { Sparkles, Smartphone, Bell, Search } from "lucide-react";
import WhatsAppSimulatorModal from "./WhatsAppSimulatorModal";

interface HeaderProps {
  title: string;
  subtitle?: string;
  actionButton?: React.ReactNode;
}

export default function Header({ title, subtitle, actionButton }: HeaderProps) {
  const [isSimulatorOpen, setIsSimulatorOpen] = useState(false);

  return (
    <>
      <header className="px-8 py-5 border-b border-slate-800/80 bg-slate-950/40 backdrop-blur-md flex items-center justify-between sticky top-0 z-20">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
            {title}
          </h1>
          {subtitle && <p className="text-xs text-slate-400 mt-0.5">{subtitle}</p>}
        </div>

        <div className="flex items-center gap-3">
          {/* WhatsApp Live Simulator Button */}
          <button
            onClick={() => setIsSimulatorOpen(true)}
            className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 text-white font-semibold text-xs shadow-lg shadow-emerald-500/20 transition-all active:scale-95"
          >
            <Smartphone className="w-4 h-4 text-emerald-100 animate-bounce" />
            <span>Open WhatsApp Simulator</span>
          </button>

          {actionButton}

          <div className="h-5 w-px bg-slate-800 mx-1" />

          {/* Notification Icon */}
          <button className="p-2 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-900 border border-slate-800/80 relative transition-colors">
            <Bell className="w-4 h-4" />
            <span className="w-2 h-2 rounded-full bg-emerald-500 absolute top-1.5 right-1.5 ring-2 ring-slate-950" />
          </button>
        </div>
      </header>

      {/* Embedded WhatsApp Mobile Simulator Modal */}
      {isSimulatorOpen && (
        <WhatsAppSimulatorModal onClose={() => setIsSimulatorOpen(false)} />
      )}
    </>
  );
}
