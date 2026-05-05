---
title: "Module 8: Client Dashboard"
id: "08-client-dashboard"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Module 8: Client Dashboard

## Overview
The dashboard clients see when they log in. Shows calls, leads, messages, and basic settings. Simple, clean, focused on value delivered.

## Expert Panel Input

**UX Expert**: Clients don't want complexity. Show them: "How many calls did Gemma handle?" and "What leads came in?" Everything else is secondary.

**Dashboard Design Expert**: Lead with the money metric. Show value immediately. Make the phone number prominent so they can test it anytime.

**Mobile-First Expert**: 70%+ will check this on their phone. Design for thumb navigation, large tap targets, quick glances.

---

## Pages

### 1. Dashboard Home (`/dashboard`)
- Calls this week/month
- New leads
- Gemma's status (active/issues)
- Quick actions

### 2. Calls (`/dashboard/calls`)
- List of all calls
- Play recordings
- View transcripts
- Filter by date/outcome

### 3. Leads (`/dashboard/leads`)
- All captured leads
- Contact details
- Call reason
- Follow-up status

### 4. Settings (`/dashboard/settings`)
- Business hours
- Emergency keywords
- Notification preferences
- Forwarding number

---

## Files to Create

### 1. frontend/src/app/(client-dashboard)/layout.tsx

```tsx
"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  Phone, 
  Users, 
  Settings,
  Menu,
  X,
  LogOut
} from "lucide-react";

interface Client {
  id: string;
  business_name: string;
  covered_number: string;
  status: string;
}

const navItems = [
  { href: "/dashboard", icon: LayoutDashboard, label: "Overview" },
  { href: "/dashboard/calls", icon: Phone, label: "Calls" },
  { href: "/dashboard/leads", icon: Users, label: "Leads" },
  { href: "/dashboard/settings", icon: Settings, label: "Settings" },
];

export default function ClientDashboardLayout({ 
  children 
}: { 
  children: React.ReactNode 
}) {
  const pathname = usePathname();
  const [client, setClient] = useState<Client | null>(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    // Fetch client data
    const fetchClient = async () => {
      try {
        const response = await fetch("/api/v1/client/me");
        const data = await response.json();
        setClient(data);
      } catch (err) {
        console.error("Failed to fetch client:", err);
      }
    };
    fetchClient();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile Header */}
      <header className="lg:hidden fixed top-0 left-0 right-0 bg-white border-b z-50">
        <div className="flex items-center justify-between px-4 py-3">
          <span className="font-bold text-lg">{client?.business_name || "Dashboard"}</span>
          <button 
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2"
          >
            {mobileMenuOpen ? <X /> : <Menu />}
          </button>
        </div>
        
        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <nav className="bg-white border-t px-4 py-2">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center gap-3 px-3 py-3 rounded-lg ${
                  pathname === item.href 
                    ? "bg-blue-50 text-blue-600" 
                    : "text-gray-600"
                }`}
              >
                <item.icon className="w-5 h-5" />
                <span>{item.label}</span>
              </Link>
            ))}
          </nav>
        )}
      </header>

      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex fixed left-0 top-0 bottom-0 w-64 bg-white border-r flex-col">
        <div className="p-6 border-b">
          <h1 className="font-bold text-lg">{client?.business_name || "Dashboard"}</h1>
          {client?.covered_number && (
            <a 
              href={`tel:${client.covered_number}`}
              className="text-sm text-blue-600 hover:underline"
            >
              {client.covered_number}
            </a>
          )}
        </div>
        
        <nav className="flex-1 p-4 space-y-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${
                  isActive 
                    ? "bg-blue-50 text-blue-600 font-medium" 
                    : "text-gray-600 hover:bg-gray-50"
                }`}
              >
                <item.icon className="w-5 h-5" />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>
        
        <div className="p-4 border-t">
          <div className="flex items-center gap-2 text-sm text-gray-500 mb-3">
            <div className={`w-2 h-2 rounded-full ${
              client?.status === "active" ? "bg-green-500" : "bg-yellow-500"
            }`} />
            <span>Gemma is {client?.status === "active" ? "active" : "setting up"}</span>
          </div>
          <button className="flex items-center gap-2 text-gray-500 hover:text-gray-700">
            <LogOut className="w-4 h-4" />
            <span>Sign out</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="lg:ml-64 pt-16 lg:pt-0 min-h-screen">
        <div className="p-4 lg:p-8">
          {children}
        </div>
      </main>

      {/* Mobile Bottom Nav */}
      <nav className="lg:hidden fixed bottom-0 left-0 right-0 bg-white border-t">
        <div className="flex justify-around py-2">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex flex-col items-center py-2 px-4 ${
                  isActive ? "text-blue-600" : "text-gray-500"
                }`}
              >
                <item.icon className="w-5 h-5" />
                <span className="text-xs mt-1">{item.label}</span>
              </Link>
            );
          })}
        </div>
      </nav>
    </div>
  );
}
```

### 2. frontend/src/app/(client-dashboard)/dashboard/page.tsx

```tsx
"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Phone, Users, Clock, TrendingUp, ArrowRight, Play } from "lucide-react";

