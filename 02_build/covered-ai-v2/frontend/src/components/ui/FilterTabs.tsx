"use client";

import React from "react";
import { cn } from "@/lib/utils";

interface FilterTab {
  id: string;
  label: string;
  count?: number;
}

export function FilterTabs({
  tabs,
  activeTab,
  onChange,
}: {
  tabs: FilterTab[];
  activeTab: string;
  onChange: (id: string) => void;
}) {
  return (
    <div className="px-4 pb-3 flex gap-2 overflow-x-auto">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onChange(tab.id)}
          className={cn(
            "px-4 py-2 text-sm font-medium rounded-full whitespace-nowrap transition-colors",
            activeTab === tab.id
              ? "bg-[var(--brand-primary)] text-white"
              : "bg-[var(--grey-100)] text-[var(--grey-600)] hover:bg-[var(--grey-200)]"
          )}
        >
          {tab.label}
          {tab.count !== undefined && ` (${tab.count})`}
        </button>
      ))}
    </div>
  );
}
