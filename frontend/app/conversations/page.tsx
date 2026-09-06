"use client";

import React, { useEffect, useState, useRef } from "react";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import { apiRequest } from "@/lib/api";
import {
  MessageSquare,
  Bot,
  UserCheck,
  CheckCircle2,
  AlertTriangle,
  Send,
  Sparkles,
  Phone,
  User,
  ShoppingBag,
  ArrowRight,
  ShieldAlert,
  Wrench,
  Search,
  CheckCheck,
} from "lucide-react";

export default function ConversationsPage() {
  const [conversations, setConversations] = useState<any[]>([]);
  const [selectedConv, setSelectedConv] = useState<any | null>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [replyText, setReplyText] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isSending, setIsSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const fetchConversations = async () => {
    try {
      const data = await apiRequest("/conversations/");
      setConversations(data);
      if (data.length > 0 && !selectedConv) {
        selectConversation(data[0]);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  const selectConversation = async (conv: any) => {
    setSelectedConv(conv);
    try {
      const detail = await apiRequest(`/conversations/${conv.id}`);
      setMessages(detail.messages || []);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchConversations();
    const interval = setInterval(fetchConversations, 5000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleTakeover = async () => {
    if (!selectedConv) return;
    try {
      await apiRequest(`/conversations/${selectedConv.id}/takeover`, { method: "POST" });
      selectedConv.status = "HUMAN_ACTIVE";
      fetchConversations();
      selectConversation(selectedConv);
    } catch (e: any) {
      alert(e.message || "Failed to takeover");
    }
  };

  const handleReleaseToAI = async () => {
    if (!selectedConv) return;
    try {
      await apiRequest(`/conversations/${selectedConv.id}/release`, { method: "POST" });
      selectedConv.status = "AI_ACTIVE";
      fetchConversations();
      selectConversation(selectedConv);
    } catch (e: any) {
      alert(e.message || "Failed to release");
    }
  };

  const handleSendHumanReply = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!replyText.trim() || !selectedConv || isSending) return;

    setIsSending(true);
    try {
      const sentMsg = await apiRequest(`/conversations/${selectedConv.id}/messages`, {
        method: "POST",
        body: JSON.stringify({ content: replyText }),
      });
      setMessages((prev) => [...prev, sentMsg]);
      setReplyText("");
      fetchConversations();
    } catch (e: any) {
      alert(e.message || "Failed to send message");
    } finally {
      setIsSending(false);
    }
  };

  const filteredConversations = conversations.filter((c) => {
    if (statusFilter !== "ALL" && c.status !== statusFilter) return false;
    if (searchTerm) {
      const phone = c.customer?.phone_number || "";
      const name = c.customer?.name || "";
      return phone.includes(searchTerm) || name.toLowerCase().includes(searchTerm.toLowerCase());
    }
    return true;
  });

  return (
    <div className="flex h-screen bg-slate-950 overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Header
          title="WhatsApp Live Inbox"
          subtitle="Real-time multi-agent conversation management & human-in-the-loop takeover"
        />

        <div className="flex-1 flex overflow-hidden">
          {/* Left Pane: Conversations List */}
          <div className="w-80 border-r border-slate-800/80 bg-slate-950 flex flex-col">
            {/* Search & Filter Bar */}
            <div className="p-3.5 border-b border-slate-800/80 space-y-2.5">
              <div className="relative">
                <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-3" />
                <input
                  type="text"
                  placeholder="Search phone or name..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
                />
              </div>

              {/* Status Filter Tabs */}
              <div className="flex items-center gap-1 overflow-x-auto pb-1 text-[11px]">
                {["ALL", "AI_ACTIVE", "HUMAN_REQUIRED", "HUMAN_ACTIVE"].map((st) => (
                  <button
                    key={st}
                    onClick={() => setStatusFilter(st)}
                    className={`px-2.5 py-1 rounded-lg font-medium whitespace-nowrap transition-colors ${
                      statusFilter === st
                        ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                        : "text-slate-400 hover:text-slate-200 hover:bg-slate-900"
                    }`}
                  >
                    {st.replace("_", " ")}
                  </button>
                ))}
              </div>
            </div>

            {/* Conversation Threads */}
            <div className="flex-1 overflow-y-auto divide-y divide-slate-900">
              {filteredConversations.length === 0 ? (
                <div className="p-8 text-center text-xs text-slate-500">
                  <p>No conversations in this view.</p>
                  <p className="mt-1 text-[11px] text-emerald-400">
                    Use &ldquo;Open WhatsApp Simulator&rdquo; in the header to simulate live chats!
                  </p>
                </div>
              ) : (
                filteredConversations.map((c) => {
                  const isSelected = selectedConv?.id === c.id;
                  const isEscalated = c.status === "HUMAN_REQUIRED";

                  return (
                    <div
                      key={c.id}
                      onClick={() => selectConversation(c)}
                      className={`p-3.5 cursor-pointer transition-colors ${
                        isSelected ? "bg-slate-900 border-l-2 border-emerald-500" : "hover:bg-slate-900/50"
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-xs text-white truncate">
                          {c.customer?.name || c.customer?.phone_number || "Customer"}
                        </span>
                        <span className="text-[10px] text-slate-500 font-mono">
                          {new Date(c.last_message_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                        </span>
                      </div>

                      <div className="flex items-center justify-between mt-1">
                        <span className="text-[11px] text-slate-400 font-mono truncate">
                          {c.customer?.phone_number}
                        </span>

                        {isEscalated ? (
                          <span className="text-[9px] font-bold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40 flex items-center gap-1">
                            <AlertTriangle className="w-2.5 h-2.5" /> Human Req
                          </span>
                        ) : c.status === "HUMAN_ACTIVE" ? (
                          <span className="text-[9px] font-bold px-1.5 py-0.5 rounded bg-sky-500/20 text-sky-300 border border-sky-500/40">
                            Human Active
                          </span>
                        ) : (
                          <span className="text-[9px] font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 flex items-center gap-1">
                            <Bot className="w-2.5 h-2.5" /> AI Active
                          </span>
                        )}
                      </div>

                      {c.last_message && (
                        <p className="text-[11px] text-slate-400 mt-1.5 truncate">
                          {c.last_message.sender_type === "AI" ? "🤖 " : ""}
                          {c.last_message.content}
                        </p>
                      )}
                    </div>
                  );
                })
              )}
            </div>
          </div>

          {/* Center Pane: Active WhatsApp Message Thread */}
          <div className="flex-1 flex flex-col bg-[#0b141a] relative">
            {selectedConv ? (
              <>
                {/* Conversation Header & Human Takeover Controls */}
                <div className="p-3.5 bg-[#202c33] border-b border-[#2a3942] flex items-center justify-between text-white shadow-sm">
                  <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-full bg-slate-700 flex items-center justify-center font-bold text-xs text-white">
                      {selectedConv.customer?.name ? selectedConv.customer.name[0] : "C"}
                    </div>
                    <div>
                      <div className="font-semibold text-xs flex items-center gap-2">
                        <span>{selectedConv.customer?.name || "Customer"}</span>
                        <span className="text-[11px] font-mono text-emerald-400">
                          {selectedConv.customer?.phone_number}
                        </span>
                      </div>
                      <p className="text-[10px] text-slate-400">
                        Buying Stage: <span className="font-semibold text-emerald-300">{selectedConv.buying_stage}</span>
                      </p>
                    </div>
                  </div>

                  {/* Takeover Actions */}
                  <div className="flex items-center gap-2">
                    {selectedConv.status === "AI_ACTIVE" || selectedConv.status === "HUMAN_REQUIRED" ? (
                      <button
                        onClick={handleTakeover}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs shadow transition-transform active:scale-95"
                      >
                        <UserCheck className="w-3.5 h-3.5" />
                        <span>Takeover Chat</span>
                      </button>
                    ) : (
                      <button
                        onClick={handleReleaseToAI}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow transition-transform active:scale-95"
                      >
                        <Bot className="w-3.5 h-3.5" />
                        <span>Release to AI Agent</span>
                      </button>
                    )}
                  </div>
                </div>

                {/* Messages Thread */}
                <div
                  className="flex-1 overflow-y-auto p-4 space-y-3.5"
                  style={{
                    backgroundImage: "radial-gradient(#1f2c34 1px, transparent 1px)",
                    backgroundSize: "20px 20px",
                  }}
                >
                  {messages.map((m) => {
                    const isCustomer = m.sender_type === "CUSTOMER";
                    const isAI = m.sender_type === "AI";
                    const isSystem = m.sender_type === "SYSTEM";

                    if (isSystem) {
                      return (
                        <div key={m.id} className="flex justify-center">
                          <span className="text-[10px] px-3 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                            {m.content}
                          </span>
                        </div>
                      );
                    }

                    return (
                      <div
                        key={m.id}
                        className={`flex flex-col ${isCustomer ? "items-start" : "items-end"}`}
                      >
                        {/* Tool Executions Pill */}
                        {m.tool_calls && m.tool_calls.length > 0 && (
                          <div className="mb-1 flex flex-wrap gap-1">
                            {m.tool_calls.map((t: any, idx: number) => (
                              <span
                                key={idx}
                                className="inline-flex items-center gap-1 text-[9px] font-mono px-2 py-0.5 rounded bg-emerald-950/90 text-emerald-300 border border-emerald-600/40"
                              >
                                <Wrench className="w-2.5 h-2.5" />
                                {t.tool}()
                              </span>
                            ))}
                          </div>
                        )}

                        <div
                          className={`max-w-[75%] p-3 rounded-2xl text-xs whitespace-pre-line leading-relaxed shadow ${
                            isCustomer
                              ? "bg-[#202c33] text-slate-100 rounded-tl-none border border-[#2a3942]"
                              : isAI
                              ? "bg-[#005c4b] text-emerald-50 rounded-tr-none"
                              : "bg-sky-900 text-sky-50 rounded-tr-none"
                          }`}
                        >
                          {!isCustomer && (
                            <div className="text-[9px] font-bold text-emerald-300 mb-1 flex items-center gap-1">
                              {isAI ? <Bot className="w-3 h-3" /> : <User className="w-3 h-3" />}
                              {isAI ? "AI Sales Representative" : "Human Agent (You)"}
                            </div>
                          )}
                          {m.content}
                          <div className="flex items-center justify-end gap-1 mt-1 text-[9px] text-slate-400">
                            <span>
                              {new Date(m.created_at).toLocaleTimeString([], {
                                hour: "2-digit",
                                minute: "2-digit",
                              })}
                            </span>
                            {!isCustomer && <CheckCheck className="w-3 h-3 text-sky-400" />}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                  <div ref={messagesEndRef} />
                </div>

                {/* Reply Bar (for human agent takeover) */}
                <form
                  onSubmit={handleSendHumanReply}
                  className="p-3 bg-[#202c33] border-t border-[#2a3942] flex items-center gap-2"
                >
                  <input
                    type="text"
                    placeholder={
                      selectedConv.status === "AI_ACTIVE"
                        ? "AI is responding autonomously. Click 'Takeover Chat' above to message directly..."
                        : "Type reply as human agent..."
                    }
                    value={replyText}
                    onChange={(e) => setReplyText(e.target.value)}
                    disabled={selectedConv.status === "AI_ACTIVE" || isSending}
                    className="flex-1 bg-[#2a3942] text-white placeholder-slate-400 text-xs px-4 py-2.5 rounded-2xl focus:outline-none focus:ring-1 focus:ring-emerald-500 disabled:opacity-50"
                  />
                  <button
                    type="submit"
                    disabled={selectedConv.status === "AI_ACTIVE" || !replyText.trim() || isSending}
                    className="w-10 h-10 rounded-full bg-[#00a884] hover:bg-[#008f6f] disabled:opacity-50 text-white flex items-center justify-center shadow transition-transform active:scale-95"
                  >
                    <Send className="w-4 h-4" />
                  </button>
                </form>
              </>
            ) : (
              <div className="flex-1 flex items-center justify-center text-xs text-slate-500">
                Select a conversation to view chat history
              </div>
            )}
          </div>

          {/* Right Pane: Customer CRM & Order State Inspector */}
          {selectedConv && (
            <div className="w-72 bg-slate-950 border-l border-slate-800/80 p-5 flex flex-col justify-between overflow-y-auto">
              <div className="space-y-5">
                <div>
                  <h4 className="text-xs font-bold text-white uppercase tracking-wider">Customer Profile</h4>
                  <div className="mt-3 p-3 rounded-2xl bg-slate-900 border border-slate-800 space-y-2">
                    <div>
                      <p className="text-[10px] text-slate-400">Name</p>
                      <p className="text-xs font-semibold text-white">{selectedConv.customer?.name || "N/A"}</p>
                    </div>
                    <div>
                      <p className="text-[10px] text-slate-400">Phone</p>
                      <p className="text-xs font-mono text-emerald-400 font-semibold">{selectedConv.customer?.phone_number}</p>
                    </div>
                    <div>
                      <p className="text-[10px] text-slate-400">Delivery Address</p>
                      <p className="text-xs text-slate-300">{selectedConv.customer?.address || "Pending collection"}</p>
                    </div>
                  </div>
                </div>

                {/* Lead Score Gauge */}
                <div>
                  <h4 className="text-xs font-bold text-white uppercase tracking-wider">AI Lead Score</h4>
                  <div className="mt-3 p-3 rounded-2xl bg-slate-900 border border-slate-800">
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-slate-400">Intent Score</span>
                      <span className="font-bold text-emerald-400 font-mono">85 / 100</span>
                    </div>
                    <div className="w-full h-2 bg-slate-950 rounded-full mt-2 overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-teal-400 to-emerald-500 w-[85%]" />
                    </div>
                    <p className="text-[10px] text-slate-400 mt-2">
                      High purchase probability • Ready to place order.
                    </p>
                  </div>
                </div>

                {/* Pending Order Summary */}
                {selectedConv.pending_order_data?.items && (
                  <div>
                    <h4 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                      <ShoppingBag className="w-3.5 h-3.5 text-emerald-400" />
                      <span>Pending Order Preview</span>
                    </h4>
                    <div className="mt-3 p-3 rounded-2xl bg-emerald-950/40 border border-emerald-500/30 text-xs space-y-2">
                      {selectedConv.pending_order_data.items.map((item: any, i: number) => (
                        <div key={i} className="flex justify-between font-medium text-slate-200">
                          <span>{item.product_name}</span>
                          <span className="font-mono font-bold text-emerald-300">৳{item.unit_price}</span>
                        </div>
                      ))}
                      <div className="pt-2 border-t border-emerald-500/20 flex justify-between font-bold text-white">
                        <span>Payment</span>
                        <span>{selectedConv.pending_order_data.payment_method || "COD"}</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              <div className="pt-4 border-t border-slate-800 text-[11px] text-slate-500">
                End-to-end multi-tenant WhatsApp agent with autonomous sales tools.
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
