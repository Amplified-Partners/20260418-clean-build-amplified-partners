/**
 * Covered AI - Client App Components
 * 
 * Built with love, designed to be loved.
 * Following principles from Norman, Krug, Walter, Fogg, and Rams.
 */

"use client";

import React from "react";
import { cn } from "@/lib/utils";

// =============================================================================
// SMART GREETING
// Shows contextual, warm greeting based on time and status
// =============================================================================

interface SmartGreetingProps {
  ownerName: string;
  callsHandled: number;
  hasUrgent: boolean;
  hasWin?: {
    type: "review" | "payment" | "booking";
    text: string;
  };
}

function getGreeting(hour: number): string {
  if (hour < 12) return "Good morning";
  if (hour < 17) return "Good afternoon";
  return "Good evening";
}

function getMessage(calls: number, hasUrgent: boolean): string {
  if (hasUrgent) {
    return "You've got something that needs your attention.";
  }
  if (calls === 0) {
    return "Quiet day so far. Gemma's ready when the calls come in.";
  }
  if (calls === 1) {
    return "Gemma handled 1 call while you were busy.";
  }
  return `Gemma handled ${calls} calls while you were busy.`;
}

export function SmartGreeting({ 
  ownerName, 
  callsHandled, 
  hasUrgent,
}: SmartGreetingProps) {
  const hour = new Date().getHours();
  const firstName = ownerName?.split(" ")[0] || "there";
  
  return (
    <div className="px-5 pt-6 pb-2">
      <h1 className="text-2xl font-semibold text-neutral-900">
        {getGreeting(hour)}, {firstName} 👋
      </h1>
      <p className="text-neutral-500 mt-1">
        {getMessage(callsHandled, hasUrgent)}
      </p>
    </div>
  );
}


// =============================================================================
// ALL CLEAR CARD
// Positive reinforcement when nothing needs attention
// =============================================================================

export function AllClearCard() {
  return (
    <div className="mx-5 p-6 bg-emerald-50 rounded-2xl border border-emerald-100 text-center">
      <div className="w-12 h-12 mx-auto mb-3 bg-emerald-100 rounded-full flex items-center justify-center">
        <span className="text-2xl">✓</span>
      </div>
      <h2 className="text-lg font-semibold text-emerald-900">All clear</h2>
      <p className="text-sm text-emerald-700 mt-1">
        Nothing needs your attention right now
      </p>
    </div>
  );
}


// =============================================================================
// URGENT CARD
// Single urgent item, prominent and actionable
// =============================================================================

interface UrgentCardProps {
  type: "emergency" | "callback" | "overdue";
  title: string;
  subtitle: string;
  timeAgo?: string;
  onAction: () => void;
  actionLabel: string;
}

const urgentConfig = {
  emergency: {
    icon: "⚡",
    label: "EMERGENCY",
    bgColor: "bg-red-50",
    borderColor: "border-red-200",
    labelColor: "text-red-700",
    buttonColor: "bg-red-600 hover:bg-red-700",
  },
  callback: {
    icon: "📞",
    label: "CALLBACK NEEDED",
    bgColor: "bg-amber-50",
    borderColor: "border-amber-200",
    labelColor: "text-amber-700",
    buttonColor: "bg-amber-500 hover:bg-amber-600",
  },
  overdue: {
    icon: "💷",
    label: "PAYMENT OVERDUE",
    bgColor: "bg-orange-50",
    borderColor: "border-orange-200",
    labelColor: "text-orange-700",
    buttonColor: "bg-orange-500 hover:bg-orange-600",
  },
};

