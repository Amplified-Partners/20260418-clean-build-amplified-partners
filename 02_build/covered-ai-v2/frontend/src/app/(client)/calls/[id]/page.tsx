/**
 * Client App - Call Detail Page
 * 
 * Full details of a single call.
 * Actions to respond.
 * 
 * Design principles:
 * - All key info visible without scrolling
 * - Primary action prominent
 * - Secondary actions accessible
 */

"use client";

import React from "react";
import { useRouter, useParams } from "next/navigation";
import { Phone, MessageSquare, Calendar, Play, FileText, MapPin } from "lucide-react";
import { Header } from "@/components/client-app";
import { cn } from "@/lib/utils";

// Mock data - in production, fetch by ID
const mockCall = {
  id: "1",
  callerName: "John Smith",
  phone: "+447712345678",
  urgency: "emergency" as const,
  summary: "Burst pipe in kitchen, water coming through ceiling",
  address: "42 Oak Road, NE3 4AB",
  callDate: "Today, 9:42am",
  duration: "2 mins 34 secs",
  needsCallback: true,
  isResolved: false,
  transcript: `
Gemma: Good morning, Titan Plumbing, this is Gemma speaking. How can I help you today?

Caller: Hi, yes, I've got an emergency. There's water coming through my kitchen ceiling.

Gemma: Oh no, that sounds urgent. Let me make sure I understand - you have water coming through your ceiling right now?

Caller: Yes, it's coming through quite fast. I think a pipe has burst upstairs.

Gemma: I understand. This is definitely an emergency. Can I take your name and address so we can get someone to you as quickly as possible?

Caller: Yes, it's John Smith, 42 Oak Road, NE3 4AB.

Gemma: Thank you, John. I'm flagging this as an emergency and Ralph will call you back within the next few minutes. In the meantime, if you can locate your stopcock and turn off the water supply, that will help minimize the damage.

Caller: Okay, yes, I'll try to find it. Thank you.

Gemma: You're welcome. Someone will be in touch very shortly.
  `.trim(),
  recordingUrl: "/recordings/call-1.mp3",
};

export default function CallDetailPage() {
  const router = useRouter();
  const params = useParams();
  const callId = params.id;
  
  // In production: fetch call by ID
  const call = mockCall;
  
  const [showTranscript, setShowTranscript] = React.useState(false);
  
  const handleCall = () => {
    window.location.href = `tel:${call.phone}`;
  };
  
  const handleSms = () => {
    window.location.href = `sms:${call.phone}`;
  };
  
  const handleBook = () => {
    router.push(`/more/schedule/new?customer=${encodeURIComponent(call.callerName)}&phone=${encodeURIComponent(call.phone)}`);
  };
  
  const handlePlayRecording = () => {
    // In production: play audio
    alert("Playing recording...");
  };
  
  return (
    <div className="min-h-screen bg-white">
      <Header
        showBack
        onBack={() => router.back()}
      />
      
      <div className="px-5 pb-8">
        {/* Caller info */}
        <div className="pt-4">
          <h1 className="text-2xl font-semibold text-neutral-900">
            {call.callerName}
          </h1>
          <a 
            href={`tel:${call.phone}`}
            className="text-blue-600 text-lg"
          >
            {call.phone}
          </a>
        </div>
        
        {/* Urgency badge */}
        {call.urgency === "emergency" && (
          <div className="mt-4 p-4 bg-red-50 rounded-xl border border-red-100">
            <div className="flex items-center gap-2">
              <span className="text-lg">⚡</span>
              <span className="font-semibold text-red-700">EMERGENCY</span>
            </div>
            <p className="mt-2 text-neutral-800">{call.summary}</p>
            
            {call.address && (
              <div className="flex items-center gap-2 mt-3 text-neutral-600">
                <MapPin className="w-4 h-4" />
                <span className="text-sm">{call.address}</span>
              </div>
            )}
            
            <p className="text-sm text-neutral-500 mt-2">
              Called: {call.callDate} • Duration: {call.duration}
            </p>
          </div>
        )}
        
        {call.urgency !== "emergency" && (
          <div className="mt-4 p-4 bg-neutral-50 rounded-xl">
            <p className="text-neutral-800">{call.summary}</p>
            
            {call.address && (
              <div className="flex items-center gap-2 mt-3 text-neutral-600">
                <MapPin className="w-4 h-4" />
                <span className="text-sm">{call.address}</span>
              </div>
            )}
            
            <p className="text-sm text-neutral-500 mt-2">
              Called: {call.callDate} • Duration: {call.duration}
            </p>
          </div>
        )}
        
        {/* Primary action */}
        {call.needsCallback && !call.isResolved && (
          <button
            onClick={handleCall}
            className="mt-6 w-full flex items-center justify-center gap-2 py-4 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 transition-colors"
          >
            <Phone className="w-5 h-5" />
            Call {call.callerName.split(" ")[0]}
          </button>
        )}
        
        {/* Secondary actions */}
        <div className="mt-4 grid grid-cols-2 gap-3">
          <button
            onClick={handleSms}
            className="flex items-center justify-center gap-2 py-3 bg-neutral-100 text-neutral-700 font-medium rounded-xl hover:bg-neutral-200 transition-colors"
          >
            <MessageSquare className="w-5 h-5" />
            Send SMS
          </button>
          <button
            onClick={handleBook}
            className="flex items-center justify-center gap-2 py-3 bg-neutral-100 text-neutral-700 font-medium rounded-xl hover:bg-neutral-200 transition-colors"
          >
            <Calendar className="w-5 h-5" />
            Book Job
          </button>
        </div>
        
        {/* Recording & Transcript */}
        <div className="mt-8 space-y-3">
          <button
            onClick={handlePlayRecording}
            className="w-full flex items-center gap-3 p-4 bg-neutral-50 rounded-xl hover:bg-neutral-100 transition-colors"
          >
            <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
              <Play className="w-5 h-5 text-blue-600" />
            </div>
            <div className="text-left">
              <p className="font-medium text-neutral-900">Listen to call</p>
              <p className="text-sm text-neutral-500">{call.duration}</p>
            </div>
          </button>
          
          <button
            onClick={() => setShowTranscript(!showTranscript)}
            className="w-full flex items-center gap-3 p-4 bg-neutral-50 rounded-xl hover:bg-neutral-100 transition-colors"
          >
            <div className="w-10 h-10 bg-neutral-100 rounded-full flex items-center justify-center">
              <FileText className="w-5 h-5 text-neutral-600" />
            </div>
            <div className="text-left flex-1">
              <p className="font-medium text-neutral-900">Read transcript</p>
              <p className="text-sm text-neutral-500">Full conversation</p>
            </div>
            <span className="text-neutral-400">
              {showTranscript ? "▼" : "→"}
            </span>
          </button>
          
          {showTranscript && (
            <div className="p-4 bg-neutral-50 rounded-xl">
              <pre className="text-sm text-neutral-700 whitespace-pre-wrap font-sans">
                {call.transcript}
              </pre>
            </div>
          )}
        </div>
        
        {/* Mark as resolved */}
        {!call.isResolved && (
          <button
            onClick={() => {
              // In production: update status
              router.back();
            }}
            className="mt-8 w-full py-3 text-neutral-500 font-medium text-center hover:text-neutral-700 transition-colors"
          >
            Mark as resolved
          </button>
        )}
      </div>
    </div>
  );
}
