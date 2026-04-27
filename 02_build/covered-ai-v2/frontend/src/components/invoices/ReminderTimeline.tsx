'use client';

import { CheckCircle, Clock, AlertTriangle, XCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

interface TimelineStep {
  label: string;
  date?: string | null;
  status: 'completed' | 'current' | 'upcoming' | 'skipped';
}

interface ReminderTimelineProps {
  sentAt: string | null;
  dueDate: string;
  reminder1SentAt: string | null;
  reminder2SentAt: string | null;
  finalNoticeSentAt: string | null;
  status: string;
}

export function ReminderTimeline({
  sentAt,
  dueDate,
  reminder1SentAt,
  reminder2SentAt,
  finalNoticeSentAt,
  status,
}: ReminderTimelineProps) {
  const isPaid = status === 'PAID';
  const isCancelled = status === 'CANCELLED' || status === 'WRITTEN_OFF';

  // Build timeline steps
  const steps: TimelineStep[] = [
    {
      label: 'Invoice Sent',
      date: sentAt,
      status: sentAt ? 'completed' : 'upcoming',
    },
    {
      label: 'Due Date',
      date: dueDate,
      status: isPaid || new Date() < new Date(dueDate) ? 'completed' : 'current',
    },
    {
      label: 'Reminder 1',
      date: reminder1SentAt,
      status: reminder1SentAt ? 'completed' : isPaid ? 'skipped' : 'upcoming',
    },
    {
      label: 'Reminder 2',
      date: reminder2SentAt,
      status: reminder2SentAt ? 'completed' : isPaid ? 'skipped' : 'upcoming',
    },
    {
      label: 'Final Notice',
      date: finalNoticeSentAt,
      status: finalNoticeSentAt ? 'completed' : isPaid ? 'skipped' : 'upcoming',
    },
  ];

  if (isPaid) {
    steps.push({
      label: 'Paid',
      date: null,
      status: 'completed',
    });
  }

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return null;
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-GB', {
      day: 'numeric',
      month: 'short',
    });
  };

  const getStepIcon = (step: TimelineStep, index: number) => {
    if (step.status === 'completed') {
      return (
        <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center">
          <CheckCircle className="w-4 h-4 text-green-600" />
        </div>
      );
    }
    if (step.status === 'current') {
      return (
        <div className="w-8 h-8 rounded-full bg-amber-100 flex items-center justify-center">
          <AlertTriangle className="w-4 h-4 text-amber-600" />
        </div>
      );
    }
    if (step.status === 'skipped') {
      return (
        <div className="w-8 h-8 rounded-full bg-[var(--grey-100)] flex items-center justify-center">
          <div className="w-3 h-3 rounded-full bg-[var(--grey-300)]" />
        </div>
      );
    }
    return (
      <div className="w-8 h-8 rounded-full bg-[var(--grey-100)] flex items-center justify-center">
        <Clock className="w-4 h-4 text-[var(--grey-400)]" />
      </div>
    );
  };

  return (
    <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
      <h4 className="font-medium text-[var(--grey-900)] mb-4">Payment Timeline</h4>

      <div className="space-y-0">
        {steps.map((step, index) => (
          <div key={step.label} className="flex items-start">
            {/* Icon */}
            <div className="flex flex-col items-center mr-3">
              {getStepIcon(step, index)}
              {index < steps.length - 1 && (
                <div
                  className={cn(
                    'w-0.5 h-8',
                    step.status === 'completed'
                      ? 'bg-green-200'
                      : 'bg-[var(--grey-200)]'
                  )}
                />
              )}
            </div>

            {/* Content */}
            <div className="flex-1 pb-4">
              <p
                className={cn(
                  'font-medium text-sm',
                  step.status === 'completed'
                    ? 'text-[var(--grey-900)]'
                    : step.status === 'current'
                    ? 'text-amber-700'
                    : 'text-[var(--grey-500)]'
                )}
              >
                {step.label}
              </p>
              {step.date && (
                <p className="text-xs text-[var(--grey-500)]">
                  {formatDate(step.date)}
                </p>
              )}
              {step.status === 'skipped' && (
                <p className="text-xs text-[var(--grey-400)] italic">Skipped</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ReminderTimeline;
