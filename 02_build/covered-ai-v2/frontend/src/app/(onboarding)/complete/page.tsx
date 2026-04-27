"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Check, Phone, MessageCircle, BarChart3 } from "lucide-react";
import { Button } from "@/components/ui";

export default function OnboardingCompletePage() {
  const router = useRouter();
  const [coveredNumberDisplay, setCoveredNumberDisplay] = useState("0191 743 2732");

  useEffect(() => {
    // Get the covered number from localStorage if available
    const display = localStorage.getItem("covered_number_display");
    if (display) {
      setCoveredNumberDisplay(display);
      // Clean up
      localStorage.removeItem("covered_number");
      localStorage.removeItem("covered_number_display");
    }
  }, []);

  return (
    <main className="flex-1 flex flex-col px-6 py-12">
      {/* Success icon */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-green-100 rounded-full mb-4">
          <Check className="w-10 h-10 text-green-600" strokeWidth={3} />
        </div>
        <h1 className="text-2xl font-bold text-[var(--grey-900)]">
          You&apos;re live!
        </h1>
      </div>

      {/* Status card */}
      <div className="bg-green-50 rounded-xl border border-green-200 p-4 text-center mb-8">
        <p className="text-[var(--grey-700)]">
          Gemma is now answering your calls.
        </p>
        <p className="mt-2 text-sm text-[var(--grey-500)]">
          Your number:{" "}
          <span className="font-medium text-[var(--grey-900)]">
            {coveredNumberDisplay}
          </span>
        </p>
        <div className="flex items-center justify-center gap-2 mt-2">
          <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          <span className="text-sm font-medium text-green-700">Active</span>
        </div>
      </div>

      {/* What happens next */}
      <div className="flex-1">
        <h2 className="text-sm font-medium text-[var(--grey-500)] mb-4">
          WHAT HAPPENS NEXT
        </h2>

        <div className="space-y-4">
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-10 h-10 bg-[var(--brand-primary-light)] rounded-full flex items-center justify-center">
              <Phone className="w-5 h-5 text-[var(--brand-primary)]" />
            </div>
            <div>
              <p className="font-medium text-[var(--grey-900)]">Calls come in</p>
              <p className="text-sm text-[var(--grey-500)]">
                Gemma answers and captures all the details
              </p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="flex-shrink-0 w-10 h-10 bg-[var(--brand-primary-light)] rounded-full flex items-center justify-center">
              <MessageCircle className="w-5 h-5 text-[var(--brand-primary)]" />
            </div>
            <div>
              <p className="font-medium text-[var(--grey-900)]">
                You get WhatsApp summaries
              </p>
              <p className="text-sm text-[var(--grey-500)]">
                Review and act on each enquiry
              </p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="flex-shrink-0 w-10 h-10 bg-[var(--brand-primary-light)] rounded-full flex items-center justify-center">
              <BarChart3 className="w-5 h-5 text-[var(--brand-primary)]" />
            </div>
            <div>
              <p className="font-medium text-[var(--grey-900)]">
                Check your dashboard
              </p>
              <p className="text-sm text-[var(--grey-500)]">
                See everything in one place
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Go to dashboard button */}
      <div className="mt-auto pt-6">
        <Button
          className="w-full"
          size="lg"
          onClick={() => router.push("/dashboard")}
        >
          Go to Dashboard
        </Button>
      </div>
    </main>
  );
}
