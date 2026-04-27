"use client";

import React, { useState } from "react";
import { Star, ExternalLink, TrendingUp, Clock, MessageCircle } from "lucide-react";
import { Header } from "@/components/layout";
import { FilterTabs, EmptyState } from "@/components/ui";
import { useAuthContext } from "@/lib/auth-context";
import { useReviews, useReviewStats } from "@/lib/hooks";
import { cn } from "@/lib/utils";

const filterTabs = [
  { id: "all", label: "All" },
  { id: "google", label: "Google" },
  { id: "trustpilot", label: "Trustpilot" },
  { id: "pending", label: "Awaiting" },
];

function ReviewsSkeleton() {
  return (
    <div className="px-4 py-6 space-y-4 animate-pulse">
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
        <div className="grid grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="text-center">
              <div className="h-8 bg-[var(--grey-200)] rounded w-16 mx-auto mb-2" />
              <div className="h-4 bg-[var(--grey-100)] rounded w-12 mx-auto" />
            </div>
          ))}
        </div>
      </div>
      {[1, 2, 3].map((i) => (
        <div key={i} className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
          <div className="h-5 bg-[var(--grey-200)] rounded w-1/3 mb-2" />
          <div className="h-4 bg-[var(--grey-100)] rounded w-full mb-2" />
          <div className="h-4 bg-[var(--grey-100)] rounded w-2/3" />
        </div>
      ))}
    </div>
  );
}

function StarRating({ rating }: { rating: number }) {
  return (
    <div className="flex gap-0.5">
      {[1, 2, 3, 4, 5].map((star) => (
        <Star
          key={star}
          className={cn(
            "w-4 h-4",
            star <= rating ? "fill-amber-400 text-amber-400" : "fill-none text-[var(--grey-300)]"
          )}
        />
      ))}
    </div>
  );
}

