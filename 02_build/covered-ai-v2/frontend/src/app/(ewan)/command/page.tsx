/**
 * Ewan Admin - Command Center
 * 
 * Everything at a glance.
 * System status, key metrics, attention items.
 */

"use client";

import React from "react";
import { 
  TrendingUp, 
  TrendingDown, 
  Phone, 
  Users, 
  DollarSign,
  AlertTriangle,
  CheckCircle,
  Clock,
  Zap,
  ArrowRight
} from "lucide-react";
import Link from "next/link";

// Mock data
const mockData = {
  systemStatus: {
    vapi: { status: "operational", latency: "45ms" },
    twilio: { status: "operational", latency: "32ms" },
    stripe: { status: "operational", latency: "89ms" },
    database: { status: "operational", latency: "12ms" },
  },
  todayMetrics: {
    revenue: { value: 2847, change: 12.5, trend: "up" },
    calls: { value: 47, change: -5.2, trend: "down" },
    signups: { value: 3, change: 50, trend: "up" },
    churn: { value: 0, change: 0, trend: "neutral" },
  },
  monthMetrics: {
    mrr: 14850,
    arr: 178200,
    clients: 52,
    avgRevenue: 285,
  },
  attentionItems: [
    { 
      id: "1", 
      type: "warning", 
      title: "Client payment failed", 
      description: "Clifton House Hotel - card declined",
      time: "2h ago",
      action: "/command/clients/clifton"
    },
    { 
      id: "2", 
      type: "info", 
      title: "New signup", 
      description: "Sarah's Salon signed up via demo number",
      time: "4h ago",
      action: "/command/clients/sarahs-salon"
    },
    { 
      id: "3", 
      type: "success", 
      title: "Pilot converted", 
      description: "David Tree Surgery moved to paid plan",
      time: "Yesterday",
      action: "/command/clients/david-tree"
    },
  ],
  recentCalls: [
    { id: "1", client: "Titan Plumbing", calls: 12, lastCall: "10m ago" },
    { id: "2", client: "Clifton House", calls: 8, lastCall: "1h ago" },
    { id: "3", client: "Sarah's Salon", calls: 5, lastCall: "2h ago" },
  ],
  pipeline: {
    demos: 24,
    warmLeads: 12,
    negotiations: 4,
    closedThisWeek: 3,
  },
};

function MetricCard({ 
  label, 
  value, 
  change, 
  trend,
  prefix = "",
  suffix = ""
}: { 
  label: string; 
  value: number | string;
  change?: number;
  trend?: "up" | "down" | "neutral";
  prefix?: string;
  suffix?: string;
}) {
  return (
    <div className="bg-neutral-900 rounded-xl p-6 border border-neutral-800">
      <p className="text-sm text-neutral-500 mb-2">{label}</p>
      <p className="text-3xl font-bold text-white">
        {prefix}{typeof value === 'number' ? value.toLocaleString() : value}{suffix}
      </p>
      {change !== undefined && (
        <div className={`flex items-center gap-1 mt-2 text-sm ${
          trend === "up" ? "text-green-500" : 
          trend === "down" ? "text-red-500" : 
          "text-neutral-500"
        }`}>
          {trend === "up" && <TrendingUp className="w-4 h-4" />}
          {trend === "down" && <TrendingDown className="w-4 h-4" />}
          <span>{change > 0 ? "+" : ""}{change}%</span>
          <span className="text-neutral-600">vs yesterday</span>
        </div>
      )}
    </div>
  );
}

function StatusDot({ status }: { status: string }) {
  const colors = {
    operational: "bg-green-500",
    degraded: "bg-yellow-500",
    down: "bg-red-500",
  };
  return (
    <div className={`w-2 h-2 rounded-full ${colors[status as keyof typeof colors] || "bg-neutral-500"}`} />
  );
}

function AttentionIcon({ type }: { type: string }) {
  switch (type) {
    case "warning":
      return <AlertTriangle className="w-5 h-5 text-amber-500" />;
    case "success":
      return <CheckCircle className="w-5 h-5 text-green-500" />;
    default:
      return <Clock className="w-5 h-5 text-blue-500" />;
  }
}

