/**
 * Ewan Admin - Clients List
 * 
 * All clients with health scores.
 * Quick actions and filtering.
 */

"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Search, Filter, Phone, Mail, MoreVertical, TrendingUp, TrendingDown } from "lucide-react";
import { cn } from "@/lib/utils";

// Mock data
const mockClients = [
  {
    id: "titan",
    name: "Titan Plumbing",
    contact: "Ralph Thompson",
    email: "ralph@titanplumbing.co.uk",
    phone: "+447712345678",
    plan: "Pro",
    mrr: 297,
    health: 95,
    callsThisMonth: 127,
    status: "active",
    trend: "up",
    joinedDate: "Oct 2024",
  },
  {
    id: "clifton",
    name: "Clifton House Hotel",
    contact: "Andy Morrison",
    email: "andy@cliftonhouse.co.uk",
    phone: "+447712345679",
    plan: "Pro",
    mrr: 297,
    health: 45,
    callsThisMonth: 89,
    status: "at-risk",
    trend: "down",
    joinedDate: "Nov 2024",
    issue: "Payment failed",
  },
  {
    id: "sarahs",
    name: "Sarah's Salon",
    contact: "Sarah Mitchell",
    email: "sarah@sarahssalon.co.uk",
    phone: "+447712345680",
    plan: "Starter",
    mrr: 197,
    health: 78,
    callsThisMonth: 34,
    status: "active",
    trend: "up",
    joinedDate: "Nov 2024",
  },
  {
    id: "david",
    name: "David Tree Surgery",
    contact: "David Hughes",
    email: "david@davidtree.co.uk",
    phone: "+447712345681",
    plan: "Pro",
    mrr: 297,
    health: 88,
    callsThisMonth: 56,
    status: "active",
    trend: "up",
    joinedDate: "Nov 2024",
  },
  {
    id: "harriet",
    name: "Harriet Aesthetics",
    contact: "Harriet Jones",
    email: "harriet@aesthetics.co.uk",
    phone: "+447712345682",
    plan: "Starter",
    mrr: 197,
    health: 72,
    callsThisMonth: 28,
    status: "pilot",
    trend: "neutral",
    joinedDate: "Nov 2024",
  },
];

