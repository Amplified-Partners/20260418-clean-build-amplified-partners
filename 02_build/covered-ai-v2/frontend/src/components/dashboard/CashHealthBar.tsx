"use client";

import React from "react";
import Link from "next/link";
import { cn } from "@/lib/utils";

interface CashHealthProps {
  collected: number;
  billed: number;
  overdue: number;
  overdueCount: number;
}

export function CashHealthBar({ collected, billed, overdue, overdueCount }: CashHealthProps) {
  const percentage = billed > 0 ? Math.round((collected / billed) * 100) : 100;

  // Determine status
  let status: "healthy" | "warning" | "critical";
  if (percentage >= 80) status = "healthy";
  else if (percentage >= 60) status = "warning";
  else status = "critical";

  const statusStyles = {
    healthy: {
      bg: "bg-green-50",
      border: "border-green-200",
      bar: "bg-green-500",
      text: "text-green-700",
    },
    warning: {
      bg: "bg-amber-50",
      border: "border-amber-200",
      bar: "bg-amber-500",
      text: "text-amber-700",
    },
    critical: {
      bg: "bg-red-50",
      border: "border-red-200",
      bar: "bg-red-500",
      text: "text-red-700",
    },
  };

  const styles = statusStyles[status];

  return (
    <section className={cn("rounded-xl border p-4", styles.bg, styles.border)}>
      <div className="flex items-center justify-between mb-3">
        <h2 className="font-semibold text-[var(--grey-900)]">Cash Health</h2>
        <span className="text-sm text-[var(--grey-500)]">This month</span>
      </div>

      {/* Progress Bar */}
      <div className="h-3 bg-[var(--grey-200)] rounded-full overflow-hidden mb-2">
        <div
          className={cn("h-full transition-all duration-500", styles.bar)}
          style={{ width: `${Math.min(percentage, 100)}%` }}
        />
      </div>

      {/* Stats */}
      <div className="flex items-center justify-between text-sm">
        <span className="text-[var(--grey-600)]">
          <strong className="text-[var(--grey-900)]">£{collected.toLocaleString()}</strong>
          {" "}collected of £{billed.toLocaleString()} billed
        </span>
        <span className={cn("font-medium", styles.text)}>{percentage}%</span>
      </div>

      {/* Overdue Warning */}
      {overdue > 0 && (
        <div className="mt-3 flex items-center justify-between text-amber-700">
          <span className="text-sm">
            ⚠️ {overdueCount} invoice{overdueCount > 1 ? "s" : ""} overdue (£{overdue.toLocaleString()})
          </span>
          <Link href="/dashboard/invoices?filter=overdue" className="text-sm font-medium underline">
            View all
          </Link>
        </div>
      )}

      {/* Success Message */}
      {status === "healthy" && overdue === 0 && (
        <div className="mt-3 p-3 bg-white rounded-lg">
          <p className="text-sm text-[var(--grey-600)]">✨ Excellent collection rate this month!</p>
        </div>
      )}
    </section>
  );
}
