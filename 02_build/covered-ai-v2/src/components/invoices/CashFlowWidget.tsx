/**
 * Cash Flow Widget Component
 *
 * Displays 4 key metrics:
 * - Total Outstanding
 * - Total Overdue (red)
 * - Collected This Month (green)
 * - Average DSO (Days Sales Outstanding)
 */

import React from "react";

interface CashMetrics {
  totalOutstanding: number;
  totalOverdue: number;
  collectedThisMonth: number;
  collectedLastMonth: number;
  averageDSO: number;
}

interface CashFlowWidgetProps {
  metrics: CashMetrics;
  loading?: boolean;
}

const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency: "GBP",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
};

const MetricCard: React.FC<{
  title: string;
  value: string;
  subtitle?: string;
  variant?: "default" | "success" | "danger" | "warning";
  loading?: boolean;
}> = ({ title, value, subtitle, variant = "default", loading }) => {
  const variantClasses = {
    default: "bg-white border-gray-200",
    success: "bg-green-50 border-green-200",
    danger: "bg-red-50 border-red-200",
    warning: "bg-amber-50 border-amber-200",
  };

  const valueClasses = {
    default: "text-gray-900",
    success: "text-green-700",
    danger: "text-red-700",
    warning: "text-amber-700",
  };

  return (
    <div
      className={`rounded-lg border p-4 ${variantClasses[variant]} transition-all hover:shadow-md`}
    >
      <p className="text-sm font-medium text-gray-600">{title}</p>
      {loading ? (
        <div className="mt-2 h-8 w-24 animate-pulse rounded bg-gray-200" />
      ) : (
        <>
          <p className={`mt-1 text-2xl font-bold ${valueClasses[variant]}`}>
            {value}
          </p>
          {subtitle && (
            <p className="mt-1 text-xs text-gray-500">{subtitle}</p>
          )}
        </>
      )}
    </div>
  );
};

export const CashFlowWidget: React.FC<CashFlowWidgetProps> = ({
  metrics,
  loading = false,
}) => {
  const monthChange = metrics.collectedThisMonth - metrics.collectedLastMonth;
  const monthChangePercent =
    metrics.collectedLastMonth > 0
      ? ((monthChange / metrics.collectedLastMonth) * 100).toFixed(0)
      : 0;

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold text-gray-900">Cash Flow</h2>
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <MetricCard
          title="Total Outstanding"
          value={formatCurrency(metrics.totalOutstanding)}
          subtitle="Unpaid invoices"
          variant="default"
          loading={loading}
        />
        <MetricCard
          title="Total Overdue"
          value={formatCurrency(metrics.totalOverdue)}
          subtitle="Past due date"
          variant={metrics.totalOverdue > 0 ? "danger" : "default"}
          loading={loading}
        />
        <MetricCard
          title="Collected This Month"
          value={formatCurrency(metrics.collectedThisMonth)}
          subtitle={
            monthChange >= 0
              ? `+${monthChangePercent}% vs last month`
              : `${monthChangePercent}% vs last month`
          }
          variant="success"
          loading={loading}
        />
        <MetricCard
          title="Avg. Days to Pay"
          value={`${metrics.averageDSO} days`}
          subtitle="DSO (Days Sales Outstanding)"
          variant={metrics.averageDSO > 30 ? "warning" : "default"}
          loading={loading}
        />
      </div>
    </div>
  );
};

export default CashFlowWidget;
