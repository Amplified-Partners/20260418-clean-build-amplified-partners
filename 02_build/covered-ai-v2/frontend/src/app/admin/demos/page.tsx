"use client";

import React, { useEffect, useState } from "react";
import { Phone, Plus, RefreshCw, Trash2, Clock } from "lucide-react";
import { demoNumbersApi, DemoNumber } from "@/lib/api";

export default function AdminDemosPage() {
  const [numbers, setNumbers] = useState<DemoNumber[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>("all");
  const [showProvision, setShowProvision] = useState(false);

  useEffect(() => {
    loadNumbers();
  }, []);

  const loadNumbers = async () => {
    setLoading(true);
    try {
      const data = await demoNumbersApi.list();
      setNumbers(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredNumbers = filter === "all"
    ? numbers
    : numbers.filter(n => n.status === filter);

  const handleExtend = async (id: string) => {
    await demoNumbersApi.extend(id, 7);
    loadNumbers();
  };

  const handleRelease = async (id: string) => {
    if (confirm("Release this number? This cannot be undone.")) {
      await demoNumbersApi.release(id);
      loadNumbers();
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Demo Numbers</h1>
          <p className="text-gray-500">Personalized demo numbers for leads</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={loadNumbers}
            className="flex items-center gap-2 px-4 py-2 bg-white border rounded-lg hover:bg-gray-50"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            Refresh
          </button>
          <button
            onClick={() => setShowProvision(true)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            <Plus className="w-4 h-4" />
            New Demo Number
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex gap-2">
        {["all", "active", "expired", "converted"].map((s) => (
          <button
            key={s}
            onClick={() => setFilter(s)}
            className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
              filter === s
                ? "bg-gray-900 text-white"
                : "bg-white text-gray-600 border hover:bg-gray-50"
            }`}
          >
            {s.charAt(0).toUpperCase() + s.slice(1)}
          </button>
        ))}
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredNumbers.map((num) => (
          <div key={num.id} className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-blue-50 rounded-lg">
                  <Phone className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <p className="font-mono font-medium">{num.phone_number_display}</p>
                  <p className="text-sm text-gray-500">{num.business_name}</p>
                </div>
              </div>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                num.status === "active" ? "bg-green-100 text-green-800" :
                num.status === "converted" ? "bg-blue-100 text-blue-800" :
                "bg-gray-100 text-gray-800"
              }`}>
                {num.status}
              </span>
            </div>

            <div className="space-y-2 text-sm">
              {num.contact_name && (
                <p className="text-gray-600">Contact: {num.contact_name}</p>
              )}
              {num.contact_email && (
                <p className="text-gray-600">{num.contact_email}</p>
              )}
              <p className="text-gray-500">
                Calls: {num.call_count} &bull; Expires: {new Date(num.expires_at).toLocaleDateString()}
              </p>
            </div>

            {num.status === "active" && (
              <div className="flex gap-2 mt-4 pt-4 border-t">
                <button
                  onClick={() => handleExtend(num.id)}
                  className="flex-1 flex items-center justify-center gap-1 px-3 py-2 text-sm bg-gray-100 rounded-lg hover:bg-gray-200"
                >
                  <Clock className="w-4 h-4" />
                  Extend 7d
                </button>
                <button
                  onClick={() => handleRelease(num.id)}
                  className="flex items-center justify-center gap-1 px-3 py-2 text-sm text-red-600 bg-red-50 rounded-lg hover:bg-red-100"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            )}
          </div>
        ))}
      </div>

      {filteredNumbers.length === 0 && (
        <div className="bg-white rounded-xl shadow-sm p-12 text-center text-gray-500">
          {loading ? "Loading..." : "No demo numbers found"}
        </div>
      )}

      {/* Provision Modal */}
      {showProvision && (
        <ProvisionModal
          onClose={() => setShowProvision(false)}
          onSuccess={() => { setShowProvision(false); loadNumbers(); }}
        />
      )}
    </div>
  );
}

function ProvisionModal({ onClose, onSuccess }: { onClose: () => void; onSuccess: () => void }) {
  const [businessName, setBusinessName] = useState("");
  const [contactName, setContactName] = useState("");
  const [contactEmail, setContactEmail] = useState("");
  const [vertical, setVertical] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await demoNumbersApi.provision({
        business_name: businessName,
        contact_name: contactName || undefined,
        contact_email: contactEmail || undefined,
        vertical: vertical || undefined,
      });
      onSuccess();
    } catch (err) {
      console.error(err);
      alert("Failed to provision number");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl shadow-xl max-w-md w-full p-6">
        <h2 className="text-xl font-bold mb-4">Provision Demo Number</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Business Name *
            </label>
            <input
              type="text"
              value={businessName}
              onChange={(e) => setBusinessName(e.target.value)}
              required
              className="w-full px-3 py-2 border rounded-lg"
              placeholder="Smith Plumbing"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Contact Name
            </label>
            <input
              type="text"
              value={contactName}
              onChange={(e) => setContactName(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg"
              placeholder="John Smith"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Contact Email
            </label>
            <input
              type="email"
              value={contactEmail}
              onChange={(e) => setContactEmail(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg"
              placeholder="john@example.com"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Vertical
            </label>
            <select
              value={vertical}
              onChange={(e) => setVertical(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg"
            >
              <option value="">Select...</option>
              <option value="plumber">Plumber</option>
              <option value="electrician">Electrician</option>
              <option value="salon">Salon</option>
              <option value="vet">Vet</option>
              <option value="dental">Dental</option>
              <option value="physio">Physio</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border rounded-lg hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading || !businessName}
              className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? "Creating..." : "Create"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
