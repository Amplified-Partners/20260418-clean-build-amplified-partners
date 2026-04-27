"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Plus, ChevronDown, FileText } from "lucide-react";
import { Header } from "@/components/layout";
import { Button, FilterTabs, EmptyState } from "@/components/ui";
import { useAuthContext } from "@/lib/auth-context";
import { useQuotes } from "@/lib/hooks";
import { cn } from "@/lib/utils";

const filterTabs = [
  { id: "all", label: "All" },
  { id: "draft", label: "Draft" },
  { id: "sent", label: "Sent" },
  { id: "accepted", label: "Accepted" },
  { id: "declined", label: "Declined" },
];

const sortOptions = [
  { value: "date", label: "Date (Newest)" },
  { value: "value", label: "Value (Highest)" },
  { value: "customer", label: "Customer A-Z" },
];

function QuotesSkeleton() {
  return (
    <div className="animate-pulse">
      {[1, 2, 3, 4].map((i) => (
        <div key={i} className="px-4 py-4 border-b border-[var(--grey-100)]">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-[var(--grey-200)] rounded-lg" />
            <div className="flex-1">
              <div className="h-5 bg-[var(--grey-200)] rounded w-1/3 mb-2" />
              <div className="h-4 bg-[var(--grey-100)] rounded w-1/2 mb-2" />
              <div className="h-4 bg-[var(--grey-100)] rounded w-1/4" />
            </div>
            <div className="h-6 bg-[var(--grey-100)] rounded-full w-16" />
          </div>
        </div>
      ))}
    </div>
  );
}

function getStatusColor(status: string) {
  switch (status) {
    case "accepted":
      return "bg-green-100 text-green-700";
    case "sent":
      return "bg-blue-100 text-blue-700";
    case "draft":
      return "bg-amber-100 text-amber-700";
    case "declined":
      return "bg-red-100 text-red-700";
    case "expired":
      return "bg-[var(--grey-100)] text-[var(--grey-600)]";
    default:
      return "bg-[var(--grey-100)] text-[var(--grey-600)]";
  }
}

function formatStatus(status: string) {
  return status.charAt(0).toUpperCase() + status.slice(1);
}

export default function QuotesPage() {
  const router = useRouter();
  const { client } = useAuthContext();
  const [activeFilter, setActiveFilter] = useState("all");
  const [sortBy, setSortBy] = useState("date");
  const [showSortDropdown, setShowSortDropdown] = useState(false);

  const { data, isLoading, error } = useQuotes(client?.id || null, {
    status: activeFilter === "all" ? undefined : activeFilter,
    sort: sortBy,
  });

  const quotes = data?.quotes || [];

  if (isLoading) {
    return (
      <>
        <Header
          title="Quotes"
          action={
            <Button size="sm" icon={<Plus className="w-4 h-4" />}>
              New Quote
            </Button>
          }
        />
        <main className="pb-24">
          <div className="pt-4">
            <FilterTabs tabs={filterTabs} activeTab={activeFilter} onChange={setActiveFilter} />
          </div>
          <QuotesSkeleton />
        </main>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Header title="Quotes" />
        <main className="pb-24 px-4 pt-6">
          <div className="bg-red-50 rounded-xl border border-red-200 p-4 text-center">
            <p className="text-red-700">Failed to load quotes</p>
          </div>
        </main>
      </>
    );
  }

  if (quotes.length === 0 && activeFilter === "all") {
    return (
      <>
        <Header
          title="Quotes"
          action={
            <Button
              size="sm"
              icon={<Plus className="w-4 h-4" />}
              onClick={() => router.push("/dashboard/quotes/new")}
            >
              New Quote
            </Button>
          }
        />
        <main className="pb-24">
          <EmptyState
            icon="📝"
            title="No quotes yet"
            description="Create your first quote to send to customers."
            action={{
              label: "Create Quote",
              onClick: () => router.push("/dashboard/quotes/new"),
            }}
          />
        </main>
      </>
    );
  }

  return (
    <>
      <Header
        title="Quotes"
        action={
          <Button
            size="sm"
            icon={<Plus className="w-4 h-4" />}
            onClick={() => router.push("/dashboard/quotes/new")}
          >
            New Quote
          </Button>
        }
      />
      <main className="pb-24">
        <div className="pt-4">
          <FilterTabs tabs={filterTabs} activeTab={activeFilter} onChange={setActiveFilter} />
        </div>

        {/* Sort dropdown */}
        <div className="px-4 py-3 border-b border-[var(--grey-100)] relative">
          <button
            onClick={() => setShowSortDropdown(!showSortDropdown)}
            className="flex items-center gap-2 text-sm text-[var(--grey-600)]"
          >
            Sort: {sortOptions.find((o) => o.value === sortBy)?.label}
            <ChevronDown className="w-4 h-4" />
          </button>
          {showSortDropdown && (
            <>
              <div className="fixed inset-0 z-10" onClick={() => setShowSortDropdown(false)} />
              <div className="absolute left-4 top-full mt-1 bg-white rounded-lg shadow-lg border border-[var(--grey-200)] py-1 z-20 w-48">
                {sortOptions.map((option) => (
                  <button
                    key={option.value}
                    onClick={() => {
                      setSortBy(option.value);
                      setShowSortDropdown(false);
                    }}
                    className={cn(
                      "w-full px-4 py-2 text-left text-sm",
                      sortBy === option.value
                        ? "bg-[var(--brand-primary-light)] text-[var(--brand-primary)]"
                        : "text-[var(--grey-700)] hover:bg-[var(--grey-50)]"
                    )}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </>
          )}
        </div>

        <ul className="divide-y divide-[var(--grey-100)] bg-white">
          {quotes.map((quote) => (
            <li
              key={quote.id}
              onClick={() => router.push(`/dashboard/quotes/${quote.id}`)}
              className="px-4 py-4 cursor-pointer hover:bg-[var(--grey-50)] transition-colors"
            >
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-[var(--brand-primary-light)] rounded-lg flex items-center justify-center">
                  <FileText className="w-5 h-5 text-[var(--brand-primary)]" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <p className="font-medium text-[var(--grey-900)]">{quote.quoteNumber}</p>
                    <span
                      className={cn(
                        "px-2 py-0.5 text-xs font-medium rounded-full",
                        getStatusColor(quote.status)
                      )}
                    >
                      {formatStatus(quote.status)}
                    </span>
                  </div>
                  <p className="text-sm text-[var(--grey-600)] mt-0.5">{quote.customerName}</p>
                  <p className="text-sm text-[var(--grey-500)] mt-1">{quote.title}</p>
                  <div className="flex items-center justify-between mt-1">
                    <p className="text-sm font-medium text-[var(--grey-700)]">
                      £{quote.total.toLocaleString()}
                    </p>
                    {quote.validUntil && (
                      <p className="text-xs text-[var(--grey-500)]">Valid: {quote.validUntil}</p>
                    )}
                  </div>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </main>
    </>
  );
}
