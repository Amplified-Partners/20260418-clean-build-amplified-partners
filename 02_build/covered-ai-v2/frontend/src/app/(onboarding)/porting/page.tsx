"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Phone, FileText, CheckCircle, AlertCircle, Download } from "lucide-react";
import { Button, Input, Select } from "@/components/ui";
import { portingApi } from "@/lib/api";

const providers = [
  { value: "", label: "Select your provider" },
  { value: "bt", label: "BT" },
  { value: "ee", label: "EE" },
  { value: "vodafone", label: "Vodafone" },
  { value: "o2", label: "O2" },
  { value: "three", label: "Three" },
  { value: "sky", label: "Sky" },
  { value: "virgin", label: "Virgin Media" },
  { value: "talktalk", label: "TalkTalk" },
  { value: "plusnet", label: "Plusnet" },
  { value: "hyperoptic", label: "Hyperoptic" },
  { value: "zen", label: "Zen Internet" },
  { value: "voipfone", label: "Voipfone" },
  { value: "ringcentral", label: "RingCentral" },
  { value: "8x8", label: "8x8" },
  { value: "other", label: "Other" },
];

export default function PortingPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [requestId, setRequestId] = useState<string | null>(null);
  
  // Form state
  const [formData, setFormData] = useState({
    numberToPort: "",
    currentProvider: "",
    accountNumber: "",
    accountHolderName: "",
    billingPostcode: "",
    authorizedSignature: "",
    agreedToTerms: false,
  });

  const handleInputChange = (field: string, value: string | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    setError("");
  };

  const validateStep1 = () => {
    if (!formData.numberToPort) return "Please enter the phone number to transfer";
    if (!formData.currentProvider) return "Please select your current provider";
    if (!formData.accountNumber) return "Please enter your account number";
    return null;
  };

  const validateStep2 = () => {
    if (!formData.accountHolderName) return "Please enter the account holder name";
    if (!formData.billingPostcode) return "Please enter your billing postcode";
    if (!formData.authorizedSignature) return "Please type your name to authorize";
    if (!formData.agreedToTerms) return "Please agree to the terms";
    return null;
  };

  const handleNext = () => {
    const validationError = validateStep1();
    if (validationError) {
      setError(validationError);
      return;
    }
    setStep(2);
  };

  const handleSubmit = async () => {
    const validationError = validateStep2();
    if (validationError) {
      setError(validationError);
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      const result = await portingApi.submit({
        number_to_port: formData.numberToPort,
        current_provider: formData.currentProvider,
        account_number: formData.accountNumber,
        account_holder_name: formData.accountHolderName,
        billing_postcode: formData.billingPostcode,
        authorized_signature: formData.authorizedSignature,
        email: localStorage.getItem("user_email") || undefined,
      });

      setRequestId(result.id);
      setStep(3);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadLoa = () => {
    if (requestId) {
      window.open(portingApi.downloadLoa(requestId), "_blank");
    }
  };

  return (
    <>
      <main className="flex-1 px-6 py-8">
        {/* Progress */}
        <div className="mb-8">
          <p className="text-sm text-[var(--grey-500)] mb-2">Number Transfer</p>
          <div className="flex gap-2">
            <div className={`h-1 flex-1 rounded-full ${step >= 1 ? 'bg-[var(--brand-primary)]' : 'bg-[var(--grey-200)]'}`} />
            <div className={`h-1 flex-1 rounded-full ${step >= 2 ? 'bg-[var(--brand-primary)]' : 'bg-[var(--grey-200)]'}`} />
            <div className={`h-1 flex-1 rounded-full ${step >= 3 ? 'bg-[var(--brand-primary)]' : 'bg-[var(--grey-200)]'}`} />
          </div>
        </div>

        {error && (
          <div className="flex items-start gap-2 text-sm text-red-600 bg-red-50 px-3 py-2 rounded-lg mb-4">
            <AlertCircle className="w-4 h-4 mt-0.5 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Step 1: Number & Provider */}
        {step === 1 && (
          <div className="space-y-6">
            <div>
              <h1 className="text-2xl font-bold text-[var(--grey-900)] mb-2">
                Your current number
              </h1>
              <p className="text-[var(--grey-600)]">
                Tell us about the number you want to transfer.
              </p>
            </div>

            <div className="space-y-4">
              <Input
                label="Phone number to transfer"
                placeholder="07700 900123 or 0191 123 4567"
                value={formData.numberToPort}
                onChange={(e) => handleInputChange("numberToPort", e.target.value)}
              />

              <Select
                label="Current provider"
                options={providers}
                value={formData.currentProvider}
                onChange={(e) => handleInputChange("currentProvider", e.target.value)}
              />

              <Input
                label="Account number with current provider"
                placeholder="Found on your bill"
                value={formData.accountNumber}
                onChange={(e) => handleInputChange("accountNumber", e.target.value)}
              />
            </div>

            <div className="bg-amber-50 rounded-lg p-3">
              <p className="text-sm text-amber-800">
                <strong>Where to find your account number:</strong> Check your latest bill, online account, or call your provider.
              </p>
            </div>
          </div>
        )}

        {/* Step 2: Authorization */}
        {step === 2 && (
          <div className="space-y-6">
            <div>
              <h1 className="text-2xl font-bold text-[var(--grey-900)] mb-2">
                Authorize the transfer
              </h1>
              <p className="text-[var(--grey-600)]">
                We need your permission to request the port.
              </p>
            </div>

            <div className="space-y-4">
              <Input
                label="Account holder name (as it appears on your bill)"
                placeholder="John Smith"
                value={formData.accountHolderName}
                onChange={(e) => handleInputChange("accountHolderName", e.target.value)}
              />

              <Input
                label="Billing postcode"
                placeholder="NE1 4ST"
                value={formData.billingPostcode}
                onChange={(e) => handleInputChange("billingPostcode", e.target.value)}
              />

              <div className="bg-[var(--grey-50)] rounded-lg p-4 space-y-3">
                <div className="flex items-start gap-3">
                  <FileText className="w-5 h-5 text-[var(--grey-500)] mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-[var(--grey-900)]">
                      Letter of Authorization
                    </p>
                    <p className="text-xs text-[var(--grey-600)] mt-1">
                      By typing your name below, you authorize Covered AI Limited to request the transfer of your phone number from your current provider.
                    </p>
                  </div>
                </div>

                <Input
                  label="Type your full name to authorize"
                  placeholder="John Smith"
                  value={formData.authorizedSignature}
                  onChange={(e) => handleInputChange("authorizedSignature", e.target.value)}
                />

                <label className="flex items-start gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.agreedToTerms}
                    onChange={(e) => handleInputChange("agreedToTerms", e.target.checked)}
                    className="mt-1 w-4 h-4 rounded border-[var(--grey-300)] text-[var(--brand-primary)] focus:ring-[var(--brand-primary)]"
                  />
                  <span className="text-sm text-[var(--grey-600)]">
                    I confirm I am the account holder or have authority to request this transfer. I understand the transfer typically takes 5-10 business days.
                  </span>
                </label>
              </div>
            </div>
          </div>
        )}

        {/* Step 3: Confirmation */}
        {step === 3 && (
          <div className="space-y-6 text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full">
              <CheckCircle className="w-8 h-8 text-green-600" />
            </div>

            <div>
              <h1 className="text-2xl font-bold text-[var(--grey-900)] mb-2">
                Transfer requested
              </h1>
              <p className="text-[var(--grey-600)]">
                We've received your porting request for <strong>{formData.numberToPort}</strong>.
              </p>
              {requestId && (
                <p className="text-sm text-[var(--grey-500)] mt-1">
                  Reference: {requestId}
                </p>
              )}
            </div>

            <div className="bg-[var(--grey-50)] rounded-lg p-4 text-left space-y-3">
              <h3 className="font-semibold text-[var(--grey-900)]">What happens next</h3>
              
              <div className="space-y-2">
                <div className="flex items-start gap-3">
                  <div className="w-5 h-5 rounded-full bg-[var(--brand-primary)] flex items-center justify-center text-xs text-white font-medium">1</div>
                  <p className="text-sm text-[var(--grey-600)]">
                    We submit the transfer request to your provider (today)
                  </p>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-5 h-5 rounded-full bg-[var(--grey-300)] flex items-center justify-center text-xs text-white font-medium">2</div>
                  <p className="text-sm text-[var(--grey-600)]">
                    We set up temporary forwarding so you miss no calls
                  </p>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-5 h-5 rounded-full bg-[var(--grey-300)] flex items-center justify-center text-xs text-white font-medium">3</div>
                  <p className="text-sm text-[var(--grey-600)]">
                    Transfer completes in 5-10 business days
                  </p>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-5 h-5 rounded-full bg-[var(--grey-300)] flex items-center justify-center text-xs text-white font-medium">4</div>
                  <p className="text-sm text-[var(--grey-600)]">
                    We'll email you when your number is live
                  </p>
                </div>
              </div>
            </div>

            {requestId && (
              <Button
                variant="secondary"
                onClick={handleDownloadLoa}
                icon={<Download className="w-4 h-4" />}
              >
                Download LOA
              </Button>
            )}

            <div className="bg-blue-50 rounded-lg p-3">
              <p className="text-sm text-blue-800">
                <strong>In the meantime:</strong> Let's get Gemma set up so she's ready when your number transfers.
              </p>
            </div>
          </div>
        )}
      </main>

      {/* Fixed bottom button */}
      <div className="sticky bottom-0 bg-white border-t border-[var(--grey-200)] px-6 py-4 safe-area-pb">
        {step === 1 && (
          <div className="flex gap-3">
            <Button
              variant="secondary"
              className="flex-1"
              onClick={() => router.push("/step-2")}
            >
              Back
            </Button>
            <Button
              className="flex-1"
              onClick={handleNext}
            >
              Next
            </Button>
          </div>
        )}
        
        {step === 2 && (
          <div className="flex gap-3">
            <Button
              variant="secondary"
              className="flex-1"
              onClick={() => setStep(1)}
            >
              Back
            </Button>
            <Button
              className="flex-1"
              onClick={handleSubmit}
              loading={isLoading}
            >
              Submit request
            </Button>
          </div>
        )}

        {step === 3 && (
          <Button
            className="w-full"
            size="lg"
            onClick={() => router.push("/step-3")}
          >
            Continue setup
          </Button>
        )}
      </div>
    </>
  );
}
