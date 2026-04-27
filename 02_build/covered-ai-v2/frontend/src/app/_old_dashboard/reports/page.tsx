"use client";

import React, { useState } from "react";
import { TrendingUp, TrendingDown, Phone, Briefcase, PoundSterling, Users, Star, FileText, ChevronRight } from "lucide-react";
import Link from "next/link";
import { Header } from "@/components/layout";
import { useAuthContext } from "@/lib/auth-context";
import { useReports } from "@/lib/hooks";
import { cn } from "@/lib/utils";

type TimePeriod = "week" | "month" | "quarter" | "year";

const periodOptions: { value: TimePeriod; label: string }[] = [
  { value: "week", label: "This Week" },
  { value: "month", label: "This Month" },
  { value: "quarter", label: "This Quarter" },
  { value: "year", label: "This Year" },
];

function ReportsSkeleton() {
  return (
    <div className="px-4 py-6 space-y-6 animate-pulse">
      <div className="grid grid-cols-2 gap-3">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
            <div className="h-8 bg-[var(--grey-200)] rounded w-1/2 mb-2" />
            <div className="h-4 bg-[var(--grey-100)] rounded w-2/3" />
          </div>
        ))}
      </div>
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
        <div className="h-40 bg-[var(--grey-100)] rounded" />
      </div>
    </div>
  );
}

interface MetricCardProps {
  icon: React.ReactNode;
  label: string;
  value: string | number;
  change?: number;
  changeLabel?: string;
}

function MetricCard({ icon, label, value, change, changeLabel }: MetricCardProps) {
  const isPositive = change !== undefined && change >= 0;

  return (
    <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
      <div className="flex items-center gap-2 mb-2">
        <div className="w-8 h-8 bg-[var(--brand-primary-light)] rounded-lg flex items-center justify-center text-[var(--brand-primary)]">
          {icon}
        </div>
      </div>
      <p className="text-2xl font-bold text-[var(--grey-900)]">{value}</p>
      <p className="text-xs text-[var(--grey-500)] mt-0.5">{label}</p>
      {change !== undefined && (
        <div
          className={cn(
            "flex items-center gap-1 mt-2 text-xs font-medium",
            isPositive ? "text-green-600" : "text-red-600"
          )}
        >
          {isPositive ? (
            <TrendingUp className="w-3 h-3" />
          ) : (
            <TrendingDown className="w-3 h-3" />
          )}
          <span>
            {isPositive ? "+" : ""}
            {change}% {changeLabel || "vs last period"}
          </span>
        </div>
      )}
    </div>
  );
}

