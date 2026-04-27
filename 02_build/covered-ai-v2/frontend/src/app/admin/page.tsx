"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  Users,
  Phone,
  Mail,
  ArrowRightLeft,
  TrendingUp,
  CheckCircle,
  Clock,
  XCircle,
  LucideIcon
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
  icon: LucideIcon;
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
