"use client";

import React, { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import {
  Phone,
  Mail,
  MapPin,
  MoreVertical,
  Send,
  CheckCircle,
  XCircle,
  Copy,
  FileText,
  Briefcase,
} from "lucide-react";
import { Header } from "@/components/layout";
import { Button, FixedBottomButton } from "@/components/ui";
import { useAuthContext } from "@/lib/auth-context";
import { useQuote } from "@/lib/hooks";
import { quotesApi, type Quote } from "@/lib/api";
import { cn } from "@/lib/utils";

type QuoteStatus = Quote["status"];

function QuoteDetailSkeleton() {
  return (
    <main className="px-4 py-6 space-y-6 pb-32 animate-pulse">
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
        <div className="h-6 bg-[var(--grey-200)] rounded w-1/3 mb-2" />
        <div className="h-5 bg-[var(--grey-100)] rounded w-1/2 mb-4" />
        <div className="flex gap-2">
          <div className="h-9 bg-[var(--grey-100)] rounded-lg w-20" />
          <div className="h-9 bg-[var(--grey-100)] rounded-lg w-24" />
        </div>
      </div>
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-12 bg-[var(--grey-100)] rounded" />
        ))}
      </div>
    </main>
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

export default function QuoteDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { client } = useAuthContext();
  const quoteId = params.id as string;
  const { data: quote, isLoading, error, refetch } = useQuote(client?.id || null, quoteId);

  const [isUpdating, setIsUpdating] = useState(false);
  const [showActions, setShowActions] = useState(false);

  const handleStatusUpdate = async (newStatus: QuoteStatus) => {
    if (!client?.id || !quoteId) return;
    setIsUpdating(true);
    try {
      await quotesApi.update(client.id, quoteId, { status: newStatus });
      await refetch();
      setShowActions(false);
    } catch (err) {
      console.error("Failed to update quote status:", err);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleSendQuote = async () => {
    if (!client?.id || !quoteId) return;
    setIsUpdating(true);
    try {
      await quotesApi.send(client.id, quoteId);
      await refetch();
    } catch (err) {
      console.error("Failed to send quote:", err);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDuplicate = async () => {
    if (!client?.id || !quoteId) return;
    try {
      const newQuote = await quotesApi.duplicate(client.id, quoteId);
      router.push(`/dashboard/quotes/${newQuote.id}`);
    } catch (err) {
      console.error("Failed to duplicate quote:", err);
    }
  };

  const handleConvertToJob = () => {
    router.push(`/dashboard/jobs/new?quoteId=${quoteId}`);
  };

  if (isLoading) {
    return (
      <>
        <Header backButton title="Quote" />
        <QuoteDetailSkeleton />
      </>
    );
  }

  if (error || !quote) {
    return (
      <>
        <Header backButton title="Quote" />
        <main className="px-4 py-6 pb-32">
          <div className="bg-red-50 rounded-xl border border-red-200 p-4 text-center">
            <p className="text-red-700">Failed to load quote</p>
          </div>
        </main>
      </>
    );
  }

  return (
    <>
      <Header
        backButton
        title="Quote"
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
              onClick={() => router.push(`/dashboard/quotes/${quoteId}/edit`)}
              className="w-full px-4 py-2 text-left text-sm text-[var(--grey-700)] hover:bg-[var(--grey-50)]"
            >
              Edit Quote
            </button>
            <button
              onClick={handleDuplicate}
              className="w-full px-4 py-2 text-left text-sm text-[var(--grey-700)] hover:bg-[var(--grey-50)] flex items-center gap-2"
            >
              <Copy className="w-4 h-4" />
              Duplicate
            </button>
            {quote.status === "accepted" && (
              <button
                onClick={handleConvertToJob}
                className="w-full px-4 py-2 text-left text-sm text-[var(--grey-700)] hover:bg-[var(--grey-50)] flex items-center gap-2"
              >
                <Briefcase className="w-4 h-4" />
                Convert to Job
              </button>
            )}
            {quote.status === "sent" && (
              <>
                <button
                  onClick={() => handleStatusUpdate("accepted")}
                  className="w-full px-4 py-2 text-left text-sm text-green-600 hover:bg-green-50 flex items-center gap-2"
                >
                  <CheckCircle className="w-4 h-4" />
                  Mark Accepted
                </button>
                <button
                  onClick={() => handleStatusUpdate("declined")}
                  className="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 flex items-center gap-2"
                >
                  <XCircle className="w-4 h-4" />
                  Mark Declined
                </button>
              </>
            )}
          </div>
        </>
      )}

      <main className="px-4 py-6 space-y-6 pb-32">
        {/* Quote Header Card */}
        <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
          <div className="flex items-start justify-between mb-2">
            <div>
              <p className="text-sm text-[var(--grey-500)]">{quote.quoteNumber}</p>
              <h2 className="text-xl font-semibold text-[var(--grey-900)]">{quote.title}</h2>
            </div>
            <span
              className={cn(
                "px-2 py-0.5 text-xs font-medium rounded-full",
                getStatusColor(quote.status)
              )}
            >
              {formatStatus(quote.status)}
            </span>
          </div>
          <p className="text-[var(--grey-600)] font-medium">{quote.customerName}</p>
          {quote.customerPhone && (
            <p className="text-sm text-[var(--grey-500)] mt-1 flex items-center gap-2">
              <Phone className="w-4 h-4" />
              {quote.customerPhone}
            </p>
          )}
          {quote.customerEmail && (
            <p className="text-sm text-[var(--grey-500)] mt-1 flex items-center gap-2">
              <Mail className="w-4 h-4" />
              {quote.customerEmail}
            </p>
          )}
          {quote.address && (
            <p className="text-sm text-[var(--grey-500)] mt-1 flex items-center gap-2">
              <MapPin className="w-4 h-4" />
              {quote.address}
            </p>
          )}

          <div className="flex gap-2 mt-4">
            {quote.customerPhone && (
              <Button
                variant="secondary"
                size="sm"
                icon={<Phone className="w-4 h-4" />}
                onClick={() => window.open(`tel:${quote.customerPhone?.replace(/\s/g, "")}`)}
              >
                Call
              </Button>
            )}
            {quote.customerEmail && (
              <Button
                variant="secondary"
                size="sm"
                icon={<Mail className="w-4 h-4" />}
                onClick={() => window.open(`mailto:${quote.customerEmail}`)}
              >
                Email
              </Button>
            )}
          </div>
        </div>

        {/* Line Items */}
        <section>
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Items</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] divide-y divide-[var(--grey-100)]">
            {quote.items?.map((item, index) => (
              <div key={index} className="p-4">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <p className="font-medium text-[var(--grey-900)]">{item.description}</p>
                    {item.quantity > 1 && (
                      <p className="text-sm text-[var(--grey-500)]">
                        {item.quantity} x £{item.unitPrice.toFixed(2)}
                      </p>
                    )}
                  </div>
                  <p className="font-medium text-[var(--grey-900)]">£{item.total.toFixed(2)}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Totals */}
        <section>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-[var(--grey-500)]">Subtotal</span>
              <span className="text-[var(--grey-900)]">£{quote.subtotal.toFixed(2)}</span>
            </div>
            {quote.discount > 0 && (
              <div className="flex justify-between text-sm">
                <span className="text-[var(--grey-500)]">Discount</span>
                <span className="text-green-600">-£{quote.discount.toFixed(2)}</span>
              </div>
            )}
            {quote.vatAmount > 0 && (
              <div className="flex justify-between text-sm">
                <span className="text-[var(--grey-500)]">VAT ({quote.vatRate}%)</span>
                <span className="text-[var(--grey-900)]">£{quote.vatAmount.toFixed(2)}</span>
              </div>
            )}
            <div className="flex justify-between pt-3 border-t border-[var(--grey-100)]">
              <span className="font-semibold text-[var(--grey-900)]">Total</span>
              <span className="font-semibold text-[var(--grey-900)]">
                £{quote.total.toFixed(2)}
              </span>
            </div>
          </div>
        </section>

        {/* Validity */}
        {quote.validUntil && (
          <section>
            <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Validity</h3>
            <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
              <div className="flex justify-between text-sm">
                <span className="text-[var(--grey-500)]">Valid Until</span>
                <span className="text-[var(--grey-900)]">{quote.validUntil}</span>
              </div>
            </div>
          </section>
        )}

        {/* Notes */}
        {quote.notes && (
          <section>
            <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Notes</h3>
            <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
              <p className="text-sm text-[var(--grey-700)]">{quote.notes}</p>
            </div>
          </section>
        )}

        {/* Terms */}
        {quote.terms && (
          <section>
            <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Terms & Conditions</h3>
            <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
              <p className="text-sm text-[var(--grey-700)] whitespace-pre-wrap">{quote.terms}</p>
            </div>
          </section>
        )}

        {/* Linked Job */}
        {quote.jobId && (
          <section>
            <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Linked Job</h3>
            <div
              onClick={() => router.push(`/dashboard/jobs/${quote.jobId}`)}
              className="bg-white rounded-xl border border-[var(--grey-200)] p-4 cursor-pointer hover:bg-[var(--grey-50)]"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Briefcase className="w-5 h-5 text-[var(--grey-400)]" />
                  <span className="font-medium text-[var(--grey-900)]">{quote.jobTitle}</span>
                </div>
                <span className="text-sm text-[var(--brand-primary)]">View</span>
              </div>
            </div>
          </section>
        )}
      </main>

      {/* Bottom Action */}
      {quote.status === "draft" && (
        <FixedBottomButton
          onClick={handleSendQuote}
          loading={isUpdating}
          icon={<Send className="w-5 h-5" />}
        >
          Send Quote
        </FixedBottomButton>
      )}

      {quote.status === "accepted" && !quote.jobId && (
        <FixedBottomButton onClick={handleConvertToJob} icon={<Briefcase className="w-5 h-5" />}>
          Convert to Job
        </FixedBottomButton>
      )}
    </>
  );
}
