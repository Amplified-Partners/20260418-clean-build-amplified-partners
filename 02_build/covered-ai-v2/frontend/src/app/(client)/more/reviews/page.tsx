/**
 * Client App - Reviews Page
 * 
 * Your reputation at a glance.
 * Recent reviews, stats, and review request status.
 */

"use client";

import React from "react";
import { useRouter } from "next/navigation";
import { Star, TrendingUp, Send } from "lucide-react";
import { Header, SectionDivider, EmptyState } from "@/components/client-app";

// Mock data
const mockData = {
  stats: {
    averageRating: 4.8,
    totalReviews: 47,
    thisMonth: 5,
    pending: 3,
  },
  recentReviews: [
    {
      id: "1",
      customerName: "Mrs Thompson",
      rating: 5,
      text: "Fantastic service, arrived within the hour. Fixed the leak quickly and cleaned up after. Highly recommend!",
      date: "2 days ago",
      source: "Google",
    },
    {
      id: "2",
      customerName: "Dave Wilson",
      rating: 5,
      text: "Emergency boiler repair on a Sunday. Can't thank them enough.",
      date: "1 week ago",
      source: "Google",
    },
    {
      id: "3",
      customerName: "Sarah Jones",
      rating: 4,
      text: "Good work, just took a bit longer than expected.",
      date: "2 weeks ago",
      source: "Google",
    },
  ],
  pendingRequests: [
    { id: "1", customerName: "Mr Abbas", sentDate: "Today", job: "Boiler service" },
    { id: "2", customerName: "Mrs Lee", sentDate: "Yesterday", job: "Tap repair" },
    { id: "3", customerName: "Johnson family", sentDate: "3 days ago", job: "Bathroom renovation" },
  ],
};

function StarRating({ rating }: { rating: number }) {
  return (
    <div className="flex gap-0.5">
      {[1, 2, 3, 4, 5].map((star) => (
        <Star
          key={star}
          className={`w-4 h-4 ${
            star <= rating ? "fill-yellow-400 text-yellow-400" : "text-neutral-200"
          }`}
        />
      ))}
    </div>
  );
}

export default function ReviewsPage() {
  const router = useRouter();
  
  return (
    <div className="min-h-screen bg-neutral-50">
      <Header
        title="Reviews"
        showBack
        onBack={() => router.back()}
      />
      
      {/* Stats */}
      <div className="px-5 py-6 bg-white border-b border-neutral-200">
        <div className="flex items-center gap-4">
          <div className="text-center">
            <div className="flex items-center justify-center gap-1">
              <span className="text-4xl font-bold text-neutral-900">
                {mockData.stats.averageRating}
              </span>
              <Star className="w-8 h-8 fill-yellow-400 text-yellow-400" />
            </div>
            <p className="text-sm text-neutral-500 mt-1">
              {mockData.stats.totalReviews} reviews
            </p>
          </div>
          <div className="flex-1 grid grid-cols-2 gap-4 ml-4 pl-4 border-l border-neutral-200">
            <div>
              <p className="text-2xl font-semibold text-neutral-900">
                {mockData.stats.thisMonth}
              </p>
              <p className="text-xs text-neutral-500">This month</p>
            </div>
            <div>
              <p className="text-2xl font-semibold text-amber-600">
                {mockData.stats.pending}
              </p>
              <p className="text-xs text-neutral-500">Pending</p>
            </div>
          </div>
        </div>
      </div>
      
      {/* Recent Reviews */}
      <SectionDivider title="Recent reviews" />
      
      {mockData.recentReviews.length === 0 ? (
        <EmptyState
          icon="⭐"
          title="No reviews yet"
          description="Reviews will appear here as customers leave them."
        />
      ) : (
        <div className="bg-white mx-5 rounded-2xl border border-neutral-200 overflow-hidden">
          {mockData.recentReviews.map((review, i) => (
            <React.Fragment key={review.id}>
              <div className="p-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <StarRating rating={review.rating} />
                    <span className="text-xs text-neutral-400">{review.source}</span>
                  </div>
                  <span className="text-xs text-neutral-400">{review.date}</span>
                </div>
                <p className="text-neutral-700 text-sm">{review.text}</p>
                <p className="text-sm font-medium text-neutral-900 mt-2">
                  — {review.customerName}
                </p>
              </div>
              {i < mockData.recentReviews.length - 1 && (
                <div className="h-px bg-neutral-100 mx-4" />
              )}
            </React.Fragment>
          ))}
        </div>
      )}
      
      {/* Pending Requests */}
      <SectionDivider title="Awaiting response" />
      
      {mockData.pendingRequests.length === 0 ? (
        <div className="mx-5 p-4 bg-green-50 rounded-xl text-center">
          <p className="text-green-700">All review requests responded to! 🎉</p>
        </div>
      ) : (
        <div className="bg-white mx-5 rounded-2xl border border-neutral-200 overflow-hidden">
          {mockData.pendingRequests.map((request, i) => (
            <React.Fragment key={request.id}>
              <div className="p-4 flex items-center justify-between">
                <div>
                  <p className="font-medium text-neutral-900">{request.customerName}</p>
                  <p className="text-sm text-neutral-500">
                    {request.job} • Sent {request.sentDate}
                  </p>
                </div>
                <div className="flex items-center gap-1 text-amber-600">
                  <Send className="w-4 h-4" />
                  <span className="text-xs">Pending</span>
                </div>
              </div>
              {i < mockData.pendingRequests.length - 1 && (
                <div className="h-px bg-neutral-100 mx-4" />
              )}
            </React.Fragment>
          ))}
        </div>
      )}
      
      {/* View on Google button */}
      <div className="mx-5 mt-6 mb-8">
        <a
          href="https://business.google.com"
          target="_blank"
          rel="noopener noreferrer"
          className="block w-full py-3 text-center text-blue-600 font-medium bg-blue-50 rounded-xl hover:bg-blue-100 transition-colors"
        >
          View on Google Business
        </a>
      </div>
    </div>
  );
}
