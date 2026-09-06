"use client";

import React, { useState, useRef, useEffect } from "react";
import { X, Send, Bot, Sparkles, Check, CheckCheck, Phone, Video, MoreVertical, Wrench, ShoppingBag } from "lucide-react";
import { apiRequest } from "@/lib/api";

interface ChatMessage {
  id: string;
  sender: "customer" | "ai";
  text: string;
  time: string;
  tools?: any[];
}

export default function WhatsAppSimulatorModal({ onClose }: { onClose: () => void }) {
  const [phoneNumber, setPhoneNumber] = useState("+880 1711-223344");
  const [customerName, setCustomerName] = useState("Walk-in Customer");
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "1",
      sender: "ai",
      text: "👋 Hello! Welcome to our store. How can I assist you with your shopping today? ✨",
      time: "Just now",
    },
  ]);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const quickPrompts = [
    "I need a gift for my wife under 3000 taka",
    "Is the black hoodie available in XL?",
    "Deliver to House 12, Road 4, Dhanmondi, Dhaka (01711223344)",
    "Yes, please place the order!",
    "Can I speak with a human agent?",
  ];

  const handleSendMessage = async (textToSend?: string) => {
    const text = textToSend || inputMessage;
    if (!text.trim() || isLoading) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      sender: "customer",
      text,
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputMessage("");
    setIsLoading(true);

    try {
      const response = await apiRequest("/conversations/simulator", {
        method: "POST",
        body: JSON.stringify({
          phone_number: phoneNumber,
          customer_name: customerName,
          message: text,
        }),
      });

      if (response && response.ai_response) {
        const aiMsg: ChatMessage = {
          id: (Date.now() + 1).toString(),
          sender: "ai",
          text: response.ai_response.content,
          time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
          tools: response.tools_executed || [],
        };
        setMessages((prev) => [...prev, aiMsg]);
      }
    } catch (error: any) {
      console.error("Simulator Error:", error);
      const errorMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: "ai",
        text: `⚠️ System: ${error.message || "Failed to process message."}`,
        time: "Now",
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-700/80 rounded-3xl w-full max-w-4xl shadow-2xl flex flex-col md:flex-row overflow-hidden max-h-[90vh]">
        {/* Left: Simulator Settings & Controls */}
        <div className="w-full md:w-80 bg-slate-950 p-6 border-b md:border-b-0 md:border-r border-slate-800 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-4 border-b border-slate-800">
              <div className="flex items-center gap-2 text-emerald-400 font-bold text-sm">
                <Sparkles className="w-4 h-4" />
                <span>WhatsApp Live Sandbox</span>
              </div>
            </div>

            <div className="mt-5 space-y-4">
              <div>
                <label className="text-xs font-semibold text-slate-300">Customer Name</label>
                <input
                  type="text"
                  value={customerName}
                  onChange={(e) => setCustomerName(e.target.value)}
                  className="w-full mt-1.5 px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500"
                />
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-300">Customer Phone Number</label>
                <input
                  type="text"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  className="w-full mt-1.5 px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white font-mono focus:outline-none focus:border-emerald-500"
                />
              </div>
            </div>

            <div className="mt-6">
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Quick Sales Prompts
              </p>
              <div className="space-y-1.5">
                {quickPrompts.map((prompt, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSendMessage(prompt)}
                    className="w-full text-left p-2 rounded-xl bg-slate-900/90 hover:bg-emerald-500/10 hover:border-emerald-500/30 border border-slate-800 text-[11px] text-slate-300 hover:text-emerald-300 transition-all truncate"
                  >
                    👉 {prompt}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800 text-[11px] text-slate-500">
            Simulates official Meta Cloud API webhook lifecycle with real-time tool calling and database updates.
          </div>
        </div>

        {/* Right: Realistic WhatsApp Mobile Phone Interface */}
        <div className="flex-1 flex flex-col bg-[#0b141a] relative h-[620px]">
          {/* WhatsApp Chat Header */}
          <div className="bg-[#202c33] px-4 py-3 border-b border-[#2a3942] flex items-center justify-between text-white shadow-md">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-emerald-600 flex items-center justify-center font-bold text-sm text-white shadow">
                <Bot className="w-5 h-5" />
              </div>
              <div>
                <div className="font-semibold text-sm flex items-center gap-1.5">
                  <span>AI Sales Specialist</span>
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                </div>
                <p className="text-[11px] text-emerald-400">Online • Verified Business</p>
              </div>
            </div>

            <div className="flex items-center gap-3 text-slate-300">
              <Phone className="w-4 h-4 cursor-pointer hover:text-white" />
              <Video className="w-4 h-4 cursor-pointer hover:text-white" />
              <button onClick={onClose} className="p-1 rounded-lg hover:bg-slate-700 text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* WhatsApp Chat Message History */}
          <div
            className="flex-1 overflow-y-auto p-4 space-y-3"
            style={{
              backgroundImage: "radial-gradient(#1f2c34 1px, transparent 1px)",
              backgroundSize: "20px 20px",
            }}
          >
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex flex-col ${msg.sender === "customer" ? "items-end" : "items-start"}`}
              >
                {/* Tool Calling Execution Indicator */}
                {msg.tools && msg.tools.length > 0 && (
                  <div className="mb-1.5 flex flex-wrap gap-1 max-w-[80%]">
                    {msg.tools.map((t: any, idx: number) => (
                      <span
                        key={idx}
                        className="inline-flex items-center gap-1 text-[10px] font-mono px-2 py-0.5 rounded-md bg-emerald-950/80 text-emerald-300 border border-emerald-600/40"
                      >
                        <Wrench className="w-2.5 h-2.5" />
                        {t.tool}()
                      </span>
                    ))}
                  </div>
                )}

                <div
                  className={`max-w-[80%] p-3 rounded-2xl text-xs whitespace-pre-line leading-relaxed shadow-md ${
                    msg.sender === "customer"
                      ? "bg-[#005c4b] text-emerald-50 rounded-tr-none"
                      : "bg-[#202c33] text-slate-100 rounded-tl-none border border-[#2a3942]"
                  }`}
                >
                  {msg.text}
                  <div className="flex items-center justify-end gap-1 mt-1 text-[9px] text-slate-400">
                    <span>{msg.time}</span>
                    {msg.sender === "customer" && <CheckCheck className="w-3.5 h-3.5 text-sky-400" />}
                  </div>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex items-center gap-2 p-3 bg-[#202c33] border border-[#2a3942] rounded-2xl rounded-tl-none w-28 text-slate-400 text-xs shadow">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-bounce" />
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-bounce [animation-delay:0.2s]" />
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-bounce [animation-delay:0.4s]" />
                <span className="text-[10px] text-emerald-400">Thinking...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* WhatsApp Chat Input Bar */}
          <div className="p-3 bg-[#202c33] border-t border-[#2a3942] flex items-center gap-2">
            <input
              type="text"
              placeholder="Type a message as customer..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
              disabled={isLoading}
              className="flex-1 bg-[#2a3942] text-white placeholder-slate-400 text-xs px-4 py-2.5 rounded-2xl focus:outline-none focus:ring-1 focus:ring-emerald-500"
            />
            <button
              onClick={() => handleSendMessage()}
              disabled={isLoading || !inputMessage.trim()}
              className="w-10 h-10 rounded-full bg-[#00a884] hover:bg-[#008f6f] disabled:opacity-50 text-white flex items-center justify-center shadow transition-transform active:scale-95"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