export default function ReviewsPage() {
  const { client } = useAuthContext();
  const [activeFilter, setActiveFilter] = useState("all");

  // Convert filter to API params
  const filterParams = activeFilter === "all"
    ? undefined
    : activeFilter === "pending"
      ? { rating_min: 0, rating_max: 0 } // pending reviews have rating 0
      : { platform: activeFilter };

  const { data: reviewsData, isLoading, error } = useReviews(client?.id || null, filterParams);
  const { data: statsData } = useReviewStats(client?.id || null);

  const reviews = reviewsData?.reviews || [];
  const stats = {
    averageRating: statsData?.average_rating || 0,
    totalReviews: statsData?.total_reviews || 0,
    pendingRequests: statsData?.jobs_needing_reviews || 0,
    responseRate: (statsData?.five_star_period || 0) / Math.max(statsData?.period_reviews || 1, 1),
  };

  if (isLoading) {
    return (
      <>
        <Header title="Reviews" />
        <main className="pb-24">
          <div className="pt-4">
            <FilterTabs tabs={filterTabs} activeTab={activeFilter} onChange={setActiveFilter} />
          </div>
          <ReviewsSkeleton />
        </main>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Header title="Reviews" />
        <main className="pb-24 px-4 pt-6">
          <div className="bg-red-50 rounded-xl border border-red-200 p-4 text-center">
            <p className="text-red-700">Failed to load reviews</p>
          </div>
        </main>
      </>
    );
  }

  return (
    <>
      <Header title="Reviews" />
      <main className="pb-24">
        <div className="pt-4">
          <FilterTabs tabs={filterTabs} activeTab={activeFilter} onChange={setActiveFilter} />
        </div>

        {/* Stats */}
        <div className="px-4 py-4">
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
            <div className="grid grid-cols-4 gap-2">
              <div className="text-center">
                <div className="flex items-center justify-center gap-1 mb-1">
                  <Star className="w-5 h-5 fill-amber-400 text-amber-400" />
                  <span className="text-2xl font-bold text-[var(--grey-900)]">
                    {stats.averageRating.toFixed(1)}
                  </span>
                </div>
                <p className="text-xs text-[var(--grey-500)]">Avg rating</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-[var(--grey-900)]">{stats.totalReviews}</p>
                <p className="text-xs text-[var(--grey-500)]">Total</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-[var(--grey-900)]">{stats.pendingRequests}</p>
                <p className="text-xs text-[var(--grey-500)]">Pending</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-[var(--grey-900)]">
                  {Math.round(stats.responseRate * 100)}%
                </p>
                <p className="text-xs text-[var(--grey-500)]">Response</p>
              </div>
            </div>
          </div>
        </div>

        {/* Google Rating Card */}
        {client?.googlePlaceId && (
          <div className="px-4 mb-4">
            <a
              href={`https://search.google.com/local/reviews?placeid=${client.googlePlaceId}`}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-white rounded-xl border border-[var(--grey-200)] p-4 flex items-center justify-between hover:bg-[var(--grey-50)] transition-colors block"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-[#4285F4] rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-lg">G</span>
                </div>
                <div>
                  <p className="font-medium text-[var(--grey-900)]">Google Business Profile</p>
                  <p className="text-sm text-[var(--grey-500)]">View all reviews on Google</p>
                </div>
              </div>
              <ExternalLink className="w-5 h-5 text-[var(--grey-400)]" />
            </a>
          </div>
        )}

        {/* Reviews List */}
        {reviews.length === 0 && activeFilter === "all" ? (
          <EmptyState
            icon="⭐"
            title="No reviews yet"
            description="Reviews from your customers will appear here."
          />
        ) : reviews.length === 0 ? (
          <div className="px-4">
            <div className="bg-white rounded-xl border border-[var(--grey-200)] p-6 text-center">
              <p className="text-[var(--grey-500)]">No reviews match this filter</p>
            </div>
          </div>
        ) : (
          <div className="px-4 space-y-3">
            {reviews.map((review) => {
              const isPending = review.rating === 0;
              const formattedDate = review.created_at
                ? new Date(review.created_at).toLocaleDateString()
                : "";

              return (
                <div
                  key={review.id}
                  className="bg-white rounded-xl border border-[var(--grey-200)] p-4"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <p className="font-medium text-[var(--grey-900)]">
                        {review.reviewer_name || "Customer"}
                      </p>
                      <div className="flex items-center gap-2 mt-1">
                        {!isPending && <StarRating rating={review.rating} />}
                        <span className="text-xs text-[var(--grey-500)] capitalize">
                          {review.platform}
                        </span>
                      </div>
                    </div>
                    <span className="text-xs text-[var(--grey-500)]">{formattedDate}</span>
                  </div>
                  {review.review_text && (
                    <p className="text-sm text-[var(--grey-700)] mt-3">{review.review_text}</p>
                  )}
                  {review.response_text && (
                    <div className="mt-3 pl-3 border-l-2 border-[var(--brand-primary-light)]">
                      <p className="text-xs font-medium text-[var(--grey-500)] mb-1">Your reply</p>
                      <p className="text-sm text-[var(--grey-600)]">{review.response_text}</p>
                    </div>
                  )}
                  {!review.response_text && !isPending && (
                    <button className="mt-3 text-sm text-[var(--brand-primary)] font-medium flex items-center gap-1">
                      <MessageCircle className="w-4 h-4" />
                      Reply
                    </button>
                  )}
                  {isPending && (
                    <div className="mt-3 flex items-center gap-2 text-amber-600">
                      <Clock className="w-4 h-4" />
                      <span className="text-xs font-medium">Awaiting review</span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {/* Review Request Tips */}
        <div className="px-4 py-6">
          <div className="bg-[var(--brand-primary-light)] rounded-xl p-4">
            <div className="flex items-start gap-3">
              <TrendingUp className="w-5 h-5 text-[var(--brand-primary)] mt-0.5" />
              <div>
                <p className="font-medium text-[var(--grey-900)]">Boost your reviews</p>
                <p className="text-sm text-[var(--grey-600)] mt-1">
                  Review requests are automatically sent 2 hours after completing a job. Your
                  current conversion rate is {Math.round(stats.responseRate * 100)}%.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </>
  );
}
