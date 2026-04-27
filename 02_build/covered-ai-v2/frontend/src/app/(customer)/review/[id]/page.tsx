/**
 * Customer App - Review Request Page
 * 
 * Simple review request with one-tap Google review.
 * Option for private feedback if unhappy.
 */

"use client";

import React, { useState } from "react";
import { Star, ThumbsUp, MessageSquare, CheckCircle } from "lucide-react";

// Mock data - in production, loaded from URL params or API
const mockRequest = {
  business: {
    name: "Titan Plumbing",
    googleReviewUrl: "https://g.page/r/YOUR_REVIEW_LINK",
    logo: null,
  },
  job: {
    date: "28th November 2024",
    description: "Emergency tap repair",
    engineer: "Ralph",
  },
  customer: {
    name: "Mrs Chen",
  },
};

export default function ReviewRequestPage() {
  const { business, job, customer } = mockRequest;
  const [rating, setRating] = useState<number | null>(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [feedback, setFeedback] = useState("");
  const [submitted, setSubmitted] = useState(false);
  
  const handleRating = (stars: number) => {
    setRating(stars);
    if (stars >= 4) {
      // Redirect to Google review
      window.open(business.googleReviewUrl, "_blank");
      setSubmitted(true);
    } else {
      // Show private feedback form
      setShowFeedback(true);
    }
  };
  
  const handleFeedbackSubmit = () => {
    // In production: send feedback to API
    setSubmitted(true);
  };
  
  if (submitted) {
    return (
      <div className="px-5 py-12 text-center">
        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <CheckCircle className="w-10 h-10 text-green-600" />
        </div>
        <h1 className="text-2xl font-bold text-neutral-900 mb-2">
          Thank You!
        </h1>
        <p className="text-neutral-600">
          {rating && rating >= 4 
            ? "We really appreciate you taking the time to leave a review."
            : "Your feedback helps us improve. We'll be in touch soon."
          }
        </p>
      </div>
    );
  }
  
  return (
    <div className="px-5 py-8">
      {/* Business header */}
      <div className="text-center mb-8">
        {business.logo ? (
          <img 
            src={business.logo} 
            alt={business.name}
            className="h-12 mx-auto mb-2"
          />
        ) : (
          <h1 className="text-xl font-bold text-neutral-900">{business.name}</h1>
        )}
      </div>
      
      {/* Main content */}
      {!showFeedback ? (
        <>
          {/* Question */}
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold text-neutral-900 mb-2">
              How did we do?
            </h2>
            <p className="text-neutral-600">
              Hi {customer.name.split(" ")[1] || customer.name}, we'd love to hear about your recent experience.
            </p>
            <p className="text-sm text-neutral-500 mt-2">
              {job.description} • {job.date}
            </p>
          </div>
          
          {/* Star rating */}
          <div className="flex justify-center gap-2 mb-8">
            {[1, 2, 3, 4, 5].map((star) => (
              <button
                key={star}
                onClick={() => handleRating(star)}
                className="p-2 transition-transform hover:scale-110"
              >
                <Star 
                  className={`w-12 h-12 ${
                    rating && star <= rating 
                      ? "fill-yellow-400 text-yellow-400" 
                      : "text-neutral-300"
                  }`}
                />
              </button>
            ))}
          </div>
          
          <p className="text-center text-sm text-neutral-500">
            Tap a star to rate your experience
          </p>
        </>
      ) : (
        <>
          {/* Private feedback form */}
          <div className="text-center mb-6">
            <div className="w-16 h-16 bg-amber-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <MessageSquare className="w-8 h-8 text-amber-600" />
            </div>
            <h2 className="text-xl font-bold text-neutral-900 mb-2">
              We're Sorry
            </h2>
            <p className="text-neutral-600">
              We'd like to make things right. Please tell us what went wrong.
            </p>
          </div>
          
          {/* Rating display */}
          <div className="flex justify-center gap-1 mb-6">
            {[1, 2, 3, 4, 5].map((star) => (
              <Star 
                key={star}
                className={`w-6 h-6 ${
                  rating && star <= rating 
                    ? "fill-yellow-400 text-yellow-400" 
                    : "text-neutral-200"
                }`}
              />
            ))}
          </div>
          
          {/* Feedback textarea */}
          <textarea
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            placeholder="Tell us what happened..."
            className="w-full p-4 border border-neutral-200 rounded-xl resize-none h-32 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          
          {/* Submit button */}
          <button
            onClick={handleFeedbackSubmit}
            disabled={!feedback.trim()}
            className="w-full mt-4 py-4 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 transition-colors disabled:bg-neutral-200 disabled:text-neutral-400"
          >
            Send Feedback
          </button>
          
          {/* Back button */}
          <button
            onClick={() => {
              setShowFeedback(false);
              setRating(null);
            }}
            className="w-full mt-3 py-3 text-neutral-500 text-sm"
          >
            Go back
          </button>
          
          <p className="text-center text-xs text-neutral-400 mt-4">
            This feedback is private and goes directly to {business.name}.
          </p>
        </>
      )}
    </div>
  );
}
