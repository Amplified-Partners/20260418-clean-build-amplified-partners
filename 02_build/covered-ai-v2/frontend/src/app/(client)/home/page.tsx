/**
 * Client App - Home Page
 * 
 * The "10-second morning check"
 * Shows everything that matters at a glance.
 * 
 * Design principles:
 * - Lead with status (all clear vs needs attention)
 * - Celebrate wins
 * - Show activity timeline
 * - Progressive disclosure
 */

"use client";

import React from "react";
import { useRouter } from "next/navigation";
import {
  SmartGreeting,
  AllClearCard,
  UrgentCard,
  WinCard,
  CallbacksSummary,
  StatsRow,
  SectionDivider,
  ActivityFeed,
} from "@/components/client-app";

// Mock data - replace with real API calls
const mockData = {
  ownerName: "Ralph",
  callsHandled: 3,
  hasUrgent: false,
  
  // Wins to celebrate
  wins: [
    {
      type: "review" as const,
      title: "New 5-star review!",
      description: "Mrs. Thompson: \"Fantastic service, arrived within the hour.\"",
    },
  ],
  
  // Urgent items (empty = all clear)
  urgentItems: [] as Array<{
    type: "emergency" | "callback" | "overdue";
    title: string;
    subtitle: string;
    timeAgo: string;
    actionLabel: string;
    phone?: string;
  }>,
  
  // Callbacks needed
  callbacks: {
    count: 0,
    oldestAge: "",
  },
  
  // Stats
  stats: [
    { icon: "📞", value: 3, label: "Calls" },
    { icon: "💰", value: "£892", label: "Paid" },
    { icon: "⭐", value: 1, label: "Reviews" },
  ],
  
  // Activity timeline
  activities: [
    { id: "1", icon: "📞", text: "Emergency call forwarded", time: "9am", done: true },
    { id: "2", icon: "💬", text: "Quote request from John", time: "11am", done: true },
    { id: "3", icon: "📅", text: "Booking confirmed with Mrs Chen", time: "2pm", done: true },
  ],
  
  // Today's jobs
  todaysJobs: [
    { time: "9am", customer: "Mrs Chen", job: "Tap repair" },
    { time: "2pm", customer: "Mr Abbas", job: "Boiler service" },
  ],
};

// Version with urgent items for testing
const mockDataWithUrgent = {
  ...mockData,
  hasUrgent: true,
  wins: [],
  urgentItems: [
    {
      type: "emergency" as const,
      title: "John Smith",
      subtitle: "Burst pipe - water through ceiling",
      timeAgo: "20m ago",
      actionLabel: "Call John 📞",
      phone: "+447712345678",
    },
  ],
  callbacks: {
    count: 2,
    oldestAge: "3 hours ago",
  },
};

export default function HomePage() {
  const router = useRouter();
  
  // Toggle between normal and urgent views for demo
  // In production, this comes from API
  const [showUrgent, setShowUrgent] = React.useState(false);
  const data = showUrgent ? mockDataWithUrgent : mockData;
  
  const handleCall = (phone?: string) => {
    if (phone) {
      window.location.href = `tel:${phone}`;
    }
  };
  
  const handleViewCallbacks = () => {
    router.push("/calls?filter=callbacks");
  };
  
  return (
    <div className="space-y-4 pb-6">
      {/* Smart greeting */}
      <SmartGreeting
        ownerName={data.ownerName}
        callsHandled={data.callsHandled}
        hasUrgent={data.hasUrgent}
      />
      
      {/* Status section */}
      {data.urgentItems.length === 0 && data.callbacks.count === 0 ? (
        // All clear
        <AllClearCard />
      ) : (
        // Urgent items
        <div className="space-y-3">
          {data.urgentItems.map((item, i) => (
            <UrgentCard
              key={i}
              type={item.type}
              title={item.title}
              subtitle={item.subtitle}
              timeAgo={item.timeAgo}
              actionLabel={item.actionLabel}
              onAction={() => handleCall(item.phone)}
            />
          ))}
          
          {/* Callbacks summary */}
          {data.callbacks.count > 0 && (
            <CallbacksSummary
              count={data.callbacks.count}
              oldestAge={data.callbacks.oldestAge}
              onClick={handleViewCallbacks}
            />
          )}
        </div>
      )}
      
      {/* Wins */}
      {data.wins.map((win, i) => (
        <WinCard
          key={i}
          type={win.type}
          title={win.title}
          description={win.description}
          action={{
            label: "See review",
            onClick: () => router.push("/more/reviews"),
          }}
        />
      ))}
      
      <SectionDivider title="Since yesterday" />
      
      {/* Stats */}
      <StatsRow stats={data.stats} />
      
      <SectionDivider title="Today" />
      
      {/* Today's jobs */}
      {data.todaysJobs.length > 0 && (
        <div className="mx-5 space-y-2">
          {data.todaysJobs.map((job, i) => (
            <div 
              key={i}
              className="flex items-center gap-3 py-2"
            >
              <span className="text-neutral-400 text-sm w-12">{job.time}</span>
              <div>
                <p className="text-sm font-medium text-neutral-900">{job.customer}</p>
                <p className="text-xs text-neutral-500">{job.job}</p>
              </div>
            </div>
          ))}
        </div>
      )}
      
      {/* Activity feed */}
      <ActivityFeed
        title="Activity"
        activities={data.activities}
      />
      
      {/* Demo toggle - remove in production */}
      <div className="mx-5 pt-8 border-t border-neutral-100">
        <p className="text-xs text-neutral-400 mb-2">Demo controls:</p>
        <button
          onClick={() => setShowUrgent(!showUrgent)}
          className="text-xs text-blue-600 underline"
        >
          {showUrgent ? "Show all-clear state" : "Show urgent state"}
        </button>
      </div>
    </div>
  );
}
