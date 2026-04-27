"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Phone, Copy, Check, ArrowRight, Clock } from "lucide-react";
import { Button, Input, Select } from "@/components/ui";
import { onboardingApi, ApiError } from "@/lib/api";

const networks = [
  { value: "bt", label: "BT Landline" },
  { value: "ee", label: "EE" },
  { value: "vodafone", label: "Vodafone" },
  { value: "o2", label: "O2" },
  { value: "three", label: "Three" },
  { value: "sky", label: "Sky Mobile" },
  { value: "giffgaff", label: "giffgaff" },
  { value: "virgin", label: "Virgin Media" },
  { value: "talktalk", label: "TalkTalk" },
  { value: "plusnet", label: "Plusnet" },
  { value: "voip", label: "VoIP (RingCentral, 8x8, etc.)" },
  { value: "other", label: "Other" },
];

type MigrationTier = "forwarding" | "porting" | null;

export default function OnboardingStep2Page() {
  const router = useRouter();
  const [migrationTier, setMigrationTier] = useState<MigrationTier>(null);
  const [network, setNetwork] = useState("ee");
  const [copied, setCopied] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [coveredNumber, setCoveredNumber] = useState("");
  const [coveredNumberDisplay, setCoveredNumberDisplay] = useState("");
  const [forwardCode, setForwardCode] = useState("");
  const [cancelCode, setCancelCode] = useState("");
  const [instructions, setInstructions] = useState<string[]>([]);

  useEffect(() => {
    const number = localStorage.getItem("covered_number") || "";
    const display = localStorage.getItem("covered_number_display") || "0191 743 2732";
    setCoveredNumber(number);
    setCoveredNumberDisplay(display);
  }, []);

  const fetchInstructions = async (selectedNetwork: string) => {
    try {
      const data = await onboardingApi.getForwardingInstructions(selectedNetwork);
      setForwardCode(data.forward_code);
      setCancelCode(data.cancel_code);
      setInstructions(data.instructions);
      if (data.covered_number_display) {
        setCoveredNumberDisplay(data.covered_number_display);
      }
    } catch (err) {
      console.error("Failed to fetch instructions:", err);
      const digits = coveredNumber.replace(/[^0-9]/g, "");
      setForwardCode(`*21*${digits}#`);
      setCancelCode("#21#");
    }
  };

  const handleNetworkChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newNetwork = e.target.value;
    setNetwork(newNetwork);
    if (migrationTier === "forwarding") {
      fetchInstructions(newNetwork);
    }
  };

  const handleSelectTier = (tier: MigrationTier) => {
    setMigrationTier(tier);
    if (tier === "forwarding") {
      fetchInstructions(network);
    }
  };

  const handleCopyCode = async () => {
    await navigator.clipboard.writeText(forwardCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleContinue = async () => {
    if (migrationTier === "porting") {
      router.push("/porting");
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      await onboardingApi.completeStep2({
        forwarding_confirmed: true,
        network_selected: network,
      });

      router.push("/step-3");
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

  return (
    <>
      <main className="flex-1 px-6 py-8">
        {/* Progress indicator */}
        <div className="mb-8">
          <p className="text-sm text-[var(--grey-500)] mb-2">Step 2 of 3</p>
          <div className="flex gap-2">
            <div className="h-1 flex-1 rounded-full bg-[var(--brand-primary)]" />
            <div className="h-1 flex-1 rounded-full bg-[var(--brand-primary)]" />
            <div className="h-1 flex-1 rounded-full bg-[var(--grey-200)]" />
          </div>
        </div>

        <h1 className="text-2xl font-bold text-[var(--grey-900)] mb-2">
          Connect your phone
        </h1>
        <p className="text-[var(--grey-600)] mb-6">
          Choose how you want Gemma to answer your calls.
        </p>

        {error && (
          <p className="text-sm text-red-600 bg-red-50 px-3 py-2 rounded-lg mb-4">
            {error}
          </p>
        )}

        {/* Covered number display */}
        <div className="bg-[var(--brand-primary-light)] rounded-xl p-4 text-center mb-6">
          <div className="inline-flex items-center justify-center w-10 h-10 bg-[var(--brand-primary)] rounded-full mb-2">
            <Phone className="w-5 h-5 text-white" />
          </div>
          <p className="text-xl font-bold text-[var(--grey-900)] tracking-wider">
            {coveredNumberDisplay}
          </p>
          <p className="text-sm text-[var(--grey-600)] mt-1">
            Your Covered number
          </p>
        </div>

        {/* Tier selection */}
        {!migrationTier && (
          <div className="space-y-3">
            {/* Tier 1: Forwarding */}
            <button
              onClick={() => handleSelectTier("forwarding")}
              className="w-full bg-white rounded-xl border-2 border-[var(--grey-200)] p-4 text-left hover:border-[var(--brand-primary)] transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-lg font-semibold text-[var(--grey-900)]">
                      Forward my calls
                    </span>
                    <span className="px-2 py-0.5 bg-green-100 text-green-700 text-xs font-medium rounded-full">
                      Quick
                    </span>
                  </div>
                  <p className="text-sm text-[var(--grey-600)]">
                    Keep your existing number. Set up forwarding in 2 minutes.
                  </p>
                </div>
                <ArrowRight className="w-5 h-5 text-[var(--grey-400)] mt-1" />
              </div>
            </button>

            {/* Tier 2: Porting */}
            <button
              onClick={() => handleSelectTier("porting")}
              className="w-full bg-white rounded-xl border-2 border-[var(--grey-200)] p-4 text-left hover:border-[var(--brand-primary)] transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-lg font-semibold text-[var(--grey-900)]">
                      Transfer my number to Covered
                    </span>
                    <span className="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs font-medium rounded-full">
                      White-glove
                    </span>
                  </div>
                  <p className="text-sm text-[var(--grey-600)]">
                    We move your number. You sign one form, we handle the rest. Takes ~7 days.
                  </p>
                </div>
                <ArrowRight className="w-5 h-5 text-[var(--grey-400)] mt-1" />
              </div>
            </button>
          </div>
        )}

        {/* Forwarding setup */}
        {migrationTier === "forwarding" && (
          <div className="space-y-4">
            <button
              onClick={() => setMigrationTier(null)}
              className="text-sm text-[var(--brand-primary)] font-medium"
            >
              ← Back to options
            </button>

            <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-4">
              <h2 className="font-semibold text-[var(--grey-900)]">
                Set up call forwarding
              </h2>

              <Select
                label="Your phone provider"
                options={networks}
                value={network}
                onChange={handleNetworkChange}
              />

              <div className="bg-[var(--grey-50)] rounded-lg p-4">
                <p className="text-sm text-[var(--grey-600)] mb-2">
                  On your phone, dial:
                </p>
                <div className="flex items-center gap-2">
                  <code className="flex-1 bg-white px-3 py-2 rounded border border-[var(--grey-200)] text-[var(--grey-900)] font-mono text-lg font-bold">
                    {forwardCode || "*21*...#"}
                  </code>
                  <Button
                    variant="secondary"
                    size="sm"
                    icon={copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                    onClick={handleCopyCode}
                  >
                    {copied ? "Copied" : "Copy"}
                  </Button>
                </div>
                {instructions.length > 0 && (
                  <ul className="mt-3 text-sm text-[var(--grey-600)] space-y-1">
                    {instructions.map((instruction, i) => (
                      <li key={i}>{i + 1}. {instruction}</li>
                    ))}
                  </ul>
                )}
                {cancelCode && (
                  <p className="mt-3 text-xs text-[var(--grey-500)]">
                    To cancel forwarding later, dial: <code className="font-mono">{cancelCode}</code>
                  </p>
                )}
              </div>

              <div className="bg-green-50 rounded-lg p-3 flex items-start gap-3">
                <Check className="w-5 h-5 text-green-600 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-green-800">
                    You keep your number
                  </p>
                  <p className="text-sm text-green-700">
                    Calls forward to Gemma. Cancel anytime.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Porting info */}
        {migrationTier === "porting" && (
          <div className="space-y-4">
            <button
              onClick={() => setMigrationTier(null)}
              className="text-sm text-[var(--brand-primary)] font-medium"
            >
              ← Back to options
            </button>

            <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-4">
              <h2 className="font-semibold text-[var(--grey-900)]">
                Transfer your number
              </h2>

              <p className="text-sm text-[var(--grey-600)]">
                We'll move your existing phone number to Covered. You don't lift a finger — just sign one form, we handle the rest.
              </p>

              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <div className="w-6 h-6 rounded-full bg-[var(--brand-primary-light)] flex items-center justify-center text-sm font-medium text-[var(--brand-primary)]">1</div>
                  <div>
                    <p className="text-sm font-medium text-[var(--grey-900)]">You fill in one form</p>
                    <p className="text-xs text-[var(--grey-500)]">Provider name, account number, sign authorization</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-6 h-6 rounded-full bg-[var(--brand-primary-light)] flex items-center justify-center text-sm font-medium text-[var(--brand-primary)]">2</div>
                  <div>
                    <p className="text-sm font-medium text-[var(--grey-900)]">We handle the transfer</p>
                    <p className="text-xs text-[var(--grey-500)]">Submit paperwork, track progress, notify you</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-6 h-6 rounded-full bg-[var(--brand-primary-light)] flex items-center justify-center text-sm font-medium text-[var(--brand-primary)]">3</div>
                  <div>
                    <p className="text-sm font-medium text-[var(--grey-900)]">Gemma answers your number</p>
                    <p className="text-xs text-[var(--grey-500)]">Usually takes 5-10 business days</p>
                  </div>
                </div>
              </div>

              <div className="bg-blue-50 rounded-lg p-3 flex items-start gap-3">
                <Clock className="w-5 h-5 text-blue-600 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-blue-800">
                    No downtime during transfer
                  </p>
                  <p className="text-sm text-blue-700">
                    We set up temporary forwarding so you miss nothing.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Fixed bottom button */}
      {migrationTier && (
        <div className="sticky bottom-0 bg-white border-t border-[var(--grey-200)] px-6 py-4 safe-area-pb">
          <Button
            className="w-full"
            size="lg"
            onClick={handleContinue}
            loading={isLoading}
          >
            {migrationTier === "porting" ? "Start transfer" : "Continue"}
          </Button>
        </div>
      )}
    </>
  );
}
