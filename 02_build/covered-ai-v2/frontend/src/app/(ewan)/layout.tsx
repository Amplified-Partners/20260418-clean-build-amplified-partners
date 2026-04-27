/**
 * Ewan Admin App Layout
 * 
 * Command center for everything.
 * Desktop-first, data-dense, full control.
 */

import React from "react";
import Link from "next/link";
import { LayoutDashboard, Users, Phone, TrendingUp, Settings, Zap } from "lucide-react";

interface EwanLayoutProps {
  children: React.ReactNode;
}

const navItems = [
  { href: "/command", icon: LayoutDashboard, label: "Command" },
  { href: "/command/clients", icon: Users, label: "Clients" },
  { href: "/command/calls", icon: Phone, label: "Calls" },
  { href: "/command/pipeline", icon: TrendingUp, label: "Pipeline" },
  { href: "/command/system", icon: Zap, label: "System" },
  { href: "/command/settings", icon: Settings, label: "Settings" },
];

export default function EwanLayout({ children }: EwanLayoutProps) {
  return (
    <div className="min-h-screen bg-neutral-950 text-white">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 bottom-0 w-64 bg-neutral-900 border-r border-neutral-800">
        {/* Logo */}
        <div className="p-6 border-b border-neutral-800">
          <h1 className="text-xl font-bold text-white">Covered</h1>
          <p className="text-xs text-neutral-500 mt-1">Mission Control</p>
        </div>
        
        {/* Navigation */}
        <nav className="p-4 space-y-1">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="flex items-center gap-3 px-4 py-3 rounded-lg text-neutral-400 hover:text-white hover:bg-neutral-800 transition-colors"
            >
              <item.icon className="w-5 h-5" />
              <span>{item.label}</span>
            </Link>
          ))}
        </nav>
        
        {/* System status */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-neutral-800">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="text-xs text-neutral-500">All systems operational</span>
          </div>
        </div>
      </aside>
      
      {/* Main content */}
      <main className="ml-64 min-h-screen">
        {children}
      </main>
    </div>
  );
}
