/**
 * OnboardingLayout Component
 *
 * Container for the 3-step onboarding flow with:
 * - Progress bar at top
 * - Step indicator
 * - Mobile-optimized layout
 */

import React from "react";

interface OnboardingLayoutProps {
  currentStep: 1 | 2 | 3;
  children: React.ReactNode;
}

export const OnboardingLayout: React.FC<OnboardingLayoutProps> = ({
  currentStep,
  children,
}) => {
  const steps = [
    { number: 1, label: "Your Business" },
    { number: 2, label: "Connect Line" },
    { number: 3, label: "Test It" },
  ];

  const progressPercent = ((currentStep - 1) / 2) * 100;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header with progress */}
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="px-4 py-4">
          {/* Step labels */}
          <div className="flex justify-between text-xs text-gray-500 mb-2">
            {steps.map((step) => (
              <span
                key={step.number}
                className={
                  step.number === currentStep
                    ? "text-indigo-600 font-medium"
                    : step.number < currentStep
                    ? "text-green-600"
                    : ""
                }
              >
                {step.label}
              </span>
            ))}
          </div>

          {/* Progress bar */}
          <div className="relative h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="absolute left-0 top-0 h-full bg-indigo-600 rounded-full transition-all duration-300 ease-out"
              style={{ width: `${progressPercent}%` }}
            />
            {/* Step indicators */}
            <div className="absolute inset-0 flex justify-between items-center px-0">
              {steps.map((step) => (
                <div
                  key={step.number}
                  className={`w-4 h-4 rounded-full border-2 ${
                    step.number <= currentStep
                      ? "bg-indigo-600 border-indigo-600"
                      : "bg-white border-gray-300"
                  } ${step.number === currentStep ? "ring-2 ring-indigo-200" : ""}`}
                  style={{
                    marginLeft: step.number === 1 ? "-2px" : undefined,
                    marginRight: step.number === 3 ? "-2px" : undefined,
                  }}
                >
                  {step.number < currentStep && (
                    <svg className="w-3 h-3 text-white m-auto" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Current step heading */}
          <div className="mt-4 text-center">
            <span className="text-xs text-gray-500">Step {currentStep} of 3</span>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="p-4 pb-24">{children}</main>
    </div>
  );
};

export default OnboardingLayout;
