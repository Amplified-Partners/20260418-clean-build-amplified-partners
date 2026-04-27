"use client";

import React, { useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import { ChevronLeft, ChevronRight, Plus, MapPin, Clock } from "lucide-react";
import { Header } from "@/components/layout";
import { Button, EmptyState } from "@/components/ui";
import { useAuthContext } from "@/lib/auth-context";
import { useSchedule } from "@/lib/hooks";
import { cn } from "@/lib/utils";

const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const MONTHS = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

function getStatusColor(status: string) {
  switch (status) {
    case "completed":
      return "bg-green-500";
    case "in_progress":
      return "bg-blue-500";
    case "scheduled":
      return "bg-amber-500";
    case "cancelled":
      return "bg-red-500";
    default:
      return "bg-[var(--grey-400)]";
  }
}

function ScheduleSkeleton() {
  return (
    <div className="px-4 py-6 space-y-4 animate-pulse">
      <div className="grid grid-cols-7 gap-1">
        {[...Array(35)].map((_, i) => (
          <div key={i} className="h-12 bg-[var(--grey-100)] rounded" />
        ))}
      </div>
      <div className="space-y-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-20 bg-[var(--grey-100)] rounded-xl" />
        ))}
      </div>
    </div>
  );
}

export default function SchedulePage() {
  const router = useRouter();
  const { client } = useAuthContext();
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState<Date | null>(new Date());
  const [viewMode, setViewMode] = useState<"month" | "week">("month");

  // Get start and end of current view for API
  const dateRange = useMemo(() => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const start = new Date(year, month, 1);
    const end = new Date(year, month + 1, 0);
    return {
      start: start.toISOString().split("T")[0],
      end: end.toISOString().split("T")[0],
    };
  }, [currentDate]);

  const { data, isLoading, error } = useSchedule(client?.id || null, dateRange);

  const jobs = data?.jobs || [];

  // Calendar grid
  const calendarDays = useMemo(() => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const startPadding = firstDay.getDay();
    const daysInMonth = lastDay.getDate();

    const days: (Date | null)[] = [];

    // Add padding for days before month starts
    for (let i = 0; i < startPadding; i++) {
      days.push(null);
    }

    // Add days of month
    for (let i = 1; i <= daysInMonth; i++) {
      days.push(new Date(year, month, i));
    }

    return days;
  }, [currentDate]);

  // Get jobs for a specific date
  const getJobsForDate = (date: Date | null) => {
    if (!date) return [];
    const dateStr = date.toISOString().split("T")[0];
    return jobs.filter((job) => job.scheduledDate === dateStr);
  };

  // Jobs for selected date
  const selectedDateJobs = selectedDate ? getJobsForDate(selectedDate) : [];

  const navigateMonth = (direction: number) => {
    setCurrentDate((prev) => {
      const newDate = new Date(prev);
      newDate.setMonth(prev.getMonth() + direction);
      return newDate;
    });
  };

  const isToday = (date: Date | null) => {
    if (!date) return false;
    const today = new Date();
    return (
      date.getDate() === today.getDate() &&
      date.getMonth() === today.getMonth() &&
      date.getFullYear() === today.getFullYear()
    );
  };

  const isSelected = (date: Date | null) => {
    if (!date || !selectedDate) return false;
    return (
      date.getDate() === selectedDate.getDate() &&
      date.getMonth() === selectedDate.getMonth() &&
      date.getFullYear() === selectedDate.getFullYear()
    );
  };

  if (error) {
    return (
      <>
        <Header title="Schedule" />
        <main className="pb-24 px-4 pt-6">
          <div className="bg-red-50 rounded-xl border border-red-200 p-4 text-center">
            <p className="text-red-700">Failed to load schedule</p>
          </div>
        </main>
      </>
    );
  }

  return (
    <>
      <Header
        title="Schedule"
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
        {/* Month Navigation */}
        <div className="px-4 py-3 flex items-center justify-between bg-white border-b border-[var(--grey-100)]">
          <button
            onClick={() => navigateMonth(-1)}
            className="w-10 h-10 flex items-center justify-center rounded-lg hover:bg-[var(--grey-100)] transition-colors"
          >
            <ChevronLeft className="w-5 h-5 text-[var(--grey-600)]" />
          </button>
          <h2 className="text-lg font-semibold text-[var(--grey-900)]">
            {MONTHS[currentDate.getMonth()]} {currentDate.getFullYear()}
          </h2>
          <button
            onClick={() => navigateMonth(1)}
            className="w-10 h-10 flex items-center justify-center rounded-lg hover:bg-[var(--grey-100)] transition-colors"
          >
            <ChevronRight className="w-5 h-5 text-[var(--grey-600)]" />
          </button>
        </div>

        {/* View Toggle */}
        <div className="px-4 py-2 flex gap-2 bg-[var(--grey-50)]">
          <button
            onClick={() => setViewMode("month")}
            className={cn(
              "px-3 py-1.5 text-sm font-medium rounded-lg transition-colors",
              viewMode === "month"
                ? "bg-white text-[var(--grey-900)] shadow-sm"
                : "text-[var(--grey-500)] hover:text-[var(--grey-700)]"
            )}
          >
            Month
          </button>
          <button
            onClick={() => setViewMode("week")}
            className={cn(
              "px-3 py-1.5 text-sm font-medium rounded-lg transition-colors",
              viewMode === "week"
                ? "bg-white text-[var(--grey-900)] shadow-sm"
                : "text-[var(--grey-500)] hover:text-[var(--grey-700)]"
            )}
          >
            Week
          </button>
        </div>

        {isLoading ? (
          <ScheduleSkeleton />
        ) : (
          <>
            {/* Calendar Grid */}
            <div className="px-4 py-4 bg-white">
              {/* Day headers */}
              <div className="grid grid-cols-7 mb-2">
                {DAYS.map((day) => (
                  <div
                    key={day}
                    className="text-center text-xs font-medium text-[var(--grey-500)] py-2"
                  >
                    {day}
                  </div>
                ))}
              </div>

              {/* Calendar days */}
              <div className="grid grid-cols-7 gap-1">
                {calendarDays.map((date, index) => {
                  const dayJobs = getJobsForDate(date);
                  const hasJobs = dayJobs.length > 0;

                  return (
                    <button
                      key={index}
                      onClick={() => date && setSelectedDate(date)}
                      disabled={!date}
                      className={cn(
                        "aspect-square p-1 rounded-lg flex flex-col items-center justify-center transition-colors relative",
                        !date && "invisible",
                        date && "hover:bg-[var(--grey-100)]",
                        isToday(date) && "bg-[var(--brand-primary-light)]",
                        isSelected(date) && "ring-2 ring-[var(--brand-primary)]"
                      )}
                    >
                      <span
                        className={cn(
                          "text-sm",
                          isToday(date)
                            ? "font-semibold text-[var(--brand-primary)]"
                            : "text-[var(--grey-900)]"
                        )}
                      >
                        {date?.getDate()}
                      </span>
                      {hasJobs && (
                        <div className="flex gap-0.5 mt-0.5">
                          {dayJobs.slice(0, 3).map((job, i) => (
                            <div
                              key={i}
                              className={cn("w-1.5 h-1.5 rounded-full", getStatusColor(job.status))}
                            />
                          ))}
                          {dayJobs.length > 3 && (
                            <span className="text-[8px] text-[var(--grey-500)]">
                              +{dayJobs.length - 3}
                            </span>
                          )}
                        </div>
                      )}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Selected Date Jobs */}
            {selectedDate && (
              <div className="px-4 py-4">
                <h3 className="text-sm font-medium text-[var(--grey-500)] mb-3">
                  {selectedDate.toLocaleDateString("en-GB", {
                    weekday: "long",
                    day: "numeric",
                    month: "long",
                  })}
                </h3>

                {selectedDateJobs.length === 0 ? (
                  <div className="bg-white rounded-xl border border-[var(--grey-200)] p-6 text-center">
                    <p className="text-[var(--grey-500)]">No jobs scheduled</p>
                    <Button
                      variant="secondary"
                      size="sm"
                      className="mt-3"
                      onClick={() =>
                        router.push(
                          `/dashboard/jobs/new?date=${selectedDate.toISOString().split("T")[0]}`
                        )
                      }
                    >
                      Add Job
                    </Button>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {selectedDateJobs.map((job) => (
                      <div
                        key={job.id}
                        onClick={() => router.push(`/dashboard/jobs/${job.id}`)}
                        className="bg-white rounded-xl border border-[var(--grey-200)] p-4 cursor-pointer hover:bg-[var(--grey-50)] transition-colors"
                      >
                        <div className="flex items-start gap-3">
                          <div
                            className={cn(
                              "w-1 h-full min-h-[40px] rounded-full",
                              getStatusColor(job.status)
                            )}
                          />
                          <div className="flex-1">
                            <p className="font-medium text-[var(--grey-900)]">{job.title}</p>
                            <p className="text-sm text-[var(--grey-600)]">{job.customerName}</p>
                            {job.scheduledTime && (
                              <p className="text-sm text-[var(--grey-500)] mt-1 flex items-center gap-1">
                                <Clock className="w-3.5 h-3.5" />
                                {job.scheduledTime}
                              </p>
                            )}
                            {job.address && (
                              <p className="text-sm text-[var(--grey-500)] mt-1 flex items-center gap-1">
                                <MapPin className="w-3.5 h-3.5" />
                                {job.address}
                              </p>
                            )}
                          </div>
                          {job.estimatedValue && (
                            <p className="text-sm font-medium text-[var(--grey-700)]">
                              £{job.estimatedValue}
                            </p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </main>
    </>
  );
}
