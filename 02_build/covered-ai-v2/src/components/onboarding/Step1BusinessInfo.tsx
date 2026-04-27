/**
 * Step1BusinessInfo Component
 *
 * First step of onboarding: collect business details.
 * - Business name
 * - Owner name
 * - Mobile number (for notifications)
 * - Business type (vertical)
 */

import React, { useState } from "react";

interface Step1Data {
  businessName: string;
  ownerName: string;
  phone: string;
  vertical: string;
}

interface Step1BusinessInfoProps {
  initialData?: Partial<Step1Data>;
  onSubmit: (data: Step1Data) => Promise<void>;
  isLoading?: boolean;
  error?: string;
}

const VERTICALS = [
  { id: "trades", label: "Tradesperson", icon: "wrench", description: "Plumber, electrician, builder" },
  { id: "vet", label: "Veterinary", icon: "heart", description: "Vet clinic, animal hospital" },
  { id: "dental", label: "Dental", icon: "tooth", description: "Dentist, orthodontist" },
  { id: "aesthetics", label: "Aesthetics", icon: "sparkles", description: "Beauty, cosmetics" },
  { id: "salon", label: "Salon", icon: "scissors", description: "Hair, nails, spa" },
  { id: "physio", label: "Physiotherapy", icon: "activity", description: "Physio, sports therapy" },
  { id: "auto", label: "Automotive", icon: "car", description: "Garage, mechanic" },
  { id: "legal", label: "Legal", icon: "scale", description: "Solicitor, law firm" },
  { id: "accountant", label: "Accountant", icon: "calculator", description: "Accounting, bookkeeping" },
  { id: "fitness", label: "Fitness", icon: "dumbbell", description: "Gym, personal training" },
];

export const Step1BusinessInfo: React.FC<Step1BusinessInfoProps> = ({
  initialData,
  onSubmit,
  isLoading = false,
  error,
}) => {
  const [businessName, setBusinessName] = useState(initialData?.businessName || "");
  const [ownerName, setOwnerName] = useState(initialData?.ownerName || "");
  const [phone, setPhone] = useState(initialData?.phone || "");
  const [vertical, setVertical] = useState(initialData?.vertical || "");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onSubmit({ businessName, ownerName, phone, vertical });
  };

  const formatPhone = (value: string) => {
    // Remove non-digits
    const digits = value.replace(/\D/g, "");
    // Format as UK mobile
    if (digits.startsWith("44")) {
      return `+${digits}`;
    }
    if (digits.startsWith("0")) {
      return `+44${digits.slice(1)}`;
    }
    if (digits.length > 0) {
      return `+44${digits}`;
    }
    return "";
  };

  return (
    <div className="max-w-md mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Let's get you set up</h1>
        <p className="text-sm text-gray-600">Tell us about your business</p>
      </div>

      {error && (
        <div className="mb-6 p-3 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Business Name */}
        <div>
          <label htmlFor="businessName" className="block text-sm font-medium text-gray-700">
            Business Name
          </label>
          <input
            id="businessName"
            type="text"
            required
            value={businessName}
            onChange={(e) => setBusinessName(e.target.value)}
            className="mt-1 block w-full px-3 py-3 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="e.g., Titan Plumbing Solutions"
          />
        </div>

        {/* Owner Name */}
        <div>
          <label htmlFor="ownerName" className="block text-sm font-medium text-gray-700">
            Your Name
          </label>
          <input
            id="ownerName"
            type="text"
            required
            value={ownerName}
            onChange={(e) => setOwnerName(e.target.value)}
            className="mt-1 block w-full px-3 py-3 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="e.g., Ralph"
          />
        </div>

        {/* Phone */}
        <div>
          <label htmlFor="phone" className="block text-sm font-medium text-gray-700">
            Your Mobile (for lead notifications)
          </label>
          <input
            id="phone"
            type="tel"
            required
            value={phone}
            onChange={(e) => setPhone(formatPhone(e.target.value))}
            className="mt-1 block w-full px-3 py-3 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="+44 7XXX XXXXXX"
          />
          <p className="mt-1 text-xs text-gray-500">We'll send you WhatsApp notifications when leads come in</p>
        </div>

        {/* Vertical Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            What type of business?
          </label>
          <div className="grid grid-cols-2 gap-3">
            {VERTICALS.slice(0, 6).map((v) => (
              <button
                key={v.id}
                type="button"
                onClick={() => setVertical(v.id)}
                className={`p-3 text-left border rounded-lg transition-all ${
                  vertical === v.id
                    ? "border-indigo-500 bg-indigo-50 ring-2 ring-indigo-200"
                    : "border-gray-200 hover:border-gray-300 hover:bg-gray-50"
                }`}
              >
                <span className="block font-medium text-sm text-gray-900">{v.label}</span>
                <span className="block text-xs text-gray-500 mt-0.5">{v.description}</span>
              </button>
            ))}
          </div>

          {/* Show more options */}
          <details className="mt-3">
            <summary className="text-sm text-indigo-600 cursor-pointer hover:text-indigo-500">
              More business types
            </summary>
            <div className="grid grid-cols-2 gap-3 mt-3">
              {VERTICALS.slice(6).map((v) => (
                <button
                  key={v.id}
                  type="button"
                  onClick={() => setVertical(v.id)}
                  className={`p-3 text-left border rounded-lg transition-all ${
                    vertical === v.id
                      ? "border-indigo-500 bg-indigo-50 ring-2 ring-indigo-200"
                      : "border-gray-200 hover:border-gray-300 hover:bg-gray-50"
                  }`}
                >
                  <span className="block font-medium text-sm text-gray-900">{v.label}</span>
                  <span className="block text-xs text-gray-500 mt-0.5">{v.description}</span>
                </button>
              ))}
            </div>
          </details>
        </div>

        {/* Submit */}
        <button
          type="submit"
          disabled={isLoading || !businessName || !ownerName || !phone || !vertical}
          className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
          ) : (
            "Continue"
          )}
        </button>
      </form>
    </div>
  );
};

export default Step1BusinessInfo;
