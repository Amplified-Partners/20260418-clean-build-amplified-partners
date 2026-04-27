'use client';

import { useState, useEffect } from 'react';
import { CheckCircle, Circle, ChevronRight, Play } from 'lucide-react';
import Link from 'next/link';

interface ChecklistItem {
  id: string;
  label: string;
  done: boolean;
  action?: string;
  videoId?: string;
}

interface OnboardingChecklistProps {
  clientId: string;
  onVideoClick?: (videoId: string) => void;
}

export function OnboardingChecklist({ clientId, onVideoClick }: OnboardingChecklistProps) {
  const [items, setItems] = useState<ChecklistItem[]>([]);
  const [completionPercent, setCompletionPercent] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProgress();
  }, [clientId]);

  const fetchProgress = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/onboarding/progress/${clientId}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
      });
      const data = await res.json();
      setItems(data.checklist);
      setCompletionPercent(data.completionPercent);
    } catch (error) {
      console.error('Error fetching onboarding progress:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-2xl p-5 border border-gray-200 animate-pulse">
        <div className="h-6 bg-gray-100 rounded w-1/3 mb-4"></div>
        <div className="h-2 bg-gray-100 rounded-full mb-5"></div>
        <div className="space-y-3">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="h-12 bg-gray-50 rounded-xl"></div>
          ))}
        </div>
      </div>
    );
  }

  if (completionPercent >= 100) {
    return null; // Hide when complete
  }

  // Endowed progress: show slightly more than actual
  const displayPercent = Math.min(completionPercent + 5, 100);

  return (
    <div className="bg-white rounded-2xl p-5 border border-gray-200">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-base font-semibold text-gray-900">
          Getting Started
        </h3>
        <span className="text-sm text-gray-500">
          {completionPercent}% complete
        </span>
      </div>

      {/* Progress bar with animation */}
      <div className="h-2 bg-gray-100 rounded-full mb-5 overflow-hidden">
        <div
          className="h-full bg-green-500 rounded-full transition-all duration-1000 ease-out"
          style={{ width: `${displayPercent}%` }}
        />
      </div>

      <div className="space-y-3">
        {items.map((item) => (
          <div key={item.id}>
            {item.done ? (
              <div className="flex items-center gap-3 p-3 rounded-xl bg-green-50">
                <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                <span className="flex-1 text-sm text-gray-500 line-through">
                  {item.label}
                </span>
              </div>
            ) : item.action ? (
              <Link
                href={item.action}
                className="w-full flex items-center gap-3 p-3 rounded-xl bg-gray-50 hover:bg-gray-100 transition-all duration-200"
              >
                <Circle className="w-5 h-5 text-gray-300 flex-shrink-0" />
                <span className="flex-1 text-left text-sm text-gray-900">
                  {item.label}
                </span>
                {item.videoId && onVideoClick && (
                  <button
                    onClick={(e) => {
                      e.preventDefault();
                      onVideoClick(item.videoId!);
                    }}
                    className="p-1 hover:bg-gray-200 rounded"
                  >
                    <Play className="w-4 h-4 text-gray-400" />
                  </button>
                )}
                <ChevronRight className="w-4 h-4 text-gray-400" />
              </Link>
            ) : (
              <div className="flex items-center gap-3 p-3 rounded-xl bg-gray-50">
                <Circle className="w-5 h-5 text-gray-300 flex-shrink-0" />
                <span className="flex-1 text-sm text-gray-900">
                  {item.label}
                </span>
              </div>
            )}
          </div>
        ))}
      </div>

      <p className="mt-4 text-xs text-gray-500 text-center">
        Complete setup to unlock all features
      </p>
    </div>
  );
}
