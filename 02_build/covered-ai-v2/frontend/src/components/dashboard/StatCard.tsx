"use client";

import React from "react";

interface StatCardProps {
  icon: string;
  value: string | number;
  label: string;
  trend?: "up" | "down" | "stable";
}

export function StatCard({ icon, value, label, trend }: StatCardProps) {
  return (
    <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 text-center">
      <span className="text-2xl">{icon}</span>
      <p className="mt-1 text-2xl font-bold text-[var(--grey-900)] tabular-nums flex items-center justify-center gap-1">
        {value}
        {trend === "up" && <span className="text-green-500 text-sm">▲</span>}
        {trend === "down" && <span className="text-red-500 text-sm">▼</span>}
      </p>
      <p className="text-xs text-[var(--grey-500)] mt-1">{label}</p>
    </div>
  );
}
