/**
 * LTV:CAC Widget Component
 *
 * Displays key unit economics metrics:
 * - LTV:CAC Ratio (main metric)
 * - Customer LTV
 * - Average CAC
 * - Repeat Rate
 */

import React from "react";

interface UnitEconomicsMetrics {
  client_id: string;
  total_customers: number;
  repeat_customers: number;
  repeat_rate: number;
  avg_job_value: number;
  avg_jobs_per_customer: number;
  customer_ltv: number;
  total_marketing_spend: number;
  new_customers_this_month: number;
  avg_cac: number;
  ltv_cac_ratio: number;
  ltv_cac_last_month: number;
  ltv_cac_trend: "up" | "down" | "stable";
  calculated_at: string | null;
}

interface LTVCACWidgetProps {
  metrics: UnitEconomicsMetrics | null;
  isLoading?: boolean;
}

export const LTVCACWidget: React.FC<LTVCACWidgetProps> = ({
  metrics,
  isLoading = false,
}) => {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="h-12 bg-gray-200 rounded w-1/2 mb-4"></div>
          <div className="grid grid-cols-3 gap-4">
            <div className="h-16 bg-gray-200 rounded"></div>
            <div className="h-16 bg-gray-200 rounded"></div>
            <div className="h-16 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  const ltvCacRatio = metrics?.ltv_cac_ratio ?? 0;
  const customerLTV = metrics?.customer_ltv ?? 0;
  const avgCAC = metrics?.avg_cac ?? 0;
  const repeatRate = metrics?.repeat_rate ?? 0;
  const trend = metrics?.ltv_cac_trend ?? "stable";
  const totalCustomers = metrics?.total_customers ?? 0;
  const newCustomersThisMonth = metrics?.new_customers_this_month ?? 0;

  // Determine health status
  const getRatioHealth = (ratio: number) => {
    if (ratio >= 3) return { color: "text-green-600", bg: "bg-green-100", label: "Healthy" };
    if (ratio >= 1) return { color: "text-yellow-600", bg: "bg-yellow-100", label: "Needs Work" };
    return { color: "text-red-600", bg: "bg-red-100", label: "At Risk" };
  };

  const health = getRatioHealth(ltvCacRatio);

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case "up":
        return (
          <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
          </svg>
        );
      case "down":
        return (
          <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
          </svg>
        );
      default:
        return (
          <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14" />
          </svg>
        );
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Unit Economics</h3>
        <span className={`px-2 py-1 text-xs font-medium rounded-full ${health.bg} ${health.color}`}>
          {health.label}
        </span>
      </div>

      {/* Main LTV:CAC Ratio */}
      <div className="flex items-center gap-3 mb-6">
        <div className={`text-4xl font-bold ${health.color}`}>
          {ltvCacRatio.toFixed(1)}:1
        </div>
        <div className="flex items-center gap-1">
          {getTrendIcon(trend)}
          <span className="text-sm text-gray-500">
            vs {metrics?.ltv_cac_last_month?.toFixed(1) ?? "0.0"}:1 last month
          </span>
        </div>
      </div>

      {/* Secondary Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-gray-50 rounded-lg p-3">
          <div className="text-sm text-gray-500">Customer LTV</div>
          <div className="text-xl font-semibold text-gray-900">
            £{customerLTV.toFixed(0)}
          </div>
        </div>

        <div className="bg-gray-50 rounded-lg p-3">
          <div className="text-sm text-gray-500">Avg CAC</div>
          <div className="text-xl font-semibold text-gray-900">
            £{avgCAC.toFixed(0)}
          </div>
        </div>

        <div className="bg-gray-50 rounded-lg p-3">
          <div className="text-sm text-gray-500">Repeat Rate</div>
          <div className="text-xl font-semibold text-gray-900">
            {(repeatRate * 100).toFixed(0)}%
          </div>
        </div>

        <div className="bg-gray-50 rounded-lg p-3">
          <div className="text-sm text-gray-500">Total Customers</div>
          <div className="text-xl font-semibold text-gray-900">
            {totalCustomers}
            {newCustomersThisMonth > 0 && (
              <span className="text-sm text-green-600 ml-1">
                +{newCustomersThisMonth}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Calculated timestamp */}
      {metrics?.calculated_at && (
        <div className="mt-4 text-xs text-gray-400 text-right">
          Last calculated: {new Date(metrics.calculated_at).toLocaleDateString("en-GB", {
            day: "numeric",
            month: "short",
            hour: "2-digit",
            minute: "2-digit",
          })}
        </div>
      )}
    </div>
  );
};

export default LTVCACWidget;
