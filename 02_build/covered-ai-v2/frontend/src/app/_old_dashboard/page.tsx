"use client";

import React from "react";
import { useRouter } from "next/navigation";
import { Header } from "@/components/layout";
import {
  NeedsAttentionFeed,
  StatCard,
  CashHealthBar,
  CustomerSnapshot,
  CashFlowOverview,
  RevenueChart,
  OutstandingInvoicesWidget,
  PaymentForecast,
} from "@/components/dashboard";
import { AiAccuracyCard } from "@/components/dashboard/AiAccuracyCard";
import { useAuthContext } from "@/lib/auth-context";
import { useDashboard, useFinancialSummary, useRevenueTrend, useOutstandingInvoices, usePaymentForecast } from "@/lib/hooks";
import type { AttentionItem as DashboardAttentionItem } from "@/components/dashboard";

// Loading skeleton
function DashboardSkeleton() {
  return (
    <main className="px-4 py-6 space-y-6 pb-24">
      {/* Attention skeleton */}
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 animate-pulse">
        <div className="h-6 bg-[var(--grey-200)] rounded w-1/3 mb-3" />
        <div className="space-y-3">
          <div className="h-16 bg-[var(--grey-100)] rounded" />
          <div className="h-16 bg-[var(--grey-100)] rounded" />
        </div>
      </div>

      {/* Stats skeleton */}
      <div className="grid grid-cols-3 gap-3">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="bg-white rounded-xl border border-[var(--grey-200)] p-4 animate-pulse"
          >
            <div className="h-8 bg-[var(--grey-200)] rounded w-2/3 mx-auto mb-2" />
            <div className="h-4 bg-[var(--grey-100)] rounded w-1/2 mx-auto" />
          </div>
        ))}
      </div>

      {/* Cash health skeleton */}
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 animate-pulse">
        <div className="h-6 bg-[var(--grey-200)] rounded w-1/4 mb-3" />
        <div className="h-3 bg-[var(--grey-100)] rounded mb-2" />
        <div className="h-4 bg-[var(--grey-100)] rounded w-2/3" />
      </div>

      {/* Customer snapshot skeleton */}
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 animate-pulse">
        <div className="h-6 bg-[var(--grey-200)] rounded w-1/3 mb-3" />
        <div className="grid grid-cols-4 gap-2">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-16 bg-[var(--grey-100)] rounded" />
          ))}
        </div>
      </div>
    </main>
  );
}

