/**
 * Step2CallForwarding Component
 *
 * Second step of onboarding: set up call forwarding.
 * - Shows Covered phone number
 * - Network-specific instructions
 * - Copy buttons for number and code
 */

import React, { useState } from "react";

interface ForwardingInstructions {
  network: string;
  covered_number: string;
  covered_number_display: string;
  forward_code: string;
  cancel_code: string;
  instructions: string[];
}

interface Step2CallForwardingProps {
  coveredNumber: string;
  coveredNumberDisplay: string;
  onGetInstructions: (network: string) => Promise<ForwardingInstructions>;
  onSubmit: (network: string) => Promise<void>;
  isLoading?: boolean;
  error?: string;
}

const NETWORKS = [
  { id: "ee", name: "EE" },
  { id: "vodafone", name: "Vodafone" },
  { id: "o2", name: "O2" },
  { id: "three", name: "Three" },
  { id: "bt", name: "BT" },
  { id: "sky", name: "Sky" },
];

export const Step2CallForwarding: React.FC<Step2CallForwardingProps> = ({
  coveredNumber,
  coveredNumberDisplay,
  onGetInstructions,
  onSubmit,
  isLoading = false,
  error,
}) => {
  const [selectedNetwork, setSelectedNetwork] = useState<string>("");
  const [instructions, setInstructions] = useState<ForwardingInstructions | null>(null);
  const [copied, setCopied] = useState<"number" | "code" | null>(null);
  const [loadingInstructions, setLoadingInstructions] = useState(false);

  const handleNetworkSelect = async (network: string) => {
    setSelectedNetwork(network);
    setLoadingInstructions(true);
    try {
      const result = await onGetInstructions(network);
      setInstructions(result);
    } catch (err) {
      console.error("Failed to get instructions:", err);
    } finally {
      setLoadingInstructions(false);
    }
  };

  const copyToClipboard = async (text: string, type: "number" | "code") => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(type);
      setTimeout(() => setCopied(null), 2000);
    } catch (err) {
      console.error("Failed to copy:", err);
    }
  };

  const handleSubmit = async () => {
    await onSubmit(selectedNetwork);
  };

  return (
    <div className="max-w-md mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Connect your phone line</h1>
        <p className="text-sm text-gray-600">Forward your calls to your new Covered number</p>
      </div>

      {error && (
        <div className="mb-6 p-3 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      {/* Covered Number Display */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <p className="text-xs text-gray-500 mb-2 text-center">Your Covered AI number</p>
        <div className="flex items-center justify-center gap-3">
          <span className="text-2xl font-mono font-bold text-gray-900">
            {coveredNumberDisplay}
          </span>
          <button
            onClick={() => copyToClipboard(coveredNumber, "number")}
            className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
            title="Copy number"
          >
            {copied === "number" ? (
              <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            ) : (
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
            )}
          </button>
        </div>
      </div>

      {/* Network Selection */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Select your mobile network
        </label>
        <div className="grid grid-cols-3 gap-2">
          {NETWORKS.map((network) => (
            <button
              key={network.id}
              type="button"
              onClick={() => handleNetworkSelect(network.id)}
              className={`p-3 text-sm font-medium rounded-lg border transition-all ${
                selectedNetwork === network.id
                  ? "border-indigo-500 bg-indigo-50 text-indigo-700"
                  : "border-gray-200 text-gray-700 hover:border-gray-300 hover:bg-gray-50"
              }`}
            >
              {network.name}
            </button>
          ))}
        </div>
      </div>

      {/* Instructions */}
      {loadingInstructions && (
        <div className="bg-gray-50 rounded-lg p-6 mb-6 animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-3/4 mb-3"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
      )}

      {instructions && !loadingInstructions && (
        <div className="bg-gray-50 rounded-lg p-6 mb-6">
          <h3 className="font-medium text-gray-900 mb-4">
            For {NETWORKS.find((n) => n.id === selectedNetwork)?.name}:
          </h3>

          {/* Forward code with copy button */}
          <div className="bg-white rounded-lg p-4 mb-4 border border-gray-200">
            <p className="text-xs text-gray-500 mb-1">Dial this code:</p>
            <div className="flex items-center justify-between">
              <code className="text-lg font-mono font-bold text-indigo-600">
                {instructions.forward_code}
              </code>
              <button
                onClick={() => copyToClipboard(instructions.forward_code, "code")}
                className="px-3 py-1.5 text-sm bg-indigo-100 text-indigo-700 rounded-md hover:bg-indigo-200 transition-colors flex items-center gap-1"
              >
                {copied === "code" ? (
                  <>
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    Copied
                  </>
                ) : (
                  <>
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                    Copy
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Step-by-step instructions */}
          <ol className="space-y-2">
            {instructions.instructions.map((step, index) => (
              <li key={index} className="flex items-start gap-3 text-sm text-gray-700">
                <span className="flex-shrink-0 w-5 h-5 rounded-full bg-indigo-100 text-indigo-600 text-xs flex items-center justify-center font-medium">
                  {index + 1}
                </span>
                {step}
              </li>
            ))}
          </ol>

          {/* Time estimate */}
          <div className="mt-4 flex items-center gap-2 text-xs text-gray-500">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Takes about 60 seconds
          </div>
        </div>
      )}

      {/* Help link */}
      <div className="text-center mb-6">
        <a href="#" className="text-sm text-indigo-600 hover:text-indigo-500">
          Having trouble? Chat with us
        </a>
      </div>

      {/* Submit */}
      <button
        onClick={handleSubmit}
        disabled={isLoading || !selectedNetwork}
        className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLoading ? (
          <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
        ) : (
          "I've set up forwarding"
        )}
      </button>
    </div>
  );
};

export default Step2CallForwarding;
