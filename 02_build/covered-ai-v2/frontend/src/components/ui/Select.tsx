"use client";

import React from "react";
import { cn } from "@/lib/utils";

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: { value: string; label: string }[];
}

export function Select({ label, options, className, ...props }: SelectProps) {
  return (
    <div className="space-y-1.5">
      {label && (
        <label className="text-sm font-medium text-[var(--grey-700)]">{label}</label>
      )}
      <select
        className={cn(
          "w-full h-11 px-4 bg-white border border-[var(--grey-300)] rounded-lg text-[var(--grey-900)]",
          "focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)]",
          className
        )}
        {...props}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  );
}
