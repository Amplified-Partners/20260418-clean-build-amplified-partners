---
title: "Module 3: Admin Dashboard"
id: "03-admin-dashboard"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Module 3: Admin Dashboard

## Overview
Internal dashboard for managing porting requests, demo numbers, outreach campaigns, and system health.

## Files to Create

### 1. frontend/src/app/(admin)/layout.tsx

```tsx
"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  Phone, 
  Mail, 
  ArrowRightLeft,
  Activity,
  Settings,
  Users,
  LogOut
} from "lucide-react";

const ADMIN_EMAILS = ["ewan@covered.ai", "ewanbramley@gmail.com"];

const navItems = [
  { href: "/admin", icon: LayoutDashboard, label: "Overview" },
  { href: "/admin/clients", icon: Users, label: "Clients" },
  { href: "/admin/porting", icon: ArrowRightLeft, label: "Porting" },
  { href: "/admin/demos", icon: Phone, label: "Demo Numbers" },
  { href: "/admin/outreach", icon: Mail, label: "Outreach" },
  { href: "/admin/events", icon: Activity, label: "Events" },
  { href: "/admin/system", icon: Settings, label: "System" },
];

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [authorized, setAuthorized] = useState(false);
  
  useEffect(() => {
    const userEmail = localStorage.getItem("user_email");
    if (!userEmail || !ADMIN_EMAILS.includes(userEmail)) {
      router.push("/dashboard");
    } else {
      setAuthorized(true);
    }
  }, [router]);

  if (!authorized) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Checking authorization...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-gray-900 text-white flex flex-col">
        <div className="p-4 border-b border-gray-800">
          <h1 className="text-xl font-bold">Covered Admin</h1>
          <p className="text-xs text-gray-400 mt-1">Internal Dashboard</p>
        </div>
        
        <nav className="flex-1 p-4 space-y-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href || 
              (item.href !== "/admin" && pathname.startsWith(item.href));
            
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                  isActive 
                    ? "bg-blue-600 text-white" 
                    : "text-gray-300 hover:bg-gray-800 hover:text-white"
                }`}
              >
                <item.icon className="w-5 h-5" />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>
        
        <div className="p-4 border-t border-gray-800">
          <Link
            href="/dashboard"
            className="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
          >
            <LogOut className="w-5 h-5" />
            <span>Back to App</span>
          </Link>
        </div>
      </aside>
      
      {/* Main content */}
      <main className="flex-1 overflow-auto">
        <div className="p-8">
          {children}
        </div>
      </main>
    </div>
  );
}
```

### 2. frontend/src/app/(admin)/page.tsx

```tsx
"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { 
  Users, 
  Phone, 
  Mail, 
  ArrowRightLeft, 
  TrendingUp, 
  AlertCircle,
  CheckCircle,
  Clock,
  XCircle
} from "lucide-react";

interface AdminStats {
  totalClients: number;
  activeClients: number;
  revenueThisMonth: number;
  revenueLastMonth: number;
  portingRequests: {
    pending: number;
    inProgress: number;
    completed: number;
  };
  demoNumbers: {
    active: number;
    expired: number;
    converted: number;
  };
  outreach: {
    activeCampaigns: number;
    totalSent: number;
    totalOpened: number;
    totalReplied: number;
  };
  systemHealth: "healthy" | "degraded" | "down";
}

