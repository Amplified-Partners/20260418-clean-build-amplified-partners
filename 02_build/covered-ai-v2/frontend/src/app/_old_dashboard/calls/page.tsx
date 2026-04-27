"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Filter } from "lucide-react";
import { Header } from "@/components/layout";
import { FilterTabs, EmptyState, IconButton } from "@/components/ui";
import { useAuthContext } from "@/lib/auth-context";
import { useCalls } from "@/lib/hooks";
import { cn } from "@/lib/utils";

interface CallBadge {
  label: string;
  variant: "danger" | "warning" | "primary" | "success" | "default";
}

function getBadges(call: {
  urgency: string;
  callbackRequired: boolean;
  callbackCompleted: boolean;
  intent: string;
}): CallBadge[] {
  const badges: CallBadge[] = [];

  if (call.urgency === "emergency") {
    badges.push({ label: "⚡ Emergency", variant: "danger" });
  } else if (call.urgency === "urgent") {
    badges.push({ label: "Urgent", variant: "warning" });
  }

  if (call.callbackRequired && !call.callbackCompleted) {
    badges.push({ label: "Callback needed", variant: "primary" });
  }

  if (call.intent === "NEW_ENQUIRY") {
    badges.push({ label: "New enquiry", variant: "success" });
  }

  if (call.callbackCompleted) {
    badges.push({ label: "✓ Resolved", variant: "default" });
  }

  return badges;
}

const filterTabs = [
  { id: "all", label: "All" },
  { id: "callbacks", label: "Callbacks" },
  { id: "emergency", label: "Emergency" },
];

// Loading skeleton
function CallsSkeleton() {
  return (
    <div className="animate-pulse">
      <div className="px-4 py-2 bg-[var(--grey-50)]">
        <div className="h-4 bg-[var(--grey-200)] rounded w-16" />
      </div>
      {[1, 2, 3].map((i) => (
        <div key={i} className="px-4 py-4 border-b border-[var(--grey-100)]">
          <div className="flex gap-3">
            <div className="w-10 h-10 bg-[var(--grey-200)] rounded-full" />
            <div className="flex-1">
              <div className="h-5 bg-[var(--grey-200)] rounded w-1/3 mb-2" />
              <div className="h-4 bg-[var(--grey-100)] rounded w-2/3 mb-2" />
              <div className="flex gap-2">
                <div className="h-5 bg-[var(--grey-100)] rounded-full w-20" />
                <div className="h-5 bg-[var(--grey-100)] rounded-full w-24" />
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default function CallsPage() {
  const router = useRouter();
  const { client } = useAuthContext();
  const [activeFilter, setActiveFilter] = useState("all");
  const { data, isLoading, error } = useCalls(client?.id || null, activeFilter);

  const calls = data?.calls || [];

  // Group calls by date
  const groupedCalls = calls.reduce((acc, call) => {
    const date = call.groupDate || "Other";
    if (!acc[date]) {
      acc[date] = [];
    }
    acc[date].push(call);
    return acc;
  }, {} as Record<string, typeof calls>);

  if (isLoading) {
    return (
      <>
        <Header title="Calls" action={<IconButton icon={<Filter className="w-5 h-5" />} />} />
        <main className="pb-24">
          <div className="pt-4">
            <FilterTabs tabs={filterTabs} activeTab={activeFilter} onChange={setActiveFilter} />
          </div>
          <CallsSkeleton />
        </main>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Header title="Calls" action={<IconButton icon={<Filter className="w-5 h-5" />} />} />
        <main className="pb-24 px-4 pt-6">
          <div className="bg-red-50 rounded-xl border border-red-200 p-4 text-center">
            <p className="text-red-700">Failed to load calls</p>
          </div>
        </main>
      </>
    );
  }

  if (calls.length === 0) {
    return (
      <>
        <Header title="Calls" action={<IconButton icon={<Filter className="w-5 h-5" />} />} />
        <main className="pb-24">
          <EmptyState
            icon="📞"
            title="No calls yet"
            description="Gemma is ready to answer. Your calls will appear here."
          />
        </main>
      </>
    );
  }

  return (
    <>
      <Header title="Calls" action={<IconButton icon={<Filter className="w-5 h-5" />} />} />
      <main className="pb-24">
        <div className="pt-4">
          <FilterTabs tabs={filterTabs} activeTab={activeFilter} onChange={setActiveFilter} />
        </div>

        {Object.entries(groupedCalls).map(([date, dateCalls]) => (
          <div key={date}>
            <h3 className="px-4 py-2 text-sm font-medium text-[var(--grey-500)] bg-[var(--grey-50)]">
              {date}
            </h3>
            <ul className="divide-y divide-[var(--grey-100)] bg-white">
              {dateCalls.map((call) => {
                const badges = getBadges(call);

                return (
                  <li
                    key={call.id}
                    onClick={() => router.push(`/dashboard/calls/${call.id}`)}
                    className={cn(
                      "px-4 py-4 cursor-pointer hover:bg-[var(--grey-50)] transition-colors",
                      call.urgency === "emergency" && "bg-red-50/30"
                    )}
                  >
                    <div className="flex items-start gap-3">
                      <span className="text-xl">📞</span>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between">
                          <p className="font-medium text-[var(--grey-900)]">{call.callerName}</p>
                          <span className="text-xs text-[var(--grey-500)]">{call.timeAgo}</span>
                        </div>
                        <p className="text-sm text-[var(--grey-500)] mt-0.5">{call.summary}</p>
                        <div className="flex flex-wrap gap-1.5 mt-2">
                          {badges.map((badge, i) => (
                            <span
                              key={i}
                              className={cn(
                                "px-2 py-0.5 text-xs font-medium rounded-full",
                                badge.variant === "danger" && "bg-red-100 text-red-700",
                                badge.variant === "warning" && "bg-amber-100 text-amber-700",
                                badge.variant === "primary" && "bg-blue-100 text-blue-700",
                                badge.variant === "success" && "bg-green-100 text-green-700",
                                badge.variant === "default" && "bg-[var(--grey-100)] text-[var(--grey-600)]"
                              )}
                            >
                              {badge.label}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </main>
    </>
  );
}