export default function CommandCenterPage() {
  const { systemStatus, todayMetrics, monthMetrics, attentionItems, recentCalls, pipeline } = mockData;
  
  return (
    <div className="p-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">Command Center</h1>
          <p className="text-neutral-500">
            {new Date().toLocaleDateString("en-GB", { 
              weekday: "long", 
              day: "numeric", 
              month: "long" 
            })}
          </p>
        </div>
        
        {/* System status summary */}
        <div className="flex items-center gap-4 bg-neutral-900 rounded-lg px-4 py-2 border border-neutral-800">
          {Object.entries(systemStatus).map(([name, data]) => (
            <div key={name} className="flex items-center gap-2">
              <StatusDot status={data.status} />
              <span className="text-xs text-neutral-400 capitalize">{name}</span>
            </div>
          ))}
        </div>
      </div>
      
      {/* Today's metrics */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        <MetricCard
          label="Revenue Today"
          value={todayMetrics.revenue.value}
          prefix="£"
          change={todayMetrics.revenue.change}
          trend={todayMetrics.revenue.trend as "up" | "down"}
        />
        <MetricCard
          label="Calls Handled"
          value={todayMetrics.calls.value}
          change={todayMetrics.calls.change}
          trend={todayMetrics.calls.trend as "up" | "down"}
        />
        <MetricCard
          label="New Signups"
          value={todayMetrics.signups.value}
          change={todayMetrics.signups.change}
          trend={todayMetrics.signups.trend as "up" | "down"}
        />
        <MetricCard
          label="Churn"
          value={todayMetrics.churn.value}
          change={todayMetrics.churn.change}
          trend="neutral"
        />
      </div>
      
      <div className="grid grid-cols-3 gap-8">
        {/* Attention needed */}
        <div className="col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-white">Needs Attention</h2>
            <Link href="/command/alerts" className="text-sm text-blue-500 hover:text-blue-400">
              View all
            </Link>
          </div>
          
          <div className="space-y-3">
            {attentionItems.map((item) => (
              <Link
                key={item.id}
                href={item.action}
                className="flex items-center gap-4 p-4 bg-neutral-900 rounded-xl border border-neutral-800 hover:border-neutral-700 transition-colors"
              >
                <AttentionIcon type={item.type} />
                <div className="flex-1">
                  <p className="text-white font-medium">{item.title}</p>
                  <p className="text-sm text-neutral-500">{item.description}</p>
                </div>
                <span className="text-xs text-neutral-600">{item.time}</span>
                <ArrowRight className="w-4 h-4 text-neutral-600" />
              </Link>
            ))}
          </div>
          
          {/* Month overview */}
          <div className="mt-8">
            <h2 className="text-lg font-semibold text-white mb-4">This Month</h2>
            <div className="grid grid-cols-4 gap-4">
              <div className="bg-neutral-900 rounded-xl p-4 border border-neutral-800">
                <p className="text-xs text-neutral-500">MRR</p>
                <p className="text-xl font-bold text-white">£{monthMetrics.mrr.toLocaleString()}</p>
              </div>
              <div className="bg-neutral-900 rounded-xl p-4 border border-neutral-800">
                <p className="text-xs text-neutral-500">ARR</p>
                <p className="text-xl font-bold text-white">£{monthMetrics.arr.toLocaleString()}</p>
              </div>
              <div className="bg-neutral-900 rounded-xl p-4 border border-neutral-800">
                <p className="text-xs text-neutral-500">Clients</p>
                <p className="text-xl font-bold text-white">{monthMetrics.clients}</p>
              </div>
              <div className="bg-neutral-900 rounded-xl p-4 border border-neutral-800">
                <p className="text-xs text-neutral-500">ARPU</p>
                <p className="text-xl font-bold text-white">£{monthMetrics.avgRevenue}</p>
              </div>
            </div>
          </div>
        </div>
        
        {/* Right sidebar */}
        <div className="space-y-8">
          {/* Pipeline */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-white">Pipeline</h2>
              <Link href="/command/pipeline" className="text-sm text-blue-500 hover:text-blue-400">
                View all
              </Link>
            </div>
            <div className="bg-neutral-900 rounded-xl p-4 border border-neutral-800 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-neutral-400">Demo calls</span>
                <span className="text-white font-semibold">{pipeline.demos}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-neutral-400">Warm leads</span>
                <span className="text-white font-semibold">{pipeline.warmLeads}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-neutral-400">In negotiation</span>
                <span className="text-white font-semibold">{pipeline.negotiations}</span>
              </div>
              <div className="pt-3 border-t border-neutral-800 flex items-center justify-between">
                <span className="text-green-500">Closed this week</span>
                <span className="text-green-500 font-semibold">{pipeline.closedThisWeek}</span>
              </div>
            </div>
          </div>
          
          {/* Recent calls by client */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-white">Active Clients</h2>
              <Link href="/command/clients" className="text-sm text-blue-500 hover:text-blue-400">
                View all
              </Link>
            </div>
            <div className="bg-neutral-900 rounded-xl border border-neutral-800 overflow-hidden">
              {recentCalls.map((client, i) => (
                <Link
                  key={client.id}
                  href={`/command/clients/${client.id}`}
                  className={`flex items-center justify-between p-4 hover:bg-neutral-800 transition-colors ${
                    i < recentCalls.length - 1 ? "border-b border-neutral-800" : ""
                  }`}
                >
                  <div>
                    <p className="text-white font-medium">{client.client}</p>
                    <p className="text-xs text-neutral-500">{client.calls} calls today</p>
                  </div>
                  <span className="text-xs text-neutral-600">{client.lastCall}</span>
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