export default function DashboardPage() {
  const router = useRouter();
  const { client, isLoading: authLoading } = useAuthContext();
  const { data, isLoading, error } = useDashboard(client?.id || null);

  // Financial data hooks
  const { data: financialSummary, isLoading: financialLoading } = useFinancialSummary(client?.id || null);
  const { data: revenueTrend, isLoading: revenueTrendLoading } = useRevenueTrend(client?.id || null, 6);
  const { data: outstandingInvoices, isLoading: outstandingLoading } = useOutstandingInvoices(client?.id || null, 5);
  const { data: paymentForecast, isLoading: forecastLoading } = usePaymentForecast(client?.id || null, 28);

  // Convert API attention items to component format
  const attentionItems: DashboardAttentionItem[] = (data?.attentionItems || []).map((item) => ({
    id: item.id,
    type: item.type,
    title: item.title,
    subtitle: item.subtitle,
    action: {
      label: item.action.label,
      variant: item.action.variant,
      onClick: () => {
        // Handle action based on type
        if (item.action.type === "call" && item.action.data?.phone) {
          window.open(`tel:${item.action.data.phone}`);
        } else if (item.action.type === "chase" && item.action.data?.invoiceId) {
          router.push(`/dashboard/invoices/${item.action.data.invoiceId}`);
        } else if (item.action.type === "view" && item.action.data?.path) {
          router.push(item.action.data.path as string);
        }
      },
    },
  }));

  // Format currency for stats
  const formatCurrency = (amount: number) => {
    if (amount >= 1000) {
      return `£${(amount / 1000).toFixed(1)}k`;
    }
    return `£${amount.toLocaleString()}`;
  };

  // Get trend direction
  const getTrend = (trend: string): "up" | "down" | "stable" | undefined => {
    if (trend === "up" || trend === "down" || trend === "stable") {
      return trend;
    }
    return undefined;
  };

  const ownerName = client?.ownerName?.split(" ")[0] || "there";

  if (authLoading || isLoading) {
    return (
      <>
        <Header greeting title={ownerName} showHelp showSettings />
        <DashboardSkeleton />
      </>
    );
  }

  if (error) {
    return (
      <>
        <Header greeting title={ownerName} showHelp showSettings />
        <main className="px-4 py-6 pb-24">
          <div className="bg-red-50 rounded-xl border border-red-200 p-4 text-center">
            <p className="text-red-700">Failed to load dashboard</p>
            <button
              onClick={() => window.location.reload()}
              className="mt-2 text-sm text-red-600 underline"
            >
              Try again
            </button>
          </div>
        </main>
      </>
    );
  }

  // Use data or fallback to defaults
  const todayStats = data?.todayStats || {
    callsToday: 0,
    callsTrend: "stable",
    revenueThisWeek: 0,
    revenueTrend: "stable",
    reviewsThisWeek: 0,
    reviewsTrend: "stable",
  };

  const cashHealth = data?.cashHealth || {
    collected: 0,
    billed: 0,
    overdue: 0,
    overdueCount: 0,
  };

  const unitEconomics = data?.unitEconomics || {
    totalCustomers: 0,
    repeatRate: 0,
    customerLTV: 0,
    ltvCacRatio: 0,
  };

  return (
    <>
      <Header greeting title={ownerName} showHelp showSettings />
      <main className="px-4 py-6 space-y-6 pb-24">
        <NeedsAttentionFeed items={attentionItems} />

        <section>
          <h2 className="text-sm font-medium text-[var(--grey-500)] mb-3">TODAY</h2>
          <div className="grid grid-cols-3 gap-3">
            <StatCard
              icon="📞"
              value={todayStats.callsToday}
              label="Calls handled"
              trend={getTrend(todayStats.callsTrend)}
            />
            <StatCard
              icon="💷"
              value={formatCurrency(todayStats.revenueThisWeek)}
              label="Coming in"
              trend={getTrend(todayStats.revenueTrend)}
            />
            <StatCard
              icon="⭐"
              value={todayStats.reviewsThisWeek}
              label="New reviews"
              trend={getTrend(todayStats.reviewsTrend)}
            />
          </div>
        </section>

        <CashHealthBar
          collected={cashHealth.collected}
          billed={cashHealth.billed}
          overdue={cashHealth.overdue}
          overdueCount={cashHealth.overdueCount}
        />

        <CustomerSnapshot
          total={unitEconomics.totalCustomers}
          repeatRate={Math.round(unitEconomics.repeatRate * 100)}
          ltv={Math.round(unitEconomics.customerLTV)}
          ltvCacRatio={Math.round(unitEconomics.ltvCacRatio)}
        />

        {/* Financial Dashboard Section */}
        <section>
          <h2 className="text-sm font-medium text-[var(--grey-500)] mb-3">FINANCIALS</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <CashFlowOverview data={financialSummary || null} isLoading={financialLoading} />
            <RevenueChart data={revenueTrend || null} isLoading={revenueTrendLoading} />
            <OutstandingInvoicesWidget
              data={outstandingInvoices || null}
              isLoading={outstandingLoading}
              onChase={(invoiceId) => router.push(`/invoices/${invoiceId}`)}
            />
            <PaymentForecast data={paymentForecast || null} isLoading={forecastLoading} />
          </div>
        </section>

        {client?.id && <AiAccuracyCard clientId={client.id} />}
      </main>
    </>
  );
}
