/**
 * Client App - Money Page
 * 
 * Simple view of payments.
 * Focus on what needs chasing.
 * 
 * Design principles:
 * - Visual progress bar for instant understanding
 * - Overdue items at top
 * - One-tap chase
 */

"use client";

import React from "react";
import { useRouter } from "next/navigation";
import { Plus } from "lucide-react";
import {
  MoneyProgress,
  InvoiceRow,
  SectionDivider,
  EmptyState,
} from "@/components/client-app";

// Mock data
const mockData = {
  summary: {
    paid: 4280,
    unpaid: 1200,
    overdue: 340,
  },
  
  overdueInvoices: [
    {
      id: "1",
      customerName: "Mr Davies",
      amount: 340,
      status: "overdue" as const,
      daysInfo: "7 days overdue",
    },
  ],
  
  pendingInvoices: [
    {
      id: "2",
      customerName: "Mrs Lee",
      amount: 180,
      status: "pending" as const,
      daysInfo: "Due in 3 days",
    },
    {
      id: "3",
      customerName: "Johnson family",
      amount: 680,
      status: "pending" as const,
      daysInfo: "Due in 7 days",
    },
  ],
  
  recentPayments: [
    {
      id: "4",
      customerName: "Mrs Thompson",
      amount: 246,
      status: "paid" as const,
      daysInfo: "Today",
    },
    {
      id: "5",
      customerName: "Mr Abbas",
      amount: 180,
      status: "paid" as const,
      daysInfo: "Yesterday",
    },
    {
      id: "6",
      customerName: "Johnson family",
      amount: 892,
      status: "paid" as const,
      daysInfo: "Monday",
    },
  ],
};

export default function MoneyPage() {
  const router = useRouter();
  
  const handleViewInvoice = (invoiceId: string) => {
    router.push(`/money/invoice/${invoiceId}`);
  };
  
  const handleChase = (invoiceId: string) => {
    // In production: send reminder via API
    alert(`Reminder sent for invoice ${invoiceId}`);
  };
  
  const handleCreateInvoice = () => {
    router.push("/money/new");
  };
  
  const hasInvoices = 
    mockData.overdueInvoices.length > 0 || 
    mockData.pendingInvoices.length > 0 || 
    mockData.recentPayments.length > 0;
  
  return (
    <div className="pb-6">
      {/* Progress bar */}
      <div className="pt-4">
        <MoneyProgress
          paid={mockData.summary.paid}
          unpaid={mockData.summary.unpaid}
          overdue={mockData.summary.overdue}
        />
      </div>
      
      {!hasInvoices ? (
        <EmptyState
          icon="💷"
          title="No invoices yet"
          description="Create your first invoice to start getting paid."
          action={{
            label: "Create Invoice",
            onClick: handleCreateInvoice,
          }}
        />
      ) : (
        <>
          {/* Overdue */}
          {mockData.overdueInvoices.length > 0 && (
            <>
              <SectionDivider title="Needs chasing" />
              <div className="bg-white mx-5 rounded-2xl border border-neutral-200 overflow-hidden">
                {mockData.overdueInvoices.map((invoice) => (
                  <InvoiceRow
                    key={invoice.id}
                    customerName={invoice.customerName}
                    amount={invoice.amount}
                    status={invoice.status}
                    daysInfo={invoice.daysInfo}
                    onClick={() => handleViewInvoice(invoice.id)}
                    onChase={() => handleChase(invoice.id)}
                  />
                ))}
              </div>
            </>
          )}
          
          {/* Pending */}
          {mockData.pendingInvoices.length > 0 && (
            <>
              <SectionDivider title="Awaiting payment" />
              <div className="bg-white mx-5 rounded-2xl border border-neutral-200 overflow-hidden">
                {mockData.pendingInvoices.map((invoice) => (
                  <InvoiceRow
                    key={invoice.id}
                    customerName={invoice.customerName}
                    amount={invoice.amount}
                    status={invoice.status}
                    daysInfo={invoice.daysInfo}
                    onClick={() => handleViewInvoice(invoice.id)}
                  />
                ))}
              </div>
            </>
          )}
          
          {/* Recent payments */}
          {mockData.recentPayments.length > 0 && (
            <>
              <SectionDivider title="Recent payments" />
              <div className="bg-white mx-5 rounded-2xl border border-neutral-200 overflow-hidden">
                {mockData.recentPayments.map((invoice) => (
                  <InvoiceRow
                    key={invoice.id}
                    customerName={invoice.customerName}
                    amount={invoice.amount}
                    status={invoice.status}
                    daysInfo={invoice.daysInfo}
                    onClick={() => handleViewInvoice(invoice.id)}
                  />
                ))}
              </div>
            </>
          )}
          
          {/* Create invoice button */}
          <div className="mx-5 mt-6">
            <button
              onClick={handleCreateInvoice}
              className="w-full flex items-center justify-center gap-2 py-3 bg-blue-600 text-white font-medium rounded-xl hover:bg-blue-700 transition-colors"
            >
              <Plus className="w-5 h-5" />
              Create Invoice
            </button>
          </div>
        </>
      )}
    </div>
  );
}
