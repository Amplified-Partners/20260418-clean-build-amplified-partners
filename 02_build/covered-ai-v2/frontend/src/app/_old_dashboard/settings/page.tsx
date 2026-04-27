"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import {
  User,
  Building2,
  Phone,
  Mail,
  MapPin,
  Bell,
  CreditCard,
  Shield,
  HelpCircle,
  LogOut,
  ChevronRight,
  ExternalLink,
  Wallet,
  FileText,
} from "lucide-react";
import { Header } from "@/components/layout";
import { Button } from "@/components/ui";
import { useAuthContext } from "@/lib/auth-context";
import { useSettings } from "@/lib/hooks";
import { settingsApi, type ClientSettings } from "@/lib/api";
import { cn } from "@/lib/utils";

function SettingsSkeleton() {
  return (
    <div className="px-4 py-6 space-y-6 animate-pulse">
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 bg-[var(--grey-200)] rounded-full" />
          <div className="flex-1">
            <div className="h-6 bg-[var(--grey-200)] rounded w-1/3 mb-2" />
            <div className="h-4 bg-[var(--grey-100)] rounded w-1/2" />
          </div>
        </div>
      </div>
      {[1, 2, 3].map((i) => (
        <div key={i} className="bg-white rounded-xl border border-[var(--grey-200)] p-4 space-y-4">
          {[1, 2, 3].map((j) => (
            <div key={j} className="h-12 bg-[var(--grey-100)] rounded" />
          ))}
        </div>
      ))}
    </div>
  );
}

interface SettingsItemProps {
  icon: React.ReactNode;
  label: string;
  value?: string;
  onClick?: () => void;
  external?: boolean;
  danger?: boolean;
}

function SettingsItem({ icon, label, value, onClick, external, danger }: SettingsItemProps) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-[var(--grey-50)] transition-colors",
        danger && "text-red-600"
      )}
    >
      <div
        className={cn(
          "w-8 h-8 rounded-lg flex items-center justify-center",
          danger ? "bg-red-100 text-red-600" : "bg-[var(--grey-100)] text-[var(--grey-600)]"
        )}
      >
        {icon}
      </div>
      <div className="flex-1 min-w-0">
        <p className={cn("font-medium", danger ? "text-red-600" : "text-[var(--grey-900)]")}>
          {label}
        </p>
        {value && <p className="text-sm text-[var(--grey-500)] truncate">{value}</p>}
      </div>
      {external ? (
        <ExternalLink className="w-5 h-5 text-[var(--grey-400)]" />
      ) : (
        <ChevronRight className="w-5 h-5 text-[var(--grey-400)]" />
      )}
    </button>
  );
}

