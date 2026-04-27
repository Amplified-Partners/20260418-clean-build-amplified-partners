'use client';

import { Calendar } from 'lucide-react';
import { formatCurrency } from '@/lib/utils';
import type { PaymentForecast as PaymentForecastType } from '@/lib/api';

interface PaymentForecastProps {
  data: PaymentForecastType | null;
  isLoading?: boolean;
}

export function PaymentForecast({ data, isLoading }: PaymentForecastProps) {
  if (isLoading) {
    return (
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 animate-pulse">
        <div className="h-6 bg-[var(--grey-100)] rounded w-1/2 mb-4" />
        <div className="space-y-2">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-10 bg-[var(--grey-100)] rounded" />
          ))}
        </div>
      </div>
    );
  }

  if (!data) return null;

  // Find max amount for scaling
  const maxAmount = Math.max(...data.weeks.map((w) => w.expected_amount));

  return (
    <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-[var(--grey-900)]">
          Payment Forecast
        </h3>
        <span className="text-sm text-[var(--grey-500)]">
          Next {data.days} days
        </span>
      </div>

      {/* Total */}
      <div className="mb-4 p-3 bg-[var(--brand-primary-light)] rounded-lg">
        <div className="flex items-center gap-2 mb-1">
          <Calendar className="w-4 h-4 text-[var(--brand-primary)]" />
          <span className="text-sm text-[var(--brand-primary)]">Expected</span>
        </div>
        <p className="text-2xl font-bold text-[var(--brand-primary)]">
          {formatCurrency(data.total_expected)}
        </p>
      </div>

      {/* Weekly Breakdown */}
      <div className="space-y-2">
        {data.weeks.map((week, index) => {
          const barWidth =
            maxAmount > 0 ? (week.expected_amount / maxAmount) * 100 : 0;

          return (
            <div key={index} className="group">
              <div className="flex items-center justify-between text-sm mb-1">
                <span className="text-[var(--grey-600)]">{week.week}</span>
                <span className="font-medium text-[var(--grey-900)]">
                  {formatCurrency(week.expected_amount)}
                </span>
              </div>
              <div className="h-2 bg-[var(--grey-100)] rounded-full overflow-hidden">
                <div
                  className="h-full bg-[var(--brand-primary)] rounded-full transition-all duration-300"
                  style={{ width: `${barWidth}%` }}
                />
              </div>
              {week.invoice_count > 0 && (
                <p className="text-xs text-[var(--grey-400)] mt-0.5">
                  {week.invoice_count} invoice{week.invoice_count !== 1 && 's'}
                </p>
              )}
            </div>
          );
        })}
      </div>

      {/* Empty State */}
      {data.total_expected === 0 && (
        <div className="text-center py-4 text-[var(--grey-400)] text-sm">
          No payments expected in this period
        </div>
      )}
    </div>
  );
}
