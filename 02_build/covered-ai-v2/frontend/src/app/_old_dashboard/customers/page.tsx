"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Plus, ChevronDown } from "lucide-react";
import { Header } from "@/components/layout";
import { Button, FilterTabs, EmptyState } from "@/components/ui";
import { useAuthContext } from "@/lib/auth-context";
import { useCustomers } from "@/lib/hooks";
import { cn } from "@/lib/utils";

const filterTabs = [
  { id: "all", label: "All" },
  { id: "active", label: "Active" },
  { id: "lead", label: "Leads" },
  { id: "inactive", label: "Inactive" },
];

const sortOptions = [
  { value: "ltv", label: "Lifetime Value" },
  { value: "jobs", label: "Most Jobs" },
  { value: "recent", label: "Most Recent" },
  { value: "name", label: "Name A-Z" },
];

function CustomersSkeleton() {
  return (
    <div className="animate-pulse">
      {[1, 2, 3, 4].map((i) => (
        <div key={i} className="px-4 py-4 border-b border-[var(--grey-100)]">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-[var(--grey-200)] rounded-full" />
            <div className="flex-1">
              <div className="h-5 bg-[var(--grey-200)] rounded w-1/3 mb-2" />
              <div className="h-4 bg-[var(--grey-100)] rounded w-1/2" />
            </div>
            <div className="h-9 bg-[var(--grey-100)] rounded-lg w-16" />
          </div>
        </div>
      ))}
    </div>
  );
}

export default function CustomersPage() {
  const router = useRouter();
  const { client } = useAuthContext();
  const [activeFilter, setActiveFilter] = useState("all");
  const [sortBy, setSortBy] = useState("ltv");
  const [showSortDropdown, setShowSortDropdown] = useState(false);

  const { data, isLoading, error } = useCustomers(client?.id || null, {
    status: activeFilter === "all" ? undefined : activeFilter,
    sort: sortBy,
  });

  const customers = data?.customers || [];

  if (isLoading) {
    return (
      <>
        <Header
          title="Customers"
          action={
            <Button size="sm" icon={<Plus className="w-4 h-4" />}>
              Add
            </Button>
          }
        />
        <main className="pb-24">
          <div className="pt-4">
            <FilterTabs tabs={filterTabs} activeTab={activeFilter} onChange={setActiveFilter} />
          </div>
          <CustomersSkeleton />
        </main>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Header title="Customers" />
        <main className="pb-24 px-4 pt-6">
          <div className="bg-red-50 rounded-xl border border-red-200 p-4 text-center">
            <p className="text-red-700">Failed to load customers</p>
          </div>
        </main>
      </>
    );
  }

  if (customers.length === 0 && activeFilter === "all") {
    return (
      <>
        <Header title="Customers" />
        <main className="pb-24">
          <EmptyState
            icon="👥"
            title="No customers yet"
            description="Customers are added automatically from calls and jobs."
          />
        </main>
      </>
    );
  }

  return (
    <>
      <Header
        title="Customers"
        action={
          <Button
            size="sm"
            icon={<Plus className="w-4 h-4" />}
            onClick={() => router.push("/dashboard/customers/new")}
          >
            Add
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
          {customers.map((customer) => (
            <li
              key={customer.id}
              onClick={() => router.push(`/dashboard/customers/${customer.id}`)}
              className="px-4 py-4 cursor-pointer hover:bg-[var(--grey-50)] transition-colors"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-[var(--brand-primary-light)] rounded-full flex items-center justify-center">
                  <span className="text-[var(--brand-primary)] font-medium">
                    {customer.name.charAt(0).toUpperCase()}
                  </span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-[var(--grey-900)]">{customer.name}</p>
                  <p className="text-sm text-[var(--grey-500)]">
                    {customer.totalJobs} jobs • Last: {customer.lastJobDate || "N/A"}
                  </p>
                  <p className="text-sm text-[var(--grey-600)] font-medium">
                    LTV: £{customer.totalRevenue.toLocaleString()}
                  </p>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    router.push(`/dashboard/customers/${customer.id}`);
                  }}
                  className="h-9 px-4 text-sm font-medium rounded-lg bg-[var(--grey-100)] hover:bg-[var(--grey-200)] text-[var(--grey-600)] transition-colors"
                >
                  View
                </button>
              </div>
            </li>
          ))}
        </ul>
      </main>
    </>
  );
}
