/**
 * Client App - Quotes Page
 * 
 * Pending and sent quotes.
 * Track conversions.
 */

"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Plus, Send, Clock, CheckCircle, XCircle } from "lucide-react";
import { Header, EmptyState, SectionDivider } from "@/components/client-app";
import { cn } from "@/lib/utils";

// Mock data
const mockQuotes = [
  {
    id: "1",
    customerName: "Sarah Jones",
    job: "Bathroom renovation",
    amount: 4500,
    status: "pending",
    sentDate: "Today",
    expiresIn: "7 days",
  },
  {
    id: "2",
    customerName: "Mike Peters",
    job: "Kitchen plumbing",
    amount: 1200,
    status: "pending",
    sentDate: "Yesterday",
    expiresIn: "6 days",
  },
  {
    id: "3",
    customerName: "Mrs Lee",
    job: "Boiler replacement",
    amount: 2800,
    status: "pending",
    sentDate: "3 days ago",
    expiresIn: "4 days",
  },
  {
    id: "4",
    customerName: "Mr Abbas",
    job: "Boiler service",
    amount: 180,
    status: "accepted",
    sentDate: "1 week ago",
    acceptedDate: "5 days ago",
  },
  {
    id: "5",
    customerName: "Dave Wilson",
    job: "Radiator installation",
    amount: 650,
    status: "declined",
    sentDate: "2 weeks ago",
    declinedDate: "10 days ago",
  },
];

const filters = [
  { id: "pending", label: "Pending" },
  { id: "accepted", label: "Accepted" },
  { id: "declined", label: "Declined" },
];

function StatusIcon({ status }: { status: string }) {
  switch (status) {
    case "pending":
      return <Clock className="w-4 h-4 text-amber-500" />;
    case "accepted":
      return <CheckCircle className="w-4 h-4 text-green-500" />;
    case "declined":
      return <XCircle className="w-4 h-4 text-red-400" />;
    default:
      return null;
  }
}

export default function QuotesPage() {
  const router = useRouter();
  const [activeFilter, setActiveFilter] = useState("pending");
  
  const filteredQuotes = mockQuotes.filter(quote => quote.status === activeFilter);
  
  // Stats
  const pendingCount = mockQuotes.filter(q => q.status === "pending").length;
  const pendingValue = mockQuotes
    .filter(q => q.status === "pending")
    .reduce((sum, q) => sum + q.amount, 0);
  
  return (
    <div className="min-h-screen bg-neutral-50">
      <Header
        title="Quotes"
        showBack
        onBack={() => router.back()}
        rightContent={
          <button
            onClick={() => router.push("/more/quotes/new")}
            className="p-2 text-blue-600"
          >
            <Plus className="w-6 h-6" />
          </button>
        }
      />
      
      {/* Stats */}
      <div className="px-5 py-4 bg-white border-b border-neutral-200">
        <div className="flex gap-4">
          <div className="flex-1">
            <p className="text-2xl font-bold text-neutral-900">{pendingCount}</p>
            <p className="text-xs text-neutral-500">Pending quotes</p>
          </div>
          <div className="flex-1">
            <p className="text-2xl font-bold text-neutral-900">
              £{pendingValue.toLocaleString()}
            </p>
            <p className="text-xs text-neutral-500">Potential value</p>
          </div>
        </div>
      </div>
      
      {/* Filters */}
      <div className="px-5 py-3 flex gap-2 overflow-x-auto">
        {filters.map((filter) => {
          const count = mockQuotes.filter(q => q.status === filter.id).length;
          return (
            <button
              key={filter.id}
              onClick={() => setActiveFilter(filter.id)}
              className={cn(
                "px-4 py-2 text-sm font-medium rounded-full whitespace-nowrap transition-colors",
                activeFilter === filter.id
                  ? "bg-blue-600 text-white"
                  : "bg-white text-neutral-600 border border-neutral-200 hover:bg-neutral-50"
              )}
            >
              {filter.label}
              {count > 0 && (
                <span className={cn(
                  "ml-1.5 px-1.5 py-0.5 text-xs rounded-full",
                  activeFilter === filter.id
                    ? "bg-white/20"
                    : "bg-neutral-100"
                )}>
                  {count}
                </span>
              )}
            </button>
          );
        })}
      </div>
      
      {/* Quotes list */}
      {filteredQuotes.length === 0 ? (
        <EmptyState
          icon="📝"
          title={`No ${activeFilter} quotes`}
          description={activeFilter === "pending" 
            ? "Create a new quote to get started." 
            : "Quotes will appear here when their status changes."
          }
          action={activeFilter === "pending" ? {
            label: "Create Quote",
            onClick: () => router.push("/more/quotes/new"),
          } : undefined}
        />
      ) : (
        <div className="px-5 pb-8">
          <div className="bg-white rounded-2xl border border-neutral-200 overflow-hidden">
            {filteredQuotes.map((quote, i) => (
              <React.Fragment key={quote.id}>
                <button
                  onClick={() => router.push(`/more/quotes/${quote.id}`)}
                  className="w-full p-4 text-left hover:bg-neutral-50 transition-colors"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="font-medium text-neutral-900">{quote.customerName}</p>
                      <p className="text-sm text-neutral-500 mt-0.5">{quote.job}</p>
                    </div>
                    <p className="font-semibold text-neutral-900">
                      £{quote.amount.toLocaleString()}
                    </p>
                  </div>
                  
                  <div className="flex items-center justify-between mt-3">
                    <div className="flex items-center gap-1.5">
                      <StatusIcon status={quote.status} />
                      <span className="text-xs text-neutral-500">
                        {quote.status === "pending" && `Expires in ${quote.expiresIn}`}
                        {quote.status === "accepted" && `Accepted ${quote.acceptedDate}`}
                        {quote.status === "declined" && `Declined ${quote.declinedDate}`}
                      </span>
                    </div>
                    <span className="text-xs text-neutral-400">
                      Sent {quote.sentDate}
                    </span>
                  </div>
                </button>
                {i < filteredQuotes.length - 1 && (
                  <div className="h-px bg-neutral-100 mx-4" />
                )}
              </React.Fragment>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
