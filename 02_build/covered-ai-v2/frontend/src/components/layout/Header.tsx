"use client";

import React from "react";
import { ChevronLeft, HelpCircle, Settings } from "lucide-react";
import { IconButton } from "@/components/ui";
import { useRouter } from "next/navigation";

export interface HeaderProps {
  greeting?: boolean;
  greetingText?: string;
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
  rightContent?: React.ReactNode;
  backButton?: boolean;
  showBack?: boolean;
  onBack?: () => void;
  showHelp?: boolean;
  showSettings?: boolean;
}

export function Header({
  greeting = false,
  greetingText,
  title,
  subtitle,
  action,
  rightContent,
  backButton = false,
  showBack = false,
  onBack,
  showHelp = false,
  showSettings = false,
}: HeaderProps) {
  const router = useRouter();

  const handleBack = () => {
    if (onBack) {
      onBack();
    } else {
      router.back();
    }
  };

  // Back button header variant
  if (backButton || showBack) {
    return (
      <header className="bg-white border-b border-[var(--grey-200)] px-4 py-3 flex items-center gap-3 sticky top-0 z-10">
        <button
          onClick={handleBack}
          className="w-10 h-10 flex items-center justify-center text-[var(--grey-400)] hover:text-[var(--grey-600)] hover:bg-[var(--grey-100)] rounded-lg transition-colors"
          aria-label="Go back"
        >
          <ChevronLeft className="w-5 h-5" />
        </button>
        <h1 className="text-xl font-semibold text-[var(--grey-900)]">{title}</h1>
        {(action || rightContent) && <div className="ml-auto">{action || rightContent}</div>}
      </header>
    );
  }

  // Greeting header (dashboard)
  if (greeting) {
    return (
      <header className="bg-white border-b border-[var(--grey-200)] px-4 py-3 sticky top-0 z-10">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-[var(--grey-500)]">{greetingText || getGreeting()}</p>
            <h1 className="text-xl font-semibold text-[var(--grey-900)]">{title}</h1>
          </div>
          <div className="flex items-center gap-2">
            {showHelp && (
              <IconButton icon={<HelpCircle className="w-5 h-5" />} aria-label="Help" />
            )}
            {showSettings && (
              <IconButton
                icon={<Settings className="w-5 h-5" />}
                aria-label="Settings"
                onClick={() => router.push("/dashboard/settings")}
              />
            )}
          </div>
        </div>
      </header>
    );
  }

  // Standard page header
  return (
    <header className="bg-white border-b border-[var(--grey-200)] px-4 py-3 sticky top-0 z-10">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold text-[var(--grey-900)]">{title}</h1>
          {subtitle && <p className="text-sm text-[var(--grey-500)]">{subtitle}</p>}
        </div>
        {action}
      </div>
    </header>
  );
}

function getGreeting(): string {
  const hour = new Date().getHours();
  if (hour < 12) return "Good morning";
  if (hour < 17) return "Good afternoon";
  return "Good evening";
}
