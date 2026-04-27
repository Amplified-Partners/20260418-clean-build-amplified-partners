"use client";

import React from "react";
import Link from "next/link";
import { cn } from "@/lib/utils";

interface CustomerSnapshotProps {
  total: number;
  repeatRate: number;
  ltv: number;
  ltvCacRatio: number;
}

export function CustomerSnapshot({ total, repeatRate, ltv, ltvCacRatio }: CustomerSnapshotProps) {
  const ratioHealth = ltvCacRatio >= 5 ? "good" : ltvCacRatio >= 3 ? "ok" : "bad";

  return (
    <section className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
      <div className="flex items-center justify-between mb-3">
        <h2 className="font-semibold text-[var(--grey-900)]">Your customers</h2>
        <Link href="/dashboard/customers" className="text-sm text-[var(--brand-primary)] font-medium">
          View all →
        </Link>
      </div>

      <div className="grid grid-cols-4 gap-2 text-center">
        <div className="bg-[var(--grey-100)] rounded-lg p-2">
          <p className="text-lg font-bold text-[var(--grey-900)]">{total}</p>
          <p className="text-xs text-[var(--grey-500)]">total</p>
        </div>
        <div className="bg-[var(--grey-100)] rounded-lg p-2">
          <p className="text-lg font-bold text-[var(--grey-900)]">{repeatRate}%</p>
          <p className="text-xs text-[var(--grey-500)]">repeat</p>
        </div>
        <div className="bg-[var(--grey-100)] rounded-lg p-2">
          <p className="text-lg font-bold text-[var(--grey-900)]">£{ltv}</p>
          <p className="text-xs text-[var(--grey-500)]">LTV</p>
        </div>
        <div
          className={cn(
            "rounded-lg p-2",
            ratioHealth === "good"
              ? "bg-green-100"
              : ratioHealth === "ok"
              ? "bg-amber-100"
              : "bg-red-100"
          )}
        >
          <p
            className={cn(
              "text-lg font-bold",
              ratioHealth === "good"
                ? "text-green-700"
                : ratioHealth === "ok"
                ? "text-amber-700"
                : "text-red-700"
            )}
          >
            {ltvCacRatio}:1
          </p>
          <p
            className={cn(
              "text-xs",
              ratioHealth === "good"
                ? "text-green-600"
                : ratioHealth === "ok"
                ? "text-amber-600"
                : "text-red-600"
            )}
          >
            ratio
          </p>
        </div>
      </div>

      {/* Insight */}
      <div className="mt-3 p-3 bg-[var(--grey-50)] rounded-lg">
        <p className="text-sm text-[var(--grey-600)]">
          💡{" "}
          {ltvCacRatio >= 10
            ? `Excellent economics. Each £1 on marketing returns £${ltvCacRatio} in customer value.`
            : ltvCacRatio >= 5
            ? "Strong customer economics. Keep it up!"
            : "Focus on improving customer retention to boost LTV."}
        </p>
      </div>
    </section>
  );
}