export function UrgentCard({
  type,
  title,
  subtitle,
  timeAgo,
  onAction,
  actionLabel,
}: UrgentCardProps) {
  const config = urgentConfig[type];
  
  return (
    <div className={cn(
      "mx-5 p-4 rounded-2xl border",
      config.bgColor,
      config.borderColor
    )}>
      <div className="flex items-center gap-2 mb-3">
        <span className="text-lg">{config.icon}</span>
        <span className={cn("text-xs font-semibold tracking-wide", config.labelColor)}>
          {config.label}
        </span>
        {timeAgo && (
          <span className="text-xs text-neutral-500 ml-auto">{timeAgo}</span>
        )}
      </div>
      
      <h3 className="font-semibold text-neutral-900">{title}</h3>
      <p className="text-sm text-neutral-600 mt-1">{subtitle}</p>
      
      <button
        onClick={onAction}
        className={cn(
          "mt-4 w-full py-3 px-4 rounded-xl text-white font-medium transition-colors",
          config.buttonColor
        )}
      >
        {actionLabel}
      </button>
    </div>
  );
}


// =============================================================================
// WIN CARD
// Celebrate positive moments
// =============================================================================

interface WinCardProps {
  type: "review" | "payment" | "booking" | "milestone";
  title: string;
  description: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}

const winConfig = {
  review: { icon: "⭐", bgColor: "bg-amber-50", borderColor: "border-amber-100" },
  payment: { icon: "💰", bgColor: "bg-emerald-50", borderColor: "border-emerald-100" },
  booking: { icon: "📅", bgColor: "bg-blue-50", borderColor: "border-blue-100" },
  milestone: { icon: "🎉", bgColor: "bg-purple-50", borderColor: "border-purple-100" },
};

export function WinCard({ type, title, description, action }: WinCardProps) {
  const config = winConfig[type];
  
  return (
    <div className={cn(
      "mx-5 p-4 rounded-2xl border",
      config.bgColor,
      config.borderColor
    )}>
      <div className="flex items-start gap-3">
        <span className="text-2xl">{config.icon}</span>
        <div className="flex-1 min-w-0">
          <h3 className="font-medium text-neutral-900">{title}</h3>
          <p className="text-sm text-neutral-600 mt-0.5">{description}</p>
          
          {action && (
            <button
              onClick={action.onClick}
              className="mt-2 text-sm font-medium text-blue-600 hover:text-blue-700"
            >
              {action.label} →
            </button>
          )}
        </div>
      </div>
    </div>
  );
}


// =============================================================================
// CALLBACKS SUMMARY
// Quick overview of pending callbacks
// =============================================================================

interface CallbacksSummaryProps {
  count: number;
  oldestAge: string;
  onClick: () => void;
}

export function CallbacksSummary({ count, oldestAge, onClick }: CallbacksSummaryProps) {
  if (count === 0) return null;
  
  return (
    <button
      onClick={onClick}
      className="mx-5 p-4 bg-white rounded-2xl border border-neutral-200 flex items-center justify-between hover:bg-neutral-50 transition-colors w-[calc(100%-2.5rem)]"
    >
      <div className="flex items-center gap-3">
        <span className="text-xl">📞</span>
        <div className="text-left">
          <p className="font-medium text-neutral-900">
            {count} callback{count !== 1 ? 's' : ''} needed
          </p>
          <p className="text-sm text-neutral-500">
            Oldest: {oldestAge}
          </p>
        </div>
      </div>
      <span className="text-neutral-400">→</span>
    </button>
  );
}


// =============================================================================
// STATS ROW
// Simple horizontal stats
// =============================================================================

interface Stat {
  icon: string;
  value: string | number;
  label: string;
}

interface StatsRowProps {
  stats: Stat[];
}

export function StatsRow({ stats }: StatsRowProps) {
  return (
    <div className="mx-5 flex gap-3">
      {stats.map((stat, i) => (
        <div 
          key={i}
          className="flex-1 p-4 bg-white rounded-2xl border border-neutral-200 text-center"
        >
          <span className="text-xl">{stat.icon}</span>
          <p className="text-xl font-semibold text-neutral-900 mt-1">{stat.value}</p>
          <p className="text-xs text-neutral-500 mt-0.5">{stat.label}</p>
        </div>
      ))}
    </div>
  );
}


