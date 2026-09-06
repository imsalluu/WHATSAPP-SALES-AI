"use client";

import React, { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import { apiRequest } from "@/lib/api";
import { Smartphone, CheckCircle2, Copy, Send, Sparkles, Shield, Key } from "lucide-react";

export default function WhatsAppSetupPage() {
  const [phoneNumberId, setPhoneNumberId] = useState("");
  const [wabaId, setWabaId] = useState("");
  const [displayPhone, setDisplayPhone] = useState("+880 1711-223344");
  const [accessToken, setAccessToken] = useState("");
  const [verifyToken, setVerifyToken] = useState("sales_ai_webhook_verify_secret");
  const [isSaving, setIsSaving] = useState(false);
  const [testRecipient, setTestRecipient] = useState("+8801711223344");
  const [testMessage, setTestMessage] = useState("Hello! This is a test message from WhatsApp Sales AI.");
  const [testResult, setTestResult] = useState<any>(null);

  useEffect(() => {
    const fetchAccount = async () => {
      try {
        const acc = await apiRequest("/whatsapp/account");
        if (acc) {
          setPhoneNumberId(acc.phone_number_id || "");
          setWabaId(acc.waba_id || "");
          setDisplayPhone(acc.display_phone_number || "+880 1800-SALESAI");
          setVerifyToken(acc.webhook_verify_token || "sales_ai_webhook_verify_secret");
        }
      } catch (e) {
        console.error(e);
      }
    };
    fetchAccount();
  }, []);

  const handleConnect = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    try {
      await apiRequest("/whatsapp/connect", {
        method: "POST",
        body: JSON.stringify({
          phone_number_id: phoneNumberId,
          waba_id: wabaId,
          display_phone_number: displayPhone,
          access_token: accessToken,
          webhook_verify_token: verifyToken,
        }),
      });
      alert("WhatsApp Business account credentials saved successfully!");
    } catch (e: any) {
      alert(e.message || "Failed to connect account");
    } finally {
      setIsSaving(false);
    }
  };

  const handleSendTestMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await apiRequest("/whatsapp/test-message", {
        method: "POST",
        body: JSON.stringify({
          recipient_phone: testRecipient,
          message: testMessage,
        }),
      });
      setTestResult(res);
    } catch (e: any) {
      alert(e.message || "Test message failed");
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    alert("Copied to clipboard!");
  };

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Header
          title="Meta WhatsApp Cloud API Configuration"
          subtitle="Connect your official Meta WhatsApp Business API account or use the built-in Sandbox Simulator"
        />

        <main className="p-8 space-y-8 flex-1 overflow-y-auto">
          {/* Connection Status Banner */}
          <div className="p-6 rounded-3xl bg-gradient-to-r from-emerald-950/60 via-slate-900 to-slate-900 border border-emerald-500/30 flex flex-col md:flex-row items-center justify-between gap-4 shadow-xl">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-2xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center justify-center shrink-0">
                <Smartphone className="w-6 h-6" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-base font-bold text-white">{displayPhone}</h3>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-semibold">
                    CONNECTED
                  </span>
                </div>
                <p className="text-xs text-slate-400 mt-0.5">
                  Ready to process incoming customer orders autonomously over WhatsApp.
                </p>
              </div>
            </div>

            <div className="text-xs text-slate-300 bg-slate-950/80 px-4 py-2 rounded-xl border border-slate-800 font-mono">
              API Version: v20.0
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Left: Meta API Credentials Form */}
            <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-4 backdrop-blur-sm">
              <h3 className="text-sm font-bold text-white flex items-center gap-2 mb-4">
                <Key className="w-4 h-4 text-emerald-400" />
                <span>Meta Developer Credentials</span>
              </h3>

              <form onSubmit={handleConnect} className="space-y-4">
                <div>
                  <label className="text-xs font-semibold text-slate-300">Phone Number ID</label>
                  <input
                    type="text"
                    value={phoneNumberId}
                    onChange={(e) => setPhoneNumberId(e.target.value)}
                    placeholder="e.g. 109823471928347"
                    className="w-full mt-1.5 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white font-mono focus:outline-none focus:border-emerald-500"
                  />
                </div>

                <div>
                  <label className="text-xs font-semibold text-slate-300">WhatsApp Business Account ID (WABA)</label>
                  <input
                    type="text"
                    value={wabaId}
                    onChange={(e) => setWabaId(e.target.value)}
                    placeholder="e.g. 102938475619283"
                    className="w-full mt-1.5 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white font-mono focus:outline-none focus:border-emerald-500"
                  />
                </div>

                <div>
                  <label className="text-xs font-semibold text-slate-300">Permanent System User Access Token</label>
                  <input
                    type="password"
                    value={accessToken}
                    onChange={(e) => setAccessToken(e.target.value)}
                    placeholder="EAAG..."
                    className="w-full mt-1.5 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white font-mono focus:outline-none focus:border-emerald-500"
                  />
                </div>

                <button
                  type="submit"
                  disabled={isSaving}
                  className="w-full py-3 px-4 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/20 transition-all active:scale-95 disabled:opacity-50"
                >
                  {isSaving ? "Saving..." : "Save Meta Cloud API Credentials"}
                </button>
              </form>
            </div>

            {/* Right: Webhook Setup Instructions & Outbound Test */}
            <div className="space-y-6">
              <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-4 backdrop-blur-sm">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <Shield className="w-4 h-4 text-emerald-400" />
                  <span>Meta Webhook Configuration</span>
                </h3>

                <div className="space-y-3">
                  <div>
                    <label className="text-[10px] font-semibold text-slate-400 uppercase">Callback URL</label>
                    <div className="mt-1 flex items-center gap-2">
                      <input
                        type="text"
                        readOnly
                        value="https://your-domain.com/api/v1/whatsapp/webhook"
                        className="flex-1 px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-300 font-mono"
                      />
                      <button
                        onClick={() => copyToClipboard("https://your-domain.com/api/v1/whatsapp/webhook")}
                        className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300"
                      >
                        <Copy className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  <div>
                    <label className="text-[10px] font-semibold text-slate-400 uppercase">Verify Token</label>
                    <div className="mt-1 flex items-center gap-2">
                      <input
                        type="text"
                        readOnly
                        value={verifyToken}
                        className="flex-1 px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-300 font-mono"
                      />
                      <button
                        onClick={() => copyToClipboard(verifyToken)}
                        className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300"
                      >
                        <Copy className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              {/* Test Outbound WhatsApp Message */}
              <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-3 backdrop-blur-sm">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <Send className="w-4 h-4 text-emerald-400" />
                  <span>Send Outbound Test Message</span>
                </h3>

                <form onSubmit={handleSendTestMessage} className="space-y-3">
                  <input
                    type="text"
                    value={testRecipient}
                    onChange={(e) => setTestRecipient(e.target.value)}
                    placeholder="Recipient Phone (+880...)"
                    className="w-full px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white font-mono focus:outline-none focus:border-emerald-500"
                  />
                  <input
                    type="text"
                    value={testMessage}
                    onChange={(e) => setTestMessage(e.target.value)}
                    placeholder="Message..."
                    className="w-full px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500"
                  />
                  <button
                    type="submit"
                    className="w-full py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-emerald-400 text-xs font-bold border border-slate-700 transition-colors"
                  >
                    Dispatch Test Message
                  </button>
                </form>

                {testResult && (
                  <div className="p-3 rounded-xl bg-slate-950 border border-emerald-500/30 text-[11px] font-mono text-emerald-300">
                    {JSON.stringify(testResult, null, 2)}
                  </div>
                )}
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
