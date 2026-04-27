"use client";

import React, { useState, useCallback, useRef } from "react";
import { RefreshCw } from "lucide-react";
import { cn } from "@/lib/utils";

interface PullToRefreshProps {
  onRefresh: () => Promise<void>;
  children: React.ReactNode;
  className?: string;
}

export function PullToRefresh({ onRefresh, children, className }: PullToRefreshProps) {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [pullProgress, setPullProgress] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);
  const startY = useRef(0);
  const isPulling = useRef(false);

  const THRESHOLD = 80;

  const handleTouchStart = useCallback((e: React.TouchEvent) => {
    if (containerRef.current?.scrollTop === 0) {
      startY.current = e.touches[0].clientY;
      isPulling.current = true;
    }
  }, []);

  const handleTouchMove = useCallback((e: React.TouchEvent) => {
    if (!isPulling.current || isRefreshing) return;

    const currentY = e.touches[0].clientY;
    const diff = currentY - startY.current;

    if (diff > 0) {
      // Calculate progress (0 to 1)
      const progress = Math.min(diff / THRESHOLD, 1);
      setPullProgress(progress);
    }
  }, [isRefreshing]);

  const handleTouchEnd = useCallback(async () => {
    if (!isPulling.current) return;

    if (pullProgress >= 1 && !isRefreshing) {
      setIsRefreshing(true);
      try {
        await onRefresh();
      } finally {
        setIsRefreshing(false);
      }
    }

    isPulling.current = false;
    setPullProgress(0);
  }, [pullProgress, isRefreshing, onRefresh]);

  return (
    <div
      ref={containerRef}
      className={cn("overflow-y-auto", className)}
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
    >
      {/* Pull indicator */}
      <div
        className={cn(
          "flex items-center justify-center transition-all duration-200",
          pullProgress > 0 || isRefreshing ? "py-4" : "py-0 h-0"
        )}
        style={{
          height: isRefreshing ? 48 : pullProgress * 48,
          opacity: pullProgress,
        }}
      >
        <RefreshCw
          className={cn(
            "w-5 h-5 text-[var(--brand-primary)] transition-transform",
            isRefreshing && "animate-spin"
          )}
          style={{
            transform: `rotate(${pullProgress * 180}deg)`,
          }}
        />
      </div>

      {children}
    </div>
  );
}