// =============================================================================
// SECTION DIVIDER
// Visual separator with optional title
// =============================================================================

interface SectionDividerProps {
  title?: string;
}

export function SectionDivider({ title }: SectionDividerProps) {
  if (!title) {
    return <div className="h-px bg-neutral-100 mx-5 my-4" />;
  }
  
  return (
    <div className="flex items-center gap-3 px-5 my-4">
      <div className="h-px bg-neutral-200 flex-1" />
      <span className="text-xs font-medium text-neutral-400 uppercase tracking-wider">
        {title}
      </span>
      <div className="h-px bg-neutral-200 flex-1" />
    </div>
  );
}


// =============================================================================
// ACTIVITY FEED
// Timeline of recent events
// =============================================================================

interface Activity {
  id: string;
  icon: string;
  text: string;
  time: string;
  done?: boolean;
}

interface ActivityFeedProps {
  title: string;
  activities: Activity[];
}

export function ActivityFeed({ title, activities }: ActivityFeedProps) {
  if (activities.length === 0) return null;
  
  return (
    <div className="mx-5">
      <h3 className="text-sm font-medium text-neutral-500 mb-3">{title}</h3>
      <div className="space-y-2">
        {activities.map((activity) => (
          <div 
            key={activity.id}
            className="flex items-center gap-3 py-2"
          >
            <span className={cn(
              "text-base",
              activity.done && "opacity-50"
            )}>
              {activity.done ? "✓" : activity.icon}
            </span>
            <p className={cn(
              "flex-1 text-sm",
              activity.done ? "text-neutral-400" : "text-neutral-700"
            )}>
              {activity.text}
            </p>
            <span className="text-xs text-neutral-400">{activity.time}</span>
          </div>
        ))}
      </div>
    </div>
  );
}


// =============================================================================
// GEMMA STATUS
// Always visible indicator that the AI is working
// =============================================================================

interface GemmaStatusProps {
  status: "active" | "issues" | "offline";
}

export function GemmaStatus({ status }: GemmaStatusProps) {
  const config = {
    active: { color: "bg-emerald-500", label: "Gemma active" },
    issues: { color: "bg-amber-500", label: "Gemma issues" },
    offline: { color: "bg-red-500", label: "Gemma offline" },
  };
  
  const { color, label } = config[status];
  
  return (
    <div className="flex items-center gap-1.5">
      <span className={cn("w-2 h-2 rounded-full", color)} />
      <span className="text-xs text-neutral-500">{label}</span>
    </div>
  );
}


// =============================================================================
// CALL CARD
// Single call in a list
// =============================================================================

interface CallCardProps {
  callerName: string;
  summary: string;
  timeAgo: string;
  urgency: "emergency" | "urgent" | "normal";
  needsCallback: boolean;
  isResolved: boolean;
  onClick: () => void;
  onCall?: () => void;
}

export function CallCard({
  callerName,
  summary,
  timeAgo,
  urgency,
  needsCallback,
  isResolved,
  onClick,
  onCall,
}: CallCardProps) {
  return (
    <div 
      onClick={onClick}
      className={cn(
        "p-4 border-b border-neutral-100 cursor-pointer hover:bg-neutral-50 transition-colors",
        urgency === "emergency" && "bg-red-50/50"
      )}
    >
      <div className="flex items-start gap-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <p className="font-medium text-neutral-900">{callerName}</p>
            <span className="text-xs text-neutral-400">{timeAgo}</span>
          </div>
          
          <p className="text-sm text-neutral-600 mt-1 line-clamp-2">{summary}</p>
          
          <div className="flex items-center gap-2 mt-2">
            {urgency === "emergency" && (
              <span className="px-2 py-0.5 text-xs font-medium rounded-full bg-red-100 text-red-700">
                ⚡ Emergency
              </span>
            )}
            {urgency === "urgent" && (
              <span className="px-2 py-0.5 text-xs font-medium rounded-full bg-amber-100 text-amber-700">
                Urgent
              </span>
            )}
            {needsCallback && !isResolved && (
              <span className="px-2 py-0.5 text-xs font-medium rounded-full bg-blue-100 text-blue-700">
                Callback needed
              </span>
            )}
            {isResolved && (
              <span className="px-2 py-0.5 text-xs font-medium rounded-full bg-neutral-100 text-neutral-600">
                ✓ Resolved
              </span>
            )}
          </div>
        </div>
        
        {needsCallback && !isResolved && onCall && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              onCall();
            }}
            className="shrink-0 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            Call
          </button>
        )}
      </div>
    </div>
  );
}


