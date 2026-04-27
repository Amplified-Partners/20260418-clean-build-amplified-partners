'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import {
  ArrowLeft,
  CheckCircle,
  XCircle,
  ExternalLink,
  Loader2,
  CreditCard,
  AlertCircle,
  Wallet,
  RefreshCw,
} from 'lucide-react';
import { Header } from '@/components/layout';
import { Button } from '@/components/ui';
import { useAuthContext } from '@/lib/auth-context';
import { stripeApi, type StripeAccountStatus } from '@/lib/api';

function PaymentsSettingsContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { client } = useAuthContext();

  const [status, setStatus] = useState<StripeAccountStatus | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Check for success/refresh params from Stripe redirect
  const success = searchParams.get('success');
  const refresh = searchParams.get('refresh');

  useEffect(() => {
    if (client?.id) {
      loadStripeStatus();
    }
  }, [client?.id]);

  const loadStripeStatus = async () => {
    if (!client?.id) return;

    setIsLoading(true);
    setError(null);
    try {
      const data = await stripeApi.getStatus(client.id);
      setStatus(data);
    } catch (err) {
      setError('Failed to load Stripe status');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleConnectStripe = async () => {
    if (!client?.id) return;

    setIsConnecting(true);
    setError(null);
    try {
      const response = await stripeApi.createAccount(client.id);
      // Redirect to Stripe onboarding
      window.location.href = response.onboarding_url;
    } catch (err: unknown) {
      const error = err as { data?: { detail?: string } };
      setError(error.data?.detail || 'Failed to create Stripe account');
      setIsConnecting(false);
    }
  };

  const handleContinueOnboarding = async () => {
    if (!client?.id) return;

    setIsConnecting(true);
    setError(null);
    try {
      const response = await stripeApi.getOnboardingLink(client.id);
      window.location.href = response.onboarding_url;
    } catch (err: unknown) {
      const error = err as { data?: { detail?: string } };
      setError(error.data?.detail || 'Failed to get onboarding link');
      setIsConnecting(false);
    }
  };

  const handleOpenDashboard = async () => {
    if (!client?.id) return;

    try {
      const response = await stripeApi.getDashboardLink(client.id);
      window.open(response.dashboard_url, '_blank');
    } catch (err) {
      setError('Failed to open Stripe dashboard');
    }
  };

  const handleDisconnect = async () => {
    if (!client?.id) return;

    if (!confirm('Are you sure you want to disconnect your Stripe account? You will not be able to accept payments until you reconnect.')) {
      return;
    }

    try {
      await stripeApi.disconnect(client.id);
      setStatus(null);
      loadStripeStatus();
    } catch (err) {
      setError('Failed to disconnect Stripe account');
    }
  };

  if (isLoading) {
    return (
      <>
        <Header
          title="Accept Payments"
          backButton
          onBack={() => router.push('/settings')}
        />
        <main className="pb-24 px-4 pt-6">
          <div className="flex items-center justify-center py-12">
            <Loader2 className="w-8 h-8 animate-spin text-[var(--brand-primary)]" />
          </div>
        </main>
      </>
    );
  }

  return (
    <>
      <Header
        title="Accept Payments"
        backButton
        onBack={() => router.push('/settings')}
      />
      <main className="pb-24 px-4 pt-6 space-y-6">
        {/* Success message from Stripe redirect */}
        {success === 'true' && (
          <div className="bg-green-50 border border-green-200 rounded-xl p-4 flex items-start gap-3">
            <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-medium text-green-900">Stripe connected successfully!</p>
              <p className="text-sm text-green-700 mt-1">
                You can now accept payments on your invoices.
              </p>
            </div>
          </div>
        )}

        {/* Refresh message (user left onboarding early) */}
        {refresh === 'true' && !status?.onboarding_complete && (
          <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-medium text-amber-900">Onboarding incomplete</p>
              <p className="text-sm text-amber-700 mt-1">
                Please complete your Stripe account setup to start accepting payments.
              </p>
            </div>
          </div>
        )}

        {/* Error message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-start gap-3">
            <XCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-red-700">{error}</p>
            </div>
          </div>
        )}

        {/* Stripe Connect Card */}
        <div className="bg-white rounded-xl border border-[var(--grey-200)] overflow-hidden">
          {/* Header */}
          <div className="p-4 border-b border-[var(--grey-200)]">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-[#635BFF] rounded-lg flex items-center justify-center">
                <CreditCard className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="font-semibold text-[var(--grey-900)]">Stripe Connect</h3>
                <p className="text-sm text-[var(--grey-500)]">
                  Accept card payments on your invoices
                </p>
              </div>
            </div>
          </div>

          {/* Status */}
          <div className="p-4">
            {!status?.connected ? (
              // Not connected
              <div className="text-center py-6">
                <div className="w-16 h-16 bg-[var(--grey-100)] rounded-full flex items-center justify-center mx-auto mb-4">
                  <Wallet className="w-8 h-8 text-[var(--grey-400)]" />
                </div>
                <h4 className="font-medium text-[var(--grey-900)] mb-2">
                  Connect your Stripe account
                </h4>
                <p className="text-sm text-[var(--grey-500)] mb-6 max-w-sm mx-auto">
                  Accept card payments directly on your invoices. Funds are deposited to your bank account.
                </p>
                <Button
                  onClick={handleConnectStripe}
                  disabled={isConnecting}
                  className="inline-flex items-center gap-2"
                >
                  {isConnecting ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Connecting...
                    </>
                  ) : (
                    <>
                      <CreditCard className="w-4 h-4" />
                      Connect with Stripe
                    </>
                  )}
                </Button>
              </div>
            ) : !status.onboarding_complete ? (
              // Connected but onboarding incomplete
              <div className="space-y-4">
                <div className="flex items-center gap-3 p-3 bg-amber-50 rounded-lg">
                  <AlertCircle className="w-5 h-5 text-amber-600" />
                  <div className="flex-1">
                    <p className="font-medium text-amber-900">Setup incomplete</p>
                    <p className="text-sm text-amber-700">
                      Complete your Stripe account setup to start accepting payments.
                    </p>
                  </div>
                </div>
                <Button
                  onClick={handleContinueOnboarding}
                  disabled={isConnecting}
                  className="w-full"
                >
                  {isConnecting ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin mr-2" />
                      Loading...
                    </>
                  ) : (
                    'Continue Setup'
                  )}
                </Button>
              </div>
            ) : (
              // Fully connected
              <div className="space-y-4">
                {/* Status indicators */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-3 bg-[var(--grey-50)] rounded-lg">
                    <div className="flex items-center gap-2 mb-1">
                      {status.charges_enabled ? (
                        <CheckCircle className="w-4 h-4 text-green-600" />
                      ) : (
                        <XCircle className="w-4 h-4 text-red-500" />
                      )}
                      <span className="text-sm font-medium text-[var(--grey-900)]">
                        Card Payments
                      </span>
                    </div>
                    <p className="text-xs text-[var(--grey-500)]">
                      {status.charges_enabled ? 'Enabled' : 'Not enabled'}
                    </p>
                  </div>
                  <div className="p-3 bg-[var(--grey-50)] rounded-lg">
                    <div className="flex items-center gap-2 mb-1">
                      {status.payouts_enabled ? (
                        <CheckCircle className="w-4 h-4 text-green-600" />
                      ) : (
                        <XCircle className="w-4 h-4 text-red-500" />
                      )}
                      <span className="text-sm font-medium text-[var(--grey-900)]">
                        Payouts
                      </span>
                    </div>
                    <p className="text-xs text-[var(--grey-500)]">
                      {status.payouts_enabled ? 'Enabled' : 'Pending verification'}
                    </p>
                  </div>
                </div>

                {/* Account ID */}
                <div className="text-xs text-[var(--grey-500)] font-mono bg-[var(--grey-50)] px-3 py-2 rounded">
                  Account: {status.account_id}
                </div>

                {/* Actions */}
                <div className="flex flex-col gap-2">
                  <Button
                    variant="secondary"
                    onClick={handleOpenDashboard}
                    className="w-full inline-flex items-center justify-center gap-2"
                  >
                    <ExternalLink className="w-4 h-4" />
                    Open Stripe Dashboard
                  </Button>
                  <button
                    onClick={loadStripeStatus}
                    className="text-sm text-[var(--grey-500)] hover:text-[var(--grey-700)] inline-flex items-center justify-center gap-1"
                  >
                    <RefreshCw className="w-3 h-3" />
                    Refresh Status
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Info cards */}
        <div className="space-y-3">
          <div className="bg-[var(--grey-50)] rounded-xl p-4">
            <h4 className="font-medium text-[var(--grey-900)] mb-2">How it works</h4>
            <ul className="text-sm text-[var(--grey-600)] space-y-2">
              <li className="flex items-start gap-2">
                <span className="text-[var(--brand-primary)] font-medium">1.</span>
                Connect your Stripe account (or create one for free)
              </li>
              <li className="flex items-start gap-2">
                <span className="text-[var(--brand-primary)] font-medium">2.</span>
                Each invoice gets a unique payment link
              </li>
              <li className="flex items-start gap-2">
                <span className="text-[var(--brand-primary)] font-medium">3.</span>
                Customers pay online with card
              </li>
              <li className="flex items-start gap-2">
                <span className="text-[var(--brand-primary)] font-medium">4.</span>
                Funds deposited to your bank in 2-3 days
              </li>
            </ul>
          </div>

          <div className="bg-[var(--grey-50)] rounded-xl p-4">
            <h4 className="font-medium text-[var(--grey-900)] mb-2">Fees</h4>
            <p className="text-sm text-[var(--grey-600)]">
              Stripe charges 1.5% + 20p per successful card payment.
              Covered AI takes a 2.9% platform fee to cover payment processing costs.
            </p>
          </div>
        </div>

        {/* Disconnect button */}
        {status?.connected && (
          <button
            onClick={handleDisconnect}
            className="w-full text-sm text-red-600 hover:text-red-700 py-3"
          >
            Disconnect Stripe Account
          </button>
        )}
      </main>
    </>
  );
}

export default function PaymentsSettingsPage() {
  return (
    <Suspense fallback={
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-[var(--brand-primary)]" />
      </div>
    }>
      <PaymentsSettingsContent />
    </Suspense>
  );
}
