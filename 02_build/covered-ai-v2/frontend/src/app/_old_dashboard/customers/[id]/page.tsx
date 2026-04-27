"use client";

import React from "react";
import { useParams, useRouter } from "next/navigation";
import { Phone, Mail, MapPin, MoreVertical, Briefcase } from "lucide-react";
import { Header } from "@/components/layout";
import { Button } from "@/components/ui";
import { useAuthContext } from "@/lib/auth-context";
import { useCustomer } from "@/lib/hooks";
import { cn } from "@/lib/utils";

function CustomerDetailSkeleton() {
  return (
    <main className="px-4 py-6 space-y-6 pb-24 animate-pulse">
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 text-center">
        <div className="w-16 h-16 bg-[var(--grey-200)] rounded-full mx-auto mb-3" />
        <div className="h-6 bg-[var(--grey-200)] rounded w-1/3 mx-auto mb-2" />
        <div className="h-4 bg-[var(--grey-100)] rounded w-1/2 mx-auto mb-1" />
        <div className="h-4 bg-[var(--grey-100)] rounded w-2/3 mx-auto mb-4" />
        <div className="flex gap-2 justify-center">
          <div className="h-9 bg-[var(--grey-100)] rounded-lg w-20" />
          <div className="h-9 bg-[var(--grey-100)] rounded-lg w-20" />
          <div className="h-9 bg-[var(--grey-100)] rounded-lg w-28" />
        </div>
      </div>
      <div className="grid grid-cols-3 gap-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
            <div className="h-8 bg-[var(--grey-200)] rounded w-1/2 mx-auto mb-1" />
            <div className="h-4 bg-[var(--grey-100)] rounded w-2/3 mx-auto" />
          </div>
        ))}
      </div>
    </main>
  );
}

