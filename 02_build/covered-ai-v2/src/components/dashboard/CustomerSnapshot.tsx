/**
 * CustomerSnapshot Component
 *
 * Shows customer/LTV metrics:
 * - Total customers (with vertical-aware label)
 * - Repeat rate
 * - Customer LTV
 * - LTV:CAC ratio with trend
 * - Insight text
 */

import React from "react";

interface CustomerData {
  total_customers: number;
  repeat_customers: number;
  repeat_rate: number;
  customer_ltv: number;
  avg_cac: number;
  ltv_cac_ratio: number;
  ltv_cac_trend: "up" | "down" | "stable";
  insight: string;
}

interface Terminology {
  customer: string;
  customers: string;
}

interface CustomerSnapshotProps {
  data: CustomerData;
  terminology: Terminology;
  isLoading?: boolean;
}

export const CustomerSnapshot: React.FC<CustomerSnapshotProps> = ({
  data,
  terminology,
  isLoading = false,
}) => {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-4">
        <div className="h-5 bg-gray-200 rounded w-32 animate-pulse mb-4"></div>
        <div className="grid grid-cols-2 gap-4 mb-4">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-16 bg-gray-100 rounded animate-pulse"></div>
          ))}
        </div>
        <div className="h-12 bg-gray-100 rounded animate-pulse"></div>
      </div>
    );
  }

  const getTrendIcon = (trend: string) => {
    if (trend === "up") {
      return (
        <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
        </svg>
      );
    }
    if (trend === "down") {
      return (
        <svg className="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
        </svg>
      );
    }
    return (
      <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14" />
      </svg>
    );
  };

  const getRatioColor = (ratio: number) => {
    if (ratio >= 3) return "text-green-600";
    if (ratio >= 1) return "text-yellow-600";
    return "text-red-600";
  };

  const capitalizedCustomers = terminology.customers.charAt(0).toUpperCase() + terminology.customers.slice(1);

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      {/* Header */}
      <div className="p-4 pb-3">
        <div className="flex items-center gap-2 mb-4">
          <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <h3 className="font-semibold text-gray-900">{capitalizedCustomers}</h3>
        </div>

        {/* Metrics grid */}
        <div className="grid grid-cols-2 gap-3">
          {/* Total customers */}
          <div className="bg-gray-50 rounded-lg p-3">
            <div className="text-2xl font-bold text-gray-900">{data.total_customers}</div>
            <div className="text-xs text-gray-500">Total {terminology.customers}</div>
          </div>

          {/* Repeat rate */}
          <div className="bg-gray-50 rounded-lg p-3">
            <div className="text-2xl font-bold text-gray-900">
              {(data.repeat_rate * 100).toFixed(0)}%
            </div>
            <div className="text-xs text-gray-500">Repeat rate</div>
          </div>

          {/* Customer LTV */}
          <div className="bg-gray-50 rounded-lg p-3">
            <div className="text-2xl font-bold text-gray-900">
              £{data.customer_ltv.toFixed(0)}
            </div>
            <div className="text-xs text-gray-500">{terminology.customer.charAt(0).toUpperCase() + terminology.customer.slice(1)} LTV</div>
          </div>

          {/* LTV:CAC */}
          <div className="bg-gray-50 rounded-lg p-3">
            <div className="flex items-center gap-2">
              <span className={`text-2xl font-bold ${getRatioColor(data.ltv_cac_ratio)}`}>
                {data.ltv_cac_ratio.toFixed(1)}:1
              </span>
              {getTrendIcon(data.ltv_cac_trend)}
            </div>
            <div className="text-xs text-gray-500">LTV:CAC</div>
          </div>
        </div>
      </div>

      {/* Insight */}
      <div className="px-4 py-3 bg-purple-50 border-t border-purple-100">
        <div className="flex items-start gap-2">
          <svg className="w-4 h-4 text-purple-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
          <p className="text-sm text-purple-700">{data.insight}</p>
        </div>
      </div>
    </div>
  );
};

export default CustomerSnapshot;
