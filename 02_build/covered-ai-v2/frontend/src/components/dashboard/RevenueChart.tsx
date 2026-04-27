'use client';

import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { cn, formatCurrency } from '@/lib/utils';
import type { RevenueTrend } from '@/lib/api';

interface RevenueChartProps {
  data: RevenueTrend | null;
  isLoading?: boolean;
}

export function RevenueChart({ data, isLoading }: RevenueChartProps) {
  if (isLoading) {
    return (
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 animate-pulse">
        <div className="h-6 bg-[var(--grey-100)] rounded w-1/3 mb-4" />
        <div className="h-40 bg-[var(--grey-100)] rounded" />
      </div>
    );
  }

  if (!data || data.data.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
        <h3 className="font-semibold text-[var(--grey-900)] mb-4">Revenue Trend</h3>
        <div className="h-40 flex items-center justify-center text-[var(--grey-400)]">
          No data available
        </div>
      </div>
    );
  }

  // Find max value for scaling
  const maxValue = Math.max(
    ...data.data.map((d) => Math.max(d.billed, d.collected))
  );

  const TrendIcon =
    data.trend_direction === 'up'
      ? TrendingUp
      : data.trend_direction === 'down'
      ? TrendingDown
      : Minus;

  return (
    <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-[var(--grey-900)]">Revenue Trend</h3>
        <div
          className={cn(
            'flex items-center gap-1 text-sm font-medium',
            data.trend_direction === 'up'
              ? 'text-green-600'
              : data.trend_direction === 'down'
              ? 'text-red-600'
              : 'text-[var(--grey-500)]'
          )}
        >
          <TrendIcon className="w-4 h-4" />
          {Math.abs(data.trend_percent)}%
        </div>
      </div>

      {/* Chart */}
      <div className="h-40 flex items-end gap-1">
        {data.data.map((month, index) => {
          const billedHeight = maxValue > 0 ? (month.billed / maxValue) * 100 : 0;
          const collectedHeight = maxValue > 0 ? (month.collected / maxValue) * 100 : 0;

          return (
            <div
              key={index}
              className="flex-1 flex flex-col items-center gap-1 group"
            >
              {/* Bars */}
              <div className="w-full h-32 flex items-end gap-0.5 relative">
                {/* Billed bar */}
                <div
                  className="flex-1 bg-[var(--grey-200)] rounded-t transition-all duration-300 group-hover:bg-[var(--grey-300)]"
                  style={{ height: `${billedHeight}%` }}
                />
                {/* Collected bar */}
                <div
                  className="flex-1 bg-green-500 rounded-t transition-all duration-300 group-hover:bg-green-600"
                  style={{ height: `${collectedHeight}%` }}
                />

                {/* Tooltip */}
                <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-10">
                  <div className="bg-[var(--grey-900)] text-white text-xs rounded px-2 py-1 whitespace-nowrap">
                    <p>Billed: {formatCurrency(month.billed)}</p>
                    <p>Collected: {formatCurrency(month.collected)}</p>
                  </div>
                </div>
              </div>

              {/* Label */}
              <span className="text-xs text-[var(--grey-500)] truncate w-full text-center">
                {month.month.split(' ')[0]}
              </span>
            </div>
          );
        })}
      </div>

      {/* Legend */}
      <div className="flex items-center justify-center gap-4 mt-4 text-xs text-[var(--grey-600)]">
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-[var(--grey-200)] rounded" />
          <span>Billed</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-green-500 rounded" />
          <span>Collected</span>
        </div>
      </div>
    </div>
  );
}
