"use client";

import React, { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import { apiRequest } from "@/lib/api";
import { PackageCheck, Search, Clock, CheckCircle2, Truck, AlertCircle, Phone, MapPin, Send } from "lucide-react";

export default function OrdersPage() {
  const [orders, setOrders] = useState<any[]>([]);
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  const fetchOrders = async () => {
    try {
      const data = await apiRequest("/orders/");
      setOrders(data);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const handleUpdateStatus = async (orderId: string, newStatus: string) => {
    try {
      await apiRequest(`/orders/${orderId}/status`, {
        method: "PATCH",
        body: JSON.stringify({ status: newStatus }),
      });
      fetchOrders();
    } catch (e: any) {
      alert(e.message || "Failed to update order status");
    }
  };

  const filtered = orders.filter((ord) => {
    if (statusFilter !== "ALL" && ord.status !== statusFilter) return false;
    if (searchTerm) {
      const num = ord.order_number.toLowerCase();
      const name = (ord.delivery_name || "").toLowerCase();
      const phone = ord.delivery_phone || "";
      return num.includes(searchTerm.toLowerCase()) || name.includes(searchTerm.toLowerCase()) || phone.includes(searchTerm);
    }
    return true;
  });

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Header
          title="Order Fulfillment & Tracking"
          subtitle="Autonomous and AI-assisted order processing with live status management"
        />

        <main className="p-8 space-y-6 flex-1 overflow-y-auto">
          {/* Controls Bar */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-sm">
            <div className="relative w-full sm:w-80">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="text"
                placeholder="Search by order #, phone, customer..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-4 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
              />
            </div>

            <div className="flex items-center gap-1.5 overflow-x-auto text-xs">
              {["ALL", "CONFIRMED", "PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED"].map((st) => (
                <button
                  key={st}
                  onClick={() => setStatusFilter(st)}
                  className={`px-3 py-1.5 rounded-xl font-semibold transition-colors ${
                    statusFilter === st
                      ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                      : "text-slate-400 hover:text-white hover:bg-slate-800"
                  }`}
                >
                  {st}
                </button>
              ))}
            </div>
          </div>

          {/* Orders Table */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl backdrop-blur-sm">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase text-[10px] bg-slate-950/60">
                    <th className="py-3.5 px-6">Order #</th>
                    <th className="py-3.5 px-6">Customer</th>
                    <th className="py-3.5 px-6">Items & Subtotal</th>
                    <th className="py-3.5 px-6">Delivery Address</th>
                    <th className="py-3.5 px-6">Total & Payment</th>
                    <th className="py-3.5 px-6">Status</th>
                    <th className="py-3.5 px-6 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {filtered.length === 0 ? (
                    <tr>
                      <td colSpan={7} className="py-12 text-center text-slate-500">
                        No orders matching this filter. Orders placed by the AI sales agent will appear here automatically!
                      </td>
                    </tr>
                  ) : (
                    filtered.map((ord) => (
                      <tr key={ord.id} className="hover:bg-slate-800/30 transition-colors">
                        <td className="py-4 px-6 font-mono font-bold text-white">
                          <div>{ord.order_number}</div>
                          <span className="text-[10px] text-slate-500 font-normal">
                            {new Date(ord.created_at).toLocaleDateString()}
                          </span>
                        </td>
                        <td className="py-4 px-6">
                          <div className="font-semibold text-slate-200">{ord.delivery_name}</div>
                          <div className="text-[11px] text-emerald-400 font-mono flex items-center gap-1 mt-0.5">
                            <Phone className="w-3 h-3" /> {ord.delivery_phone}
                          </div>
                        </td>
                        <td className="py-4 px-6">
                          <div className="space-y-1">
                            {ord.items?.map((it: any, i: number) => (
                              <div key={i} className="text-slate-300">
                                {it.product_name} <span className="text-slate-500">x{it.quantity}</span>
                              </div>
                            ))}
                          </div>
                        </td>
                        <td className="py-4 px-6 max-w-xs">
                          <div className="text-slate-300 truncate flex items-center gap-1">
                            <MapPin className="w-3 h-3 text-slate-500 shrink-0" />
                            <span>{ord.delivery_address}</span>
                          </div>
                          <span className="text-[10px] text-slate-500">{ord.delivery_city || "Dhaka"}</span>
                        </td>
                        <td className="py-4 px-6 font-mono">
                          <div className="font-bold text-white text-sm">৳{ord.total_amount.toLocaleString()}</div>
                          <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 font-sans">
                            {ord.payment_method} • {ord.payment_status}
                          </span>
                        </td>
                        <td className="py-4 px-6">
                          <span
                            className={`px-2.5 py-1 rounded-full text-[10px] font-bold border ${
                              ord.status === "CONFIRMED"
                                ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                                : ord.status === "SHIPPED"
                                ? "bg-sky-500/10 text-sky-400 border-sky-500/20"
                                : ord.status === "DELIVERED"
                                ? "bg-teal-500/15 text-teal-300 border-teal-500/30"
                                : ord.status === "CANCELLED"
                                ? "bg-rose-500/10 text-rose-400 border-rose-500/20"
                                : "bg-amber-500/10 text-amber-400 border-amber-500/20"
                            }`}
                          >
                            {ord.status}
                          </span>
                        </td>
                        <td className="py-4 px-6 text-right">
                          <select
                            value={ord.status}
                            onChange={(e) => handleUpdateStatus(ord.id, e.target.value)}
                            className="bg-slate-950 border border-slate-700 text-slate-200 text-xs px-2.5 py-1 rounded-xl focus:outline-none focus:border-emerald-500"
                          >
                            <option value="CONFIRMED">CONFIRMED</option>
                            <option value="PROCESSING">PROCESSING</option>
                            <option value="SHIPPED">SHIPPED</option>
                            <option value="DELIVERED">DELIVERED</option>
                            <option value="CANCELLED">CANCELLED</option>
                          </select>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
