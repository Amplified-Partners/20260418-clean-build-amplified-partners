"use client";

import React from "react";
import { cn } from "@/lib/utils";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
}

export function Input({ label, error, hint, className, ...props }: InputProps) {
  return (
    <div className="space-y-1.5">
      {label && (
        <label className="text-sm font-medium text-[var(--grey-700)]">{label}</label>
      )}
      <input
        className={cn(
          "w-full h-11 px-4 bg-white border rounded-lg text-[var(--grey-900)]",
          "placeholder:text-[var(--grey-400)]",
          "focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent",
          "transition-shadow",
          error ? "border-red-500" : "border-[var(--grey-300)]",
          className
        )}
        {...props}
      />
      {hint && !error && (
        <p className="text-xs text-[var(--grey-500)]">{hint}</p>
      )}
      {error && <p className="text-sm text-red-600">{error}</p>}
    </div>
  );
}
