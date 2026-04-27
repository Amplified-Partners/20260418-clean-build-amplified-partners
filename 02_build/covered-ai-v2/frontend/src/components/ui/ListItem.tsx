"use client";

import React from "react";
import { cn } from "@/lib/utils";

interface ListItemProps {
  title: string;
  subtitle: string;
  meta?: string;
  badge?: {
    label: string;
    variant: "default" | "primary" | "success" | "warning" | "danger";
  };
  action?: {
    label: string;
    variant: "primary" | "secondary" | "warning";
    onClick: () => void;
  };
  highlighted?: boolean;
  onClick?: () => void;
}

const badgeVariants = {
  default: "bg-[var(--grey-100)] text-[var(--grey-600)]",
  primary: "bg-blue-100 text-blue-700",
  success: "bg-green-100 text-green-700",
  warning: "bg-amber-100 text-amber-700",
  danger: "bg-red-100 text-red-700",
};

const actionVariants = {
  primary: "bg-[var(--brand-primary)] hover:bg-[var(--brand-primary-hover)] text-white",
  secondary: "bg-[var(--grey-100)] hover:bg-[var(--grey-200)] text-[var(--grey-600)]",
  warning: "bg-amber-500 hover:bg-amber-600 text-white",
};

export function ListItem({
  title,
  subtitle,
  meta,
  badge,
  action,
  highlighted,
  onClick,
}: ListItemProps) {
  return (
    <li
      className={cn(
        "px-4 py-3 min-h-[64px] flex items-center justify-between gap-3 touch-manipulation",
        highlighted && "bg-red-50/50",
        onClick && "cursor-pointer hover:bg-[var(--grey-50)] active:bg-[var(--grey-100)]"
      )}
      onClick={onClick}
    >
      <div className="min-w-0">
        <div className="flex items-center gap-2">
          <p className="font-medium text-[var(--grey-900)]">{title}</p>
          {badge && (
            <span
              className={cn(
                "px-2 py-0.5 text-xs font-medium rounded-full",
                badgeVariants[badge.variant]
              )}
            >
              {badge.label}
            </span>
          )}
        </div>
        <p className="text-sm text-[var(--grey-500)] mt-0.5">{subtitle}</p>
        {meta && (
          <p
            className={cn(
              "text-xs mt-1",
              highlighted ? "text-red-600" : "text-[var(--grey-500)]"
            )}
          >
            {meta}
          </p>
        )}
      </div>
      {action && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            action.onClick();
          }}
          className={cn(
            "shrink-0 min-h-[44px] px-4 text-sm font-medium rounded-lg transition-colors touch-manipulation active:scale-[0.98]",
            actionVariants[action.variant]
          )}
        >
          {action.label}
        </button>
      )}
    </li>
  );
}
