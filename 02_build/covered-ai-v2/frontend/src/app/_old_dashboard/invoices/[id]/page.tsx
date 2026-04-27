"use client";

import React, { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Phone, Mail, MoreVertical, Download, Send, Edit, X, CheckCircle } from "lucide-react";
import { Header } from "@/components/layout";
import { Button, CelebrationModal } from "@/components/ui";
import { PaymentLinkButton } from "@/components/invoices";
import { useAuthContext } from "@/lib/auth-context";
import { useInvoice } from "@/lib/hooks";
import { invoicesApi } from "@/lib/api";
import { cn } from "@/lib/utils";

const statusStyles: Record<string, { bg: string; text: string; label: string }> = {
  DRAFT: { bg: "bg-[var(--grey-100)]", text: "text-[var(--grey-600)]", label: "Draft" },
  SENT: { bg: "bg-blue-100", text: "text-blue-700", label: "Sent" },
  REMINDED: { bg: "bg-amber-100", text: "text-amber-700", label: "Reminded" },
  OVERDUE: { bg: "bg-red-100", text: "text-red-700", label: "Overdue" },
  PAID: { bg: "bg-green-100", text: "text-green-700", label: "Paid" },
  CANCELLED: { bg: "bg-[var(--grey-100)]", text: "text-[var(--grey-500)]", label: "Cancelled" },
};

function InvoiceDetailSkeleton() {
  return (
    <main className="px-4 py-6 space-y-6 pb-32 animate-pulse">
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-6 text-center">
        <div className="h-6 bg-[var(--grey-200)] rounded w-20 mx-auto mb-4" />
        <div className="h-10 bg-[var(--grey-200)] rounded w-32 mx-auto mb-2" />
        <div className="h-4 bg-[var(--grey-100)] rounded w-24 mx-auto" />
      </div>
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-5 bg-[var(--grey-100)] rounded" />
        ))}
      </div>
    </main>
  );
}

