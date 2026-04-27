"use client";

import { useState, useEffect } from "react";
import { Brain, TrendingUp, TrendingDown, AlertCircle } from "lucide-react";

interface ActionMetrics {
  counts: {
    total: number;
    successful: number;
    failed: number;
    overridden: number;
    lowConfidence: number;
  };
  rates: {
    successRate: number;
    accuracyRate: number;
    avgConfidence: number;
  };
}

interface AiAccuracyCardProps {
  clientId: string;
}

export function AiAccuracyCard({ clientId }: AiAccuracyCardProps) {
  const [metrics, setMetrics] = useState<ActionMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchMetrics() {
      try {
        const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const response = await fetch(
          `${API_URL}/api/v1/actions/clients/${clientId}/metrics?days=30`,
          { credentials: "include" }
        );

        if (!response.ok) {
          throw new Error("Failed to fetch metrics");
        }

        const data = await response.json();
        setMetrics(data);
      } catch (err) {
        console.error("Error fetching AI metrics:", err);
        setError("Unable to load AI metrics");
      } finally {
        setLoading(false);
      }
    }

    if (clientId) {
      fetchMetrics();
    }
  }, [clientId]);

  if (loading) {
    return (
      <div className="bg-white rounded-2xl border border-[var(--grey-200)] p-5 animate-pulse">
        <div className="h-5 bg-[var(--grey-100)] rounded w-24 mb-4" />
        <div className="h-10 bg-[var(--grey-100)] rounded w-20 mb-4" />
        <div className="space-y-2">
          <div className="h-4 bg-[var(--grey-100)] rounded w-full" />
          <div className="h-4 bg-[var(--grey-100)] rounded w-full" />
          <div className="h-4 bg-[var(--grey-100)] rounded w-3/4" />
        </div>
      </div>
    );
  }

  if (error || !metrics) {
    return (
      <div className="bg-white rounded-2xl border border-[var(--grey-200)] p-5">
        <div className="flex items-center gap-2 text-[var(--grey-500)]">
          <AlertCircle className="w-5 h-5" />
          <span className="text-sm">AI metrics unavailable</span>
        </div>
      </div>
    );
  }

  const accuracyPercent = Math.round(metrics.rates.accuracyRate * 100);
  const confidencePercent = Math.round(metrics.rates.avgConfidence * 100);
  const successPercent = Math.round(metrics.rates.successRate * 100);

  const getAccuracyColor = (rate: number) => {
    if (rate >= 0.95) return "text-green-600";
    if (rate >= 0.85) return "text-amber-600";
    return "text-red-600";
  };

  const getAccuracyBgColor = (rate: number) => {
    if (rate >= 0.95) return "bg-green-50";
    if (rate >= 0.85) return "bg-amber-50";
    return "bg-red-50";
  };

  const getTrend = () => {
    if (metrics.rates.accuracyRate >= 0.95) {
      return { icon: TrendingUp, color: "text-green-600", label: "Excellent" };
    }
    if (metrics.rates.accuracyRate >= 0.85) {
      return { icon: TrendingUp, color: "text-amber-600", label: "Good" };
    }
    return { icon: TrendingDown, color: "text-red-600", label: "Needs attention" };
  };

  const trend = getTrend();
  const TrendIcon = trend.icon;

  return (
    <div className="bg-white rounded-2xl border border-[var(--grey-200)] p-5">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-purple-100 flex items-center justify-center">
            <Brain className="w-4 h-4 text-purple-600" />
          </div>
          <h3 className="text-base font-semibold text-[var(--grey-900)]">AI Accuracy</h3>
        </div>
        <span className="text-xs text-[var(--grey-500)]">Last 30 days</span>
      </div>

      <div className="flex items-baseline gap-2 mb-4">
        <span className={`text-3xl font-bold ${getAccuracyColor(metrics.rates.accuracyRate)}`}>
          {accuracyPercent}%
        </span>
        <div className="flex items-center gap-1">
          <TrendIcon className={`w-4 h-4 ${trend.color}`} />
          <span className={`text-sm ${trend.color}`}>{trend.label}</span>
        </div>
      </div>

      <div className="space-y-3">
        <div className="flex justify-between items-center text-sm">
          <span className="text-[var(--grey-600)]">Actions taken</span>
          <span className="font-medium text-[var(--grey-900)]">{metrics.counts.total}</span>
        </div>

        <div className="flex justify-between items-center text-sm">
          <span className="text-[var(--grey-600)]">Success rate</span>
          <span className="font-medium text-[var(--grey-900)]">{successPercent}%</span>
        </div>

        <div className="flex justify-between items-center text-sm">
          <span className="text-[var(--grey-600)]">Overridden by you</span>
          <span className={`font-medium ${metrics.counts.overridden > 0 ? "text-amber-600" : "text-[var(--grey-900)]"}`}>
            {metrics.counts.overridden}
          </span>
        </div>

        <div className="flex justify-between items-center text-sm">
          <span className="text-[var(--grey-600)]">Avg confidence</span>
          <span className="font-medium text-[var(--grey-900)]">{confidencePercent}%</span>
        </div>

        {metrics.counts.lowConfidence > 0 && (
          <div className="flex justify-between items-center text-sm">
            <span className="text-[var(--grey-600)]">Low confidence</span>
            <span className="font-medium text-[var(--grey-500)]">{metrics.counts.lowConfidence}</span>
          </div>
        )}
      </div>

      {metrics.counts.overridden > 5 && (
        <div className={`mt-4 p-3 rounded-lg ${getAccuracyBgColor(metrics.rates.accuracyRate)}`}>
          <p className="text-xs text-[var(--grey-700)]">
            {metrics.counts.overridden} actions were corrected. We're learning from your feedback
            to improve accuracy.
          </p>
        </div>
      )}

      {metrics.counts.total === 0 && (
        <div className="mt-4 p-3 rounded-lg bg-[var(--grey-50)]">
          <p className="text-xs text-[var(--grey-600)]">
            No AI actions recorded yet. As Covered AI handles calls and sends communications,
            you'll see accuracy metrics here.
          </p>
        </div>
      )}
    </div>
  );
}
