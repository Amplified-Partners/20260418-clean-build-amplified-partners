"use client";

import React from "react";
import { Button } from "./Button";

interface CelebrationModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  subtitle: string;
  amount: string;
  emoji?: string;
}

export function CelebrationModal({
  isOpen,
  onClose,
  title,
  subtitle,
  amount,
  emoji = "🎉",
}: CelebrationModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-2xl p-8 text-center max-w-sm mx-4 shadow-2xl">
        <span className="text-6xl">{emoji}</span>
        <h2 className="mt-4 text-2xl font-bold text-[var(--grey-900)]">{title}</h2>
        <p className="mt-2 text-[var(--grey-600)]">{subtitle}</p>
        <p className="mt-4 text-4xl font-bold text-green-600">{amount}</p>
        <Button className="mt-6 w-full" onClick={onClose}>
          Nice!
        </Button>
      </div>
    </div>
  );
}
