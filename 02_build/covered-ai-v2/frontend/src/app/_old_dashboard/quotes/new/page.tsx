"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Plus, Trash2 } from "lucide-react";
import { Header } from "@/components/layout";
import { Button, FixedBottomButton } from "@/components/ui";
import { useAuthContext } from "@/lib/auth-context";
import { quotesApi, customersApi, jobsApi } from "@/lib/api";

interface LineItem {
  id: string;
  description: string;
  quantity: number;
  unitPrice: number;
}

interface FormData {
  title: string;
  customerId: string;
  customerName: string;
  customerPhone: string;
  customerEmail: string;
  address: string;
  validDays: string;
  vatRate: string;
  discount: string;
  notes: string;
  terms: string;
}

function NewQuoteForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { client } = useAuthContext();

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState<FormData>({
    title: "",
    customerId: "",
    customerName: "",
    customerPhone: "",
    customerEmail: "",
    address: "",
    validDays: "30",
    vatRate: "20",
    discount: "0",
    notes: "",
    terms: "Payment due within 14 days of invoice.\nThis quote is valid for the period stated above.",
  });

  const [lineItems, setLineItems] = useState<LineItem[]>([
    { id: "1", description: "", quantity: 1, unitPrice: 0 },
  ]);

  // Pre-fill from customer or job
  useEffect(() => {
    const customerId = searchParams.get("customerId");
    const jobId = searchParams.get("jobId");

    if (customerId && client?.id) {
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
    } else if (jobId && client?.id) {
      jobsApi.getById(client.id, jobId).then((job) => {
        if (job) {
          setFormData((prev) => ({
            ...prev,
            title: job.title || "",
            customerId: job.customerId || "",
            customerName: job.customerName || "",
            customerPhone: job.customerPhone || "",
            customerEmail: job.customerEmail || "",
            address: job.address || "",
          }));
          if (job.estimatedValue) {
            setLineItems([
              { id: "1", description: job.title || "", quantity: 1, unitPrice: job.estimatedValue },
            ]);
          }
        }
      });
    }
  }, [searchParams, client?.id]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleLineItemChange = (id: string, field: keyof LineItem, value: string | number) => {
    setLineItems((prev) =>
      prev.map((item) => (item.id === id ? { ...item, [field]: value } : item))
    );
  };

  const addLineItem = () => {
    setLineItems((prev) => [
      ...prev,
      { id: Date.now().toString(), description: "", quantity: 1, unitPrice: 0 },
    ]);
  };

  const removeLineItem = (id: string) => {
    if (lineItems.length > 1) {
      setLineItems((prev) => prev.filter((item) => item.id !== id));
    }
  };

  const calculateSubtotal = () => {
    return lineItems.reduce((sum, item) => sum + item.quantity * item.unitPrice, 0);
  };

  const calculateVat = () => {
    const subtotal = calculateSubtotal();
    const discount = parseFloat(formData.discount) || 0;
    const vatRate = parseFloat(formData.vatRate) || 0;
    return ((subtotal - discount) * vatRate) / 100;
  };

  const calculateTotal = () => {
    const subtotal = calculateSubtotal();
    const discount = parseFloat(formData.discount) || 0;
    const vat = calculateVat();
    return subtotal - discount + vat;
  };

  const handleSubmit = async () => {
    if (!client?.id) return;
    if (!formData.title.trim()) {
      setError("Quote title is required");
      return;
    }
    if (!formData.customerName.trim()) {
      setError("Customer name is required");
      return;
    }
    if (lineItems.every((item) => !item.description.trim())) {
      setError("At least one line item is required");
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const validDays = parseInt(formData.validDays) || 30;
      const validUntil = new Date();
      validUntil.setDate(validUntil.getDate() + validDays);

      const payload = {
        title: formData.title,
        customerId: formData.customerId || undefined,
        customerName: formData.customerName,
        customerPhone: formData.customerPhone || undefined,
        customerEmail: formData.customerEmail || undefined,
        address: formData.address || undefined,
        items: lineItems
          .filter((item) => item.description.trim())
          .map((item) => ({
            description: item.description,
            quantity: item.quantity,
            unitPrice: item.unitPrice,
            total: item.quantity * item.unitPrice,
          })),
        subtotal: calculateSubtotal(),
        discount: parseFloat(formData.discount) || 0,
        vatRate: parseFloat(formData.vatRate) || 0,
        vatAmount: calculateVat(),
        total: calculateTotal(),
        validUntil: validUntil.toISOString().split("T")[0],
        notes: formData.notes || undefined,
        terms: formData.terms || undefined,
        status: "draft",
      };

      const newQuote = await quotesApi.create(client.id, payload);
      router.push(`/dashboard/quotes/${newQuote.id}`);
    } catch (err) {
      console.error("Failed to create quote:", err);
      setError("Failed to create quote. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <Header backButton title="New Quote" />
      <main className="px-4 py-6 space-y-6 pb-32">
        {error && (
          <div className="bg-red-50 rounded-xl border border-red-200 p-4 text-center">
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        )}

        {/* Quote Details */}
        <section>
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Quote Details</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-4">
            <div>
              <label className="block text-sm font-medium text-[var(--grey-700)] mb-1">
                Quote Title *
              </label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleChange}
                placeholder="e.g., Bathroom Installation"
                className="w-full h-11 px-3 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] placeholder:text-[var(--grey-400)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-[var(--grey-700)] mb-1">
                Valid For (days)
              </label>
              <input
                type="number"
                name="validDays"
                value={formData.validDays}
                onChange={handleChange}
                min="1"
                className="w-full h-11 px-3 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent"
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

        {/* Line Items */}
        <section>
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-[var(--grey-500)]">Items</h3>
            <button
              onClick={addLineItem}
              className="text-sm text-[var(--brand-primary)] font-medium flex items-center gap-1"
            >
              <Plus className="w-4 h-4" />
              Add Item
            </button>
          </div>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] divide-y divide-[var(--grey-100)]">
            {lineItems.map((item, index) => (
              <div key={item.id} className="p-4 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-[var(--grey-500)]">
                    Item {index + 1}
                  </span>
                  {lineItems.length > 1 && (
                    <button
                      onClick={() => removeLineItem(item.id)}
                      className="text-red-500 hover:text-red-700"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  )}
                </div>
                <div>
                  <input
                    type="text"
                    value={item.description}
                    onChange={(e) => handleLineItemChange(item.id, "description", e.target.value)}
                    placeholder="Description"
                    className="w-full h-11 px-3 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] placeholder:text-[var(--grey-400)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent"
                  />
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs text-[var(--grey-500)] mb-1">Quantity</label>
                    <input
                      type="number"
                      value={item.quantity}
                      onChange={(e) =>
                        handleLineItemChange(item.id, "quantity", parseInt(e.target.value) || 1)
                      }
                      min="1"
                      className="w-full h-11 px-3 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-xs text-[var(--grey-500)] mb-1">Unit Price (£)</label>
                    <input
                      type="number"
                      value={item.unitPrice}
                      onChange={(e) =>
                        handleLineItemChange(item.id, "unitPrice", parseFloat(e.target.value) || 0)
                      }
                      min="0"
                      step="0.01"
                      className="w-full h-11 px-3 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent"
                    />
                  </div>
                </div>
                <div className="text-right text-sm font-medium text-[var(--grey-700)]">
                  £{(item.quantity * item.unitPrice).toFixed(2)}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Pricing */}
        <section>
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Pricing</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-[var(--grey-700)] mb-1">
                  Discount (£)
                </label>
                <input
                  type="number"
                  name="discount"
                  value={formData.discount}
                  onChange={handleChange}
                  min="0"
                  step="0.01"
                  className="w-full h-11 px-3 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-[var(--grey-700)] mb-1">
                  VAT Rate (%)
                </label>
                <input
                  type="number"
                  name="vatRate"
                  value={formData.vatRate}
                  onChange={handleChange}
                  min="0"
                  max="100"
                  className="w-full h-11 px-3 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent"
                />
              </div>
            </div>

            {/* Totals */}
            <div className="pt-3 border-t border-[var(--grey-100)] space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-[var(--grey-500)]">Subtotal</span>
                <span className="text-[var(--grey-900)]">£{calculateSubtotal().toFixed(2)}</span>
              </div>
              {parseFloat(formData.discount) > 0 && (
                <div className="flex justify-between text-sm">
                  <span className="text-[var(--grey-500)]">Discount</span>
                  <span className="text-green-600">
                    -£{(parseFloat(formData.discount) || 0).toFixed(2)}
                  </span>
                </div>
              )}
              {parseFloat(formData.vatRate) > 0 && (
                <div className="flex justify-between text-sm">
                  <span className="text-[var(--grey-500)]">VAT ({formData.vatRate}%)</span>
                  <span className="text-[var(--grey-900)]">£{calculateVat().toFixed(2)}</span>
                </div>
              )}
              <div className="flex justify-between pt-2 border-t border-[var(--grey-100)]">
                <span className="font-semibold text-[var(--grey-900)]">Total</span>
                <span className="font-semibold text-[var(--grey-900)]">
                  £{calculateTotal().toFixed(2)}
                </span>
              </div>
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
              placeholder="Additional notes for the customer..."
              rows={3}
              className="w-full px-3 py-2 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] placeholder:text-[var(--grey-400)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent resize-none"
            />
          </div>
        </section>

        {/* Terms */}
        <section>
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Terms & Conditions</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
            <textarea
              name="terms"
              value={formData.terms}
              onChange={handleChange}
              placeholder="Terms and conditions..."
              rows={4}
              className="w-full px-3 py-2 rounded-lg border border-[var(--grey-200)] text-[var(--grey-900)] placeholder:text-[var(--grey-400)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] focus:border-transparent resize-none"
            />
          </div>
        </section>
      </main>

      <FixedBottomButton onClick={handleSubmit} loading={isSubmitting}>
        Create Quote
      </FixedBottomButton>
    </>
  );
}

function NewQuoteSkeleton() {
  return (
    <>
      <Header backButton title="New Quote" />
      <main className="px-4 py-6 space-y-6 pb-32 animate-pulse">
        <section>
          <div className="h-5 bg-[var(--grey-200)] rounded w-24 mb-2" />
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-4">
            <div className="h-11 bg-[var(--grey-100)] rounded-lg" />
            <div className="h-11 bg-[var(--grey-100)] rounded-lg" />
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
        <section>
          <div className="h-5 bg-[var(--grey-200)] rounded w-16 mb-2" />
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 h-32" />
        </section>
      </main>
    </>
  );
}

export default function NewQuotePage() {
  return (
    <Suspense fallback={<NewQuoteSkeleton />}>
      <NewQuoteForm />
    </Suspense>
  );
}