interface DashboardStats {
  calls_today: number;
  calls_this_week: number;
  calls_this_month: number;
  new_leads_today: number;
  new_leads_this_week: number;
  avg_call_duration: number;
  covered_number: string;
}

interface RecentCall {
  id: string;
  caller_number: string;
  caller_name: string | null;
  duration: number;
  outcome: string;
  created_at: string;
  has_recording: boolean;
}

export default function DashboardHome() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [recentCalls, setRecentCalls] = useState<RecentCall[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, callsRes] = await Promise.all([
          fetch("/api/v1/client/stats"),
          fetch("/api/v1/client/calls?limit=5"),
        ]);
        
        setStats(await statsRes.json());
        setRecentCalls((await callsRes.json()).calls || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="animate-pulse space-y-6">
        <div className="h-8 bg-gray-200 rounded w-48" />
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-24 bg-gray-200 rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-500">Here's what Gemma's been up to</p>
        </div>
        
        {stats?.covered_number && (
          <a 
            href={`tel:${stats.covered_number}`}
            className="inline-flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700"
          >
            <Phone className="w-4 h-4" />
            Test Your Line
          </a>
        )}
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          icon={Phone}
          label="Calls Today"
          value={stats?.calls_today || 0}
          trend={`${stats?.calls_this_week || 0} this week`}
          color="blue"
        />
        <StatCard
          icon={Users}
          label="New Leads"
          value={stats?.new_leads_today || 0}
          trend={`${stats?.new_leads_this_week || 0} this week`}
          color="green"
        />
        <StatCard
          icon={Clock}
          label="Avg Call Time"
          value={formatDuration(stats?.avg_call_duration || 0)}
          trend="minutes"
          color="purple"
        />
        <StatCard
          icon={TrendingUp}
          label="This Month"
          value={stats?.calls_this_month || 0}
          trend="total calls"
          color="orange"
        />
      </div>

      {/* Recent Calls */}
      <div className="bg-white rounded-xl shadow-sm">
        <div className="flex items-center justify-between p-4 border-b">
          <h2 className="font-semibold text-gray-900">Recent Calls</h2>
          <Link 
            href="/dashboard/calls"
            className="text-sm text-blue-600 hover:underline flex items-center gap-1"
          >
            View all <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
        
        {recentCalls.length > 0 ? (
          <div className="divide-y">
            {recentCalls.map((call) => (
              <div key={call.id} className="p-4 flex items-center justify-between hover:bg-gray-50">
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                    call.outcome === "lead" ? "bg-green-100" : "bg-gray-100"
                  }`}>
                    <Phone className={`w-5 h-5 ${
                      call.outcome === "lead" ? "text-green-600" : "text-gray-500"
                    }`} />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">
                      {call.caller_name || call.caller_number}
                    </p>
                    <p className="text-sm text-gray-500">
                      {formatTime(call.created_at)} • {formatDuration(call.duration)}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  {call.outcome === "lead" && (
                    <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full">
                      Lead
                    </span>
                  )}
                  {call.has_recording && (
                    <button className="p-2 hover:bg-gray-100 rounded-lg">
                      <Play className="w-4 h-4 text-gray-500" />
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="p-8 text-center text-gray-500">
            <Phone className="w-12 h-12 mx-auto mb-3 text-gray-300" />
            <p>No calls yet</p>
            <p className="text-sm mt-1">Calls will appear here when Gemma answers them</p>
          </div>
        )}
      </div>

      {/* Quick Tips */}
      <div className="bg-blue-50 rounded-xl p-6">
        <h3 className="font-semibold text-blue-900 mb-2">💡 Quick Tip</h3>
        <p className="text-blue-800">
          Forward your main number to {stats?.covered_number || "your Covered number"} to have Gemma answer all your calls. 
          <Link href="/dashboard/settings" className="underline ml-1">Set up forwarding →</Link>
        </p>
      </div>
    </div>
  );
}

function StatCard({ 
  icon: Icon, 
  label, 
  value, 
  trend, 
  color 
}: { 
  icon: any; 
  label: string; 
  value: string | number; 
  trend: string;
  color: string;
}) {
  const colorClasses: Record<string, string> = {
    blue: "bg-blue-50 text-blue-600",
    green: "bg-green-50 text-green-600",
    purple: "bg-purple-50 text-purple-600",
    orange: "bg-orange-50 text-orange-600",
  };

  return (
    <div className="bg-white rounded-xl shadow-sm p-4">
      <div className="flex items-center gap-3 mb-2">
        <div className={`p-2 rounded-lg ${colorClasses[color]}`}>
          <Icon className="w-4 h-4" />
        </div>
        <span className="text-sm text-gray-500">{label}</span>
      </div>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
      <p className="text-xs text-gray-400 mt-1">{trend}</p>
    </div>
  );
}

function formatDuration(seconds: number): string {
  if (seconds < 60) return `${seconds}s`;
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function formatTime(isoString: string): string {
  const date = new Date(isoString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`;
  return date.toLocaleDateString();
}
```

### 3. frontend/src/app/(client-dashboard)/dashboard/calls/page.tsx

```tsx
"use client";

import React, { useEffect, useState } from "react";
import { Phone, Play, Pause, Download, ChevronDown, Search } from "lucide-react";

interface Call {
  id: string;
  caller_number: string;
  caller_name: string | null;
  duration: number;
  outcome: string;
  summary: string | null;
  transcript: string | null;
  recording_url: string | null;
  created_at: string;
}

export default function CallsPage() {
  const [calls, setCalls] = useState<Call[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [search, setSearch] = useState("");
  const [expandedCall, setExpandedCall] = useState<string | null>(null);
  const [playingAudio, setPlayingAudio] = useState<string | null>(null);

  useEffect(() => {
    const fetchCalls = async () => {
      try {
        const response = await fetch(`/api/v1/client/calls?filter=${filter}`);
        const data = await response.json();
        setCalls(data.calls || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchCalls();
  }, [filter]);

  const filteredCalls = calls.filter((call) => {
    if (!search) return true;
    const searchLower = search.toLowerCase();
    return (
      call.caller_number.includes(searchLower) ||
      call.caller_name?.toLowerCase().includes(searchLower) ||
      call.summary?.toLowerCase().includes(searchLower)
    );
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Calls</h1>
        <p className="text-gray-500">All calls handled by Gemma</p>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search calls..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border rounded-lg"
          />
        </div>
        <div className="flex gap-2">
          {["all", "leads", "missed", "completed"].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-lg text-sm font-medium ${
                filter === f
                  ? "bg-blue-600 text-white"
                  : "bg-white border text-gray-600 hover:bg-gray-50"
              }`}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Calls List */}
      <div className="bg-white rounded-xl shadow-sm divide-y">
        {loading ? (
          <div className="p-8 text-center text-gray-500">Loading calls...</div>
        ) : filteredCalls.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            <Phone className="w-12 h-12 mx-auto mb-3 text-gray-300" />
            <p>No calls found</p>
          </div>
        ) : (
          filteredCalls.map((call) => (
            <div key={call.id}>
              {/* Call Row */}
              <div 
                className="p-4 flex items-center justify-between hover:bg-gray-50 cursor-pointer"
                onClick={() => setExpandedCall(expandedCall === call.id ? null : call.id)}
              >
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                    call.outcome === "lead" ? "bg-green-100" :
                    call.outcome === "missed" ? "bg-red-100" :
                    "bg-gray-100"
                  }`}>
                    <Phone className={`w-5 h-5 ${
                      call.outcome === "lead" ? "text-green-600" :
                      call.outcome === "missed" ? "text-red-600" :
                      "text-gray-500"
                    }`} />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">
                      {call.caller_name || call.caller_number}
                    </p>
                    <p className="text-sm text-gray-500">
                      {new Date(call.created_at).toLocaleString()} • {formatDuration(call.duration)}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  {call.outcome === "lead" && (
                    <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full">
                      Lead
                    </span>
                  )}
                  <ChevronDown className={`w-5 h-5 text-gray-400 transition-transform ${
                    expandedCall === call.id ? "rotate-180" : ""
                  }`} />
                </div>
              </div>

              {/* Expanded Details */}
              {expandedCall === call.id && (
                <div className="px-4 pb-4 bg-gray-50 border-t">
                  <div className="pt-4 space-y-4">
                    {/* Summary */}
                    {call.summary && (
                      <div>
                        <h4 className="text-sm font-medium text-gray-700 mb-1">Summary</h4>
                        <p className="text-gray-600">{call.summary}</p>
                      </div>
                    )}

                    {/* Audio Player */}
                    {call.recording_url && (
                      <div>
                        <h4 className="text-sm font-medium text-gray-700 mb-2">Recording</h4>
                        <div className="flex items-center gap-3">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              setPlayingAudio(playingAudio === call.id ? null : call.id);
                            }}
                            className="p-2 bg-blue-600 text-white rounded-full hover:bg-blue-700"
                          >
                            {playingAudio === call.id ? (
                              <Pause className="w-4 h-4" />
                            ) : (
                              <Play className="w-4 h-4" />
                            )}
                          </button>
                          <div className="flex-1 h-2 bg-gray-200 rounded-full">
                            <div className="h-2 bg-blue-600 rounded-full w-0" />
                          </div>
                          <span className="text-sm text-gray-500">{formatDuration(call.duration)}</span>
                          <a
                            href={call.recording_url}
                            download
                            onClick={(e) => e.stopPropagation()}
                            className="p-2 hover:bg-gray-200 rounded-lg"
                          >
                            <Download className="w-4 h-4 text-gray-500" />
                          </a>
                        </div>
                      </div>
                    )}

                    {/* Transcript */}
                    {call.transcript && (
                      <div>
                        <h4 className="text-sm font-medium text-gray-700 mb-2">Transcript</h4>
                        <div className="bg-white p-4 rounded-lg border text-sm text-gray-600 max-h-48 overflow-y-auto">
                          {call.transcript}
                        </div>
                      </div>
                    )}

                    {/* Actions */}
                    <div className="flex gap-2 pt-2">
                      <button className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700">
                        Add to CRM
                      </button>
                      <button className="px-4 py-2 border rounded-lg text-sm hover:bg-gray-50">
                        Mark as Followed Up
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

function formatDuration(seconds: number): string {
  if (seconds < 60) return `${seconds}s`;
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}
```

### 4. frontend/src/app/(client-dashboard)/dashboard/leads/page.tsx

```tsx
"use client";

import React, { useEffect, useState } from "react";
import { Users, Phone, Mail, MessageSquare, Check, Clock } from "lucide-react";

interface Lead {
  id: string;
  name: string;
  phone: string;
  email: string | null;
  reason: string;
  urgency: string;
  status: string;
  notes: string | null;
  call_id: string;
  created_at: string;
}

export default function LeadsPage() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    const fetchLeads = async () => {
      try {
        const response = await fetch(`/api/v1/client/leads?status=${filter}`);
        const data = await response.json();
        setLeads(data.leads || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchLeads();
  }, [filter]);

  const updateLeadStatus = async (leadId: string, status: string) => {
    try {
      await fetch(`/api/v1/client/leads/${leadId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status }),
      });
      setLeads(leads.map(l => l.id === leadId ? { ...l, status } : l));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Leads</h1>
        <p className="text-gray-500">People who called and need follow-up</p>
      </div>

      {/* Filters */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {["all", "new", "contacted", "converted", "lost"].map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap ${
              filter === f
                ? "bg-blue-600 text-white"
                : "bg-white border text-gray-600 hover:bg-gray-50"
            }`}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Leads Grid */}
      {loading ? (
        <div className="text-center py-8 text-gray-500">Loading leads...</div>
      ) : leads.length === 0 ? (
        <div className="bg-white rounded-xl shadow-sm p-8 text-center">
          <Users className="w-12 h-12 mx-auto mb-3 text-gray-300" />
          <p className="text-gray-500">No leads yet</p>
          <p className="text-sm text-gray-400 mt-1">
            When Gemma captures caller details, they'll appear here
          </p>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {leads.map((lead) => (
            <div key={lead.id} className="bg-white rounded-xl shadow-sm p-4">
              {/* Header */}
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="font-semibold text-gray-900">{lead.name}</h3>
                  <p className="text-sm text-gray-500">
                    {new Date(lead.created_at).toLocaleDateString()}
                  </p>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  lead.urgency === "urgent" ? "bg-red-100 text-red-700" :
                  lead.urgency === "high" ? "bg-orange-100 text-orange-700" :
                  "bg-gray-100 text-gray-700"
                }`}>
                  {lead.urgency}
                </span>
              </div>

              {/* Reason */}
              <p className="text-sm text-gray-600 mb-4">{lead.reason}</p>

              {/* Contact */}
              <div className="space-y-2 mb-4">
                <a 
                  href={`tel:${lead.phone}`}
                  className="flex items-center gap-2 text-sm text-blue-600 hover:underline"
                >
                  <Phone className="w-4 h-4" />
                  {lead.phone}
                </a>
                {lead.email && (
                  <a 
                    href={`mailto:${lead.email}`}
                    className="flex items-center gap-2 text-sm text-blue-600 hover:underline"
                  >
                    <Mail className="w-4 h-4" />
                    {lead.email}
                  </a>
                )}
              </div>

              {/* Status */}
              <div className="flex items-center justify-between pt-3 border-t">
                <span className={`flex items-center gap-1 text-sm ${
                  lead.status === "new" ? "text-blue-600" :
                  lead.status === "contacted" ? "text-yellow-600" :
                  lead.status === "converted" ? "text-green-600" :
                  "text-gray-500"
                }`}>
                  {lead.status === "new" && <Clock className="w-4 h-4" />}
                  {lead.status === "contacted" && <MessageSquare className="w-4 h-4" />}
                  {lead.status === "converted" && <Check className="w-4 h-4" />}
                  {lead.status.charAt(0).toUpperCase() + lead.status.slice(1)}
                </span>
                
                <div className="flex gap-1">
                  {lead.status === "new" && (
                    <button
                      onClick={() => updateLeadStatus(lead.id, "contacted")}
                      className="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
                    >
                      Mark Contacted
                    </button>
                  )}
                  {lead.status === "contacted" && (
                    <button
                      onClick={() => updateLeadStatus(lead.id, "converted")}
                      className="px-3 py-1 text-sm bg-green-100 text-green-700 rounded hover:bg-green-200"
                    >
                      Mark Converted
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

### 5. frontend/src/app/(client-dashboard)/dashboard/settings/page.tsx

```tsx
"use client";

import React, { useEffect, useState } from "react";
import { Save, Phone, Bell, Clock, AlertTriangle } from "lucide-react";

interface ClientSettings {
  business_name: string;
  covered_number: string;
  forwarding_number: string;
  notification_email: string;
  notification_sms: string;
  business_hours: {
    start: string;
    end: string;
    days: string[];
  };
  emergency_keywords: string[];
  greeting_name: string;
}

export default function SettingsPage() {
  const [settings, setSettings] = useState<ClientSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const response = await fetch("/api/v1/client/settings");
        const data = await response.json();
        setSettings(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchSettings();
  }, []);

  const handleSave = async () => {
    setSaving(true);
    try {
      await fetch("/api/v1/client/settings", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(settings),
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  if (loading || !settings) {
    return <div className="text-center py-8">Loading settings...</div>;
  }

  return (
    <div className="space-y-6 max-w-2xl">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
          <p className="text-gray-500">Configure how Gemma handles your calls</p>
        </div>
        <button
          onClick={handleSave}
          disabled={saving}
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          <Save className="w-4 h-4" />
          {saving ? "Saving..." : saved ? "Saved!" : "Save Changes"}
        </button>
      </div>

      {/* Phone Numbers */}
      <section className="bg-white rounded-xl shadow-sm p-6">
        <div className="flex items-center gap-2 mb-4">
          <Phone className="w-5 h-5 text-blue-600" />
          <h2 className="text-lg font-semibold">Phone Numbers</h2>
        </div>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Your Covered Number
            </label>
            <input
              type="text"
              value={settings.covered_number}
              disabled
              className="w-full px-3 py-2 bg-gray-100 border rounded-lg text-gray-500"
            />
            <p className="text-xs text-gray-500 mt-1">
              This is the number Gemma answers. Forward your main line here.
            </p>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Forward Emergencies To
            </label>
            <input
              type="tel"
              value={settings.forwarding_number}
              onChange={(e) => setSettings({ ...settings, forwarding_number: e.target.value })}
              className="w-full px-3 py-2 border rounded-lg"
              placeholder="+44 7xxx xxx xxx"
            />
            <p className="text-xs text-gray-500 mt-1">
              Urgent calls will be forwarded to this number
            </p>
          </div>
        </div>
      </section>

      {/* Notifications */}
      <section className="bg-white rounded-xl shadow-sm p-6">
        <div className="flex items-center gap-2 mb-4">
          <Bell className="w-5 h-5 text-blue-600" />
          <h2 className="text-lg font-semibold">Notifications</h2>
        </div>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Email Notifications
            </label>
            <input
              type="email"
              value={settings.notification_email}
              onChange={(e) => setSettings({ ...settings, notification_email: e.target.value })}
              className="w-full px-3 py-2 border rounded-lg"
              placeholder="you@example.com"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              SMS Notifications
            </label>
            <input
              type="tel"
              value={settings.notification_sms}
              onChange={(e) => setSettings({ ...settings, notification_sms: e.target.value })}
              className="w-full px-3 py-2 border rounded-lg"
              placeholder="+44 7xxx xxx xxx"
            />
          </div>
        </div>
      </section>

      {/* Business Hours */}
      <section className="bg-white rounded-xl shadow-sm p-6">
        <div className="flex items-center gap-2 mb-4">
          <Clock className="w-5 h-5 text-blue-600" />
          <h2 className="text-lg font-semibold">Business Hours</h2>
        </div>
        
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Opens
              </label>
              <input
                type="time"
                value={settings.business_hours.start}
                onChange={(e) => setSettings({
                  ...settings,
                  business_hours: { ...settings.business_hours, start: e.target.value }
                })}
                className="w-full px-3 py-2 border rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Closes
              </label>
              <input
                type="time"
                value={settings.business_hours.end}
                onChange={(e) => setSettings({
                  ...settings,
                  business_hours: { ...settings.business_hours, end: e.target.value }
                })}
                className="w-full px-3 py-2 border rounded-lg"
              />
            </div>
          </div>
          
          <p className="text-sm text-gray-500">
            Gemma mentions your hours to callers and handles after-hours calls appropriately.
          </p>
        </div>
      </section>

      {/* Emergency Keywords */}
      <section className="bg-white rounded-xl shadow-sm p-6">
        <div className="flex items-center gap-2 mb-4">
          <AlertTriangle className="w-5 h-5 text-red-600" />
          <h2 className="text-lg font-semibold">Emergency Keywords</h2>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Words that trigger urgent handling
          </label>
          <input
            type="text"
            value={settings.emergency_keywords.join(", ")}
            onChange={(e) => setSettings({
              ...settings,
              emergency_keywords: e.target.value.split(",").map(k => k.trim())
            })}
            className="w-full px-3 py-2 border rounded-lg"
            placeholder="flood, burst, emergency, urgent"
          />
          <p className="text-xs text-gray-500 mt-1">
            Comma-separated. When callers mention these words, Gemma treats it as urgent.
          </p>
        </div>
      </section>
    </div>
  );
}
```

---

## Backend API Routes

### src/api/routes/client_dashboard.py

```python
"""
Client Dashboard API Routes

Endpoints for the client-facing dashboard.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta

router = APIRouter(prefix="/client", tags=["client-dashboard"])


# Auth dependency (simplified)
async def get_current_client():
    # TODO: Implement proper auth
    return {"id": "client_123", "business_name": "Test Business"}


@router.get("/me")
async def get_current_client_info(client = Depends(get_current_client)):
    """Get current client info."""
    return {
        "id": client["id"],
        "business_name": client["business_name"],
        "covered_number": "+441234567890",
        "status": "active",
    }


@router.get("/stats")
async def get_dashboard_stats(client = Depends(get_current_client)):
    """Get dashboard statistics."""
    # TODO: Implement actual stats from database
    return {
        "calls_today": 3,
        "calls_this_week": 12,
        "calls_this_month": 47,
        "new_leads_today": 1,
        "new_leads_this_week": 5,
        "avg_call_duration": 124,
        "covered_number": "+441234567890",
    }


@router.get("/calls")
async def get_client_calls(
    limit: int = 50,
    filter: str = "all",
    client = Depends(get_current_client)
):
    """Get client's calls."""
    # TODO: Implement actual call fetching
    return {
        "calls": [
            {
                "id": "call_1",
                "caller_number": "+447123456789",
                "caller_name": "John Smith",
                "duration": 145,
                "outcome": "lead",
                "summary": "Caller needs emergency plumbing - burst pipe in kitchen",
                "transcript": "Gemma: Hi, thanks for calling... [truncated]",
                "recording_url": "https://example.com/recording.mp3",
                "created_at": datetime.utcnow().isoformat(),
                "has_recording": True,
            }
        ],
        "total": 1,
    }


@router.get("/leads")
async def get_client_leads(
    status: str = "all",
    client = Depends(get_current_client)
):
    """Get client's leads."""
    return {
        "leads": [
            {
                "id": "lead_1",
                "name": "John Smith",
                "phone": "+447123456789",
                "email": "john@example.com",
                "reason": "Burst pipe in kitchen, needs emergency repair",
                "urgency": "urgent",
                "status": "new",
                "notes": None,
                "call_id": "call_1",
                "created_at": datetime.utcnow().isoformat(),
            }
        ],
        "total": 1,
    }


@router.patch("/leads/{lead_id}")
async def update_lead(
    lead_id: str,
    status: str,
    client = Depends(get_current_client)
):
    """Update lead status."""
    return {"message": "Lead updated", "status": status}


@router.get("/settings")
async def get_client_settings(client = Depends(get_current_client)):
    """Get client settings."""
    return {
        "business_name": client["business_name"],
        "covered_number": "+441234567890",
        "forwarding_number": "+447987654321",
        "notification_email": "owner@example.com",
        "notification_sms": "+447987654321",
        "business_hours": {
            "start": "08:00",
            "end": "18:00",
            "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        },
        "emergency_keywords": ["flood", "burst", "emergency", "urgent", "gas"],
        "greeting_name": "the business",
    }


@router.put("/settings")
async def update_client_settings(
    settings: dict,
    client = Depends(get_current_client)
):
    """Update client settings."""
    # TODO: Validate and save settings
    return {"message": "Settings updated"}
```

Add to main.py:
```python
from src.api.routes import client_dashboard
app.include_router(client_dashboard.router, prefix="/api/v1", tags=["client-dashboard"])
```
