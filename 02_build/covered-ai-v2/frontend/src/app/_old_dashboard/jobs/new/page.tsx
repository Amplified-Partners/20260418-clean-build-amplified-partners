"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Header } from "@/components/layout";
import { Button, FixedBottomButton } from "@/components/ui";
import { useAuthContext } from "@/lib/auth-context";
import { jobsApi, customersApi, callsApi } from "@/lib/api";

interface FormData {
  title: string;
  description: string;
  customerId: string;
  customerName: string;
  customerPhone: string;
  customerEmail: string;
  address: string;
  scheduledDate: string;
  scheduledTime: string;
  estimatedDuration: string;
  estimatedValue: string;
  notes: string;
}

function NewJobForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { client } = useAuthContext();

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState<FormData>({
    title: "",
    description: "",
    customerId: "",
    customerName: "",
    customerPhone: "",
    customerEmail: "",
    address: "",
    scheduledDate: "",
    scheduledTime: "",
    estimatedDuration: "",
    estimatedValue: "",
    notes: "",
  });

  // Pre-fill from call or customer
  useEffect(() => {
    const callId = searchParams.get("callId");
    const customerId = searchParams.get("customerId");

    if (callId && client?.id) {
      callsApi.getById(client.id, callId).then((call) => {
        if (call) {
          setFormData((prev) => ({
            ...prev,
            customerId: call.customerId || "",
            customerName: call.callerName || "",
            customerPhone: call.callerPhone || "",
            address: call.address || "",
            description: call.summary || "",
          }));
        }
      });
    } else if (customerId && client?.id) {
      customersApi.getById(client.id, customerId).then((customer) => {
        if (customer) {
          setFormData((prev) => ({
            ...prev,
            customerId: customer.id,
            customerName: customer.name,
            customerPhone: customer.phone || "",
            customerEmail: customer.email || "",
            address: customer.address || "",
          }));
        }
      });
    }
  }, [searchParams, client?.id]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async () => {
    if (!client?.id) return;
    if (!formData.title.trim()) {
      setError("Job title is required");
      return;
    }
    if (!formData.customerName.trim()) {
      setError("Customer name is required");
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const payload = {
        title: formData.title,
        description: formData.description || undefined,
        customerId: formData.customerId || undefined,
        customerName: formData.customerName,
        customerPhone: formData.customerPhone || undefined,
        customerEmail: formData.customerEmail || undefined,
        address: formData.address || undefined,
        scheduledDate: formData.scheduledDate || undefined,
        scheduledTime: formData.scheduledTime || undefined,
        estimatedDuration: formData.estimatedDuration || undefined,
        estimatedValue: formData.estimatedValue ? parseFloat(formData.estimatedValue) : undefined,
        notes: formData.notes || undefined,
        status: formData.scheduledDate ? "scheduled" : "pending",
      };

      const newJob = await jobsApi.create(client.id, payload);
      router.push(`/dashboard/jobs/${newJob.id}`);
    } catch (err) {
      console.error("Failed to create job:", err);
      setError("Failed to create job. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <Header backButton title="New Job" />
      <main className="px-4 py-6 space-y-6 pb-32">
        {error && (
          <div className="bg-red-50 rounded-xl border border-red-200 p-4 text-center">
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        )}

        {/* Job Details */}
        <section>
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Job Details</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-4">
            <div>
              <label className="block text-sm font-medium text-[var(--grey-700)] mb-1">
                Job Title *
              </label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleChange}
                placeholder="e.g., Boiler Repair"
                className="w-full h-11 px-3 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] placeholder:text-[var(--grey-400)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-[var(--grey-700)] mb-1">
                Description
              </label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                placeholder="Describe the job..."
                rows={3}
                className="w-full px-3 py-2 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] placeholder:text-[var(--grey-400)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent resize-none"
              />
            </div>
          </div>
        </section>

        {/* Customer */}
        <section>
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Customer</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-4">
            <div>
              <label className="block text-sm font-medium text-[var(--grey-700)] mb-1">
                Customer Name *
              </label>
              <input
                type="text"
                name="customerName"
                value={formData.customerName}
                onChange={handleChange}
                placeholder="Full name"
                className="w-full h-11 px-3 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] placeholder:text-[var(--grey-400)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-[var(--grey-700)] mb-1">Phone</label>
              <input
                type="tel"
                name="customerPhone"
                value={formData.customerPhone}
                onChange={handleChange}
                placeholder="07700 900000"
                className="w-full h-11 px-3 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] placeholder:text-[var(--grey-400)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-[var(--grey-700)] mb-1">Email</label>
              <input
                type="email"
                name="customerEmail"
                value={formData.customerEmail}
                onChange={handleChange}
                placeholder="email@example.com"
                className="w-full h-11 px-3 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] placeholder:text-[var(--grey-400)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-[var(--grey-700)] mb-1">
                Address
              </label>
              <input
                type="text"
                name="address"
                value={formData.address}
                onChange={handleChange}
                placeholder="Full address"
                className="w-full h-11 px-3 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] placeholder:text-[var(--grey-400)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent"
              />
            </div>
          </div>
        </section>

        {/* Schedule */}
        <section>
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Schedule</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-[var(--grey-700)] mb-1">
                  Date
                </label>
                <input
                  type="date"
                  name="scheduledDate"
                  value={formData.scheduledDate}
                  onChange={handleChange}
                  className="w-full h-11 px-3 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-[var(--grey-700)] mb-1">
                  Time
                </label>
                <input
                  type="time"
                  name="scheduledTime"
                  value={formData.scheduledTime}
                  onChange={handleChange}
                  className="w-full h-11 px-3 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-[var(--grey-700)] mb-1">
                Estimated Duration
              </label>
              <input
                type="text"
                name="estimatedDuration"
                value={formData.estimatedDuration}
                onChange={handleChange}
                placeholder="e.g., 2 hours"
                className="w-full h-11 px-3 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] placeholder:text-[var(--grey-400)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent"
              />
            </div>
          </div>
        </section>

        {/* Pricing */}
        <section>
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Pricing</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
            <div>
              <label className="block text-sm font-medium text-[var(--grey-700)] mb-1">
                Estimated Value (£)
              </label>
              <input
                type="number"
                name="estimatedValue"
                value={formData.estimatedValue}
                onChange={handleChange}
                placeholder="0.00"
                min="0"
                step="0.01"
                className="w-full h-11 px-3 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] placeholder:text-[var(--grey-400)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent"
              />
            </div>
          </div>
        </section>

        {/* Notes */}
        <section>
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Notes</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
            <textarea
              name="notes"
              value={formData.notes}
              onChange={handleChange}
              placeholder="Internal notes about this job..."
              rows={3}
              className="w-full px-3 py-2 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] placeholder:text-[var(--grey-400)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent resize-none"
            />
          </div>
        </section>
      </main>

      <FixedBottomButton onClick={handleSubmit} loading={isSubmitting}>
        Create Job
      </FixedBottomButton>
    </>
  );
}

function NewJobSkeleton() {
  return (
    <>
      <Header backButton title="New Job" />
      <main className="px-4 py-6 space-y-6 pb-32 animate-pulse">
        <section>
          <div className="h-5 bg-[var(--grey-200)] rounded w-24 mb-2" />
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-4">
            <div className="h-11 bg-[var(--grey-100)] rounded-lg" />
            <div className="h-20 bg-[var(--grey-100)] rounded-lg" />
          </div>
        </section>
        <section>
          <div className="h-5 bg-[var(--grey-200)] rounded w-20 mb-2" />
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-11 bg-[var(--grey-100)] rounded-lg" />
            ))}
          </div>
        </section>
      </main>
    </>
  );
}

export default function NewJobPage() {
  return (
    <Suspense fallback={<NewJobSkeleton />}>
      <NewJobForm />
    </Suspense>
  );
}