// =============================================================================
// MONEY PROGRESS
// Visual bar showing paid vs unpaid
// =============================================================================

interface MoneyProgressProps {
  paid: number;
  unpaid: number;
  overdue: number;
}

export function MoneyProgress({ paid, unpaid, overdue }: MoneyProgressProps) {
  const total = paid + unpaid;
  const paidPercent = total > 0 ? (paid / total) * 100 : 0;
  
  const formatMoney = (amount: number) => {
    if (amount >= 1000) {
      return `£${(amount / 1000).toFixed(1)}k`;
    }
    return `£${amount.toLocaleString()}`;
  };
  
  return (
    <div className="mx-5 p-4 bg-white rounded-2xl border border-neutral-200">
      <div className="flex items-baseline justify-between mb-3">
        <div>
          <span className="text-2xl font-semibold text-neutral-900">
            {formatMoney(paid)}
          </span>
          <span className="text-sm text-neutral-500 ml-1">paid</span>
        </div>
        <div className="text-right">
          <span className="text-lg text-neutral-600">
            {formatMoney(unpaid)}
          </span>
          <span className="text-sm text-neutral-500 ml-1">unpaid</span>
        </div>
      </div>
      
      <div className="h-3 bg-neutral-100 rounded-full overflow-hidden">
        <div 
          className="h-full bg-emerald-500 rounded-full transition-all duration-500"
          style={{ width: `${paidPercent}%` }}
        />
      </div>
      
      {overdue > 0 && (
        <p className="text-sm text-orange-600 mt-2">
          {formatMoney(overdue)} overdue
        </p>
      )}
    </div>
  );
}


// =============================================================================
// INVOICE ROW
// Single invoice in a list
// =============================================================================

interface InvoiceRowProps {
  customerName: string;
  amount: number;
  status: "paid" | "pending" | "overdue";
  daysInfo: string; // "Today" or "7 days overdue"
  onClick: () => void;
  onChase?: () => void;
}

export function InvoiceRow({
  customerName,
  amount,
  status,
  daysInfo,
  onClick,
  onChase,
}: InvoiceRowProps) {
  const statusConfig = {
    paid: { icon: "✓", color: "text-emerald-600", bgColor: "bg-emerald-50" },
    pending: { icon: "🟡", color: "text-amber-600", bgColor: "bg-amber-50" },
    overdue: { icon: "🔴", color: "text-red-600", bgColor: "bg-red-50" },
  };
  
  const config = statusConfig[status];
  
  const formatMoney = (amount: number) => `£${amount.toLocaleString()}`;
  
  return (
    <div
      onClick={onClick}
      className={cn(
        "p-4 flex items-center justify-between cursor-pointer hover:bg-neutral-50 transition-colors",
        status === "overdue" && "bg-red-50/30"
      )}
    >
      <div className="flex items-center gap-3">
        <span>{config.icon}</span>
        <div>
          <p className="font-medium text-neutral-900">{customerName}</p>
          <p className={cn("text-sm", config.color)}>{daysInfo}</p>
        </div>
      </div>
      
      <div className="flex items-center gap-3">
        <span className="font-semibold text-neutral-900">{formatMoney(amount)}</span>
        {status !== "paid" && onChase && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              onChase();
            }}
            className="px-3 py-1.5 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
          >
            Chase
          </button>
        )}
      </div>
    </div>
  );
}


