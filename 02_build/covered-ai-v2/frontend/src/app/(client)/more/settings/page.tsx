/**
 * Client App - Settings Page
 * 
 * Simple, focused settings.
 * Gemma configuration front and center.
 */

"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Header, SectionDivider } from "@/components/client-app";
import { cn } from "@/lib/utils";

// Mock data
const mockSettings = {
  gemma: {
    status: "active" as const,
    greeting: "Good morning, thanks for calling Titan Plumbing. This is Gemma speaking. How can I help you today?",
    emergencyKeywords: ["burst", "flooding", "gas leak", "no heating", "emergency"],
    forwardEmergencies: true,
    forwardingNumber: "+447712345678",
  },
  notifications: {
    emergencies: true,
    newLeads: true,
    payments: true,
    dailyDigest: true,
    weeklyReport: true,
  },
  phone: {
    coveredNumber: "+441234567890",
    network: "EE",
    forwardingEnabled: true,
  },
};

function Toggle({ 
  enabled, 
  onChange 
}: { 
  enabled: boolean; 
  onChange: (value: boolean) => void 
}) {
  return (
    <button
      onClick={() => onChange(!enabled)}
      className={cn(
        "relative w-12 h-7 rounded-full transition-colors",
        enabled ? "bg-blue-600" : "bg-neutral-200"
      )}
    >
      <span
        className={cn(
          "absolute top-1 w-5 h-5 bg-white rounded-full shadow transition-transform",
          enabled ? "left-6" : "left-1"
        )}
      />
    </button>
  );
}

function SettingRow({
  title,
  description,
  children,
}: {
  title: string;
  description?: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex items-center justify-between py-4 px-5">
      <div className="flex-1 min-w-0 mr-4">
        <p className="font-medium text-neutral-900">{title}</p>
        {description && (
          <p className="text-sm text-neutral-500 mt-0.5">{description}</p>
        )}
      </div>
      {children}
    </div>
  );
}

