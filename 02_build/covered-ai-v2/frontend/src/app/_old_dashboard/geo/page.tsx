"use client";

import React, { useState } from "react";
import {
  MapPin,
  TrendingUp,
  TrendingDown,
  Search,
  Target,
  Globe,
  ArrowRight,
  CheckCircle,
  AlertCircle,
  Info,
} from "lucide-react";
import { Header } from "@/components/layout";
import { Button, FilterTabs } from "@/components/ui";
import { useAuthContext } from "@/lib/auth-context";
import { useGeoEngine } from "@/lib/hooks";
import { cn } from "@/lib/utils";

const filterTabs = [
  { id: "overview", label: "Overview" },
  { id: "rankings", label: "Rankings" },
  { id: "competitors", label: "Competitors" },
  { id: "opportunities", label: "Opportunities" },
];

function GeoSkeleton() {
  return (
    <div className="px-4 py-6 space-y-6 animate-pulse">
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
        <div className="h-8 bg-[var(--grey-200)] rounded w-1/3 mb-4" />
        <div className="grid grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-16 bg-[var(--grey-100)] rounded" />
          ))}
        </div>
      </div>
      {[1, 2].map((i) => (
        <div key={i} className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
          <div className="h-6 bg-[var(--grey-200)] rounded w-1/4 mb-3" />
          <div className="space-y-3">
            {[1, 2, 3].map((j) => (
              <div key={j} className="h-12 bg-[var(--grey-100)] rounded" />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

interface RankingItemProps {
  keyword: string;
  position: number;
  previousPosition?: number;
  searchVolume?: number;
}

function RankingItem({ keyword, position, previousPosition, searchVolume }: RankingItemProps) {
  const change = previousPosition ? previousPosition - position : 0;
  const isImproved = change > 0;
  const isDeclined = change < 0;

  return (
    <div className="flex items-center gap-3 px-4 py-3">
      <div
        className={cn(
          "w-10 h-10 rounded-lg flex items-center justify-center text-sm font-bold",
          position <= 3
            ? "bg-green-100 text-green-700"
            : position <= 10
            ? "bg-amber-100 text-amber-700"
            : "bg-[var(--grey-100)] text-[var(--grey-600)]"
        )}
      >
        #{position}
      </div>
      <div className="flex-1 min-w-0">
        <p className="font-medium text-[var(--grey-900)] truncate">{keyword}</p>
        {searchVolume && (
          <p className="text-xs text-[var(--grey-500)]">{searchVolume.toLocaleString()} searches/mo</p>
        )}
      </div>
      {change !== 0 && (
        <div
          className={cn(
            "flex items-center gap-1 text-sm font-medium",
            isImproved ? "text-green-600" : "text-red-600"
          )}
        >
          {isImproved ? (
            <TrendingUp className="w-4 h-4" />
          ) : (
            <TrendingDown className="w-4 h-4" />
          )}
          <span>{Math.abs(change)}</span>
        </div>
      )}
    </div>
  );
}

interface CompetitorCardProps {
  name: string;
  avgPosition: number;
  reviewCount: number;
  rating: number;
}

function CompetitorCard({ name, avgPosition, reviewCount, rating }: CompetitorCardProps) {
  return (
    <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
      <div className="flex items-start justify-between mb-3">
        <div>
          <p className="font-medium text-[var(--grey-900)]">{name}</p>
          <div className="flex items-center gap-2 mt-1">
            <span className="text-sm text-amber-500">★ {rating.toFixed(1)}</span>
            <span className="text-xs text-[var(--grey-500)]">({reviewCount} reviews)</span>
          </div>
        </div>
        <div className="text-right">
          <p className="text-sm text-[var(--grey-500)]">Avg position</p>
          <p className="font-bold text-[var(--grey-900)]">#{avgPosition.toFixed(1)}</p>
        </div>
      </div>
    </div>
  );
}

interface OpportunityCardProps {
  title: string;
  description: string;
  impact: "high" | "medium" | "low";
  action: string;
}

function OpportunityCard({ title, description, impact, action }: OpportunityCardProps) {
  const impactColors = {
    high: "bg-green-100 text-green-700",
    medium: "bg-amber-100 text-amber-700",
    low: "bg-[var(--grey-100)] text-[var(--grey-600)]",
  };

  return (
    <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
      <div className="flex items-start gap-3">
        <Target className="w-5 h-5 text-[var(--brand-primary)] mt-0.5" />
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <p className="font-medium text-[var(--grey-900)]">{title}</p>
            <span className={cn("px-2 py-0.5 text-xs font-medium rounded-full", impactColors[impact])}>
              {impact} impact
            </span>
          </div>
          <p className="text-sm text-[var(--grey-600)] mb-3">{description}</p>
          <Button variant="secondary" size="sm">
            {action}
            <ArrowRight className="w-4 h-4 ml-1" />
          </Button>
        </div>
      </div>
    </div>
  );
}

export default function GeoEnginePage() {
  const { client } = useAuthContext();
  const [activeTab, setActiveTab] = useState("overview");
  const { data, isLoading, error } = useGeoEngine(client?.id || null);

  if (isLoading) {
    return (
      <>
        <Header title="GEO Engine" />
        <main className="pb-24">
          <div className="pt-4">
            <FilterTabs tabs={filterTabs} activeTab={activeTab} onChange={setActiveTab} />
          </div>
          <GeoSkeleton />
        </main>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Header title="GEO Engine" />
        <main className="pb-24 px-4 pt-6">
          <div className="bg-red-50 rounded-xl border border-red-200 p-4 text-center">
            <p className="text-red-700">Failed to load GEO Engine data</p>
          </div>
        </main>
      </>
    );
  }

  const geoData = data || {
    overview: {
      avgPosition: 0,
      positionChange: 0,
      trackedKeywords: 0,
      top3Keywords: 0,
      visibilityScore: 0,
    },
    rankings: [],
    competitors: [],
    opportunities: [],
  };

  const renderOverview = () => (
    <div className="px-4 py-6 space-y-6">
      {/* Visibility Score */}
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
        <h3 className="text-sm font-medium text-[var(--grey-500)] mb-3">LOCAL VISIBILITY SCORE</h3>
        <div className="flex items-center gap-4">
          <div
            className={cn(
              "w-20 h-20 rounded-full flex items-center justify-center border-4",
              geoData.overview.visibilityScore >= 70
                ? "border-green-500 bg-green-50"
                : geoData.overview.visibilityScore >= 40
                ? "border-amber-500 bg-amber-50"
                : "border-red-500 bg-red-50"
            )}
          >
            <span className="text-2xl font-bold text-[var(--grey-900)]">
              {geoData.overview.visibilityScore}
            </span>
          </div>
          <div className="flex-1">
            <p className="text-sm text-[var(--grey-600)]">
              Your local visibility score measures how easily customers can find you in local
              searches.
            </p>
            {geoData.overview.visibilityScore < 70 && (
              <p className="text-sm text-amber-600 mt-2 flex items-center gap-1">
                <AlertCircle className="w-4 h-4" />
                Room for improvement
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-3 gap-3">
        <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 text-center">
          <div className="flex items-center justify-center gap-1 mb-1">
            <span className="text-2xl font-bold text-[var(--grey-900)]">
              #{geoData.overview.avgPosition.toFixed(1)}
            </span>
            {geoData.overview.positionChange !== 0 && (
              <span
                className={cn(
                  "text-xs font-medium",
                  geoData.overview.positionChange > 0 ? "text-green-600" : "text-red-600"
                )}
              >
                {geoData.overview.positionChange > 0 ? "↑" : "↓"}
                {Math.abs(geoData.overview.positionChange)}
              </span>
            )}
          </div>
          <p className="text-xs text-[var(--grey-500)]">Avg Position</p>
        </div>
        <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 text-center">
          <p className="text-2xl font-bold text-[var(--grey-900)]">
            {geoData.overview.trackedKeywords}
          </p>
          <p className="text-xs text-[var(--grey-500)]">Keywords</p>
        </div>
        <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 text-center">
          <p className="text-2xl font-bold text-green-600">{geoData.overview.top3Keywords}</p>
          <p className="text-xs text-[var(--grey-500)]">In Top 3</p>
        </div>
      </div>

      {/* Top Rankings Preview */}
      {geoData.rankings.length > 0 && (
        <div className="bg-white rounded-xl border border-[var(--grey-200)]">
          <div className="px-4 py-3 border-b border-[var(--grey-100)] flex items-center justify-between">
            <h3 className="font-medium text-[var(--grey-900)]">Top Rankings</h3>
            <button
              onClick={() => setActiveTab("rankings")}
              className="text-sm text-[var(--brand-primary)] font-medium"
            >
              See all
            </button>
          </div>
          <div className="divide-y divide-[var(--grey-100)]">
            {geoData.rankings.slice(0, 3).map((ranking, index) => (
              <RankingItem key={index} {...ranking} />
            ))}
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="bg-[var(--brand-primary-light)] rounded-xl p-4">
        <div className="flex items-start gap-3">
          <Info className="w-5 h-5 text-[var(--brand-primary)] mt-0.5" />
          <div>
            <p className="font-medium text-[var(--grey-900)]">Boost your visibility</p>
            <p className="text-sm text-[var(--grey-600)] mt-1">
              Get more reviews, respond to them, and keep your Google Business Profile updated to
              improve your local rankings.
            </p>
          </div>
        </div>
      </div>
    </div>
  );

  const renderRankings = () => (
    <div className="px-4 py-6 space-y-4">
      {geoData.rankings.length === 0 ? (
        <div className="bg-white rounded-xl border border-[var(--grey-200)] p-6 text-center">
          <Search className="w-12 h-12 text-[var(--grey-300)] mx-auto mb-3" />
          <p className="font-medium text-[var(--grey-900)]">No rankings tracked yet</p>
          <p className="text-sm text-[var(--grey-500)] mt-1">
            We'll start tracking your local search rankings automatically.
          </p>
        </div>
      ) : (
        <div className="bg-white rounded-xl border border-[var(--grey-200)] divide-y divide-[var(--grey-100)]">
          {geoData.rankings.map((ranking, index) => (
            <RankingItem key={index} {...ranking} />
          ))}
        </div>
      )}
    </div>
  );

  const renderCompetitors = () => (
    <div className="px-4 py-6 space-y-4">
      {geoData.competitors.length === 0 ? (
        <div className="bg-white rounded-xl border border-[var(--grey-200)] p-6 text-center">
          <Globe className="w-12 h-12 text-[var(--grey-300)] mx-auto mb-3" />
          <p className="font-medium text-[var(--grey-900)]">Competitor analysis coming soon</p>
          <p className="text-sm text-[var(--grey-500)] mt-1">
            We're analyzing your local competitors.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {geoData.competitors.map((competitor, index) => (
            <CompetitorCard key={index} {...competitor} />
          ))}
        </div>
      )}
    </div>
  );

  const renderOpportunities = () => (
    <div className="px-4 py-6 space-y-4">
      {geoData.opportunities.length === 0 ? (
        <div className="bg-white rounded-xl border border-[var(--grey-200)] p-6 text-center">
          <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-3" />
          <p className="font-medium text-[var(--grey-900)]">You're doing great!</p>
          <p className="text-sm text-[var(--grey-500)] mt-1">
            No new opportunities identified at this time.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {geoData.opportunities.map((opportunity, index) => (
            <OpportunityCard key={index} {...opportunity} />
          ))}
        </div>
      )}
    </div>
  );

  return (
    <>
      <Header title="GEO Engine" />
      <main className="pb-24">
        <div className="pt-4">
          <FilterTabs tabs={filterTabs} activeTab={activeTab} onChange={setActiveTab} />
        </div>

        {activeTab === "overview" && renderOverview()}
        {activeTab === "rankings" && renderRankings()}
        {activeTab === "competitors" && renderCompetitors()}
        {activeTab === "opportunities" && renderOpportunities()}
      </main>
    </>
  );
}