export default function SettingsPage() {
  const router = useRouter();
  const { client, user, logout } = useAuthContext();
  const { data, isLoading, error } = useSettings(client?.id || null);
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  const handleLogout = async () => {
    setIsLoggingOut(true);
    try {
      await logout();
      router.push("/login");
    } catch (err) {
      console.error("Logout failed:", err);
    } finally {
      setIsLoggingOut(false);
    }
  };

  if (isLoading) {
    return (
      <>
        <Header title="Settings" />
        <main className="pb-24">
          <SettingsSkeleton />
        </main>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Header title="Settings" />
        <main className="pb-24 px-4 pt-6">
          <div className="bg-red-50 rounded-xl border border-red-200 p-4 text-center">
            <p className="text-red-700">Failed to load settings</p>
          </div>
        </main>
      </>
    );
  }

  const settings: Partial<ClientSettings> = data?.settings || {};

  return (
    <>
      <Header title="Settings" />
      <main className="pb-24">
        {/* Profile Card */}
        <div className="px-4 py-6">
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-[var(--brand-primary-light)] rounded-full flex items-center justify-center">
                <span className="text-2xl font-semibold text-[var(--brand-primary)]">
                  {client?.ownerName?.charAt(0).toUpperCase() || "U"}
                </span>
              </div>
              <div className="flex-1 min-w-0">
                <h2 className="text-lg font-semibold text-[var(--grey-900)]">
                  {client?.ownerName || "User"}
                </h2>
                <p className="text-sm text-[var(--grey-500)] truncate">{client?.businessName}</p>
                <p className="text-sm text-[var(--grey-500)]">{user?.email}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Business Settings */}
        <section className="px-4 mb-6">
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2 px-1">BUSINESS</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] divide-y divide-[var(--grey-100)]">
            <SettingsItem
              icon={<Building2 className="w-4 h-4" />}
              label="Business Details"
              value={client?.businessName}
              onClick={() => router.push("/dashboard/settings/business")}
            />
            <SettingsItem
              icon={<Phone className="w-4 h-4" />}
              label="Covered Number"
              value={client?.coveredNumber || "Not set up"}
              onClick={() => router.push("/dashboard/settings/phone")}
            />
            <SettingsItem
              icon={<MapPin className="w-4 h-4" />}
              label="Service Area"
              value={settings.serviceArea || "Not configured"}
              onClick={() => router.push("/dashboard/settings/area")}
            />
          </div>
        </section>

        {/* Preferences */}
        <section className="px-4 mb-6">
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2 px-1">PREFERENCES</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] divide-y divide-[var(--grey-100)]">
            <SettingsItem
              icon={<Bell className="w-4 h-4" />}
              label="Notifications"
              value="Push, Email, SMS"
              onClick={() => router.push("/dashboard/settings/notifications")}
            />
            <SettingsItem
              icon={<User className="w-4 h-4" />}
              label="Gemma Settings"
              value="Voice, greeting, hours"
              onClick={() => router.push("/dashboard/settings/gemma")}
            />
          </div>
        </section>

        {/* Payments & Subscription */}
        <section className="px-4 mb-6">
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2 px-1">PAYMENTS</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] divide-y divide-[var(--grey-100)]">
            <SettingsItem
              icon={<Wallet className="w-4 h-4" />}
              label="Accept Payments"
              value="Stripe Connect"
              onClick={() => router.push("/settings/payments")}
            />
            <SettingsItem
              icon={<FileText className="w-4 h-4" />}
              label="Accounting"
              value="Xero Integration"
              onClick={() => router.push("/settings/accounting")}
            />
            <SettingsItem
              icon={<CreditCard className="w-4 h-4" />}
              label="Plan & Billing"
              value={`${client?.subscriptionPlan || "Free"} plan`}
              onClick={() => router.push("/dashboard/settings/billing")}
            />
          </div>
        </section>

        {/* Support */}
        <section className="px-4 mb-6">
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2 px-1">SUPPORT</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] divide-y divide-[var(--grey-100)]">
            <SettingsItem
              icon={<HelpCircle className="w-4 h-4" />}
              label="Help Centre"
              onClick={() => window.open("https://help.covered.ai", "_blank")}
              external
            />
            <SettingsItem
              icon={<Mail className="w-4 h-4" />}
              label="Contact Support"
              value="support@covered.ai"
              onClick={() => window.open("mailto:support@covered.ai")}
              external
            />
            <SettingsItem
              icon={<Shield className="w-4 h-4" />}
              label="Privacy Policy"
              onClick={() => window.open("https://covered.ai/privacy", "_blank")}
              external
            />
          </div>
        </section>

        {/* Account Actions */}
        <section className="px-4 mb-6">
          <h3 className="text-sm font-medium text-[var(--grey-500)] mb-2 px-1">ACCOUNT</h3>
          <div className="bg-white rounded-xl border border-[var(--grey-200)] divide-y divide-[var(--grey-100)]">
            <SettingsItem
              icon={<LogOut className="w-4 h-4" />}
              label="Log Out"
              onClick={handleLogout}
              danger
            />
          </div>
        </section>

        {/* App Info */}
        <div className="px-4 py-6 text-center">
          <p className="text-xs text-[var(--grey-400)]">Covered AI v2.0.0</p>
          <p className="text-xs text-[var(--grey-400)] mt-1">
            © 2024 Covered AI. All rights reserved.
          </p>
        </div>
      </main>
    </>
  );
}