export default function InvoiceDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { client } = useAuthContext();
  const invoiceId = params.id as string;
  const { data: invoice, isLoading, error, refetch } = useInvoice(client?.id || null, invoiceId);

  const [showMenu, setShowMenu] = useState(false);
  const [showCelebration, setShowCelebration] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);

  const handleSendReminder = async () => {
    if (!client?.id || !invoiceId) return;
    setIsUpdating(true);
    try {
      await invoicesApi.sendReminder(client.id, invoiceId);
      await refetch();
    } catch (err) {
      console.error("Failed to send reminder:", err);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleMarkAsPaid = async () => {
    if (!client?.id || !invoiceId) return;
    setIsUpdating(true);
    try {
      await invoicesApi.markPaid(client.id, invoiceId);
      await refetch();
      setShowCelebration(true);
    } catch (err) {
      console.error("Failed to mark as paid:", err);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleSendInvoice = async () => {
    if (!client?.id || !invoiceId) return;
    setIsUpdating(true);
    try {
      await invoicesApi.send(client.id, invoiceId);
      await refetch();
    } catch (err) {
      console.error("Failed to send invoice:", err);
    } finally {
      setIsUpdating(false);
    }
  };

  if (isLoading) {
    return (
      <>
        <Header backButton title="Invoice" />
        <InvoiceDetailSkeleton />
      </>
    );
  }

  if (error || !invoice) {
    return (
      <>
        <Header backButton title="Invoice" />
        <main className="px-4 py-6 pb-32">
          <div className="bg-red-50 rounded-xl border border-red-200 p-4 text-center">
            <p className="text-red-700">Failed to load invoice</p>
          </div>
        </main>
      </>
    );
  }

  const style = statusStyles[invoice.status] || statusStyles.DRAFT;
  const isOverdue = invoice.status === "OVERDUE";
  const isPaid = invoice.status === "PAID";
  const isDraft = invoice.status === "DRAFT";

  return (
    <>
      <Header
        backButton
        title={invoice.invoiceNumber}
        action={
          <div className="relative">
            <button
              onClick={() => setShowMenu(!showMenu)}
              className="w-10 h-10 flex items-center justify-center text-[var(--grey-400)] hover:text-[var(--grey-600)] hover:bg-[var(--grey-100)] rounded-lg transition-colors"
            >
              <MoreVertical className="w-5 h-5" />
            </button>
            {showMenu && (
              <>
                <div
                  className="fixed inset-0 z-10"
                  onClick={() => setShowMenu(false)}
                />
                <div className="absolute right-0 top-full mt-1 bg-white rounded-lg shadow-lg border border-[var(--grey-200)] py-1 z-20 w-48">
                  <button className="w-full px-4 py-2 text-left text-sm text-[var(--grey-700)] hover:bg-[var(--grey-50)] flex items-center gap-2">
                    <Download className="w-4 h-4" />
                    Download PDF
                  </button>
                  {!isPaid && (
                    <button
                      onClick={() => {
                        handleSendInvoice();
                        setShowMenu(false);
                      }}
                      className="w-full px-4 py-2 text-left text-sm text-[var(--grey-700)] hover:bg-[var(--grey-50)] flex items-center gap-2"
                    >
                      <Send className="w-4 h-4" />
                      {isDraft ? "Send invoice" : "Resend invoice"}
                    </button>
                  )}
                  {isDraft && (
                    <button className="w-full px-4 py-2 text-left text-sm text-[var(--grey-700)] hover:bg-[var(--grey-50)] flex items-center gap-2">
                      <Edit className="w-4 h-4" />
                      Edit
                    </button>
                  )}
                  {!isPaid && (
                    <button className="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 flex items-center gap-2">
                      <X className="w-4 h-4" />
                      Cancel invoice
                    </button>
                  )}
                </div>
              </>
            )}
          </div>
        }
      />
      <main className="px-4 py-6 space-y-6 pb-32">
        {/* Amount Card */}
        <div className="bg-white rounded-xl border border-[var(--grey-200)] p-6 text-center">
          <span className={cn("px-3 py-1 text-sm font-medium rounded-full", style.bg, style.text)}>
            {style.label}
          </span>
          <p className="text-4xl font-bold text-[var(--grey-900)] mt-4 tabular-nums">
            £{invoice.total.toLocaleString()}
          </p>
          <p className={cn("text-sm mt-2", isOverdue ? "text-red-600" : "text-[var(--grey-500)]")}>
            Due: {invoice.dueDateFormatted}
          </p>
        </div>

        {/* Customer Card */}
        <section>
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Customer</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
            <p className="font-medium text-[var(--grey-900)]">{invoice.customerName}</p>
            {invoice.customerPhone && (
              <p className="text-sm text-[var(--grey-500)] mt-1 flex items-center gap-2">
                <Phone className="w-4 h-4" />
                {invoice.customerPhone}
              </p>
            )}
            <p className="text-sm text-[var(--grey-500)] mt-1 flex items-center gap-2">
              <Mail className="w-4 h-4" />
              {invoice.customerEmail}
            </p>
          </div>
        </section>

        {/* Line Items */}
        <section>
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Items</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
            {invoice.lineItems.map((item, i) => (
              <div key={i} className="flex justify-between text-sm py-2">
                <span className="text-[var(--grey-700)]">{item.description}</span>
                <span className="text-[var(--grey-900)] tabular-nums">
                  £{item.amount.toFixed(2)}
                </span>
              </div>
            ))}
            <div className="border-t border-[var(--grey-200)] mt-2 pt-2 space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-[var(--grey-600)]">Subtotal</span>
                <span className="text-[var(--grey-900)] tabular-nums">
                  £{invoice.subtotal.toFixed(2)}
                </span>
              </div>
              {invoice.vatRate > 0 && (
                <div className="flex justify-between text-sm">
                  <span className="text-[var(--grey-600)]">VAT ({invoice.vatRate}%)</span>
                  <span className="text-[var(--grey-900)] tabular-nums">
                    £{invoice.vat.toFixed(2)}
                  </span>
                </div>
              )}
              <div className="flex justify-between text-lg font-semibold border-t border-[var(--grey-200)] pt-2 mt-2">
                <span className="text-[var(--grey-900)]">Total</span>
                <span className="text-[var(--grey-900)] tabular-nums">
                  £{invoice.total.toFixed(2)}
                </span>
              </div>
            </div>
          </div>
        </section>

        {/* Payment Link */}
        {!isDraft && (
          <section>
            <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Payment</h3>
            <PaymentLinkButton
              invoiceId={invoice.id}
              paymentLinkUrl={invoice.paymentLinkUrl}
              status={invoice.status}
              onPaymentLinkCreated={refetch}
            />
          </section>
        )}

        {/* Timeline */}
        {invoice.timeline && invoice.timeline.length > 0 && (
          <section>
            <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Timeline</h3>
            <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
              <div className="space-y-3">
                {invoice.timeline.map((event, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <div
                      className={cn(
                        "w-2 h-2 rounded-full",
                        event.completed ? "bg-[var(--brand-primary)]" : "bg-[var(--grey-300)]"
                      )}
                    />
                    <span className="text-sm text-[var(--grey-700)] capitalize flex-1">
                      {event.status}
                    </span>
                    <span className="text-sm text-[var(--grey-500)]">{event.date}</span>
                  </div>
                ))}
              </div>
            </div>
          </section>
        )}
      </main>

      {/* Bottom Actions */}
      {!isPaid && (
        <div className="fixed bottom-0 left-0 right-0 max-w-md mx-auto bg-white border-t border-[var(--grey-200)] px-4 py-4 safe-area-pb">
          <div className="flex gap-3">
            {isDraft ? (
              <Button className="flex-1" onClick={handleSendInvoice} disabled={isUpdating}>
                Send Invoice
              </Button>
            ) : (
              <>
                <Button variant="secondary" className="flex-1" onClick={handleSendReminder} disabled={isUpdating}>
                  Send Reminder
                </Button>
                <Button className="flex-1" onClick={handleMarkAsPaid} disabled={isUpdating}>
                  Mark as Paid
                </Button>
              </>
            )}
          </div>
        </div>
      )}

      {/* Celebration Modal */}
      <CelebrationModal
        isOpen={showCelebration}
        onClose={() => setShowCelebration(false)}
        title="Payment received!"
        subtitle={`${invoice.customerName} paid their invoice`}
        amount={`+£${invoice.total}`}
      />
    </>
  );
}
