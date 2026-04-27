import React from "react";

export default function OnboardingLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-[var(--grey-50)]">
      <div className="max-w-md mx-auto min-h-screen bg-white flex flex-col">
        {children}
      </div>
    </div>
  );
}