export default function AdminDashboard() {
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // TODO: Fetch from API
    setStats({
      totalClients: 2,
      activeClients: 2,
      revenueThisMonth: 594,
      revenueLastMonth: 0,
      portingRequests: { pending: 0, inProgress: 0, completed: 0 },
      demoNumbers: { active: 0, expired: 0, converted: 0 },
      outreach: { activeCampaigns: 0, totalSent: 0, totalOpened: 0, totalReplied: 0 },
      systemHealth: "healthy",
    });
    setLoading(false);
  }, []);

  if (loading) {
    return <div className="animate-pulse">Loading dashboard...</div>;
  }

  const healthColors = {
    healthy: "bg-green-100 text-green-800 border-green-200",
    degraded: "bg-yellow-100 text-yellow-800 border-yellow-200",
    down: "bg-red-100 text-red-800 border-red-200",
  };

  const healthIcons = {
    healthy: CheckCircle,
    degraded: Clock,
    down: XCircle,
  };

  const HealthIcon = healthIcons[stats?.systemHealth || "healthy"];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
        <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full border ${healthColors[stats?.systemHealth || "healthy"]}`}>
          <HealthIcon className="w-4 h-4" />
          <span className="text-sm font-medium capitalize">{stats?.systemHealth}</span>
        </div>
      </div>

      {/* Revenue Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          icon={Users}
          label="Active Clients"
          value={stats?.activeClients || 0}
          subvalue={`${stats?.totalClients} total`}
          color="blue"
        />
        <StatCard
          icon={TrendingUp}
          label="Revenue (This Month)"
          value={`£${stats?.revenueThisMonth || 0}`}
          subvalue={`£${stats?.revenueLastMonth} last month`}
          color="green"
        />
        <StatCard
          icon={ArrowRightLeft}
          label="Porting Requests"
          value={stats?.portingRequests.pending || 0}
          subvalue={`${stats?.portingRequests.inProgress} in progress`}
          color="purple"
          href="/admin/porting"
        />
        <StatCard
          icon={Phone}
          label="Demo Numbers"
          value={stats?.demoNumbers.active || 0}
          subvalue={`${stats?.demoNumbers.converted} converted`}
          color="orange"
          href="/admin/demos"
        />
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <QuickActionCard
          title="Porting Requests"
          description="Manage number porting requests"
          href="/admin/porting"
          stats={[
            { label: "Pending", value: stats?.portingRequests.pending || 0 },
            { label: "In Progress", value: stats?.portingRequests.inProgress || 0 },
            { label: "Completed", value: stats?.portingRequests.completed || 0 },
          ]}
        />
        <QuickActionCard
          title="Demo Numbers"
          description="Manage personalized demo numbers"
          href="/admin/demos"
          stats={[
            { label: "Active", value: stats?.demoNumbers.active || 0 },
            { label: "Expired", value: stats?.demoNumbers.expired || 0 },
            { label: "Converted", value: stats?.demoNumbers.converted || 0 },
          ]}
        />
        <QuickActionCard
          title="Outreach"
          description="Email campaign performance"
          href="/admin/outreach"
          stats={[
            { label: "Sent", value: stats?.outreach.totalSent || 0 },
            { label: "Opened", value: stats?.outreach.totalOpened || 0 },
            { label: "Replied", value: stats?.outreach.totalReplied || 0 },
          ]}
        />
      </div>
    </div>
  );
}

function StatCard({ 
  icon: Icon, 
  label, 
  value, 
  subvalue, 
  color,
  href 
}: { 
  icon: any; 
  label: string; 
  value: string | number; 
  subvalue: string;
  color: string;
  href?: string;
}) {
  const colorClasses: Record<string, string> = {
    blue: "bg-blue-50 text-blue-600",
    green: "bg-green-50 text-green-600",
    purple: "bg-purple-50 text-purple-600",
    orange: "bg-orange-50 text-orange-600",
  };

  const content = (
    <div className="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
      <div className="flex items-center gap-4">
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          <Icon className="w-6 h-6" />
        </div>
        <div>
          <p className="text-sm text-gray-500">{label}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          <p className="text-xs text-gray-400">{subvalue}</p>
        </div>
      </div>
    </div>
  );

  if (href) {
    return <Link href={href}>{content}</Link>;
  }
  return content;
}

function QuickActionCard({
  title,
  description,
  href,
  stats,
}: {
  title: string;
  description: string;
  href: string;
  stats: { label: string; value: number }[];
}) {
  return (
    <Link href={href}>
      <div className="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow h-full">
        <h3 className="font-semibold text-gray-900">{title}</h3>
        <p className="text-sm text-gray-500 mb-4">{description}</p>
        <div className="flex gap-4">
          {stats.map((stat) => (
            <div key={stat.label}>
              <p className="text-xl font-bold text-gray-900">{stat.value}</p>
              <p className="text-xs text-gray-400">{stat.label}</p>
            </div>
          ))}
        </div>
      </div>
    </Link>
  );
}
```

