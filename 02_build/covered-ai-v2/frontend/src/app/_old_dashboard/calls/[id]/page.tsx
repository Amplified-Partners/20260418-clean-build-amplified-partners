"use client";

import React, { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Phone, MessageCircle, Briefcase, ChevronDown, ChevronUp } from "lucide-react";
import { Header } from "@/components/layout";
import { Button, FixedBottomButton } from "@/components/ui";
import { useAuthContext } from "@/lib/auth-context";
import { useCall } from "@/lib/hooks";
import { callsApi } from "@/lib/api";
import { cn } from "@/lib/utils";

// Loading skeleton
function CallDetailSkeleton() {
  return (
    <main className="px-4 py-6 space-y-6 pb-32 animate-pulse">
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
        <div className="h-6 bg-[var(--grey-200)] rounded w-1/2 mb-2" />
        <div className="h-4 bg-[var(--grey-100)] rounded w-1/3 mb-1" />
        <div className="h-4 bg-[var(--grey-100)] rounded w-2/3 mb-4" />
        <div className="flex gap-2">
          <div className="h-9 bg-[var(--grey-100)] rounded-lg w-20" />
          <div className="h-9 bg-[var(--grey-100)] rounded-lg w-24" />
          <div className="h-9 bg-[var(--grey-100)] rounded-lg w-24" />
        </div>
      </div>
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
        <div className="h-20 bg-[var(--grey-100)] rounded" />
      </div>
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-3">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="flex justify-between">
            <div className="h-4 bg-[var(--grey-100)] rounded w-1/4" />
            <div className="h-4 bg-[var(--grey-200)] rounded w-1/3" />
          </div>
        ))}
      </div>
    </main>
  );
}

export default function CallDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { client } = useAuthContext();
  const callId = params.id as string;
  const { data: call, isLoading, error, refetch } = useCall(client?.id || null, callId);

  const [transcriptExpanded, setTranscriptExpanded] = useState(false);
  const [isMarkingComplete, setIsMarkingComplete] = useState(false);

  const handleMarkCallbackComplete = async () => {
    if (!client?.id || !callId) return;
    setIsMarkingComplete(true);
    try {
      await callsApi.markCallbackComplete(client.id, callId);
      await refetch();
    } catch (err) {
      console.error("Failed to mark callback complete:", err);
    } finally {
      setIsMarkingComplete(false);
    }
  };

  const handleCreateJob = () => {
    router.push(`/dashboard/jobs/new?callId=${callId}`);
  };

  if (isLoading) {
    return (
      <>
        <Header backButton title="Call Details" />
        <CallDetailSkeleton />
      </>
    );
  }

  if (error || !call) {
    return (
      <>
        <Header backButton title="Call Details" />
        <main className="px-4 py-6 pb-32">
          <div className="bg-red-50 rounded-xl border border-red-200 p-4 text-center">
            <p className="text-red-700">Failed to load call details</p>
          </div>
        </main>
      </>
    );
  }

  return (
    <>
      <Header backButton title="Call Details" />
      <main className="px-4 py-6 space-y-6 pb-32">
        {/* Contact Card */}
        <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
          <h2 className="text-xl font-semibold text-[var(--grey-900)]">{call.callerName}</h2>
          <p className="text-sm text-[var(--grey-500)] mt-1 flex items-center gap-2">
            <Phone className="w-4 h-4" />
            {call.callerPhone}
          </p>
          {call.address && (
            <p className="text-sm text-[var(--grey-500)] mt-1">📍 {call.address}</p>
          )}

          <div className="flex gap-2 mt-4">
            <Button
              variant="secondary"
              size="sm"
              icon={<Phone className="w-4 h-4" />}
              onClick={() => window.open(`tel:${call.callerPhone.replace(/\s/g, "")}`)}
            >
              Call
            </Button>
            <Button
              variant="secondary"
              size="sm"
              icon={<MessageCircle className="w-4 h-4" />}
              onClick={() => window.open(`sms:${call.callerPhone.replace(/\s/g, "")}`)}
            >
              Message
            </Button>
            <Button
              variant="secondary"
              size="sm"
              icon={<Briefcase className="w-4 h-4" />}
              onClick={handleCreateJob}
            >
              Create Job
            </Button>
          </div>
        </div>

        {/* Call Summary */}
        <section>
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Call Summary</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
            <p className="text-[var(--grey-700)]">{call.summary}</p>
          </div>
        </section>

        {/* Details */}
        <section>
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2">Details</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-[var(--grey-500)]">Time:</span>
              <span className="text-[var(--grey-900)]">{call.time}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-[var(--grey-500)]">Duration:</span>
              <span className="text-[var(--grey-900)]">{call.duration}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-[var(--grey-500)]">Intent:</span>
              <span
                className={cn(
                  "px-2 py-0.5 text-xs font-medium rounded-full",
                  call.urgency === "emergency" && "bg-red-100 text-red-700"
                )}
              >
                {call.intent}
              </span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-[var(--grey-500)]">Status:</span>
              <span
                className={cn(
                  "px-2 py-0.5 text-xs font-medium rounded-full",
                  call.callbackCompleted
                    ? "bg-green-100 text-green-700"
                    : "bg-blue-100 text-blue-700"
                )}
              >
                {call.callbackCompleted ? "✓ Resolved" : "Callback needed"}
              </span>
            </div>
          </div>
        </section>

        {/* Transcript */}
        {call.transcript && call.transcript.length > 0 && (
          <section>
            <button
              onClick={() => setTranscriptExpanded(!transcriptExpanded)}
              className="flex items-center justify-between w-full text-sm font-medium text-[var(--grey-500)] mb-2"
            >
              <span>Transcript</span>
              {transcriptExpanded ? (
                <ChevronUp className="w-4 h-4" />
              ) : (
                <ChevronDown className="w-4 h-4" />
              )}
            </button>
            <div
              className={cn(
                "bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-4 overflow-hidden transition-all",
                transcriptExpanded ? "max-h-[500px] overflow-y-auto" : "max-h-24"
              )}
            >
              {call.transcript.map((entry, i) => (
                <div key={i}>
                  <p className="text-xs font-medium text-[var(--grey-500)] mb-1">
                    {entry.speaker}:
                  </p>
                  <p className="text-sm text-[var(--grey-700)]">{entry.text}</p>
                </div>
              ))}
            </div>
          </section>
        )}
      </main>

      {/* Bottom Action */}
      {call.callbackRequired && !call.callbackCompleted && (
        <FixedBottomButton onClick={handleMarkCallbackComplete} loading={isMarkingComplete}>
          Mark Callback Complete
        </FixedBottomButton>
      )}
    </>
  );
}
