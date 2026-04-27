"use client";

import React from "react";
import { BottomNavigation } from "./BottomNavigation";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-[var(--grey-50)] overflow-x-hidden">
      <div className="max-w-md mx-auto bg-white min-h-screen flex flex-col overflow-x-hidden">
        <div className="flex-1 pb-20">
          {children}
        </div>
        <BottomNavigation />
      </div>
    </div>
  );
}