export default function SettingsPage() {
  const router = useRouter();
  const [settings, setSettings] = useState(mockSettings);
  
  const updateNotification = (key: keyof typeof settings.notifications, value: boolean) => {
    setSettings(prev => ({
      ...prev,
      notifications: { ...prev.notifications, [key]: value },
    }));
  };
  
  const updateGemma = (key: keyof typeof settings.gemma, value: unknown) => {
    setSettings(prev => ({
      ...prev,
      gemma: { ...prev.gemma, [key]: value },
    }));
  };
  
  return (
    <div className="min-h-screen bg-neutral-50">
      <Header
        title="Settings"
        showBack
        onBack={() => router.back()}
      />
      
      {/* Gemma Settings */}
      <div className="mt-4">
        <h2 className="px-5 py-2 text-xs font-semibold text-neutral-500 uppercase tracking-wider">
          Gemma
        </h2>
        <div className="bg-white border-y border-neutral-200">
          {/* Status indicator */}
          <div className="px-5 py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className={cn(
                "w-3 h-3 rounded-full",
                settings.gemma.status === "active" ? "bg-emerald-500" : "bg-red-500"
              )} />
              <span className="font-medium text-neutral-900">
                {settings.gemma.status === "active" ? "Gemma is answering calls" : "Gemma is offline"}
              </span>
            </div>
          </div>
          
          <div className="h-px bg-neutral-100 mx-5" />
          
          <SettingRow
            title="Forward emergencies"
            description="Call you immediately for urgent issues"
          >
            <Toggle
              enabled={settings.gemma.forwardEmergencies}
              onChange={(value) => updateGemma("forwardEmergencies", value)}
            />
          </SettingRow>
          
          <div className="h-px bg-neutral-100 mx-5" />
          
          <button
            onClick={() => router.push("/more/settings/greeting")}
            className="w-full px-5 py-4 flex items-center justify-between hover:bg-neutral-50 transition-colors"
          >
            <div className="text-left">
              <p className="font-medium text-neutral-900">Greeting message</p>
              <p className="text-sm text-neutral-500 mt-0.5 line-clamp-1">
                {settings.gemma.greeting}
              </p>
            </div>
            <span className="text-neutral-400">→</span>
          </button>
          
          <div className="h-px bg-neutral-100 mx-5" />
          
          <button
            onClick={() => router.push("/more/settings/keywords")}
            className="w-full px-5 py-4 flex items-center justify-between hover:bg-neutral-50 transition-colors"
          >
            <div className="text-left">
              <p className="font-medium text-neutral-900">Emergency keywords</p>
              <p className="text-sm text-neutral-500 mt-0.5">
                {settings.gemma.emergencyKeywords.length} keywords configured
              </p>
            </div>
            <span className="text-neutral-400">→</span>
          </button>
        </div>
      </div>
      
      {/* Phone Settings */}
      <div className="mt-6">
        <h2 className="px-5 py-2 text-xs font-semibold text-neutral-500 uppercase tracking-wider">
          Phone
        </h2>
        <div className="bg-white border-y border-neutral-200">
          <div className="px-5 py-4">
            <p className="text-sm text-neutral-500">Your Covered number</p>
            <p className="font-medium text-neutral-900 mt-1">
              {settings.phone.coveredNumber}
            </p>
          </div>
          
          <div className="h-px bg-neutral-100 mx-5" />
          
          <div className="px-5 py-4">
            <p className="text-sm text-neutral-500">Forwarding to</p>
            <p className="font-medium text-neutral-900 mt-1">
              {settings.gemma.forwardingNumber}
            </p>
          </div>
          
          <div className="h-px bg-neutral-100 mx-5" />
          
          <button
            onClick={() => router.push("/more/settings/forwarding")}
            className="w-full px-5 py-4 flex items-center justify-between hover:bg-neutral-50 transition-colors"
          >
            <div className="text-left">
              <p className="font-medium text-neutral-900">Forwarding setup</p>
              <p className="text-sm text-neutral-500 mt-0.5">
                {settings.phone.network} • {settings.phone.forwardingEnabled ? "Enabled" : "Disabled"}
              </p>
            </div>
            <span className="text-neutral-400">→</span>
          </button>
        </div>
      </div>
      
      {/* Notifications */}
      <div className="mt-6">
        <h2 className="px-5 py-2 text-xs font-semibold text-neutral-500 uppercase tracking-wider">
          Notifications
        </h2>
        <div className="bg-white border-y border-neutral-200">
          <SettingRow
            title="Emergencies"
            description="Instant alerts for urgent calls"
          >
            <Toggle
              enabled={settings.notifications.emergencies}
              onChange={(value) => updateNotification("emergencies", value)}
            />
          </SettingRow>
          
          <div className="h-px bg-neutral-100 mx-5" />
          
          <SettingRow
            title="New leads"
            description="When someone new calls"
          >
            <Toggle
              enabled={settings.notifications.newLeads}
              onChange={(value) => updateNotification("newLeads", value)}
            />
          </SettingRow>
          
          <div className="h-px bg-neutral-100 mx-5" />
          
          <SettingRow
            title="Payments"
            description="When invoices are paid"
          >
            <Toggle
              enabled={settings.notifications.payments}
              onChange={(value) => updateNotification("payments", value)}
            />
          </SettingRow>
          
          <div className="h-px bg-neutral-100 mx-5" />
          
          <SettingRow
            title="Daily digest"
            description="Summary each morning at 7am"
          >
            <Toggle
              enabled={settings.notifications.dailyDigest}
              onChange={(value) => updateNotification("dailyDigest", value)}
            />
          </SettingRow>
          
          <div className="h-px bg-neutral-100 mx-5" />
          
          <SettingRow
            title="Weekly report"
            description="Summary every Monday"
          >
            <Toggle
              enabled={settings.notifications.weeklyReport}
              onChange={(value) => updateNotification("weeklyReport", value)}
            />
          </SettingRow>
        </div>
      </div>
      
      {/* Test call */}
      <div className="mx-5 mt-8 mb-6">
        <button
          onClick={() => {
            // In production: trigger test call
            alert("Test call initiated. Your phone will ring in a few seconds.");
          }}
          className="w-full py-3 bg-neutral-100 text-neutral-700 font-medium rounded-xl hover:bg-neutral-200 transition-colors"
        >
          Test Gemma
        </button>
        <p className="text-xs text-neutral-500 text-center mt-2">
          Gemma will call you to check everything is working
        </p>
      </div>
    </div>
  );
}