### 3. frontend/src/app/(admin)/porting/page.tsx

```tsx
"use client";

import React, { useEffect, useState } from "react";
import { Download, Eye, RefreshCw, ChevronDown } from "lucide-react";
import { portingApi, PortingListItem } from "@/lib/api";

const statusColors: Record<string, string> = {
  pending: "bg-yellow-100 text-yellow-800",
  loa_generated: "bg-blue-100 text-blue-800",
  submitted: "bg-purple-100 text-purple-800",
  in_progress: "bg-indigo-100 text-indigo-800",
  completed: "bg-green-100 text-green-800",
  failed: "bg-red-100 text-red-800",
  cancelled: "bg-gray-100 text-gray-800",
};

const statusLabels: Record<string, string> = {
  pending: "Pending",
  loa_generated: "LOA Generated",
  submitted: "Submitted",
  in_progress: "In Progress",
  completed: "Completed",
  failed: "Failed",
  cancelled: "Cancelled",
};

export default function AdminPortingPage() {
  const [requests, setRequests] = useState<PortingListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>("all");

  useEffect(() => {
    loadRequests();
  }, []);

  const loadRequests = async () => {
    setLoading(true);
    try {
      const data = await portingApi.list();
      setRequests(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredRequests = filter === "all" 
    ? requests 
    : requests.filter(r => r.status === filter);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Porting Requests</h1>
          <p className="text-gray-500">Manage number porting requests</p>
        </div>
        <button 
          onClick={loadRequests}
          className="flex items-center gap-2 px-4 py-2 bg-white border rounded-lg hover:bg-gray-50"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          Refresh
        </button>
      </div>

      {/* Filters */}
      <div className="flex gap-2 flex-wrap">
        {["all", "pending", "loa_generated", "submitted", "in_progress", "completed", "failed"].map((s) => (
          <button
            key={s}
            onClick={() => setFilter(s)}
            className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
              filter === s 
                ? "bg-gray-900 text-white" 
                : "bg-white text-gray-600 border hover:bg-gray-50"
            }`}
          >
            {s === "all" ? "All" : statusLabels[s] || s}
          </button>
        ))}
      </div>

      {/* Table */}
      <div className="bg-white rounded-xl shadow-sm overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Number</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Provider</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Submitted</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Est. Complete</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {filteredRequests.map((req) => (
              <tr key={req.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-sm font-mono text-gray-900">{req.id}</td>
                <td className="px-4 py-3 text-sm text-gray-900">{req.number_to_port}</td>
                <td className="px-4 py-3 text-sm text-gray-600">{req.current_provider}</td>
                <td className="px-4 py-3">
                  <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${statusColors[req.status] || "bg-gray-100"}`}>
                    {statusLabels[req.status] || req.status}
                  </span>
                </td>
                <td className="px-4 py-3 text-sm text-gray-500">
                  {new Date(req.submitted_at).toLocaleDateString()}
                </td>
                <td className="px-4 py-3 text-sm text-gray-500">
                  {req.estimated_completion || "-"}
                </td>
                <td className="px-4 py-3">
                  <div className="flex gap-1">
                    <button 
                      className="p-2 hover:bg-gray-100 rounded-lg"
                      title="View details"
                    >
                      <Eye className="w-4 h-4 text-gray-500" />
                    </button>
                    <a 
                      href={portingApi.downloadLoa(req.id)} 
                      target="_blank"
                      className="p-2 hover:bg-gray-100 rounded-lg"
                      title="Download LOA"
                    >
                      <Download className="w-4 h-4 text-gray-500" />
                    </a>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        
        {filteredRequests.length === 0 && (
          <div className="p-12 text-center text-gray-500">
            {loading ? "Loading..." : "No porting requests found"}
          </div>
        )}
      </div>
    </div>
  );
}
```

### 4. frontend/src/app/(admin)/demos/page.tsx

```tsx
"use client";

import React, { useEffect, useState } from "react";
import { Phone, Plus, RefreshCw, Trash2, Clock, CheckCircle } from "lucide-react";
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
                Calls: {num.call_count} • Expires: {new Date(num.expires_at).toLocaleDateString()}
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
```

### 5. frontend/src/app/(admin)/outreach/page.tsx

```tsx
"use client";

import React, { useEffect, useState } from "react";
import { Mail, Plus, RefreshCw, Play, Pause, Download } from "lucide-react";
import { outreachApi, OutreachCampaign } from "@/lib/api";

export default function AdminOutreachPage() {
  const [campaigns, setCampaigns] = useState<OutreachCampaign[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCampaigns();
  }, []);

  const loadCampaigns = async () => {
    setLoading(true);
    try {
      const data = await outreachApi.listCampaigns();
      setCampaigns(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleStart = async (id: string) => {
    await outreachApi.startCampaign(id);
    loadCampaigns();
  };

  const handlePause = async (id: string) => {
    await outreachApi.pauseCampaign(id);
    loadCampaigns();
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Outreach Campaigns</h1>
          <p className="text-gray-500">Email campaigns and tracking</p>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={loadCampaigns}
            className="flex items-center gap-2 px-4 py-2 bg-white border rounded-lg hover:bg-gray-50"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            Refresh
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            <Plus className="w-4 h-4" />
            New Campaign
          </button>
        </div>
      </div>

      {/* Campaigns Table */}
      <div className="bg-white rounded-xl shadow-sm overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Campaign</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Leads</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Sent</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Opened</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Replied</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Converted</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {campaigns.map((campaign) => (
              <tr key={campaign.id} className="hover:bg-gray-50">
                <td className="px-4 py-3">
                  <p className="font-medium text-gray-900">{campaign.name}</p>
                  <p className="text-sm text-gray-500">{campaign.template}</p>
                </td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    campaign.status === "active" ? "bg-green-100 text-green-800" :
                    campaign.status === "paused" ? "bg-yellow-100 text-yellow-800" :
                    campaign.status === "completed" ? "bg-blue-100 text-blue-800" :
                    "bg-gray-100 text-gray-800"
                  }`}>
                    {campaign.status}
                  </span>
                </td>
                <td className="px-4 py-3 text-sm text-gray-600">{campaign.total_leads}</td>
                <td className="px-4 py-3 text-sm text-gray-600">{campaign.sent}</td>
                <td className="px-4 py-3 text-sm text-gray-600">
                  {campaign.opened} ({campaign.sent ? Math.round(campaign.opened / campaign.sent * 100) : 0}%)
                </td>
                <td className="px-4 py-3 text-sm text-gray-600">{campaign.replied}</td>
                <td className="px-4 py-3 text-sm text-gray-600">{campaign.converted}</td>
                <td className="px-4 py-3">
                  <div className="flex gap-1">
                    {campaign.status === "active" ? (
                      <button
                        onClick={() => handlePause(campaign.id)}
                        className="p-2 hover:bg-gray-100 rounded-lg"
                        title="Pause"
                      >
                        <Pause className="w-4 h-4 text-gray-500" />
                      </button>
                    ) : campaign.status === "draft" || campaign.status === "paused" ? (
                      <button
                        onClick={() => handleStart(campaign.id)}
                        className="p-2 hover:bg-gray-100 rounded-lg"
                        title="Start"
                      >
                        <Play className="w-4 h-4 text-gray-500" />
                      </button>
                    ) : null}
                    <a
                      href={outreachApi.exportCampaign(campaign.id)}
                      className="p-2 hover:bg-gray-100 rounded-lg"
                      title="Export CSV"
                    >
                      <Download className="w-4 h-4 text-gray-500" />
                    </a>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {campaigns.length === 0 && (
          <div className="p-12 text-center text-gray-500">
            {loading ? "Loading..." : "No campaigns found"}
          </div>
        )}
      </div>
    </div>
  );
}
```

### 6. frontend/src/app/(admin)/events/page.tsx

```tsx
"use client";

