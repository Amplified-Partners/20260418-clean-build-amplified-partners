"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Plus, ChevronDown, Calendar, MapPin } from "lucide-react";
import { Header } from "@/components/layout";
import { Button, FilterTabs, EmptyState } from "@/components/ui";
import { useAuthContext } from "@/lib/auth-context";
import { useJobs } from "@/lib/hooks";
import { cn } from "@/lib/utils";

const filterTabs = [
  { id: "all", label: "All" },
  { id: "scheduled", label: "Scheduled" },
  { id: "in_progress", label: "In Progress" },
  { id: "completed", label: "Completed" },
];

const sortOptions = [
  { value: "date", label: "Date (Newest)" },
  { value: "value", label: "Value (Highest)" },
  { value: "customer", label: "Customer A-Z" },
];

function JobsSkeleton() {
  return (
    <div className="animate-pulse">
      {[1, 2, 3, 4].map((i) => (
        <div key={i} className="px-4 py-4 border-b border-[var(--grey-100)]">
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 bg-[var(--grey-200)] rounded-lg" />
            <div className="flex-1">
              <div className="h-5 bg-[var(--grey-200)] rounded w-1/2 mb-2" />
              <div className="h-4 bg-[var(--grey-100)] rounded w-2/3 mb-2" />
              <div className="h-4 bg-[var(--grey-100)] rounded w-1/3" />
            </div>
            <div className="h-6 bg-[var(--grey-100)] rounded-full w-20" />
          </div>
        </div>
      ))}
    </div>
  );
}

function getStatusColor(status: string) {
  switch (status) {
    case "completed":
      return "bg-green-100 text-green-700";
    case "in_progress":
      return "bg-blue-100 text-blue-700";
    case "scheduled":
      return "bg-amber-100 text-amber-700";
    case "cancelled":
      return "bg-red-100 text-red-700";
    default:
      return "bg-[var(--grey-100)] text-[var(--grey-600)]";
  }
}

function formatStatus(status: string) {
  return status
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

export default function JobsPage() {
  const router = useRouter();
  const { client } = useAuthContext();
  const [activeFilter, setActiveFilter] = useState("all");
  const [sortBy, setSortBy] = useState("date");
  const [showSortDropdown, setShowSortDropdown] = useState(false);

  const { data, isLoading, error } = useJobs(client?.id || null, {
    status: activeFilter === "all" ? undefined : activeFilter,
    sort: sortBy,
  });

  const jobs = data?.jobs || [];

  // Group jobs by date
  const groupedJobs = jobs.reduce((acc, job) => {
    const date = job.scheduledDate || "Unscheduled";
    if (!acc[date]) {
      acc[date] = [];
    }
    acc[date].push(job);
    return acc;
  }, {} as Record<string, typeof jobs>);

  if (isLoading) {
    return (
      <>
        <Header
          title="Jobs"
          action={
            <Button size="sm" icon={<Plus className="w-4 h-4" />}>
              New Job
            </Button>
          }
        />
        <main className="pb-24">
          <div className="pt-4">
            <FilterTabs tabs={filterTabs} activeTab={activeFilter} onChange={setActiveFilter} />
          </div>
          <JobsSkeleton />
        </main>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Header title="Jobs" />
        <main className="pb-24 px-4 pt-6">
          <div className="bg-red-50 rounded-xl border border-red-200 p-4 text-center">
            <p className="text-red-700">Failed to load jobs</p>
          </div>
        </main>
      </>
    );
  }

  if (jobs.length === 0 && activeFilter === "all") {
    return (
      <>
        <Header
          title="Jobs"
          action={
            <Button
              size="sm"
              icon={<Plus className="w-4 h-4" />}
              onClick={() => router.push("/dashboard/jobs/new")}
            >
              New Job
            </Button>
          }
        />
        <main className="pb-24">
          <EmptyState
            icon="🔧"
            title="No jobs yet"
            description="Create your first job to get started."
            action={{
              label: "Create Job",
              onClick: () => router.push("/dashboard/jobs/new"),
            }}
          />
        </main>
      </>
    );
  }

  return (
    <>
      <Header
        title="Jobs"
        action={
          <Button
            size="sm"
            icon={<Plus className="w-4 h-4" />}
            onClick={() => router.push("/dashboard/jobs/new")}
          >
            New Job
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

        {Object.entries(groupedJobs).map(([date, dateJobs]) => (
          <div key={date}>
            <h3 className="px-4 py-2 text-sm font-medium text-[var(--grey-500)] bg-[var(--grey-50)]">
              {date}
            </h3>
            <ul className="divide-y divide-[var(--grey-100)] bg-white">
              {dateJobs.map((job) => (
                <li
                  key={job.id}
                  onClick={() => router.push(`/dashboard/jobs/${job.id}`)}
                  className="px-4 py-4 cursor-pointer hover:bg-[var(--grey-50)] transition-colors"
                >
                  <div className="flex items-start gap-3">
                    <div className="w-10 h-10 bg-[var(--brand-primary-light)] rounded-lg flex items-center justify-center">
                      <span className="text-lg">🔧</span>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <p className="font-medium text-[var(--grey-900)]">{job.title}</p>
                        <span
                          className={cn(
                            "px-2 py-0.5 text-xs font-medium rounded-full",
                            getStatusColor(job.status)
                          )}
                        >
                          {formatStatus(job.status)}
                        </span>
                      </div>
                      <p className="text-sm text-[var(--grey-600)] mt-0.5">{job.customerName}</p>
                      {job.address && (
                        <p className="text-sm text-[var(--grey-500)] mt-1 flex items-center gap-1">
                          <MapPin className="w-3.5 h-3.5" />
                          {job.address}
                        </p>
                      )}
                      {job.scheduledTime && (
                        <p className="text-sm text-[var(--grey-500)] mt-1 flex items-center gap-1">
                          <Calendar className="w-3.5 h-3.5" />
                          {job.scheduledTime}
                        </p>
                      )}
                      {job.estimatedValue && (
                        <p className="text-sm font-medium text-[var(--grey-700)] mt-1">
                          £{job.estimatedValue.toLocaleString()}
                        </p>
                      )}
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </main>
    </>
  );
}
