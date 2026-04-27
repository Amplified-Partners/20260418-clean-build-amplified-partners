"use client";

import React, { useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Plus, Send, Trash2 } from "lucide-react";
import { Header } from "@/components/layout";
import { Button, Input, Select, Toggle, FixedBottomButton } from "@/components/ui";

interface LineItem {
  id: string;
  description: string;
  amount: string;
}

const dueDateOptions = [
  { value: "7", label: "7 days" },
  { value: "14", label: "14 days" },
  { value: "30", label: "30 days" },
  { value: "custom", label: "Custom date" },
];

function NewInvoiceForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const jobId = searchParams.get("jobId");
  const customerId = searchParams.get("customerId");

  const [customer, setCustomer] = useState("");
  const [customerEmail, setCustomerEmail] = useState("");
  const [customerPhone, setCustomerPhone] = useState("");
  const [lineItems, setLineItems] = useState<LineItem[]>([
    { id: "1", description: "", amount: "" },
  ]);
  const [dueDays, setDueDays] = useState("14");
  const [sendNow, setSendNow] = useState(true);
  const [isLoading, setIsLoading] = useState(false);

  // Calculate due date display
  const getDueDateDisplay = () => {
    const days = parseInt(dueDays);
    if (isNaN(days)) return "";
    const date = new Date();
    date.setDate(date.getDate() + days);
    return date.toLocaleDateString("en-GB", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  };

  // Calculate totals
  const subtotal = lineItems.reduce((sum, item) => {
    const amount = parseFloat(item.amount) || 0;
    return sum + amount;
  }, 0);
  const vatRate = 20;
  const vat = subtotal * (vatRate / 100);
  const total = subtotal + vat;

  const addLineItem = () => {
    setLineItems([
      ...lineItems,
      { id: Date.now().toString(), description: "", amount: "" },
    ]);
  };

  const removeLineItem = (id: string) => {
    if (lineItems.length > 1) {
      setLineItems(lineItems.filter((item) => item.id !== id));
    }
  };

  const updateLineItem = (id: string, field: "description" | "amount", value: string) => {
    setLineItems(
      lineItems.map((item) =>
        item.id === id ? { ...item, [field]: value } : item
      )
    );
  };

  const handleSubmit = async () => {
    if (!customer || lineItems.every((item) => !item.description || !item.amount)) {
      return;
    }

    setIsLoading(true);

    try {
      const res = await fetch("/api/v1/invoices", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customerName: customer,
          customerEmail,
          customerPhone,
          lineItems: lineItems.map((item) => ({
            description: item.description,
            amount: parseFloat(item.amount) || 0,
          })),
          dueDays: parseInt(dueDays),
          sendNow,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        router.push(`/dashboard/invoices/${data.id}`);
      }
    } catch (error) {
      console.error("Failed to create invoice:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const isValid =
    customer &&
    customerEmail &&
    lineItems.some((item) => item.description && parseFloat(item.amount) > 0);

  return (
    <>
      <Header backButton title="New Invoice" />
      <main className="px-4 py-6 space-y-6 pb-32">
        {/* Customer */}
        <div className="space-y-4">
          <Input
            label="Customer name"
            placeholder="Search or add customer..."
            value={customer}
            onChange={(e) => setCustomer(e.target.value)}
          />
          <Input
            label="Email"
            type="email"
            placeholder="customer@example.com"
            value={customerEmail}
            onChange={(e) => setCustomerEmail(e.target.value)}
          />
          <Input
            label="Phone (optional)"
            type="tel"
            placeholder="07700 900123"
            value={customerPhone}
            onChange={(e) => setCustomerPhone(e.target.value)}
          />
        </div>

        {/* Line Items */}
        <div className="space-y-3">
          <label className="text-sm font-medium text-[var(--grey-700)]">Items</label>
          <div className="bg-[var(--grey-50)] rounded-xl p-4 space-y-3">
            {lineItems.map((item, index) => (
              <div key={item.id} className="flex gap-3 items-start">
                <div className="flex-1">
                  <Input
                    placeholder="Description"
                    value={item.description}
                    onChange={(e) =>
                      updateLineItem(item.id, "description", e.target.value)
                    }
                  />
                </div>
                <div className="w-24">
                  <Input
                    placeholder="£"
                    value={item.amount}
                    onChange={(e) => updateLineItem(item.id, "amount", e.target.value)}
                    className="text-right tabular-nums"
                  />
                </div>
                {lineItems.length > 1 && (
                  <button
                    onClick={() => removeLineItem(item.id)}
                    className="mt-2.5 text-[var(--grey-400)] hover:text-red-500 transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                )}
              </div>
            ))}
          </div>
          <button
            onClick={addLineItem}
            className="text-sm text-[var(--brand-primary)] font-medium flex items-center gap-1 hover:underline"
          >
            <Plus className="w-4 h-4" />
            Add item
          </button>
        </div>

        {/* Totals */}
        <div className="bg-[var(--grey-50)] rounded-xl p-4 space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-[var(--grey-600)]">Subtotal</span>
            <span className="text-[var(--grey-900)] tabular-nums">
              £{subtotal.toFixed(2)}
            </span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-[var(--grey-600)]">VAT ({vatRate}%)</span>
            <span className="text-[var(--grey-900)] tabular-nums">
              £{vat.toFixed(2)}
            </span>
          </div>
          <div className="flex justify-between text-lg font-semibold border-t border-[var(--grey-200)] pt-2 mt-2">
            <span className="text-[var(--grey-900)]">Total</span>
            <span className="text-[var(--grey-900)] tabular-nums">
              £{total.toFixed(2)}
            </span>
          </div>
        </div>

        {/* Due Date */}
        <Select
          label="Due date"
          options={dueDateOptions.map((opt) => ({
            ...opt,
            label: opt.value === "custom" ? opt.label : `${opt.label} (${getDueDateDisplay()})`,
          }))}
          value={dueDays}
          onChange={(e) => setDueDays(e.target.value)}
        />

        {/* Send Toggle */}
        <Toggle
          label="Send immediately"
          description="Email invoice to customer now"
          checked={sendNow}
          onChange={setSendNow}
        />
      </main>

      {/* Bottom Button */}
      <FixedBottomButton
        icon={<Send className="w-5 h-5" />}
        onClick={handleSubmit}
        loading={isLoading}
        disabled={!isValid}
      >
        {sendNow ? `Send Invoice — £${total.toFixed(2)}` : `Save Invoice — £${total.toFixed(2)}`}
      </FixedBottomButton>
    </>
  );
}

function NewInvoiceSkeleton() {
  return (
    <>
      <Header backButton title="New Invoice" />
      <main className="px-4 py-6 space-y-6 pb-32 animate-pulse">
        <div className="space-y-4">
          <div className="h-12 bg-[var(--grey-200)] rounded-lg" />
          <div className="h-12 bg-[var(--grey-200)] rounded-lg" />
          <div className="h-12 bg-[var(--grey-200)] rounded-lg" />
        </div>
        <div className="bg-[var(--grey-50)] rounded-xl p-4 h-32" />
        <div className="bg-[var(--grey-50)] rounded-xl p-4 h-24" />
      </main>
    </>
  );
}

export default function NewInvoicePage() {
  return (
    <Suspense fallback={<NewInvoiceSkeleton />}>
      <NewInvoiceForm />
    </Suspense>
  );
}
