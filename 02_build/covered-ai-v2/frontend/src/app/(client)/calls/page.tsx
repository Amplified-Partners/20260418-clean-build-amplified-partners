/**
 * Client App - Calls Page
 *
 * Simple list of calls with clear status.
 * One-tap to call back.
 *
 * Design principles:
 * - Filter by what matters (callbacks, emergencies)
 * - Clear visual hierarchy
 * - Action always visible
 */

"use client";

import React, { useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import {
  CallCard,
  EmptyState,
} from "@/components/client-app";
import { cn } from "@/lib/utils";

// Filter tabs
const filters = [
  { id: "all", label: "All" },
  { id: "callbacks", label: "Callbacks" },
  { id: "emergency", label: "Emergency" },
];

// Mock data
const mockCalls = [
  {
    id: "1",
    callerName: "John Smith",
    summary: "Burst pipe in kitchen, water coming through ceiling",
    timeAgo: "20m",
    urgency: "emergency" as const,
    needsCallback: true,
    isResolved: false,
    phone: "+447712345678",
    groupDate: "Today",
  },
  {
    id: "2",
    callerName: "Sarah Jones",
    summary: "Wants a quote for bathroom renovation",
    timeAgo: "2h",
    urgency: "normal" as const,
    needsCallback: true,
    isResolved: false,
    phone: "+447712345679",
    groupDate: "Today",
  },
  {
    id: "3",
    callerName: "Mike Peters",
    summary: "Confirmed booking for Thursday - radiator bleed",
    timeAgo: "4h",
    urgency: "normal" as const,
    needsCallback: false,
    isResolved: true,
    groupDate: "Today",
  },
  {
    id: "4",
    callerName: "Mrs Thompson",
    summary: "Job completed, payment received",
    timeAgo: "1d",
    urgency: "normal" as const,
    needsCallback: false,
    isResolved: true,
    groupDate: "Yesterday",
  },
  {
    id: "5",
    callerName: "Dave Wilson",
    summary: "Emergency boiler repair - sorted same day",
    timeAgo: "1d",
    urgency: "emergency" as const,
    needsCallback: false,
    isResolved: true,
    groupDate: "Yesterday",
  },
];

function CallsContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const initialFilter = searchParams.get("filter") || "all";
  const [activeFilter, setActiveFilter] = useState(initialFilter);
  
  // Filter calls
  const filteredCalls = mockCalls.filter((call) => {
    if (activeFilter === "callbacks") {
      return call.needsCallback && !call.isResolved;
    }
    if (activeFilter === "emergency") {
      return call.urgency === "emergency";
    }
    return true;
  });
  
  // Group by date
  const groupedCalls = filteredCalls.reduce((acc, call) => {
    const date = call.groupDate;
    if (!acc[date]) {
      acc[date] = [];
    }
    acc[date].push(call);
    return acc;
  }, {} as Record<string, typeof filteredCalls>);
  
  const handleCall = (phone: string) => {
    window.location.href = `tel:${phone}`;
  };
  
  const handleViewCall = (callId: string) => {
    router.push(`/calls/${callId}`);
  };
  
  return (
    <div>
      {/* Filters */}
      <div className="sticky top-[57px] z-30 bg-white border-b border-neutral-100">
        <div className="flex gap-1 p-2 overflow-x-auto">
          {filters.map((filter) => (
            <button
              key={filter.id}
              onClick={() => setActiveFilter(filter.id)}
              className={cn(
                "px-4 py-2 text-sm font-medium rounded-full whitespace-nowrap transition-colors",
                activeFilter === filter.id
                  ? "bg-blue-600 text-white"
                  : "bg-neutral-100 text-neutral-600 hover:bg-neutral-200"
              )}
            >
              {filter.label}
              {filter.id === "callbacks" && (
                <span className="ml-1.5 px-1.5 py-0.5 text-xs bg-white/20 rounded-full">
                  {mockCalls.filter(c => c.needsCallback && !c.isResolved).length}
                </span>
              )}
            </button>
          ))}
        </div>
      </div>
      
      {/* Calls list */}
      {filteredCalls.length === 0 ? (
        <EmptyState
          icon="📞"
          title={activeFilter === "callbacks" ? "No callbacks needed" : "No calls yet"}
          description={
            activeFilter === "callbacks"
              ? "You're all caught up!"
              : "Gemma is ready to answer. Your calls will appear here."
          }
        />
      ) : (
        <div>
          {Object.entries(groupedCalls).map(([date, calls]) => (
            <div key={date}>
              <h3 className="px-4 py-2 text-xs font-semibold text-neutral-500 uppercase tracking-wider bg-neutral-50">
                {date}
              </h3>
              <div className="bg-white">
                {calls.map((call) => (
                  <CallCard
                    key={call.id}
                    callerName={call.callerName}
                    summary={call.summary}
                    timeAgo={call.timeAgo}
                    urgency={call.urgency}
                    needsCallback={call.needsCallback}
                    isResolved={call.isResolved}
                    onClick={() => handleViewCall(call.id)}
                    onCall={call.phone ? () => handleCall(call.phone!) : undefined}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default function CallsPage() {
  return (
    <Suspense fallback={<div className="p-4 text-center text-neutral-500">Loading...</div>}>
      <CallsContent />
    </Suspense>
  );
}
