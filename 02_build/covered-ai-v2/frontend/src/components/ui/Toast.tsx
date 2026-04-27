"use client";

import React from "react";
import { cn } from "@/lib/utils";

interface ToastProps {
  message: string;
  variant?: "success" | "error" | "info";
  isVisible: boolean;
}

const variants = {
  success: { bg: "bg-[var(--grey-900)]", icon: "✓", iconColor: "text-green-400" },
  error: { bg: "bg-red-600", icon: "✕", iconColor: "text-white" },
  info: { bg: "bg-[var(--grey-900)]", icon: "ℹ", iconColor: "text-blue-400" },
};

export function Toast({ message, variant = "success", isVisible }: ToastProps) {
  if (!isVisible) return null;

  const config = variants[variant];

  return (
    <div className="fixed bottom-24 left-4 right-4 mx-auto max-w-sm z-50">
      <div
        className={cn(
          "px-4 py-3 rounded-lg shadow-lg flex items-center gap-3 text-white",
          config.bg
        )}
      >
        <span className={config.iconColor}>{config.icon}</span>
        <span>{message}</span>
      </div>
    </div>
  );
}
