"use client";

import React from "react";
import { cn } from "@/lib/utils";

export interface AttentionItem {
  id: string;
  type: "emergency" | "callback" | "overdue" | "review" | "followup";
  title: string;
  subtitle: string;
  action: {
    label: string;
    variant: "danger" | "warning" | "primary";
    onClick: () => void;
  };
}

const typeConfig = {
  emergency: { icon: "⚡", bgClass: "bg-red-50/30" },
  callback: { icon: "📞", bgClass: "" },
  overdue: { icon: "💷", bgClass: "" },
  review: { icon: "⭐", bgClass: "" },
  followup: { icon: "📋", bgClass: "" },
};

const actionVariants = {
  danger: "bg-red-600 hover:bg-red-700 text-white",
  warning: "bg-amber-500 hover:bg-amber-600 text-white",
  primary: "bg-[var(--brand-primary)] hover:bg-[var(--brand-primary-hover)] text-white",
};

function AllClearState() {
  return (
    <section className="bg-green-50 rounded-xl border border-green-200 p-6 text-center">
      <span className="text-5xl">✓</span>
      <h2 className="mt-3 text-lg font-semibold text-green-900">All clear</h2>
      <p className="text-sm text-green-700 mt-1">Nothing needs your attention right now</p>
    </section>
  );
}

export function NeedsAttentionFeed({ items }: { items: AttentionItem[] }) {
  if (items.length === 0) return <AllClearState />;

  return (
    <section className="bg-white rounded-xl border border-[var(--grey-200)] overflow-hidden shadow-sm">
      {/* Header */}
      <div className="px-4 py-3 bg-red-50 border-b border-red-100">
        <div className="flex items-center gap-2">
          <span className="flex h-6 w-6 items-center justify-center rounded-full bg-red-500 text-white text-xs font-bold">
            {items.length}
          </span>
          <h2 className="font-semibold text-red-900">Needs Attention</h2>
        </div>
      </div>

      {/* Items */}
      <ul className="divide-y divide-[var(--grey-100)]">
        {items.map((item) => {
          const config = typeConfig[item.type];
          return (
            <li
              key={item.id}
              className={cn(
                "px-4 py-3 flex items-center justify-between gap-3",
                config.bgClass
              )}
            >
              <div className="flex items-center gap-3 min-w-0">
                <span className="text-xl">{config.icon}</span>
                <div className="min-w-0">
                  <p className="font-medium text-[var(--grey-900)] truncate">{item.title}</p>
                  <p className="text-sm text-[var(--grey-500)] truncate">{item.subtitle}</p>
                </div>
              </div>
              <button
                onClick={item.action.onClick}
                className={cn(
                  "shrink-0 h-9 px-4 text-sm font-medium rounded-lg transition-colors",
                  actionVariants[item.action.variant]
                )}
              >
                {item.action.label}
              </button>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
