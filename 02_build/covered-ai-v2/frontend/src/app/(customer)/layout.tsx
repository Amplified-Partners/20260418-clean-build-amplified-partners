/**
 * Customer App Layout
 * 
 * For end customers (Mrs Thompson, Dave, Sarah).
 * No login required - magic links only.
 * Business branded.
 */

import React from "react";

interface CustomerLayoutProps {
  children: React.ReactNode;
}

export default function CustomerLayout({ children }: CustomerLayoutProps) {
  return (
    <div className="min-h-screen bg-white">
      {/* No nav - single purpose pages */}
      <main className="max-w-lg mx-auto">
        {children}
      </main>
      
      {/* Powered by footer */}
      <footer className="py-4 text-center">
        <p className="text-xs text-neutral-400">
          Powered by <span className="font-medium">Covered</span>
        </p>
      </footer>
    </div>
  );
}