// =============================================================================
// BOTTOM NAV
// Fixed navigation at bottom
// =============================================================================

interface NavItem {
  id: string;
  icon: React.ReactNode;
  label: string;
  href: string;
  badge?: number;
}

interface BottomNavProps {
  items: NavItem[];
  activeId: string;
}

export function BottomNav({ items, activeId }: BottomNavProps) {
  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-neutral-200 z-50">
      <div className="max-w-md mx-auto flex items-center justify-around py-2 pb-safe">
        {items.map((item) => {
          const isActive = item.id === activeId;
          return (
            <a
              key={item.id}
              href={item.href}
              className={cn(
                "flex flex-col items-center gap-0.5 px-4 py-2 rounded-lg transition-colors relative",
                isActive ? "text-blue-600" : "text-neutral-400"
              )}
            >
              <div className="relative">
                {item.icon}
                {item.badge && item.badge > 0 && (
                  <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center">
                    {item.badge > 9 ? "9+" : item.badge}
                  </span>
                )}
              </div>
              <span className="text-[10px] font-medium">{item.label}</span>
            </a>
          );
        })}
      </div>
    </nav>
  );
}


// =============================================================================
// HEADER
// Simple header with optional back button
// =============================================================================

interface HeaderProps {
  title?: string;
  showBack?: boolean;
  onBack?: () => void;
  right?: React.ReactNode;
  rightContent?: React.ReactNode;
  transparent?: boolean;
}

export function Header({ title, showBack, onBack, right, rightContent, transparent }: HeaderProps) {
  return (
    <header className={cn(
      "sticky top-0 z-40 px-4 py-3 flex items-center justify-between",
      transparent ? "bg-transparent" : "bg-white/95 backdrop-blur-sm border-b border-neutral-100"
    )}>
      <div className="flex items-center gap-3">
        {showBack && (
          <button
            onClick={onBack}
            className="p-2 -ml-2 hover:bg-neutral-100 rounded-lg transition-colors"
          >
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M12.5 15L7.5 10L12.5 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        )}
        {title && (
          <h1 className="text-lg font-semibold text-neutral-900">{title}</h1>
        )}
      </div>
      {right || rightContent}
    </header>
  );
}


// =============================================================================
// EMPTY STATE
// Friendly message when there's no data
// =============================================================================

interface EmptyStateProps {
  icon: string;
  title: string;
  description: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export function EmptyState({ icon, title, description, action }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-8 text-center">
      <span className="text-5xl mb-4">{icon}</span>
      <h3 className="text-lg font-semibold text-neutral-900">{title}</h3>
      <p className="text-neutral-500 mt-1 max-w-xs">{description}</p>
      {action && (
        <button
          onClick={action.onClick}
          className="mt-4 px-6 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
        >
          {action.label}
        </button>
      )}
    </div>
  );
}


// =============================================================================
// MENU ITEM
// Single item in the "More" menu
// =============================================================================

interface MenuItemProps {
  icon: string;
  title: string;
  subtitle?: string;
  onClick: () => void;
  badge?: string;
}

export function MenuItem({ icon, title, subtitle, onClick, badge }: MenuItemProps) {
  return (
    <button
      onClick={onClick}
      className="w-full p-4 flex items-center gap-4 hover:bg-neutral-50 transition-colors"
    >
      <span className="text-2xl">{icon}</span>
      <div className="flex-1 text-left">
        <p className="font-medium text-neutral-900">{title}</p>
        {subtitle && (
          <p className="text-sm text-neutral-500">{subtitle}</p>
        )}
      </div>
      {badge && (
        <span className="px-2 py-1 text-xs font-medium bg-neutral-100 text-neutral-600 rounded-full">
          {badge}
        </span>
      )}
      <span className="text-neutral-300">→</span>
    </button>
  );
}
