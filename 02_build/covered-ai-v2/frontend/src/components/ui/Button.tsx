"use client";

import React from "react";
import { cn } from "@/lib/utils";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger" | "ghost";
  size?: "sm" | "md" | "lg";
  icon?: React.ReactNode;
  loading?: boolean;
}

const variants = {
  primary: "bg-[var(--brand-primary)] hover:bg-[var(--brand-primary-hover)] text-white",
  secondary: "bg-white hover:bg-[var(--grey-50)] text-[var(--grey-700)] border border-[var(--grey-300)]",
  danger: "bg-red-600 hover:bg-red-700 text-white",
  ghost: "bg-transparent hover:bg-[var(--grey-100)] text-[var(--grey-600)]",
};

const sizes = {
  sm: "min-h-[44px] px-4 text-sm",
  md: "min-h-[48px] px-6 text-base",
  lg: "min-h-[52px] px-8 text-lg",
};

export function Button({
  variant = "primary",
  size = "md",
  icon,
  loading,
  children,
  className,
  disabled,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        "font-medium rounded-lg transition-colors flex items-center justify-center gap-2 touch-manipulation active:scale-[0.98]",
        variants[variant],
        sizes[size],
        (disabled || loading) && "opacity-50 cursor-not-allowed",
        className
      )}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
            fill="none"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
          />
        </svg>
      ) : (
        icon
      )}
      {children}
    </button>
  );
}

interface IconButtonProps {
  icon: React.ReactNode;
  onClick?: () => void;
  className?: string;
  "aria-label"?: string;
}

export function IconButton({ icon, onClick, className, ...props }: IconButtonProps) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "min-w-[44px] min-h-[44px] flex items-center justify-center text-[var(--grey-400)] hover:text-[var(--grey-600)] hover:bg-[var(--grey-100)] active:bg-[var(--grey-200)] rounded-lg transition-colors touch-manipulation",
        className
      )}
      {...props}
    >
      {icon}
    </button>
  );
}
