"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, Phone, FileText, Calendar, Settings } from "lucide-react";
import { cn } from "@/lib/utils";

const navItems = [
  { id: "home", icon: Home, label: "Home", href: "/" },
  { id: "calls", icon: Phone, label: "Calls", href: "/calls" },
  { id: "invoices", icon: FileText, label: "Invoices", href: "/invoices" },
  { id: "schedule", icon: Calendar, label: "Schedule", href: "/schedule" },
  { id: "settings", icon: Settings, label: "Settings", href: "/settings" },
];

export function BottomNavigation() {
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-0 left-0 right-0 max-w-md mx-auto bg-white border-t border-[var(--grey-200)] safe-area-pb z-50">
      <div className="flex items-center justify-around px-2 py-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(`${item.href}/`));
          const isHome = item.href === "/" && pathname === "/";

          return (
            <Link
              key={item.id}
              href={item.href}
              className={cn(
                "flex flex-col items-center justify-center gap-0.5 min-w-[56px] min-h-[48px] px-2 py-1 rounded-lg transition-colors touch-manipulation",
                isActive || isHome
                  ? "text-[var(--brand-primary)]"
                  : "text-[var(--grey-400)] active:bg-[var(--grey-100)]"
              )}
            >
              <Icon className="w-6 h-6" strokeWidth={isActive || isHome ? 2.5 : 2} />
              <span className="text-[10px] font-medium leading-tight">{item.label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
