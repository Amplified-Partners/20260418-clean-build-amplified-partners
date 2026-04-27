'use client';

import { useRouter } from 'next/navigation';
import { AlertCircle, ChevronRight, Clock, CheckCircle } from 'lucide-react';
import { cn, formatCurrency } from '@/lib/utils';
import { Button } from '@/components/ui';
import type { OutstandingInvoices, OutstandingInvoice } from '@/lib/api';

interface OutstandingInvoicesWidgetProps {
  data: OutstandingInvoices | null;
  isLoading?: boolean;
  onChase?: (invoiceId: string) => void;
}

export function OutstandingInvoicesWidget({
  data,
  isLoading,
  onChase,
}: OutstandingInvoicesWidgetProps) {
  const router = useRouter();

  if (isLoading) {
    return (
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 animate-pulse">
        <div className="h-6 bg-[var(--grey-100)] rounded w-1/2 mb-4" />
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-16 bg-[var(--grey-100)] rounded" />
          ))}
        </div>
      </div>
    );
  }

  if (!data || data.invoices.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
        <h3 className="font-semibold text-[var(--grey-900)] mb-4">
          Outstanding Invoices
        </h3>
        <div className="text-center py-6">
          <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-3" />
          <p className="text-[var(--grey-600)]">All invoices are paid!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-[var(--grey-900)]">
          Outstanding Invoices
        </h3>
        <span className="text-sm font-medium text-[var(--brand-primary)]">
          {formatCurrency(data.total_outstanding)}
        </span>
      </div>

      {/* Invoice List */}
      <div className="space-y-2">
        {data.invoices.map((invoice) => (
          <InvoiceRow
            key={invoice.id}
            invoice={invoice}
            onChase={() => onChase?.(invoice.id)}
            onClick={() => router.push(`/invoices/${invoice.id}`)}
          />
        ))}
      </div>

      {/* View All Link */}
      {data.count > data.invoices.length && (
        <button
          onClick={() => router.push('/invoices?status=outstanding')}
          className="w-full mt-4 text-sm text-[var(--brand-primary)] hover:underline flex items-center justify-center gap-1"
        >
          View all {data.count} invoices
          <ChevronRight className="w-4 h-4" />
        </button>
      )}
    </div>
  );
}

interface InvoiceRowProps {
  invoice: OutstandingInvoice;
  onChase: () => void;
  onClick: () => void;
}

function InvoiceRow({ invoice, onChase, onClick }: InvoiceRowProps) {
  const getUrgencyStyles = () => {
    switch (invoice.urgency) {
      case 'overdue':
        return 'bg-red-50 border-red-200';
      case 'due_soon':
        return 'bg-amber-50 border-amber-200';
      default:
        return 'bg-white border-[var(--grey-200)]';
    }
  };

  const getDueText = () => {
    if (invoice.urgency === 'overdue') {
      return `${Math.abs(invoice.days_until_due)} days overdue`;
    } else if (invoice.days_until_due === 0) {
      return 'Due today';
    } else if (invoice.days_until_due === 1) {
      return 'Due tomorrow';
    } else {
      return `Due in ${invoice.days_until_due} days`;
    }
  };

  return (
    <div
      className={cn(
        'p-3 rounded-lg border cursor-pointer hover:shadow-sm transition-shadow',
        getUrgencyStyles()
      )}
      onClick={onClick}
    >
      <div className="flex items-center justify-between">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span className="font-medium text-[var(--grey-900)] text-sm">
              {invoice.invoice_number}
            </span>
            {invoice.urgency === 'overdue' && (
              <AlertCircle className="w-4 h-4 text-red-500" />
            )}
            {invoice.urgency === 'due_soon' && (
              <Clock className="w-4 h-4 text-amber-500" />
            )}
          </div>
          <p className="text-sm text-[var(--grey-600)] truncate">
            {invoice.customer_name}
          </p>
          <p
            className={cn(
              'text-xs mt-1',
              invoice.urgency === 'overdue'
                ? 'text-red-600'
                : invoice.urgency === 'due_soon'
                ? 'text-amber-600'
                : 'text-[var(--grey-500)]'
            )}
          >
            {getDueText()}
          </p>
        </div>

        <div className="text-right pl-4">
          <p className="font-semibold text-[var(--grey-900)]">
            {formatCurrency(invoice.amount)}
          </p>
          {invoice.urgency === 'overdue' && !invoice.final_notice_sent && (
            <Button
              size="sm"
              variant="secondary"
              onClick={(e) => {
                e.stopPropagation();
                onChase();
              }}
              className="mt-1 text-xs"
            >
              Chase
            </Button>
          )}
        </div>
      </div>

      {/* Reminder indicators */}
      <div className="flex items-center gap-2 mt-2">
        <span
          className={cn(
            'text-xs px-2 py-0.5 rounded-full',
            invoice.reminder1_sent
              ? 'bg-amber-100 text-amber-700'
              : 'bg-[var(--grey-100)] text-[var(--grey-400)]'
          )}
        >
          R1
        </span>
        <span
          className={cn(
            'text-xs px-2 py-0.5 rounded-full',
            invoice.reminder2_sent
              ? 'bg-orange-100 text-orange-700'
              : 'bg-[var(--grey-100)] text-[var(--grey-400)]'
          )}
        >
          R2
        </span>
        <span
          className={cn(
            'text-xs px-2 py-0.5 rounded-full',
            invoice.final_notice_sent
              ? 'bg-red-100 text-red-700'
              : 'bg-[var(--grey-100)] text-[var(--grey-400)]'
          )}
        >
          Final
        </span>
      </div>
    </div>
  );
}
