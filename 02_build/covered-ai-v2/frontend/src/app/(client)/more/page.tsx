/**
 * Client App - More Page
 * 
 * Access to less frequent features.
 * Clean menu structure.
 * 
 * Design principles:
 * - Progressive disclosure
 * - Clear categorization
 * - Subscription info visible
 */

"use client";

import React from "react";
import { useRouter } from "next/navigation";
import { MenuItem, SectionDivider } from "@/components/client-app";

// Mock data
const mockData = {
  businessName: "Titan Plumbing",
  plan: "Pro",
  nextPayment: "15 Dec",
  amount: "£297",
  
  pendingQuotes: 3,
  upcomingJobs: 2,
};

export default function MorePage() {
  const router = useRouter();
  
  return (
    <div className="pb-6">
      {/* Business header */}
      <div className="px-5 pt-4 pb-2">
        <h1 className="text-xl font-semibold text-neutral-900">
          {mockData.businessName}
        </h1>
      </div>
      
      {/* Primary menu items */}
      <div className="bg-white mx-5 rounded-2xl border border-neutral-200 overflow-hidden mt-4">
        <MenuItem
          icon="📅"
          title="Schedule"
          subtitle="View and manage jobs"
          badge={mockData.upcomingJobs > 0 ? `${mockData.upcomingJobs} upcoming` : undefined}
          onClick={() => router.push("/more/schedule")}
        />
        <div className="h-px bg-neutral-100 mx-4" />
        <MenuItem
          icon="👥"
          title="Customers"
          subtitle="Your customer list"
          onClick={() => router.push("/more/customers")}
        />
        <div className="h-px bg-neutral-100 mx-4" />
        <MenuItem
          icon="📝"
          title="Quotes"
          subtitle="Pending and sent"
          badge={mockData.pendingQuotes > 0 ? `${mockData.pendingQuotes} pending` : undefined}
          onClick={() => router.push("/more/quotes")}
        />
        <div className="h-px bg-neutral-100 mx-4" />
        <MenuItem
          icon="⭐"
          title="Reviews"
          subtitle="Your reputation"
          onClick={() => router.push("/more/reviews")}
        />
      </div>
      
      <SectionDivider />
      
      {/* Settings section */}
      <div className="bg-white mx-5 rounded-2xl border border-neutral-200 overflow-hidden">
        <MenuItem
          icon="⚙️"
          title="Settings"
          subtitle="Gemma, notifications, forwarding"
          onClick={() => router.push("/more/settings")}
        />
        <div className="h-px bg-neutral-100 mx-4" />
        <MenuItem
          icon="❓"
          title="Help"
          subtitle="Support and guides"
          onClick={() => router.push("/more/help")}
        />
      </div>
      
      <SectionDivider />
      
      {/* Subscription info */}
      <div className="mx-5 p-4 bg-neutral-50 rounded-2xl">
        <div className="flex items-center justify-between">
          <div>
            <p className="font-medium text-neutral-900">
              Covered {mockData.plan} Plan
            </p>
            <p className="text-sm text-neutral-500">
              Next payment: {mockData.nextPayment} • {mockData.amount}
            </p>
          </div>
          <button
            onClick={() => router.push("/more/billing")}
            className="text-sm text-blue-600 font-medium"
          >
            Manage
          </button>
        </div>
      </div>
      
      {/* Sign out */}
      <div className="mx-5 mt-6">
        <button
          onClick={() => {
            // In production: sign out
            router.push("/login");
          }}
          className="w-full py-3 text-red-600 font-medium text-center"
        >
          Sign Out
        </button>
      </div>
      
      {/* Version info */}
      <p className="text-center text-xs text-neutral-400 mt-4">
        Covered AI v2.0.0
      </p>
    </div>
  );
}
