"use client";

import React, { useEffect, useState } from "react";
import { RefreshCw, Users, Phone, Mail, ExternalLink } from "lucide-react";
import { clientsApi, Client } from "@/lib/api";

export default function AdminClientsPage() {
  const [clients, setClients] = useState<Client[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadClients();
  }, []);

  const loadClients = async () => {
    setLoading(true);
    try {
      const data = await clientsApi.list();
      setClients(data.clients || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const statusColors: Record<string, string> = {
    active: "bg-green-100 text-green-800",
    trialing: "bg-blue-100 text-blue-800",
    cancelled: "bg-red-100 text-red-800",
    past_due: "bg-yellow-100 text-yellow-800",
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Clients</h1>
          <p className="text-gray-500">All registered businesses</p>
        </div>
        <button
          onClick={loadClients}
          className="flex items-center gap-2 px-4 py-2 bg-white border rounded-lg hover:bg-gray-50"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          Refresh
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl shadow-sm p-4">
          <p className="text-sm text-gray-500">Total Clients</p>
          <p className="text-2xl font-bold">{clients.length}</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-4">
          <p className="text-sm text-gray-500">Active</p>
          <p className="text-2xl font-bold text-green-600">
            {clients.filter(c => c.subscriptionStatus === "active").length}
          </p>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-4">
          <p className="text-sm text-gray-500">Trialing</p>
          <p className="text-2xl font-bold text-blue-600">
            {clients.filter(c => c.subscriptionStatus === "trialing").length}
          </p>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-4">
          <p className="text-sm text-gray-500">MRR</p>
          <p className="text-2xl font-bold">
            £{clients.filter(c => c.subscriptionStatus === "active").length * 297}
          </p>
        </div>
      </div>

      {/* Clients Table */}
      <div className="bg-white rounded-xl shadow-sm overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Business</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Owner</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Covered Number</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vertical</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Plan</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {clients.map((client) => (
              <tr key={client.id} className="hover:bg-gray-50">
                <td className="px-4 py-3">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-blue-50 rounded-lg">
                      <Users className="w-4 h-4 text-blue-600" />
                    </div>
                    <div>
                      <p className="font-medium text-gray-900">{client.businessName}</p>
                      <p className="text-sm text-gray-500">{client.email}</p>
                    </div>
                  </div>
                </td>
                <td className="px-4 py-3 text-sm text-gray-600">{client.ownerName}</td>
                <td className="px-4 py-3">
                  {client.coveredNumber ? (
                    <div className="flex items-center gap-2">
                      <Phone className="w-4 h-4 text-gray-400" />
                      <span className="font-mono text-sm">{client.coveredNumber}</span>
                    </div>
                  ) : (
                    <span className="text-gray-400 text-sm">Not assigned</span>
                  )}
                </td>
                <td className="px-4 py-3">
                  <span className="capitalize text-sm text-gray-600">{client.vertical}</span>
                </td>
                <td className="px-4 py-3 text-sm text-gray-600 capitalize">{client.subscriptionPlan}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    statusColors[client.subscriptionStatus] || "bg-gray-100 text-gray-800"
                  }`}>
                    {client.subscriptionStatus}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <a
                    href={`/dashboard?client_id=${client.id}`}
                    target="_blank"
                    className="p-2 hover:bg-gray-100 rounded-lg inline-flex"
                    title="View Dashboard"
                  >
                    <ExternalLink className="w-4 h-4 text-gray-500" />
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {clients.length === 0 && (
          <div className="p-12 text-center text-gray-500">
            {loading ? "Loading..." : "No clients found"}
          </div>
        )}
      </div>
    </div>
  );
}
