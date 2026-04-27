'use client';

import { TrendingUp, TrendingDown, AlertTriangle } from 'lucide-react';
import { cn, formatCurrency } from '@/lib/utils';
import type { FinancialSummary } from '@/lib/api';

interface CashFlowOverviewProps {
  data: FinancialSummary | null;
  isLoading?: boolean;
}

export function CashFlowOverview({ data, isLoading }: CashFlowOverviewProps) {
  if (isLoading) {
    return (
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 animate-pulse">
        <div className="h-6 bg-[var(--grey-100)] rounded w-1/3 mb-4" />
        <div className="h-4 bg-[var(--grey-100)] rounded w-full mb-3" />
        <div className="grid grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-16 bg-[var(--grey-100)] rounded" />
          ))}
        </div>
      </div>
    );
  }

  if (!data) return null;

  const collectionPercent = data.total_billed > 0
    ? (data.total_collected / data.total_billed) * 100
    : 0;

  return (
    <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-[var(--grey-900)]">Cash Flow</h3>
        <span className="text-sm text-[var(--grey-500)]">
          {data.invoice_count} invoice{data.invoice_count !== 1 && 's'}
        </span>
      </div>

      {/* Progress Bar */}
      <div className="mb-4">
        <div className="flex items-center justify-between text-sm mb-1">
          <span className="text-[var(--grey-600)]">Collection Rate</span>
          <span className="font-medium text-[var(--grey-900)]">
            {data.collection_rate.toFixed(1)}%
          </span>
        </div>
        <div className="h-3 bg-[var(--grey-100)] rounded-full overflow-hidden">
          <div
            className={cn(
              "h-full rounded-full transition-all duration-500",
              collectionPercent >= 80
                ? "bg-green-500"
                : collectionPercent >= 50
                ? "bg-amber-500"
                : "bg-red-500"
            )}
            style={{ width: `${Math.min(collectionPercent, 100)}%` }}
          />
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-3 gap-4">
        <div className="text-center">
          <p className="text-xs text-[var(--grey-500)] mb-1">Billed</p>
          <p className="text-lg font-semibold text-[var(--grey-900)]">
            {formatCurrency(data.total_billed)}
          </p>
        </div>
        <div className="text-center">
          <p className="text-xs text-[var(--grey-500)] mb-1">Collected</p>
          <p className="text-lg font-semibold text-green-600">
            {formatCurrency(data.total_collected)}
          </p>
        </div>
        <div className="text-center">
          <p className="text-xs text-[var(--grey-500)] mb-1">Outstanding</p>
          <p className="text-lg font-semibold text-[var(--grey-900)]">
            {formatCurrency(data.total_outstanding)}
          </p>
        </div>
      </div>

      {/* Overdue Warning */}
      {data.total_overdue > 0 && (
        <div className="mt-4 p-3 bg-red-50 rounded-lg flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-red-600" />
          <span className="text-sm text-red-700">
            {formatCurrency(data.total_overdue)} overdue ({data.overdue_count} invoice{data.overdue_count !== 1 && 's'})
          </span>
        </div>
      )}
    </div>
  );
}
