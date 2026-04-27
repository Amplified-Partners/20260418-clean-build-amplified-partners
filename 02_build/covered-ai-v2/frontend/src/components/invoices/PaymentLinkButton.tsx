'use client';

import { useState } from 'react';
import { CreditCard, Copy, ExternalLink, Loader2, CheckCircle } from 'lucide-react';
import { Button } from '@/components/ui';
import { stripeApi } from '@/lib/api';

interface PaymentLinkButtonProps {
  invoiceId: string;
  paymentLinkUrl: string | null;
  status: string;
  onPaymentLinkCreated?: () => void;
}

export function PaymentLinkButton({
  invoiceId,
  paymentLinkUrl,
  status,
  onPaymentLinkCreated,
}: PaymentLinkButtonProps) {
  const [isCreating, setIsCreating] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Don't show for paid or cancelled invoices
  if (status === 'PAID' || status === 'CANCELLED') {
    return null;
  }

  const handleCreatePaymentLink = async () => {
    setIsCreating(true);
    setError(null);
    try {
      await stripeApi.createPaymentLink(invoiceId);
      onPaymentLinkCreated?.();
    } catch (err: unknown) {
      const error = err as { data?: { detail?: string } };
      setError(error.data?.detail || 'Failed to create payment link');
    } finally {
      setIsCreating(false);
    }
  };

  const handleCopyLink = async () => {
    if (!paymentLinkUrl) return;

    try {
      await navigator.clipboard.writeText(paymentLinkUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const handleOpenLink = () => {
    if (paymentLinkUrl) {
      window.open(paymentLinkUrl, '_blank');
    }
  };

  // Payment link exists
  if (paymentLinkUrl) {
    return (
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
            <CreditCard className="w-5 h-5 text-green-600" />
          </div>
          <div>
            <h4 className="font-medium text-[var(--grey-900)]">Payment Link Ready</h4>
            <p className="text-xs text-[var(--grey-500)]">
              Share this link with your customer
            </p>
          </div>
        </div>

        <div className="flex gap-2">
          <Button
            variant="secondary"
            onClick={handleCopyLink}
            className="flex-1 inline-flex items-center justify-center gap-2"
          >
            {copied ? (
              <>
                <CheckCircle className="w-4 h-4 text-green-600" />
                Copied!
              </>
            ) : (
              <>
                <Copy className="w-4 h-4" />
                Copy Link
              </>
            )}
          </Button>
          <Button
            variant="secondary"
            onClick={handleOpenLink}
            className="inline-flex items-center justify-center gap-2"
          >
            <ExternalLink className="w-4 h-4" />
          </Button>
        </div>
      </div>
    );
  }

  // No payment link yet
  return (
    <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
      <div className="flex items-center gap-3 mb-3">
        <div className="w-10 h-10 bg-[#635BFF]/10 rounded-lg flex items-center justify-center">
          <CreditCard className="w-5 h-5 text-[#635BFF]" />
        </div>
        <div>
          <h4 className="font-medium text-[var(--grey-900)]">Accept Card Payment</h4>
          <p className="text-xs text-[var(--grey-500)]">
            Create a payment link for this invoice
          </p>
        </div>
      </div>

      {error && (
        <p className="text-sm text-red-600 mb-3">{error}</p>
      )}

      <Button
        onClick={handleCreatePaymentLink}
        disabled={isCreating}
        className="w-full"
      >
        {isCreating ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin mr-2" />
            Creating...
          </>
        ) : (
          <>
            <CreditCard className="w-4 h-4 mr-2" />
            Create Payment Link
          </>
        )}
      </Button>
    </div>
  );
}

export default PaymentLinkButton;
