/**
 * CashHealthBar Component
 *
 * Visual progress bar showing cash health with traffic light colors:
 * - Green: >= 80% (healthy)
 * - Yellow: 60-79% (warning)
 * - Red: < 60% (critical)
 *
 * Also shows overdue warning and 30-day forecast.
 */

import React from "react";

interface CashHealth {
  collected_this_month: number;
  total_outstanding: number;
  total_overdue: number;
  health_percent: number;
  health_status: "green" | "yellow" | "red";
  average_dso: number;
  forecast_30_day: number;
}

interface CashHealthBarProps {
  cash: CashHealth;
  isLoading?: boolean;
}

const STATUS_CONFIG = {
  green: {
    bg: "bg-green-500",
    text: "text-green-700",
    label: "Healthy",
    bgLight: "bg-green-50",
  },
  yellow: {
    bg: "bg-yellow-500",
    text: "text-yellow-700",
    label: "Needs Attention",
    bgLight: "bg-yellow-50",
  },
  red: {
    bg: "bg-red-500",
    text: "text-red-700",
    label: "Critical",
    bgLight: "bg-red-50",
  },
};

export const CashHealthBar: React.FC<CashHealthBarProps> = ({
  cash,
  isLoading = false,
}) => {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-4">
        <div className="h-4 bg-gray-200 rounded w-24 animate-pulse mb-3"></div>
        <div className="h-3 bg-gray-200 rounded-full w-full animate-pulse mb-3"></div>
        <div className="grid grid-cols-3 gap-2">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="h-12 bg-gray-100 rounded animate-pulse"></div>
          ))}
        </div>
      </div>
    );
  }

  const config = STATUS_CONFIG[cash.health_status];
  const hasOverdue = cash.total_overdue > 0;

  return (
    <div className={`bg-white rounded-lg shadow overflow-hidden`}>
      {/* Header */}
      <div className="p-4 pb-3">
        <div className="flex justify-between items-center mb-3">
          <div className="flex items-center gap-2">
            <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 className="font-semibold text-gray-900">Cash Health</h3>
          </div>
          <span className={`px-2 py-1 text-xs font-medium rounded-full ${config.bgLight} ${config.text}`}>
            {config.label}
          </span>
        </div>

        {/* Progress bar */}
        <div className="relative">
          <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
            <div
              className={`h-full ${config.bg} transition-all duration-500`}
              style={{ width: `${cash.health_percent}%` }}
            />
          </div>
          <div className="flex justify-between mt-1 text-xs text-gray-400">
            <span>0%</span>
            <span className="font-medium text-gray-600">{cash.health_percent}%</span>
            <span>100%</span>
          </div>
        </div>
      </div>

      {/* Metrics grid */}
      <div className="grid grid-cols-3 divide-x divide-gray-100 border-t">
        <div className="p-3 text-center">
          <div className="text-lg font-semibold text-green-600">
            £{cash.collected_this_month.toLocaleString("en-GB", { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
          </div>
          <div className="text-xs text-gray-500">Collected</div>
        </div>
        <div className="p-3 text-center">
          <div className="text-lg font-semibold text-gray-700">
            £{cash.total_outstanding.toLocaleString("en-GB", { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
          </div>
          <div className="text-xs text-gray-500">Outstanding</div>
        </div>
        <div className="p-3 text-center">
          <div className={`text-lg font-semibold ${hasOverdue ? "text-red-600" : "text-gray-400"}`}>
            £{cash.total_overdue.toLocaleString("en-GB", { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
          </div>
          <div className="text-xs text-gray-500">Overdue</div>
        </div>
      </div>

      {/* Overdue warning */}
      {hasOverdue && (
        <div className="bg-red-50 px-4 py-2 border-t border-red-100">
          <div className="flex items-center gap-2 text-sm text-red-700">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <span>
              <strong>£{cash.total_overdue.toLocaleString()}</strong> overdue - chase today
            </span>
          </div>
        </div>
      )}

      {/* Footer with DSO and forecast */}
      <div className="px-4 py-2 bg-gray-50 border-t flex justify-between text-xs text-gray-500">
        <span>Avg DSO: <strong className="text-gray-700">{cash.average_dso} days</strong></span>
        <span>30-day forecast: <strong className="text-green-600">£{cash.forecast_30_day.toLocaleString()}</strong></span>
      </div>
    </div>
  );
};

export default CashHealthBar;
