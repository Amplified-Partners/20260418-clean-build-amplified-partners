/**
 * Customer App - Invoice Payment Page
 * 
 * Simple invoice view with one-tap payment.
 * No login required - magic link access.
 */

"use client";

import React, { useState } from "react";
import { CreditCard, Building2, CheckCircle, FileText } from "lucide-react";

// Mock data - in production, loaded from URL params or API
const mockInvoice = {
  business: {
    name: "Titan Plumbing",
    address: "123 Trade Street, Newcastle, NE1 1AA",
    phone: "+447712345678",
    email: "hello@titanplumbing.co.uk",
    logo: null,
  },
  invoice: {
    id: "INV-2024-047",
    date: "28th November 2024",
    dueDate: "5th December 2024",
    status: "pending", // pending, paid, overdue
    items: [
      { description: "Emergency callout - burst pipe", amount: 120 },
      { description: "Parts - isolation valve", amount: 35 },
      { description: "Labour - 2 hours", amount: 160 },
    ],
    subtotal: 315,
    vat: 63,
    total: 378,
  },
  customer: {
    name: "Mrs Chen",
    address: "14 Park Road, NE3 4AB",
  },
  payment: {
    bankName: "Barclays",
    accountName: "Titan Plumbing Ltd",
    sortCode: "20-30-40",
    accountNumber: "12345678",
    reference: "INV-2024-047",
  },
};

export default function InvoicePaymentPage() {
  const { business, invoice, customer, payment } = mockInvoice;
  const [paymentMethod, setPaymentMethod] = useState<"card" | "bank" | null>(null);
  const [isPaid, setIsPaid] = useState(invoice.status === "paid");
  
  const handleCardPayment = () => {
    // In production: redirect to Stripe checkout
    setIsPaid(true);
  };
  
  if (isPaid) {
    return (
      <div className="px-5 py-12 text-center">
        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <CheckCircle className="w-10 h-10 text-green-600" />
        </div>
        <h1 className="text-2xl font-bold text-neutral-900 mb-2">
          Payment Received
        </h1>
        <p className="text-neutral-600 mb-8">
          Thank you for your payment of £{invoice.total.toFixed(2)}
        </p>
        <p className="text-sm text-neutral-500">
          A receipt has been sent to your email.
        </p>
      </div>
    );
  }
  
  return (
    <div className="px-5 py-8">
      {/* Business header */}
      <div className="text-center mb-6">
        {business.logo ? (
          <img 
            src={business.logo} 
            alt={business.name}
            className="h-10 mx-auto mb-2"
          />
        ) : (
          <h1 className="text-lg font-bold text-neutral-900">{business.name}</h1>
        )}
      </div>
      
      {/* Invoice header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <p className="text-sm text-neutral-500">Invoice</p>
          <p className="font-semibold text-neutral-900">{invoice.id}</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-neutral-500">Due</p>
          <p className="font-semibold text-neutral-900">{invoice.dueDate}</p>
        </div>
      </div>
      
      {/* Amount due */}
      <div className="bg-blue-50 rounded-2xl p-6 text-center mb-6">
        <p className="text-sm text-blue-600 mb-1">Amount Due</p>
        <p className="text-4xl font-bold text-neutral-900">
          £{invoice.total.toFixed(2)}
        </p>
      </div>
      
      {/* Line items */}
      <div className="bg-neutral-50 rounded-xl p-4 mb-6">
        <div className="space-y-3">
          {invoice.items.map((item, i) => (
            <div key={i} className="flex justify-between text-sm">
              <span className="text-neutral-600">{item.description}</span>
              <span className="text-neutral-900">£{item.amount.toFixed(2)}</span>
            </div>
          ))}
          <div className="border-t border-neutral-200 pt-3 mt-3">
            <div className="flex justify-between text-sm">
              <span className="text-neutral-500">Subtotal</span>
              <span className="text-neutral-700">£{invoice.subtotal.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-sm mt-1">
              <span className="text-neutral-500">VAT (20%)</span>
              <span className="text-neutral-700">£{invoice.vat.toFixed(2)}</span>
            </div>
            <div className="flex justify-between font-semibold mt-2">
              <span className="text-neutral-900">Total</span>
              <span className="text-neutral-900">£{invoice.total.toFixed(2)}</span>
            </div>
          </div>
        </div>
      </div>
      
      {/* Payment options */}
      <div className="space-y-3 mb-6">
        <p className="text-sm font-medium text-neutral-700">Pay by:</p>
        
        {/* Card payment */}
        <button
          onClick={handleCardPayment}
          className="w-full flex items-center gap-4 p-4 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors"
        >
          <CreditCard className="w-6 h-6" />
          <div className="text-left">
            <p className="font-semibold">Pay by Card</p>
            <p className="text-sm text-blue-100">Visa, Mastercard, Amex</p>
          </div>
        </button>
        
        {/* Bank transfer */}
        <button
          onClick={() => setPaymentMethod(paymentMethod === "bank" ? null : "bank")}
          className="w-full flex items-center gap-4 p-4 bg-neutral-100 text-neutral-700 rounded-xl hover:bg-neutral-200 transition-colors"
        >
          <Building2 className="w-6 h-6" />
          <div className="text-left">
            <p className="font-semibold">Bank Transfer</p>
            <p className="text-sm text-neutral-500">View bank details</p>
          </div>
        </button>
        
        {paymentMethod === "bank" && (
          <div className="bg-neutral-50 rounded-xl p-4 space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-neutral-500">Bank</span>
              <span className="text-neutral-900">{payment.bankName}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-neutral-500">Account name</span>
              <span className="text-neutral-900">{payment.accountName}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-neutral-500">Sort code</span>
              <span className="text-neutral-900 font-mono">{payment.sortCode}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-neutral-500">Account number</span>
              <span className="text-neutral-900 font-mono">{payment.accountNumber}</span>
            </div>
            <div className="flex justify-between text-sm pt-2 border-t border-neutral-200">
              <span className="text-neutral-500">Reference</span>
              <span className="text-neutral-900 font-mono font-semibold">{payment.reference}</span>
            </div>
            <p className="text-xs text-neutral-500 pt-2">
              Please use the reference above so we can match your payment.
            </p>
          </div>
        )}
      </div>
      
      {/* Download PDF */}
      <div className="text-center">
        <button className="inline-flex items-center gap-2 text-blue-600 text-sm font-medium">
          <FileText className="w-4 h-4" />
          Download PDF
        </button>
      </div>
      
      {/* Contact */}
      <div className="mt-8 pt-6 border-t border-neutral-100 text-center">
        <p className="text-sm text-neutral-500">
          Questions? Contact {business.name}
        </p>
        <a href={`tel:${business.phone}`} className="text-blue-600 text-sm font-medium">
          {business.phone}
        </a>
      </div>
    </div>
  );
}