import React, { useEffect, useState } from "react";
import { Activity, RefreshCw, ChevronDown, ChevronRight } from "lucide-react";

interface Event {
  id: string;
  source: string;
  event_type: string;
  status: string;
  payload: any;
  error: string | null;
  created_at: string;
  processed_at: string | null;
}

export default function AdminEventsPage() {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState({ source: "", status: "" });
  const [expandedId, setExpandedId] = useState<string | null>(null);

  useEffect(() => {
    loadEvents();
  }, [filter]);

  const loadEvents = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filter.source) params.append("source", filter.source);
      if (filter.status) params.append("status", filter.status);
      
      const response = await fetch(`/api/v1/events?${params}&limit=100`);
      const data = await response.json();
      setEvents(data.events || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const sourceColors: Record<string, string> = {
    vapi: "bg-purple-100 text-purple-800",
    twilio: "bg-red-100 text-red-800",
    stripe: "bg-blue-100 text-blue-800",
    resend: "bg-green-100 text-green-800",
  };

  const statusColors: Record<string, string> = {
    received: "bg-yellow-100 text-yellow-800",
    processed: "bg-green-100 text-green-800",
    failed: "bg-red-100 text-red-800",
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Event Log</h1>
          <p className="text-gray-500">Webhook events and processing status</p>
        </div>
        <button 
          onClick={loadEvents}
          className="flex items-center gap-2 px-4 py-2 bg-white border rounded-lg hover:bg-gray-50"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          Refresh
        </button>
      </div>

      {/* Filters */}
      <div className="flex gap-4">
        <select
          value={filter.source}
          onChange={(e) => setFilter({ ...filter, source: e.target.value })}
          className="px-3 py-2 border rounded-lg"
        >
          <option value="">All Sources</option>
          <option value="vapi">Vapi</option>
          <option value="twilio">Twilio</option>
          <option value="stripe">Stripe</option>
          <option value="resend">Resend</option>
        </select>
        <select
          value={filter.status}
          onChange={(e) => setFilter({ ...filter, status: e.target.value })}
          className="px-3 py-2 border rounded-lg"
        >
          <option value="">All Statuses</option>
          <option value="received">Received</option>
          <option value="processed">Processed</option>
          <option value="failed">Failed</option>
        </select>
      </div>

      {/* Events List */}
      <div className="bg-white rounded-xl shadow-sm divide-y">
        {events.map((event) => (
          <div key={event.id}>
            <div 
              className="px-4 py-3 flex items-center gap-4 hover:bg-gray-50 cursor-pointer"
              onClick={() => setExpandedId(expandedId === event.id ? null : event.id)}
            >
              {expandedId === event.id ? (
                <ChevronDown className="w-4 h-4 text-gray-400" />
              ) : (
                <ChevronRight className="w-4 h-4 text-gray-400" />
              )}
              <span className={`px-2 py-1 rounded text-xs font-medium ${sourceColors[event.source] || "bg-gray-100"}`}>
                {event.source}
              </span>
              <span className="flex-1 text-sm font-mono text-gray-900">
                {event.event_type}
              </span>
              <span className={`px-2 py-1 rounded text-xs font-medium ${statusColors[event.status] || "bg-gray-100"}`}>
                {event.status}
              </span>
              <span className="text-sm text-gray-500">
                {new Date(event.created_at).toLocaleTimeString()}
              </span>
            </div>
            {expandedId === event.id && (
              <div className="px-4 py-3 bg-gray-50 border-t">
                <pre className="text-xs overflow-auto max-h-96 p-3 bg-gray-900 text-gray-100 rounded-lg">
                  {JSON.stringify(event.payload, null, 2)}
                </pre>
                {event.error && (
                  <div className="mt-2 p-3 bg-red-50 text-red-800 rounded-lg text-sm">
                    <strong>Error:</strong> {event.error}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}

        {events.length === 0 && (
          <div className="p-12 text-center text-gray-500">
            {loading ? "Loading..." : "No events found"}
          </div>
        )}
      </div>
    </div>
  );
}
```

### 7. frontend/src/app/(admin)/system/page.tsx

```tsx
"use client";

import React, { useEffect, useState } from "react";
import { CheckCircle, XCircle, RefreshCw, Server, Database, Phone, Mail, CreditCard } from "lucide-react";

interface SystemStatus {
  api: { status: string; latency: number };
  database: { status: string; connections: number };
  twilio: { status: string; balance: number };
  vapi: { status: string; assistants: number };
  resend: { status: string };
  stripe: { status: string };
}

export default function AdminSystemPage() {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkStatus();
  }, []);

  const checkStatus = async () => {
    setLoading(true);
    // TODO: Implement actual health checks
    setStatus({
      api: { status: "healthy", latency: 45 },
      database: { status: "healthy", connections: 2 },
      twilio: { status: "healthy", balance: 50.0 },
      vapi: { status: "healthy", assistants: 3 },
      resend: { status: "healthy" },
      stripe: { status: "healthy" },
    });
    setLoading(false);
  };

  const services = [
    { key: "api", label: "API Server", icon: Server, extra: status?.api.latency ? `${status.api.latency}ms` : null },
    { key: "database", label: "Database", icon: Database, extra: status?.database.connections ? `${status.database.connections} connections` : null },
    { key: "twilio", label: "Twilio", icon: Phone, extra: status?.twilio.balance ? `$${status.twilio.balance.toFixed(2)} balance` : null },
    { key: "vapi", label: "Vapi", icon: Phone, extra: status?.vapi.assistants ? `${status.vapi.assistants} assistants` : null },
    { key: "resend", label: "Resend", icon: Mail, extra: null },
    { key: "stripe", label: "Stripe", icon: CreditCard, extra: null },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">System Status</h1>
          <p className="text-gray-500">Service health and configuration</p>
        </div>
        <button 
          onClick={checkStatus}
          className="flex items-center gap-2 px-4 py-2 bg-white border rounded-lg hover:bg-gray-50"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          Check Status
        </button>
      </div>

      {/* Service Status Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {services.map((service) => {
          const serviceStatus = status?.[service.key as keyof SystemStatus];
          const isHealthy = serviceStatus?.status === "healthy";
          
          return (
            <div key={service.key} className="bg-white rounded-xl shadow-sm p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className={`p-2 rounded-lg ${isHealthy ? "bg-green-50" : "bg-red-50"}`}>
                    <service.icon className={`w-5 h-5 ${isHealthy ? "text-green-600" : "text-red-600"}`} />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{service.label}</p>
                    {service.extra && (
                      <p className="text-sm text-gray-500">{service.extra}</p>
                    )}
                  </div>
                </div>
                {isHealthy ? (
                  <CheckCircle className="w-5 h-5 text-green-600" />
                ) : (
                  <XCircle className="w-5 h-5 text-red-600" />
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Environment Info */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h2 className="font-semibold text-gray-900 mb-4">Environment</h2>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-gray-500">API URL</p>
            <p className="font-mono text-gray-900">{process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}</p>
          </div>
          <div>
            <p className="text-gray-500">Environment</p>
            <p className="font-mono text-gray-900">{process.env.NODE_ENV}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
```
