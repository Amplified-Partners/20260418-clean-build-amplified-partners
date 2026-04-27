/**
 * Client App Layout
 * 
 * Clean, mobile-first layout with bottom navigation.
 * Gemma status always visible.
 */

"use client";

import React from "react";
import { usePathname } from "next/navigation";
import { Home, Phone, PoundSterling, MoreHorizontal } from "lucide-react";
import { GemmaStatus, BottomNav } from "@/components/client-app";

const navItems = [
  { 
    id: "home", 
    icon: <Home className="w-6 h-6" />, 
    label: "Home", 
    href: "/home" 
  },
  { 
    id: "calls", 
    icon: <Phone className="w-6 h-6" />, 
    label: "Calls", 
    href: "/calls" 
  },
  { 
    id: "money", 
    icon: <PoundSterling className="w-6 h-6" />, 
    label: "Money", 
    href: "/money" 
  },
  { 
    id: "more", 
    icon: <MoreHorizontal className="w-6 h-6" />, 
    label: "More", 
    href: "/more" 
  },
];

export default function ClientLayout({ 
  children 
}: { 
  children: React.ReactNode 
}) {
  const pathname = usePathname();
  
  // Determine active nav item
  const activeId = navItems.find(
    item => pathname === item.href || pathname.startsWith(`${item.href}/`)
  )?.id || "home";

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Constrained container for mobile feel */}
      <div className="max-w-md mx-auto bg-white min-h-screen flex flex-col">
        
        {/* Top bar with Gemma status */}
        <div className="sticky top-0 z-50 bg-white/95 backdrop-blur-sm border-b border-neutral-100">
          <div className="px-5 py-3 flex items-center justify-between">
            <span className="text-sm font-semibold text-neutral-900">Covered</span>
            <GemmaStatus status="active" />
          </div>
        </div>
        
        {/* Main content */}
        <main className="flex-1 pb-20">
          {children}
        </main>
        
        {/* Bottom navigation */}
        <BottomNav items={navItems} activeId={activeId} />
      </div>
    </div>
  );
}
