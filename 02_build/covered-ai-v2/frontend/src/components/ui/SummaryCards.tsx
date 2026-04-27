"use client";

import React from "react";
import { cn } from "@/lib/utils";

interface SummaryCard {
  value: string;
  label: string;
  variant: "default" | "danger" | "success";
}

const variants = {
  default: "bg-white border-[var(--grey-200)] text-[var(--grey-900)]",
  danger: "bg-red-50 border-red-200 text-red-600",
  success: "bg-green-50 border-green-200 text-green-600",
};

export function SummaryCards({ cards }: { cards: SummaryCard[] }) {
  return (
    <div className="px-4 py-4 grid grid-cols-3 gap-3">
      {cards.map((card, i) => (
        <div
          key={i}
          className={cn(
            "rounded-xl border p-3 text-center",
            variants[card.variant]
          )}
        >
          <p className="text-xl font-bold tabular-nums">{card.value}</p>
          <p className="text-xs">{card.label}</p>
        </div>
      ))}
    </div>
  );
}
