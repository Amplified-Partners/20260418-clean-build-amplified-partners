'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import {
  CheckCircle,
  XCircle,
  Loader2,
  AlertCircle,
} from 'lucide-react';
import { Header } from '@/components/layout';
import { XeroConnectionCard } from '@/components/settings';
import { useAuthContext } from '@/lib/auth-context';
import { xeroApi, type XeroConnectionStatus } from '@/lib/api';

function AccountingSettingsContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { client } = useAuthContext();

  const [xeroStatus, setXeroStatus] = useState<XeroConnectionStatus | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Check for success param from Xero redirect
  const success = searchParams.get('success');

  useEffect(() => {
    if (client?.id) {
      loadXeroStatus();
    }
  }, [client?.id]);

  const loadXeroStatus = async () => {
    if (!client?.id) return;

    setIsLoading(true);
    setError(null);
    try {
      const data = await xeroApi.getStatus(client.id);
      setXeroStatus(data);
    } catch (err) {
      setError('Failed to load Xero status');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <>
        <Header
          title="Accounting"
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
        title="Accounting"
        backButton
        onBack={() => router.push('/settings')}
      />
      <main className="pb-24 px-4 pt-6 space-y-6">
        {/* Success message from Xero redirect */}
        {success === 'true' && (
          <div className="bg-green-50 border border-green-200 rounded-xl p-4 flex items-start gap-3">
            <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-medium text-green-900">Xero connected successfully!</p>
              <p className="text-sm text-green-700 mt-1">
                Your invoices will now sync to Xero automatically.
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

        {/* Xero Connection Card */}
        {client?.id && (
          <XeroConnectionCard
            clientId={client.id}
            status={xeroStatus}
            onStatusChange={loadXeroStatus}
          />
        )}

        {/* Info cards */}
        <div className="space-y-3">
          <div className="bg-[var(--grey-50)] rounded-xl p-4">
            <h4 className="font-medium text-[var(--grey-900)] mb-2">How it works</h4>
            <ul className="text-sm text-[var(--grey-600)] space-y-2">
              <li className="flex items-start gap-2">
                <span className="text-[var(--brand-primary)] font-medium">1.</span>
                Connect your Xero account
              </li>
              <li className="flex items-start gap-2">
                <span className="text-[var(--brand-primary)] font-medium">2.</span>
                New invoices are automatically synced to Xero
              </li>
              <li className="flex items-start gap-2">
                <span className="text-[var(--brand-primary)] font-medium">3.</span>
                Contacts are created or matched automatically
              </li>
              <li className="flex items-start gap-2">
                <span className="text-[var(--brand-primary)] font-medium">4.</span>
                Keep your books up-to-date without manual entry
              </li>
            </ul>
          </div>

          <div className="bg-[var(--grey-50)] rounded-xl p-4">
            <h4 className="font-medium text-[var(--grey-900)] mb-2">What gets synced</h4>
            <ul className="text-sm text-[var(--grey-600)] space-y-2">
              <li className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-600" />
                Invoice amounts and line items
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-600" />
                Customer contact details
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-600" />
                Due dates and invoice numbers
              </li>
              <li className="flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-amber-500" />
                Payments are not synced (mark paid in both systems)
              </li>
            </ul>
          </div>

          <div className="bg-amber-50 rounded-xl p-4">
            <h4 className="font-medium text-amber-900 mb-2">Note</h4>
            <p className="text-sm text-amber-700">
              Xero integration requires a Xero subscription. Invoices sync as
              &quot;Authorised&quot; status in Xero, meaning they&apos;re ready to send. You
              can then send them via Xero or mark them as sent.
            </p>
          </div>
        </div>
      </main>
    </>
  );
}

export default function AccountingSettingsPage() {
  return (
    <Suspense fallback={
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-[var(--brand-primary)]" />
      </div>
    }>
      <AccountingSettingsContent />
    </Suspense>
  );
}
