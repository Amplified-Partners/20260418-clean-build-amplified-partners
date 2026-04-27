"use client";

import React from "react";

interface ToggleProps {
  label: string;
  description?: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
}

export function Toggle({ label, description, checked, onChange }: ToggleProps) {
  return (
    <label className="flex items-center justify-between p-4 bg-blue-50 rounded-xl cursor-pointer">
      <div>
        <p className="font-medium text-[var(--grey-900)]">{label}</p>
        {description && (
          <p className="text-sm text-[var(--grey-500)]">{description}</p>
        )}
      </div>
      <div className="relative">
        <input
          type="checkbox"
          className="sr-only peer"
          checked={checked}
          onChange={(e) => onChange(e.target.checked)}
        />
        <div className="w-11 h-6 bg-[var(--grey-200)] rounded-full peer peer-checked:bg-[var(--brand-primary)] transition-colors" />
        <div className="absolute left-0.5 top-0.5 w-5 h-5 bg-white rounded-full shadow peer-checked:translate-x-5 transition-transform" />
      </div>
    </label>
  );
}