export default function CustomerDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { client } = useAuthContext();
  const customerId = params.id as string;
  const { data: customer, isLoading, error } = useCustomer(client?.id || null, customerId);

  if (isLoading) {
    return (
      <>
        <Header backButton title="Customer" />
        <CustomerDetailSkeleton />
      </>
    );
  }

  if (error || !customer) {
    return (
      <>
        <Header backButton title="Customer" />
        <main className="px-4 py-6 pb-24">
          <div className="bg-red-50 rounded-xl border border-red-200 p-4 text-center">
            <p className="text-red-700">Failed to load customer</p>
          </div>
        </main>
      </>
    );
  }

  return (
    <>
      <Header
        backButton
        title="Customer"
        action={
          <button className="w-10 h-10 flex items-center justify-center text-[var(--grey-400)] hover:text-[var(--grey-600)] hover:bg-[var(--grey-100)] rounded-lg transition-colors">
            <MoreVertical className="w-5 h-5" />
          </button>
        }
      />
      <main className="px-4 py-6 space-y-6 pb-24">
        {/* Customer Card */}
        <div className="bg-white rounded-xl border border-[var(--grey-200)] p-6 text-center">
          <div className="w-16 h-16 bg-[var(--brand-primary-light)] rounded-full flex items-center justify-center mx-auto mb-3">
            <span className="text-2xl text-[var(--brand-primary)] font-semibold">
              {customer.name.charAt(0).toUpperCase()}
            </span>
          </div>
          <h2 className="text-xl font-semibold text-[var(--grey-900)]">{customer.name}</h2>
          {customer.phone && (
            <p className="text-sm text-[var(--grey-500)] mt-1 flex items-center justify-center gap-2">
              <Phone className="w-4 h-4" />
              {customer.phone}
            </p>
          )}
          {customer.email && (
            <p className="text-sm text-[var(--grey-500)] mt-1 flex items-center justify-center gap-2">
              <Mail className="w-4 h-4" />
              {customer.email}
            </p>
          )}
          {customer.address && (
            <p className="text-sm text-[var(--grey-500)] mt-1 flex items-center justify-center gap-2">
              <MapPin className="w-4 h-4" />
              {customer.address}
            </p>
          )}

          <div className="flex gap-2 justify-center mt-4">
            <Button
              variant="secondary"
              size="sm"
              icon={<Phone className="w-4 h-4" />}
              onClick={() => window.open(`tel:${customer.phone?.replace(/\s/g, "")}`)}
            >
              Call
            </Button>
            {customer.email && (
              <Button
                variant="secondary"
                size="sm"
                icon={<Mail className="w-4 h-4" />}
                onClick={() => window.open(`mailto:${customer.email}`)}
              >
                Email
              </Button>
            )}
            <Button
              variant="secondary"
              size="sm"
              icon={<Briefcase className="w-4 h-4" />}
              onClick={() => router.push(`/dashboard/jobs/new?customerId=${customer.id}`)}
            >
              Create Job
            </Button>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-3">
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 text-center">
            <p className="text-2xl font-bold text-[var(--grey-900)]">{customer.totalJobs}</p>
            <p className="text-xs text-[var(--grey-500)]">Jobs</p>
          </div>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 text-center">
            <p className="text-2xl font-bold text-[var(--grey-900)]">
              £{customer.totalRevenue.toLocaleString()}
            </p>
            <p className="text-xs text-[var(--grey-500)]">Total</p>
          </div>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 text-center">
            <p className="text-2xl font-bold text-[var(--grey-900)]">
              £{Math.round(customer.avgJobValue).toLocaleString()}
            </p>
            <p className="text-xs text-[var(--grey-500)]">Avg</p>
          </div>
        </div>

        {/* Jobs */}
        {customer.jobs && customer.jobs.length > 0 && (
          <section>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-[var(--grey-500)]">Jobs</h3>
              <button
                onClick={() => router.push(`/dashboard/jobs?customerId=${customer.id}`)}
                className="text-sm text-[var(--brand-primary)] font-medium"
              >
                See all
              </button>
            </div>
            <div className="bg-white rounded-xl border border-[var(--grey-200)] divide-y divide-[var(--grey-100)]">
              {customer.jobs.slice(0, 3).map((job) => (
                <div
                  key={job.id}
                  onClick={() => router.push(`/dashboard/jobs/${job.id}`)}
                  className="px-4 py-3 cursor-pointer hover:bg-[var(--grey-50)]"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium text-[var(--grey-900)]">{job.title}</p>
                      <p className="text-sm text-[var(--grey-500)]">
                        {job.estimatedValue ? `£${job.estimatedValue}` : ""}
                      </p>
                    </div>
                    <span
                      className={cn(
                        "px-2 py-0.5 text-xs font-medium rounded-full",
                        job.status === "completed"
                          ? "bg-green-100 text-green-700"
                          : job.status === "cancelled"
                          ? "bg-red-100 text-red-700"
                          : "bg-blue-100 text-blue-700"
                      )}
                    >
                      {job.status.charAt(0).toUpperCase() + job.status.slice(1)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Invoices */}
        {customer.invoices && customer.invoices.length > 0 && (
          <section>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-[var(--grey-500)]">Invoices</h3>
              <button
                onClick={() => router.push(`/dashboard/invoices?customerId=${customer.id}`)}
                className="text-sm text-[var(--brand-primary)] font-medium"
              >
                See all
              </button>
            </div>
            <div className="bg-white rounded-xl border border-[var(--grey-200)] divide-y divide-[var(--grey-100)]">
              {customer.invoices.slice(0, 3).map((invoice) => (
                <div
                  key={invoice.id}
                  onClick={() => router.push(`/dashboard/invoices/${invoice.id}`)}
                  className="px-4 py-3 cursor-pointer hover:bg-[var(--grey-50)]"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium text-[var(--grey-900)]">{invoice.invoiceNumber}</p>
                      <p className="text-sm text-[var(--grey-500)]">£{invoice.amount}</p>
                    </div>
                    <span
                      className={cn(
                        "px-2 py-0.5 text-xs font-medium rounded-full",
                        invoice.status === "PAID"
                          ? "bg-green-100 text-green-700"
                          : invoice.status === "OVERDUE"
                          ? "bg-red-100 text-red-700"
                          : "bg-blue-100 text-blue-700"
                      )}
                    >
                      {invoice.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Notes */}
        {customer.notes && (
          <section>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-[var(--grey-500)]">Notes</h3>
              <button className="text-sm text-[var(--brand-primary)] font-medium">Edit</button>
            </div>
            <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
              <p className="text-sm text-[var(--grey-700)]">{customer.notes}</p>
            </div>
          </section>
        )}
      </main>
    </>
  );
}
