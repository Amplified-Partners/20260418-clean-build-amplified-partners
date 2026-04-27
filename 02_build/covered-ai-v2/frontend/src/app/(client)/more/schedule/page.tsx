/**
 * Client App - Schedule Page
 * 
 * Today's jobs and upcoming work.
 * Simple calendar view.
 */

"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Plus, MapPin, Phone, ChevronLeft, ChevronRight } from "lucide-react";
import { Header, EmptyState } from "@/components/client-app";
import { cn } from "@/lib/utils";

// Mock data
const mockJobs = [
  {
    id: "1",
    date: "2024-12-02",
    time: "09:00",
    duration: "2h",
    customerName: "Mrs Chen",
    job: "Tap repair",
    address: "14 Park Road, NE3 4AB",
    phone: "+447712345678",
    status: "confirmed",
  },
  {
    id: "2",
    date: "2024-12-02",
    time: "14:00",
    duration: "1.5h",
    customerName: "Mr Abbas",
    job: "Boiler service",
    address: "82 High Street, NE1 2XY",
    phone: "+447712345679",
    status: "confirmed",
  },
  {
    id: "3",
    date: "2024-12-03",
    time: "10:00",
    duration: "3h",
    customerName: "Johnson family",
    job: "Bathroom renovation - day 1",
    address: "7 Oak Avenue, NE4 5CD",
    phone: "+447712345680",
    status: "confirmed",
  },
  {
    id: "4",
    date: "2024-12-04",
    time: "09:00",
    duration: "3h",
    customerName: "Johnson family",
    job: "Bathroom renovation - day 2",
    address: "7 Oak Avenue, NE4 5CD",
    phone: "+447712345680",
    status: "confirmed",
  },
];

function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);
  
  if (date.toDateString() === today.toDateString()) return "Today";
  if (date.toDateString() === tomorrow.toDateString()) return "Tomorrow";
  
  return date.toLocaleDateString("en-GB", { 
    weekday: "long", 
    day: "numeric", 
    month: "short" 
  });
}

function getWeekDates(offset: number = 0): Date[] {
  const today = new Date();
  const startOfWeek = new Date(today);
  startOfWeek.setDate(today.getDate() - today.getDay() + 1 + (offset * 7)); // Monday
  
  const dates: Date[] = [];
  for (let i = 0; i < 7; i++) {
    const date = new Date(startOfWeek);
    date.setDate(startOfWeek.getDate() + i);
    dates.push(date);
  }
  return dates;
}

export default function SchedulePage() {
  const router = useRouter();
  const [weekOffset, setWeekOffset] = useState(0);
  const [selectedDate, setSelectedDate] = useState<string>(
    new Date().toISOString().split("T")[0]
  );
  
  const weekDates = getWeekDates(weekOffset);
  const jobsForDate = mockJobs.filter(job => job.date === selectedDate);
  
  // Group all jobs by date for the dots
  const jobsByDate = mockJobs.reduce((acc, job) => {
    acc[job.date] = (acc[job.date] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
  
  return (
    <div className="min-h-screen bg-neutral-50">
      <Header
        title="Schedule"
        showBack
        onBack={() => router.back()}
        rightContent={
          <button
            onClick={() => router.push("/more/schedule/new")}
            className="p-2 text-blue-600"
          >
            <Plus className="w-6 h-6" />
          </button>
        }
      />
      
      {/* Week navigation */}
      <div className="bg-white border-b border-neutral-200">
        <div className="flex items-center justify-between px-4 py-2">
          <button
            onClick={() => setWeekOffset(weekOffset - 1)}
            className="p-2 text-neutral-400 hover:text-neutral-600"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
          <span className="text-sm font-medium text-neutral-600">
            {weekDates[0].toLocaleDateString("en-GB", { month: "short", year: "numeric" })}
          </span>
          <button
            onClick={() => setWeekOffset(weekOffset + 1)}
            className="p-2 text-neutral-400 hover:text-neutral-600"
          >
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
        
        {/* Day selector */}
        <div className="flex justify-around px-2 pb-3">
          {weekDates.map((date) => {
            const dateStr = date.toISOString().split("T")[0];
            const isSelected = dateStr === selectedDate;
            const isToday = date.toDateString() === new Date().toDateString();
            const hasJobs = jobsByDate[dateStr] > 0;
            
            return (
              <button
                key={dateStr}
                onClick={() => setSelectedDate(dateStr)}
                className={cn(
                  "flex flex-col items-center py-2 px-3 rounded-xl transition-colors",
                  isSelected ? "bg-blue-600" : "hover:bg-neutral-100"
                )}
              >
                <span className={cn(
                  "text-xs",
                  isSelected ? "text-blue-100" : "text-neutral-400"
                )}>
                  {date.toLocaleDateString("en-GB", { weekday: "short" }).slice(0, 1)}
                </span>
                <span className={cn(
                  "text-lg font-semibold mt-0.5",
                  isSelected ? "text-white" : isToday ? "text-blue-600" : "text-neutral-900"
                )}>
                  {date.getDate()}
                </span>
                {hasJobs && (
                  <div className={cn(
                    "w-1.5 h-1.5 rounded-full mt-1",
                    isSelected ? "bg-white" : "bg-blue-600"
                  )} />
                )}
              </button>
            );
          })}
        </div>
      </div>
      
      {/* Selected date */}
      <div className="px-5 py-3">
        <h2 className="text-lg font-semibold text-neutral-900">
          {formatDate(selectedDate)}
        </h2>
      </div>
      
      {/* Jobs for selected date */}
      {jobsForDate.length === 0 ? (
        <EmptyState
          icon="📅"
          title="No jobs scheduled"
          description="Enjoy your day off, or add a new job."
          action={{
            label: "Add Job",
            onClick: () => router.push("/more/schedule/new"),
          }}
        />
      ) : (
        <div className="px-5 space-y-3 pb-8">
          {jobsForDate.map((job) => (
            <button
              key={job.id}
              onClick={() => router.push(`/more/schedule/${job.id}`)}
              className="w-full bg-white rounded-xl border border-neutral-200 p-4 text-left hover:border-blue-300 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="font-medium text-neutral-900">{job.customerName}</p>
                  <p className="text-sm text-neutral-500">{job.job}</p>
                </div>
                <div className="text-right">
                  <p className="font-medium text-neutral-900">{job.time}</p>
                  <p className="text-xs text-neutral-400">{job.duration}</p>
                </div>
              </div>
              
              <div className="mt-3 pt-3 border-t border-neutral-100 flex items-center gap-4">
                <div className="flex items-center gap-1 text-neutral-500 text-sm">
                  <MapPin className="w-4 h-4" />
                  <span className="truncate">{job.address}</span>
                </div>
              </div>
              
              <div className="mt-3 flex gap-2">
                <a
                  href={`tel:${job.phone}`}
                  onClick={(e) => e.stopPropagation()}
                  className="flex-1 py-2 bg-neutral-100 text-neutral-700 text-sm font-medium rounded-lg text-center hover:bg-neutral-200 transition-colors"
                >
                  Call
                </a>
                <a
                  href={`https://maps.google.com/?q=${encodeURIComponent(job.address)}`}
                  onClick={(e) => e.stopPropagation()}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex-1 py-2 bg-neutral-100 text-neutral-700 text-sm font-medium rounded-lg text-center hover:bg-neutral-200 transition-colors"
                >
                  Navigate
                </a>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
