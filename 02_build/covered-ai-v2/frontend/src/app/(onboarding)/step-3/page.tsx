"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Phone, CheckCircle, Loader2 } from "lucide-react";
import { Button } from "@/components/ui";
import { onboardingApi, ApiError } from "@/lib/api";

export default function OnboardingStep3Page() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [testCallReceived, setTestCallReceived] = useState(false);
  const [coveredNumber, setCoveredNumber] = useState("");
  const [coveredNumberDisplay, setCoveredNumberDisplay] = useState("");
  const [isPolling, setIsPolling] = useState(true);

  useEffect(() => {
    // Get covered number from localStorage
    const number = localStorage.getItem("covered_number") || "";
    const display = localStorage.getItem("covered_number_display") || "0191 743 2732";
    setCoveredNumber(number);
    setCoveredNumberDisplay(display);

    // Poll for test call status
    const pollInterval = setInterval(async () => {
      if (!isPolling) return;

      try {
        const status = await onboardingApi.getTestCallStatus();
        if (status.test_call_received) {
          setTestCallReceived(true);
          setIsPolling(false);
        }
      } catch (err) {
        console.error("Failed to check test call status:", err);
      }
    }, 3000);

    return () => clearInterval(pollInterval);
  }, [isPolling]);

  const handleSimulateCall = async () => {
    try {
      const result = await onboardingApi.simulateTestCall();
      setTestCallReceived(result.test_call_received);
      setIsPolling(false);
    } catch (err) {
      console.error("Failed to simulate call:", err);
    }
  };

  const handleFinish = async () => {
    setIsLoading(true);
    setError("");

    try {
      const data = await onboardingApi.completeStep3();

      // Clean up localStorage
      localStorage.removeItem("covered_number");
      localStorage.removeItem("covered_number_display");

      router.push("/complete");
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError("Failed to complete setup. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleSkip = async () => {
    setIsLoading(true);
    setError("");

    try {
      const data = await onboardingApi.skipTest();

      // Clean up localStorage
      localStorage.removeItem("covered_number");
      localStorage.removeItem("covered_number_display");

      router.push("/complete");
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError("Failed to complete setup. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <main className="flex-1 px-6 py-8">
        {/* Progress indicator */}
        <div className="mb-8">
          <p className="text-sm text-[var(--grey-500)] mb-2">Step 3 of 3</p>
          <div className="flex gap-2">
            <div className="h-1 flex-1 rounded-full bg-[var(--brand-primary)]" />
            <div className="h-1 flex-1 rounded-full bg-[var(--brand-primary)]" />
            <div className="h-1 flex-1 rounded-full bg-[var(--brand-primary)]" />
          </div>
        </div>

        <h1 className="text-2xl font-bold text-[var(--grey-900)] mb-6">
          Make a test call
        </h1>

        {error && (
          <p className="text-sm text-red-600 bg-red-50 px-3 py-2 rounded-lg mb-4">
            {error}
          </p>
        )}

        <div className="space-y-6">
          {/* Test call status */}
          <div className={`rounded-xl p-6 text-center ${
            testCallReceived
              ? "bg-green-50 border-2 border-green-200"
              : "bg-[var(--grey-50)]"
          }`}>
            {testCallReceived ? (
              <>
                <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
                  <CheckCircle className="w-8 h-8 text-green-600" />
                </div>
                <h2 className="text-xl font-bold text-[var(--grey-900)] mb-2">
                  Test call received!
                </h2>
                <p className="text-sm text-[var(--grey-600)]">
                  Gemma is ready to answer your calls.
                </p>
              </>
            ) : (
              <>
                <div className="inline-flex items-center justify-center w-16 h-16 bg-[var(--brand-primary-light)] rounded-full mb-4">
                  <Phone className="w-8 h-8 text-[var(--brand-primary)]" />
                </div>
                <h2 className="text-xl font-bold text-[var(--grey-900)] mb-2">
                  Call your Covered number
                </h2>
                <p className="text-2xl font-bold text-[var(--brand-primary)] my-3">
                  {coveredNumberDisplay}
                </p>
                <p className="text-sm text-[var(--grey-600)] mb-4">
                  Call this number to hear Gemma in action and verify everything works.
                </p>
                <Button
                  variant="primary"
                  onClick={() => window.open(`tel:${coveredNumber}`)}
                >
                  <Phone className="w-4 h-4 mr-2" />
                  Call Now
                </Button>
              </>
            )}
          </div>

          {/* Waiting indicator */}
          {!testCallReceived && (
            <div className="flex items-center justify-center gap-2 text-sm text-[var(--grey-500)]">
              <Loader2 className="w-4 h-4 animate-spin" />
              Waiting for your test call...
            </div>
          )}

          {/* Dev mode - simulate call */}
          {process.env.NODE_ENV === "development" && !testCallReceived && (
            <button
              onClick={handleSimulateCall}
              className="w-full text-center text-xs text-[var(--grey-400)] hover:text-[var(--grey-600)]"
            >
              [Dev] Simulate test call
            </button>
          )}
        </div>
      </main>

      {/* Fixed bottom buttons */}
      <div className="sticky bottom-0 bg-white border-t border-[var(--grey-200)] px-6 py-4 safe-area-pb space-y-2">
        {testCallReceived ? (
          <Button
            className="w-full"
            size="lg"
            onClick={handleFinish}
            loading={isLoading}
          >
            Complete Setup
          </Button>
        ) : (
          <>
            <Button
              className="w-full"
              size="lg"
              variant="secondary"
              onClick={handleSkip}
              loading={isLoading}
            >
              Skip for now
            </Button>
            <p className="text-xs text-center text-[var(--grey-400)]">
              You can make a test call anytime from your dashboard
            </p>
          </>
        )}
      </div>
    </>
  );
}
