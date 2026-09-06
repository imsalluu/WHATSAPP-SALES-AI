"use client";

import React, { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import { apiRequest } from "@/lib/api";
import { ShoppingBag, Plus, Search, Sparkles, Tag, Check, Image as ImageIcon, Layers, RefreshCw } from "lucide-react";

export default function ProductsPage() {
  const [products, setProducts] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);

  // Form State
  const [name, setName] = useState("");
  const [sku, setSku] = useState("");
  const [price, setPrice] = useState("");
  const [discountPrice, setDiscountPrice] = useState("");
  const [category, setCategory] = useState("Clothing");
  const [description, setDescription] = useState("");

  const fetchProducts = async () => {
    try {
      const data = await apiRequest("/products/");
      setProducts(data);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleSeedCatalog = async () => {
    try {
      await apiRequest("/products/seed-samples", { method: "POST" });
      fetchProducts();
    } catch (e: any) {
      alert(e.message || "Failed to seed catalog");
    }
  };

  const handleCreateProduct = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiRequest("/products/", {
        method: "POST",
        body: JSON.stringify({
          name,
          sku,
          price: parseFloat(price),
          discount_price: discountPrice ? parseFloat(discountPrice) : null,
          category,
          description,
        }),
      });
      setShowAddModal(false);
      setName("");
      setSku("");
      setPrice("");
      setDiscountPrice("");
      setDescription("");
      fetchProducts();
    } catch (e: any) {
      alert(e.message || "Failed to create product");
    }
  };

  const filtered = products.filter((p) => {
    return (
      p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.sku.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (p.category && p.category.toLowerCase().includes(searchTerm.toLowerCase()))
    );
  });

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Header
          title="Product Catalog & Inventory"
          subtitle="Real-time synchronized catalog accessible to the AI Sales Agent for price, inventory & recommendations"
          actionButton={
            <div className="flex items-center gap-2">
              <button
                onClick={handleSeedCatalog}
                className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs font-semibold border border-slate-700 transition-colors"
              >
                <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
                <span>Seed Realistic Catalog</span>
              </button>
              <button
                onClick={() => setShowAddModal(true)}
                className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs font-bold shadow-lg shadow-emerald-500/20 transition-all active:scale-95"
              >
                <Plus className="w-4 h-4" />
                <span>Add Product</span>
              </button>
            </div>
          }
        />

        <main className="p-8 space-y-6 flex-1 overflow-y-auto">
          {/* Search & Stats Bar */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-sm">
            <div className="relative w-full sm:w-80">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="text"
                placeholder="Search products by title, SKU, category..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-4 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
              />
            </div>

            <div className="flex items-center gap-4 text-xs text-slate-400">
              <span>Total Products: <strong className="text-white font-mono">{products.length}</strong></span>
              <span>Available Variants: <strong className="text-emerald-400 font-mono">{products.reduce((acc, p) => acc + (p.variants?.length || 0), 0)}</strong></span>
            </div>
          </div>

          {/* Product Catalog Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {filtered.map((prod) => (
              <div
                key={prod.id}
                className="p-5 rounded-3xl bg-slate-900/80 border border-slate-800 hover:border-slate-700 transition-all shadow-xl backdrop-blur-sm flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                      {prod.sku}
                    </span>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      {prod.category || "General"}
                    </span>
                  </div>

                  <h3 className="mt-3 font-bold text-sm text-white tracking-tight leading-snug">{prod.name}</h3>
                  <p className="mt-1 text-xs text-slate-400 line-clamp-2">{prod.description || "No description provided."}</p>

                  {/* Pricing */}
                  <div className="mt-4 flex items-baseline gap-2">
                    <span className="text-lg font-black text-white font-mono">
                      ৳{(prod.discount_price || prod.price).toLocaleString()}
                    </span>
                    {prod.discount_price && (
                      <span className="text-xs text-slate-500 line-through font-mono">
                        ৳{prod.price.toLocaleString()}
                      </span>
                    )}
                  </div>

                  {/* Variants & Stock Pills */}
                  {prod.variants && prod.variants.length > 0 && (
                    <div className="mt-4 pt-3 border-t border-slate-800/80">
                      <p className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1">
                        <Layers className="w-3 h-3 text-emerald-400" />
                        <span>Live Stock Availability</span>
                      </p>
                      <div className="flex flex-wrap gap-1.5">
                        {prod.variants.map((v: any) => (
                          <span
                            key={v.id}
                            className="text-[10px] font-mono px-2 py-0.5 rounded-lg bg-slate-950 text-slate-300 border border-slate-800"
                          >
                            {v.title}: <strong className="text-emerald-400">{v.stock_quantity} left</strong>
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </main>
      </div>

      {/* Add Product Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl w-full max-w-lg p-6 shadow-2xl">
            <h3 className="text-lg font-bold text-white mb-4">Add New Catalog Product</h3>
            <form onSubmit={handleCreateProduct} className="space-y-4">
              <div>
                <label className="text-xs font-semibold text-slate-300">Product Title</label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full mt-1.5 px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500"
                  placeholder="e.g. Premium Cotton T-Shirt"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-semibold text-slate-300">SKU Code</label>
                  <input
                    type="text"
                    required
                    value={sku}
                    onChange={(e) => setSku(e.target.value)}
                    className="w-full mt-1.5 px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500 font-mono"
                    placeholder="TSH-COT-01"
                  />
                </div>
                <div>
                  <label className="text-xs font-semibold text-slate-300">Category</label>
                  <input
                    type="text"
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    className="w-full mt-1.5 px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500"
                    placeholder="Clothing"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-semibold text-slate-300">Regular Price (৳)</label>
                  <input
                    type="number"
                    required
                    value={price}
                    onChange={(e) => setPrice(e.target.value)}
                    className="w-full mt-1.5 px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500 font-mono"
                    placeholder="1200"
                  />
                </div>
                <div>
                  <label className="text-xs font-semibold text-slate-300">Discount Price (৳)</label>
                  <input
                    type="number"
                    value={discountPrice}
                    onChange={(e) => setDiscountPrice(e.target.value)}
                    className="w-full mt-1.5 px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500 font-mono"
                    placeholder="990"
                  />
                </div>
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-300">Description</label>
                <textarea
                  rows={3}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full mt-1.5 px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500"
                  placeholder="Key features, sizing notes, fabric composition..."
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-xs font-bold text-slate-950 shadow"
                >
                  Save Product
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
