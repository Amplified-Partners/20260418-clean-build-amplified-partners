"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Plus } from "lucide-react";
import { Header } from "@/components/layout";
import { Button, FilterTabs, SummaryCards, EmptyState } from "@/components/ui";
import { cn } from "@/lib/utils";
import { useAuthContext } from "@/lib/auth-context";
import { useInvoices, useInvoiceSummary } from "@/lib/hooks";
import { invoicesApi, type Invoice } from "@/lib/api";

const filterTabs = [
  { id: "all", label: "All" },
  { id: "DRAFT", label: "Draft" },
  { id: "SENT", label: "Sent" },
  { id: "OVERDUE", label: "Overdue" },
  { id: "PAID", label: "Paid" },
];

function getStatusBadge(status: Invoice["status"]) {
  switch (status) {
    case "DRAFT":
      return { label: "Draft", className: "bg-[var(--grey-100)] text-[var(--grey-600)]" };
    case "SENT":
      return { label: "Sent", className: "bg-blue-100 text-blue-700" };
    case "REMINDED":
      return { label: "Reminded", className: "bg-amber-100 text-amber-700" };
    case "OVERDUE":
      return { label: "Overdue", className: "bg-red-100 text-red-700" };
    case "PAID":
      return { label: "Paid", className: "bg-green-100 text-green-700" };
    case "CANCELLED":
      return { label: "Cancelled", className: "bg-[var(--grey-100)] text-[var(--grey-500)]" };
    default:
      return { label: status, className: "bg-[var(--grey-100)] text-[var(--grey-600)]" };
  }
}

// Loading skeleton
function InvoicesSkeleton() {
  return (
    <main className="pb-24">
      <div className="px-4 pt-2 animate-pulse">
        <div className="grid grid-cols-3 gap-3 mb-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="bg-white rounded-lg border border-[var(--grey-200)] p-3">
              <div className="h-6 bg-[var(--grey-200)] rounded w-2/3 mb-1" />
              <div className="h-3 bg-[var(--grey-100)] rounded w-1/2" />
            </div>
          ))}
        </div>
        <div className="h-10 bg-[var(--grey-100)] rounded mb-4" />
        <div className="space-y-2">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="bg-white rounded-lg border border-[var(--grey-200)] p-4">
              <div className="h-5 bg-[var(--grey-200)] rounded w-1/3 mb-2" />
              <div className="h-4 bg-[var(--grey-100)] rounded w-2/3" />
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}

