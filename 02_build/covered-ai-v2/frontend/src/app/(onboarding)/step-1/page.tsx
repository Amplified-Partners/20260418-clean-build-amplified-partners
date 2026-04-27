"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Button, Input, Select } from "@/components/ui";
import { cn } from "@/lib/utils";
import { onboardingApi, ApiError } from "@/lib/api";

const verticals = [
  { id: "trades", label: "Plumber", icon: "🔧" },
  { id: "electrician", label: "Electrician", icon: "⚡" },
  { id: "salon", label: "Salon", icon: "💇" },
  { id: "vet", label: "Vet", icon: "🐾" },
  { id: "dental", label: "Dental", icon: "🦷" },
  { id: "physio", label: "Physio", icon: "💪" },
  { id: "other", label: "Other...", icon: "📋" },
];

const businessTypes = [
  { value: "sole_trader", label: "Sole Trader" },
  { value: "ltd_company", label: "Limited Company" },
  { value: "partnership", label: "Partnership" },
];

export default function OnboardingStep1Page() {
  const router = useRouter();
  const [businessName, setBusinessName] = useState("");
  const [ownerName, setOwnerName] = useState("");
  const [phone, setPhone] = useState("");
  const [selectedVertical, setSelectedVertical] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleContinue = async () => {
    if (!businessName || !ownerName || !phone || !selectedVertical) return;

    setIsLoading(true);
    setError("");

    try {
      const data = await onboardingApi.completeStep1({
        business_name: businessName,
        owner_name: ownerName,
        phone,
        vertical: selectedVertical,
      });

      // Store the covered number for step 2
      localStorage.setItem("covered_number", data.covered_number);
      localStorage.setItem("covered_number_display", data.covered_number_display);

      router.push("/step-2");
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError("Failed to save. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const isValid = businessName && ownerName && phone && selectedVertical;

  return (
    <>
      <main className="flex-1 px-6 py-8">
        {/* Progress indicator */}
        <div className="mb-8">
          <p className="text-sm text-[var(--grey-500)] mb-2">Step 1 of 3</p>
          <div className="flex gap-2">
            <div className="h-1 flex-1 rounded-full bg-[var(--brand-primary)]" />
            <div className="h-1 flex-1 rounded-full bg-[var(--grey-200)]" />
            <div className="h-1 flex-1 rounded-full bg-[var(--grey-200)]" />
          </div>
        </div>

        <h1 className="text-2xl font-bold text-[var(--grey-900)] mb-6">
          Tell us about your business
        </h1>

        {error && (
          <p className="text-sm text-red-600 bg-red-50 px-3 py-2 rounded-lg mb-4">
            {error}
          </p>
        )}

        <div className="space-y-5">
          <Input
            label="Business name"
            placeholder="e.g. Dave's Plumbing"
            value={businessName}
            onChange={(e) => setBusinessName(e.target.value)}
          />

          <Input
            label="Your name"
            placeholder="e.g. Dave Smith"
            value={ownerName}
            onChange={(e) => setOwnerName(e.target.value)}
          />

          <Input
            label="Your phone number"
            placeholder="e.g. 07700 900123"
            type="tel"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
          />

          <div className="space-y-2">
            <label className="text-sm font-medium text-[var(--grey-700)]">
              What do you do?
            </label>
            <div className="grid grid-cols-3 gap-2">
              {verticals.map((v) => (
                <button
                  key={v.id}
                  type="button"
                  onClick={() => setSelectedVertical(v.id)}
                  className={cn(
                    "flex flex-col items-center gap-1 p-3 rounded-xl border-2 transition-all",
                    selectedVertical === v.id
                      ? "border-[var(--brand-primary)] bg-[var(--brand-primary-light)]"
                      : "border-[var(--grey-200)] bg-white hover:border-[var(--grey-300)]"
                  )}
                >
                  <span className="text-2xl">{v.icon}</span>
                  <span
                    className={cn(
                      "text-xs font-medium",
                      selectedVertical === v.id
                        ? "text-[var(--brand-primary)]"
                        : "text-[var(--grey-600)]"
                    )}
                  >
                    {v.label}
                  </span>
                </button>
              ))}
            </div>
          </div>
        </div>
      </main>

      {/* Fixed bottom button */}
      <div className="sticky bottom-0 bg-white border-t border-[var(--grey-200)] px-6 py-4 safe-area-pb">
        <Button
          className="w-full"
          size="lg"
          onClick={handleContinue}
          disabled={!isValid}
          loading={isLoading}
        >
          Continue
        </Button>
      </div>
    </>
  );
}