function SimpleBarChart({ data }: { data: { label: string; value: number }[] }) {
  const maxValue = Math.max(...data.map((d) => d.value), 1);

  return (
    <div className="space-y-3">
      {data.map((item, index) => (
        <div key={index}>
          <div className="flex justify-between text-sm mb-1">
            <span className="text-[var(--grey-600)]">{item.label}</span>
            <span className="font-medium text-[var(--grey-900)]">£{item.value.toLocaleString()}</span>
          </div>
          <div className="h-2 bg-[var(--grey-100)] rounded-full overflow-hidden">
            <div
              className="h-full bg-[var(--brand-primary)] rounded-full transition-all duration-300"
              style={{ width: `${(item.value / maxValue) * 100}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}

export default function ReportsPage() {
  const { client } = useAuthContext();
  const [period, setPeriod] = useState<TimePeriod>("month");
  const { data, isLoading, error } = useReports(client?.id || null, period);

  if (isLoading) {
    return (
      <>
        <Header title="Reports" />
        <main className="pb-24">
          <ReportsSkeleton />
        </main>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Header title="Reports" />
        <main className="pb-24 px-4 pt-6">
          <div className="bg-red-50 rounded-xl border border-red-200 p-4 text-center">
            <p className="text-red-700">Failed to load reports</p>
          </div>
        </main>
      </>
    );
  }

  const stats = data?.stats || {
    totalRevenue: 0,
    revenueChange: 0,
    totalJobs: 0,
    jobsChange: 0,
    totalCalls: 0,
    callsChange: 0,
    newCustomers: 0,
    customersChange: 0,
    averageJobValue: 0,
    conversionRate: 0,
  };

  const revenueByWeek = data?.revenueByWeek || [];
  const topServices = data?.topServices || [];

  const formatCurrency = (amount: number) => {
    if (amount >= 1000) {
      return `£${(amount / 1000).toFixed(1)}k`;
    }
    return `£${amount.toLocaleString()}`;
  };

  return (
    <>
      <Header title="Reports" />
      <main className="pb-24">
        {/* Period Selector */}
        <div className="px-4 py-3 flex gap-2 overflow-x-auto bg-[var(--grey-50)] border-b border-[var(--grey-100)]">
          {periodOptions.map((option) => (
            <button
              key={option.value}
              onClick={() => setPeriod(option.value)}
              className={cn(
                "px-4 py-2 text-sm font-medium rounded-lg whitespace-nowrap transition-colors",
                period === option.value
                  ? "bg-white text-[var(--grey-900)] shadow-sm"
                  : "text-[var(--grey-500)] hover:text-[var(--grey-700)]"
              )}
            >
              {option.label}
            </button>
          ))}
        </div>

        <div className="px-4 py-6 space-y-6">
          {/* Financial Reports Link */}
          <Link
            href="/reports/financial"
            className="block bg-gradient-to-r from-[var(--brand-primary)] to-[var(--brand-primary-dark)] rounded-xl p-4 text-white hover:opacity-90 transition-opacity"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
                  <FileText className="w-5 h-5" />
                </div>
                <div>
                  <p className="font-semibold">Financial Reports</p>
                  <p className="text-sm opacity-80">Cash flow, VAT returns, exports</p>
                </div>
              </div>
              <ChevronRight className="w-5 h-5" />
            </div>
          </Link>

          {/* Key Metrics */}
          <section>
            <h2 className="text-sm font-medium text-[var(--grey-500)] mb-3">KEY METRICS</h2>
            <div className="grid grid-cols-2 gap-3">
              <MetricCard
                icon={<PoundSterling className="w-4 h-4" />}
                label="Revenue"
                value={formatCurrency(stats.totalRevenue)}
                change={stats.revenueChange}
              />
              <MetricCard
                icon={<Briefcase className="w-4 h-4" />}
                label="Jobs Completed"
                value={stats.totalJobs}
                change={stats.jobsChange}
              />
              <MetricCard
                icon={<Phone className="w-4 h-4" />}
                label="Calls Answered"
                value={stats.totalCalls}
                change={stats.callsChange}
              />
              <MetricCard
                icon={<Users className="w-4 h-4" />}
                label="New Customers"
                value={stats.newCustomers}
                change={stats.customersChange}
              />
            </div>
          </section>

          {/* Additional Stats */}
          <section>
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
                <p className="text-sm text-[var(--grey-500)]">Avg Job Value</p>
                <p className="text-xl font-bold text-[var(--grey-900)] mt-1">
                  {formatCurrency(stats.averageJobValue)}
                </p>
              </div>
              <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
                <p className="text-sm text-[var(--grey-500)]">Call → Job Rate</p>
                <p className="text-xl font-bold text-[var(--grey-900)] mt-1">
                  {Math.round(stats.conversionRate * 100)}%
                </p>
              </div>
            </div>
          </section>

          {/* Revenue Chart */}
          {revenueByWeek.length > 0 && (
            <section>
              <h2 className="text-sm font-medium text-[var(--grey-500)] mb-3">REVENUE BY WEEK</h2>
              <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
                <SimpleBarChart
                  data={revenueByWeek.map((item) => ({
                    label: item.week,
                    value: item.revenue,
                  }))}
                />
              </div>
            </section>
          )}

          {/* Top Services */}
          {topServices.length > 0 && (
            <section>
              <h2 className="text-sm font-medium text-[var(--grey-500)] mb-3">TOP SERVICES</h2>
              <div className="bg-white rounded-xl border border-[var(--grey-200)] divide-y divide-[var(--grey-100)]">
                {topServices.map((service, index) => (
                  <div key={index} className="px-4 py-3 flex items-center justify-between">
                    <div>
                      <p className="font-medium text-[var(--grey-900)]">{service.name}</p>
                      <p className="text-sm text-[var(--grey-500)]">{service.count} jobs</p>
                    </div>
                    <p className="font-medium text-[var(--grey-700)]">
                      {formatCurrency(service.revenue)}
                    </p>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Gemma Performance */}
          <section>
            <h2 className="text-sm font-medium text-[var(--grey-500)] mb-3">GEMMA PERFORMANCE</h2>
            <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-[var(--brand-primary-light)] rounded-full flex items-center justify-center">
                    <Phone className="w-5 h-5 text-[var(--brand-primary)]" />
                  </div>
                  <div>
                    <p className="font-medium text-[var(--grey-900)]">Calls Answered</p>
                    <p className="text-sm text-[var(--grey-500)]">24/7 availability</p>
                  </div>
                </div>
                <p className="text-xl font-bold text-[var(--grey-900)]">{stats.totalCalls}</p>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                    <TrendingUp className="w-5 h-5 text-green-600" />
                  </div>
                  <div>
                    <p className="font-medium text-[var(--grey-900)]">Lead Conversion</p>
                    <p className="text-sm text-[var(--grey-500)]">Calls that became jobs</p>
                  </div>
                </div>
                <p className="text-xl font-bold text-[var(--grey-900)]">
                  {Math.round(stats.conversionRate * 100)}%
                </p>
              </div>
            </div>
          </section>
        </div>
      </main>
    </>
  );
}
