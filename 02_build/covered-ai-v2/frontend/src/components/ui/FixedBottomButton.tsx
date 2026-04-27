"use client";

import React from "react";
import { Button } from "./Button";

interface FixedBottomButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  loading?: boolean;
  disabled?: boolean;
  icon?: React.ReactNode;
}

export function FixedBottomButton({
  children,
  onClick,
  loading,
  disabled,
  icon,
}: FixedBottomButtonProps) {
  return (
    <div className="fixed bottom-0 left-0 right-0 max-w-md mx-auto bg-white border-t border-[var(--grey-200)] px-4 py-4 safe-area-pb">
      <Button
        className="w-full"
        size="lg"
        onClick={onClick}
        loading={loading}
        disabled={disabled}
        icon={icon}
      >
        {children}
      </Button>
    </div>
  );
}