export default function InvoicesPage() {
  const router = useRouter();
  const { client } = useAuthContext();
  const [activeFilter, setActiveFilter] = useState("all");
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  const statusFilter = activeFilter === "all" ? undefined : activeFilter;
  const { data, isLoading, error, refetch } = useInvoices(client?.id || null, statusFilter);
  const { data: summary } = useInvoiceSummary(client?.id || null);

  const invoices = data?.invoices || [];

  // Handle send invoice
  const handleSend = async (invoiceId: string) => {
    if (!client?.id) return;
    setActionLoading(invoiceId);
    try {
      await invoicesApi.send(client.id, invoiceId);
      refetch();
    } catch (err) {
      console.error("Failed to send invoice:", err);
    } finally {
      setActionLoading(null);
    }
  };

  // Handle chase invoice (send reminder)
  const handleChase = async (invoiceId: string) => {
    if (!client?.id) return;
    setActionLoading(invoiceId);
    try {
      await invoicesApi.sendReminder(client.id, invoiceId);
      refetch();
    } catch (err) {
      console.error("Failed to send reminder:", err);
    } finally {
      setActionLoading(null);
    }
  };

  if (isLoading) {
    return (
      <>
        <Header
          title="Invoices"
          action={
            <Button
              size="sm"
              icon={<Plus className="w-4 h-4" />}
              onClick={() => router.push("/invoices/new")}
            >
              New
            </Button>
          }
        />
        <InvoicesSkeleton />
      </>
    );
  }

  if (error) {
    return (
      <>
        <Header title="Invoices" />
        <main className="px-4 py-6 pb-24">
          <div className="bg-red-50 rounded-xl border border-red-200 p-4 text-center">
            <p className="text-red-700">Failed to load invoices</p>
            <button
              onClick={() => refetch()}
              className="mt-2 text-sm text-red-600 underline"
            >
              Try again
            </button>
          </div>
        </main>
      </>
    );
  }

  if (invoices.length === 0 && activeFilter === "all") {
    return (
      <>
        <Header
          title="Invoices"
          action={
            <Button
              size="sm"
              icon={<Plus className="w-4 h-4" />}
              onClick={() => router.push("/invoices/new")}
            >
              New
            </Button>
          }
        />
        <main className="pb-24">
          <EmptyState
            icon="📄"
            title="No invoices yet"
            description="Create your first invoice in 60 seconds."
            action={{
              label: "Create invoice",
              onClick: () => router.push("/invoices/new"),
            }}
          />
        </main>
      </>
    );
  }

  // Summary values from API
  const outstanding = summary?.outstanding || 0;
  const overdue = summary?.overdue || 0;
  const collected = summary?.collected || 0;

  return (
    <>
      <Header
        title="Invoices"
        action={
          <Button
            size="sm"
            icon={<Plus className="w-4 h-4" />}
            onClick={() => router.push("/invoices/new")}
          >
            New
          </Button>
        }
      />
      <main className="pb-24">
        <SummaryCards
          cards={[
            { value: `£${outstanding.toLocaleString()}`, label: "Outstanding", variant: "default" },
            { value: `£${overdue.toLocaleString()}`, label: "Overdue", variant: "danger" },
            { value: `£${collected.toLocaleString()}`, label: "Collected", variant: "success" },
          ]}
        />

        <div className="pt-2">
          <FilterTabs tabs={filterTabs} activeTab={activeFilter} onChange={setActiveFilter} />
        </div>

        {invoices.length === 0 ? (
          <div className="px-4 py-12 text-center">
            <p className="text-[var(--grey-500)]">No invoices match this filter</p>
          </div>
        ) : (
          <ul className="divide-y divide-[var(--grey-100)] bg-white">
            {invoices.map((invoice) => {
              const badge = getStatusBadge(invoice.status);
              const isOverdue = invoice.status === "OVERDUE";
              const isDraft = invoice.status === "DRAFT";
              const isActionLoading = actionLoading === invoice.id;

              return (
                <li
                  key={invoice.id}
                  className={cn(
                    "px-4 py-4 cursor-pointer hover:bg-[var(--grey-50)] transition-colors",
                    isOverdue && "bg-red-50/30"
                  )}
                  onClick={() => router.push(`/invoices/${invoice.id}`)}
                >
                  <div className="flex items-center justify-between gap-3">
                    <div className="min-w-0">
                      <div className="flex items-center gap-2">
                        <p className="font-medium text-[var(--grey-900)]">
                          {invoice.invoiceNumber}
                        </p>
                        <span
                          className={cn(
                            "px-2 py-0.5 text-xs font-medium rounded-full",
                            badge.className
                          )}
                        >
                          {badge.label}
                        </span>
                      </div>
                      <p className="text-sm text-[var(--grey-500)] mt-0.5">
                        {invoice.customerName} • £{invoice.amount.toLocaleString()}
                      </p>
                      <p
                        className={cn(
                          "text-xs mt-1",
                          isOverdue ? "text-red-600" : "text-[var(--grey-500)]"
                        )}
                      >
                        {invoice.statusText}
                      </p>
                    </div>
                    <div onClick={(e) => e.stopPropagation()}>
                      {isDraft ? (
                        <button
                          onClick={() => handleSend(invoice.id)}
                          disabled={isActionLoading}
                          className="shrink-0 min-h-[44px] px-4 text-sm font-medium rounded-lg bg-[var(--brand-primary)] hover:bg-[var(--brand-primary-hover)] text-white transition-colors disabled:opacity-50"
                        >
                          {isActionLoading ? "..." : "Send"}
                        </button>
                      ) : isOverdue ? (
                        <button
                          onClick={() => handleChase(invoice.id)}
                          disabled={isActionLoading}
                          className="shrink-0 min-h-[44px] px-4 text-sm font-medium rounded-lg bg-amber-500 hover:bg-amber-600 text-white transition-colors disabled:opacity-50"
                        >
                          {isActionLoading ? "..." : "Chase"}
                        </button>
                      ) : (
                        <button
                          onClick={() => router.push(`/invoices/${invoice.id}`)}
                          className="shrink-0 min-h-[44px] px-4 text-sm font-medium rounded-lg bg-[var(--grey-100)] hover:bg-[var(--grey-200)] text-[var(--grey-600)] transition-colors"
                        >
                          View
                        </button>
                      )}
                    </div>
                  </div>
                </li>
              );
            })}
          </ul>
        )}
      </main>
    </>
  );
}