function HealthBadge({ health }: { health: number }) {
  const color = health >= 80 ? "bg-green-500" : health >= 60 ? "bg-yellow-500" : "bg-red-500";
  return (
    <div className="flex items-center gap-2">
      <div className={`w-2 h-2 rounded-full ${color}`} />
      <span className={cn(
        "text-sm font-medium",
        health >= 80 ? "text-green-500" : health >= 60 ? "text-yellow-500" : "text-red-500"
      )}>
        {health}
      </span>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const styles = {
    active: "bg-green-500/10 text-green-500",
    "at-risk": "bg-red-500/10 text-red-500",
    pilot: "bg-blue-500/10 text-blue-500",
    churned: "bg-neutral-500/10 text-neutral-500",
  };
  return (
    <span className={`px-2 py-1 text-xs font-medium rounded ${styles[status as keyof typeof styles]}`}>
      {status}
    </span>
  );
}

export default function ClientsPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("all");
  
  const filteredClients = mockClients.filter(client => {
    const matchesSearch = 
      client.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      client.contact.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === "all" || client.status === statusFilter;
    return matchesSearch && matchesStatus;
  });
  
  // Stats
  const totalMrr = mockClients.reduce((sum, c) => sum + c.mrr, 0);
  const activeCount = mockClients.filter(c => c.status === "active").length;
  const atRiskCount = mockClients.filter(c => c.status === "at-risk").length;
  
  return (
    <div className="p-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">Clients</h1>
          <p className="text-neutral-500">{mockClients.length} total clients</p>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="bg-neutral-900 rounded-lg px-4 py-2 border border-neutral-800">
            <span className="text-neutral-500 text-sm">MRR:</span>
            <span className="text-white font-semibold ml-2">£{totalMrr.toLocaleString()}</span>
          </div>
        </div>
      </div>
      
      {/* Stats row */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        <div className="bg-neutral-900 rounded-xl p-4 border border-neutral-800">
          <p className="text-xs text-neutral-500">Active</p>
          <p className="text-2xl font-bold text-green-500">{activeCount}</p>
        </div>
        <div className="bg-neutral-900 rounded-xl p-4 border border-neutral-800">
          <p className="text-xs text-neutral-500">At Risk</p>
          <p className="text-2xl font-bold text-red-500">{atRiskCount}</p>
        </div>
        <div className="bg-neutral-900 rounded-xl p-4 border border-neutral-800">
          <p className="text-xs text-neutral-500">Pilots</p>
          <p className="text-2xl font-bold text-blue-500">
            {mockClients.filter(c => c.status === "pilot").length}
          </p>
        </div>
        <div className="bg-neutral-900 rounded-xl p-4 border border-neutral-800">
          <p className="text-xs text-neutral-500">Avg Health</p>
          <p className="text-2xl font-bold text-white">
            {Math.round(mockClients.reduce((sum, c) => sum + c.health, 0) / mockClients.length)}
          </p>
        </div>
      </div>
      
      {/* Filters */}
      <div className="flex items-center gap-4 mb-6">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-500" />
          <input
            type="text"
            placeholder="Search clients..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-3 bg-neutral-900 border border-neutral-800 rounded-lg text-white placeholder:text-neutral-500 focus:outline-none focus:border-neutral-700"
          />
        </div>
        
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="px-4 py-3 bg-neutral-900 border border-neutral-800 rounded-lg text-white focus:outline-none focus:border-neutral-700"
        >
          <option value="all">All Status</option>
          <option value="active">Active</option>
          <option value="at-risk">At Risk</option>
          <option value="pilot">Pilot</option>
        </select>
      </div>
      
      {/* Clients table */}
      <div className="bg-neutral-900 rounded-xl border border-neutral-800 overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-neutral-800">
              <th className="text-left px-6 py-4 text-xs font-medium text-neutral-500 uppercase tracking-wider">
                Client
              </th>
              <th className="text-left px-6 py-4 text-xs font-medium text-neutral-500 uppercase tracking-wider">
                Status
              </th>
              <th className="text-left px-6 py-4 text-xs font-medium text-neutral-500 uppercase tracking-wider">
                Health
              </th>
              <th className="text-left px-6 py-4 text-xs font-medium text-neutral-500 uppercase tracking-wider">
                MRR
              </th>
              <th className="text-left px-6 py-4 text-xs font-medium text-neutral-500 uppercase tracking-wider">
                Calls
              </th>
              <th className="text-left px-6 py-4 text-xs font-medium text-neutral-500 uppercase tracking-wider">
                Trend
              </th>
              <th className="text-right px-6 py-4 text-xs font-medium text-neutral-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            {filteredClients.map((client) => (
              <tr 
                key={client.id}
                className="border-b border-neutral-800 hover:bg-neutral-800/50 transition-colors"
              >
                <td className="px-6 py-4">
                  <Link href={`/command/clients/${client.id}`} className="block">
                    <p className="text-white font-medium">{client.name}</p>
                    <p className="text-sm text-neutral-500">{client.contact}</p>
                  </Link>
                </td>
                <td className="px-6 py-4">
                  <StatusBadge status={client.status} />
                  {client.issue && (
                    <p className="text-xs text-red-400 mt-1">{client.issue}</p>
                  )}
                </td>
                <td className="px-6 py-4">
                  <HealthBadge health={client.health} />
                </td>
                <td className="px-6 py-4">
                  <span className="text-white">£{client.mrr}</span>
                  <span className="text-neutral-500 text-sm ml-1">/{client.plan}</span>
                </td>
                <td className="px-6 py-4 text-neutral-400">
                  {client.callsThisMonth}
                </td>
                <td className="px-6 py-4">
                  {client.trend === "up" && <TrendingUp className="w-4 h-4 text-green-500" />}
                  {client.trend === "down" && <TrendingDown className="w-4 h-4 text-red-500" />}
                  {client.trend === "neutral" && <span className="text-neutral-500">—</span>}
                </td>
                <td className="px-6 py-4 text-right">
                  <div className="flex items-center justify-end gap-2">
                    <a
                      href={`tel:${client.phone}`}
                      className="p-2 text-neutral-500 hover:text-white hover:bg-neutral-700 rounded-lg transition-colors"
                    >
                      <Phone className="w-4 h-4" />
                    </a>
                    <a
                      href={`mailto:${client.email}`}
                      className="p-2 text-neutral-500 hover:text-white hover:bg-neutral-700 rounded-lg transition-colors"
                    >
                      <Mail className="w-4 h-4" />
                    </a>
                    <button className="p-2 text-neutral-500 hover:text-white hover:bg-neutral-700 rounded-lg transition-colors">
                      <MoreVertical className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
