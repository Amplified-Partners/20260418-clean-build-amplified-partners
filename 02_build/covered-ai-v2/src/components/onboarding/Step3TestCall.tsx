/**
 * Step3TestCall Component
 *
 * Third step of onboarding: make a test call.
 * - Shows call button (tel: link)
 * - Polls for test call status
 * - Shows success state when call received
 * - Option to skip
 */

import React, { useState, useEffect } from "react";

interface Step3TestCallProps {
  coveredNumber: string;
  coveredNumberDisplay: string;
  testCallReceived: boolean;
  onCheckStatus: () => Promise<{ test_call_received: boolean }>;
  onComplete: () => Promise<void>;
  onSkip: () => Promise<void>;
  isLoading?: boolean;
  error?: string;
}

export const Step3TestCall: React.FC<Step3TestCallProps> = ({
  coveredNumber,
  coveredNumberDisplay,
  testCallReceived: initialTestCallReceived,
  onCheckStatus,
  onComplete,
  onSkip,
  isLoading = false,
  error,
}) => {
  const [testCallReceived, setTestCallReceived] = useState(initialTestCallReceived);
  const [polling, setPolling] = useState(false);

  // Poll for test call status
  useEffect(() => {
    if (testCallReceived) return;

    const pollInterval = setInterval(async () => {
      try {
        const status = await onCheckStatus();
        if (status.test_call_received) {
          setTestCallReceived(true);
          setPolling(false);
        }
      } catch (err) {
        console.error("Failed to check status:", err);
      }
    }, 3000); // Poll every 3 seconds

    setPolling(true);

    return () => {
      clearInterval(pollInterval);
      setPolling(false);
    };
  }, [testCallReceived, onCheckStatus]);

  // Success state
  if (testCallReceived) {
    return (
      <div className="max-w-md mx-auto">
        <div className="text-center mb-8">
          {/* Success animation */}
          <div className="mx-auto w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mb-6 animate-bounce">
            <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>

          <h1 className="text-2xl font-bold text-gray-900 mb-2">Test successful!</h1>
          <p className="text-lg text-green-600 font-medium mb-2">You're Live!</p>
          <p className="text-sm text-gray-600">Gemma is now answering your calls 24/7</p>
        </div>

        {/* WhatsApp preview */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
          <p className="text-xs text-gray-500 mb-3">Your first real lead will look like this:</p>
          <div className="bg-green-50 rounded-lg p-4 border border-green-100">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                <span className="text-white text-xs font-bold">C</span>
              </div>
              <span className="text-sm font-medium text-gray-900">COVERED AI</span>
            </div>
            <div className="text-sm text-gray-700">
              <p className="font-medium text-red-600">New Lead: Burst pipe (EMERGENCY)</p>
              <p>Sarah M, NE4 5TH</p>
              <p className="text-gray-500">"Water coming through ceiling"</p>
            </div>
          </div>
        </div>

        {/* Complete button */}
        <button
          onClick={onComplete}
          disabled={isLoading}
          className="w-full flex justify-center py-4 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
          ) : (
            "Go to Dashboard"
          )}
        </button>
      </div>
    );
  }

  // Waiting state
  return (
    <div className="max-w-md mx-auto">
      <div className="text-center mb-8">
        <div className="mx-auto w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
          <svg className="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
          </svg>
        </div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Let's test it!</h1>
        <p className="text-sm text-gray-600">Make a test call to meet Gemma, your AI assistant</p>
      </div>

      {error && (
        <div className="mb-6 p-3 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      {/* Call button */}
      <a
        href={`tel:${coveredNumber}`}
        className="block w-full py-4 px-4 border border-transparent rounded-md shadow-sm text-center text-lg font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 mb-6"
      >
        <span className="flex items-center justify-center gap-2">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
          </svg>
          Call {coveredNumberDisplay}
        </span>
      </a>

      {/* Suggestion */}
      <div className="bg-gray-50 rounded-lg p-4 mb-6">
        <p className="text-sm text-gray-600 mb-2">
          <span className="font-medium">Try saying:</span>
        </p>
        <p className="text-sm text-gray-700 italic">
          "Hi, I've got a leaky tap in Newcastle, postcode NE4"
        </p>
      </div>

      {/* Status indicator */}
      <div className="bg-white rounded-lg border border-gray-200 p-4 mb-6">
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600">Call status:</span>
          <span className="flex items-center gap-2 text-sm">
            {polling ? (
              <>
                <span className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></span>
                <span className="text-yellow-600">Waiting for call...</span>
              </>
            ) : (
              <>
                <span className="w-2 h-2 bg-gray-300 rounded-full"></span>
                <span className="text-gray-500">Not received</span>
              </>
            )}
          </span>
        </div>
      </div>

      {/* Skip option */}
      <button
        onClick={onSkip}
        disabled={isLoading}
        className="w-full text-center text-sm text-gray-500 hover:text-gray-700 py-2"
      >
        Skip for now - I'll test later
      </button>
    </div>
  );
};

export default Step3TestCall;
