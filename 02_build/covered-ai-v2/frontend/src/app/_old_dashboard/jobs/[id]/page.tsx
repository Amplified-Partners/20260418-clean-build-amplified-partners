"use client";

import React, { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import {
  Phone,
  Mail,
  MapPin,
  Calendar,
  Clock,
  MoreVertical,
  FileText,
  CheckCircle,
  XCircle,
  PlayCircle,
} from "lucide-react";
import { Header } from "@/components/layout";
import { Button, FixedBottomButton } from "@/components/ui";
import { useAuthContext } from "@/lib/auth-context";
import { useJob } from "@/lib/hooks";
import { jobsApi, type Job } from "@/lib/api";
import { cn } from "@/lib/utils";

type JobStatus = Job["status"];

function JobDetailSkeleton() {
  return (
    <main className="px-4 py-6 space-y-6 pb-32 animate-pulse">
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
        <div className="h-6 bg-[var(--grey-200)] rounded w-2/3 mb-2" />
        <div className="h-5 bg-[var(--grey-100)] rounded w-1/2 mb-4" />
        <div className="flex gap-2">
          <div className="h-9 bg-[var(--grey-100)] rounded-lg w-20" />
          <div className="h-9 bg-[var(--grey-100)] rounded-lg w-24" />
        </div>
      </div>
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-3">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="flex justify-between">
            <div className="h-4 bg-[var(--grey-100)] rounded w-1/4" />
            <div className="h-4 bg-[var(--grey-200)] rounded w-1/3" />
          </div>
        ))}
      </div>
    </main>
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

export default function JobDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { client } = useAuthContext();
  const jobId = params.id as string;
  const { data: job, isLoading, error, refetch } = useJob(client?.id || null, jobId);

  const [isUpdating, setIsUpdating] = useState(false);
  const [showActions, setShowActions] = useState(false);

  const handleStatusUpdate = async (newStatus: JobStatus) => {
    if (!client?.id || !jobId) return;
    setIsUpdating(true);
    try {
      await jobsApi.update(client.id, jobId, { status: newStatus });
      await refetch();
      setShowActions(false);
    } catch (err) {
      console.error("Failed to update job status:", err);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleCreateInvoice = () => {
    router.push(`/dashboard/invoices/new?jobId=${jobId}`);
  };

  if (isLoading) {
    return (
      <>
        <Header backButton title="Job Details" />
        <JobDetailSkeleton />
      </>
    );
  }

  if (error || !job) {
    return (
      <>
        <Header backButton title="Job Details" />
        <main className="px-4 py-6 pb-32">
          <div className="bg-red-50 rounded-xl border border-red-200 p-4 text-center">
            <p className="text-red-700">Failed to load job details</p>
          </div>
        </main>
      </>
    );
  }

  const statusActions: Partial<Record<JobStatus, { status: JobStatus; label: string; icon: typeof PlayCircle }>> = {
    scheduled: { status: "in_progress", label: "Start Job", icon: PlayCircle },
    in_progress: { status: "completed", label: "Complete Job", icon: CheckCircle },
  };
  const nextStatusAction = statusActions[job.status];

  return (
    <>
      <Header
        backButton
        title="Job Details"
        action={
          <button
            onClick={() => setShowActions(!showActions)}
            className="w-10 h-10 flex items-center justify-center text-[var(--grey-400)] hover:text-[var(--grey-600)] hover:bg-[var(--grey-100)] rounded-lg transition-colors"
          >
            <MoreVertical className="w-5 h-5" />
          </button>
        }
      />

      {/* Actions dropdown */}
      {showActions && (
        <>
          <div className="fixed inset-0 z-10" onClick={() => setShowActions(false)} />
          <div className="absolute right-4 top-16 bg-white rounded-lg shadow-lg border border-[var(--grey-200)] py-1 z-20 w-48">
            <button
              onClick={() => router.push(`/dashboard/jobs/${jobId}/edit`)}
              className="w-full px-4 py-2 text-left text-sm text-[var(--grey-700)] hover:bg-[var(--grey-50)]"
            >
              Edit Job
            </button>
            <button
              onClick={handleCreateInvoice}
              className="w-full px-4 py-2 text-left text-sm text-[var(--grey-700)] hover:bg-[var(--grey-50)]"
            >
              Create Invoice
            </button>
            {job.status !== "cancelled" && (
              <button
                onClick={() => handleStatusUpdate("cancelled" as JobStatus)}
                className="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50"
              >
                Cancel Job
              </button>
            )}
          </div>
        </>
      )}

      <main className="px-4 py-6 space-y-6 pb-32">
        {/* Job Header Card */}
        <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
          <div className="flex items-start justify-between mb-2">
            <h2 className="text-xl font-semibold text-[var(--grey-900)]">{job.title}</h2>
            <span
              className={cn(
                "px-2 py-0.5 text-xs font-medium rounded-full",
                getStatusColor(job.status)
              )}
            >
              {formatStatus(job.status)}
            </span>
          </div>
          <p className="text-[var(--grey-600)] font-medium">{job.customerName}</p>
          {job.customerPhone && (
            <p className="text-sm text-[var(--grey-500)] mt-1 flex items-center gap-2">
              <Phone className="w-4 h-4" />
              {job.customerPhone}
            </p>
          )}
          {job.address && (
            <p className="text-sm text-[var(--grey-500)] mt-1 flex items-center gap-2">
              <MapPin className="w-4 h-4" />
              {job.address}
            </p>
          )}

          <div className="flex gap-2 mt-4">
            {job.customerPhone && (
              <Button
                variant="secondary"
                size="sm"
                icon={<Phone className="w-4 h-4" />}
                onClick={() => window.open(`tel:${job.customerPhone?.replace(/\s/g, "")}`)}
              >
                Call
              </Button>
            )}
            {job.customerEmail && (
              <Button
                variant="secondary"
                size="sm"
                icon={<Mail className="w-4 h-4" />}
                onClick={() => window.open(`mailto:${job.customerEmail}`)}
              >
                Email
              </Button>
            )}
            {job.address && (
              <Button
                variant="secondary"
                size="sm"
                icon={<MapPin className="w-4 h-4" />}
                onClick={() =>
                  window.open(`https://maps.google.com/?q=${encodeURIComponent(job.address || "")}`)
                }
              >
                Map
              </Button>
            )}
          </div>
        </div>

        {/* Schedule */}
        <section>
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Schedule</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-3">
            {job.scheduledDate && (
              <div className="flex justify-between text-sm">
                <span className="text-[var(--grey-500)] flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  Date
                </span>
                <span className="text-[var(--grey-900)]">{job.scheduledDate}</span>
              </div>
            )}
            {job.scheduledTime && (
              <div className="flex justify-between text-sm">
                <span className="text-[var(--grey-500)] flex items-center gap-2">
                  <Clock className="w-4 h-4" />
                  Time
                </span>
                <span className="text-[var(--grey-900)]">{job.scheduledTime}</span>
              </div>
            )}
            {job.estimatedDuration && (
              <div className="flex justify-between text-sm">
                <span className="text-[var(--grey-500)]">Est. Duration</span>
                <span className="text-[var(--grey-900)]">{job.estimatedDuration}</span>
              </div>
            )}
          </div>
        </section>

        {/* Financials */}
        <section>
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Financials</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-3">
            {job.estimatedValue != null && (
              <div className="flex justify-between text-sm">
                <span className="text-[var(--grey-500)]">Estimated Value</span>
                <span className="text-[var(--grey-900)] font-medium">
                  £{job.estimatedValue.toLocaleString()}
                </span>
              </div>
            )}
            {job.actualValue != null && (
              <div className="flex justify-between text-sm">
                <span className="text-[var(--grey-500)]">Actual Value</span>
                <span className="text-[var(--grey-900)] font-medium">
                  £{job.actualValue.toLocaleString()}
                </span>
              </div>
            )}
            {job.invoiceId && (
              <div className="flex justify-between text-sm items-center">
                <span className="text-[var(--grey-500)]">Invoice</span>
                <button
                  onClick={() => router.push(`/dashboard/invoices/${job.invoiceId}`)}
                  className="text-[var(--brand-primary)] font-medium flex items-center gap-1"
                >
                  <FileText className="w-4 h-4" />
                  View Invoice
                </button>
              </div>
            )}
          </div>
        </section>

        {/* Description */}
        {job.description && (
          <section>
            <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Description</h3>
            <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
              <p className="text-sm text-[var(--grey-700)]">{job.description}</p>
            </div>
          </section>
        )}

        {/* Notes */}
        {job.notes && (
          <section>
            <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Notes</h3>
            <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
              <p className="text-sm text-[var(--grey-700)]">{job.notes}</p>
            </div>
          </section>
        )}

        {/* Linked Quote */}
        {job.quoteId && (
          <section>
            <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Linked Quote</h3>
            <div
              onClick={() => router.push(`/dashboard/quotes/${job.quoteId}`)}
              className="bg-white rounded-xl border border-[var(--grey-200)] p-4 cursor-pointer hover:bg-[var(--grey-50)]"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-[var(--grey-900)]">Quote #{job.quoteNumber}</p>
                  {job.quoteValue != null && (
                    <p className="text-sm text-[var(--grey-500)]">
                      £{job.quoteValue.toLocaleString()}
                    </p>
                  )}
                </div>
                <span className="text-sm text-[var(--brand-primary)]">View</span>
              </div>
            </div>
          </section>
        )}
      </main>

      {/* Bottom Action */}
      {nextStatusAction && (
        <FixedBottomButton
          onClick={() => handleStatusUpdate(nextStatusAction.status)}
          loading={isUpdating}
          icon={<nextStatusAction.icon className="w-5 h-5" />}
        >
          {nextStatusAction.label}
        </FixedBottomButton>
      )}

      {job.status === "completed" && !job.invoiceId && (
        <FixedBottomButton onClick={handleCreateInvoice} icon={<FileText className="w-5 h-5" />}>
          Create Invoice
        </FixedBottomButton>
      )}
    </>
  );
}
