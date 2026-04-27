'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import {
  CheckCircle,
  XCircle,
  Download,
  Clock,
  AlertTriangle,
  Building2,
  Phone,
  Mail,
} from 'lucide-react';
import { Button } from '@/components/ui';
import { cn, formatCurrency } from '@/lib/utils';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface QuoteLineItem {
  description: string;
  quantity: number;
  unitPrice: number;
  amount: number;
}

interface QuoteData {
  id: string;
  quoteNumber: string;
  title: string;
  description?: string;
  status: string;
  customerName: string;
  customerAddress?: string;
  businessName: string;
  businessLogoUrl?: string;
  businessPhone?: string;
  businessEmail?: string;
  lineItems: QuoteLineItem[];
  subtotal: number;
  vatRate: number;
  vatAmount: number;
  total: number;
  validUntil: string;
  createdAt: string;
  isExpired: boolean;
  canAccept: boolean;
  canReject: boolean;
  pdfUrl?: string;
  quoteTerms?: string;
}

type ResponseStatus = 'idle' | 'success' | 'error' | 'loading';

export default function QuoteViewPage() {
  const params = useParams();
  const token = params.token as string;

  const [quote, setQuote] = useState<QuoteData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [responseStatus, setResponseStatus] = useState<ResponseStatus>('idle');
  const [responseMessage, setResponseMessage] = useState<string>('');
  const [rejectionReason, setRejectionReason] = useState('');
  const [showRejectForm, setShowRejectForm] = useState(false);

  useEffect(() => {
    if (token) {
      loadQuote();
    }
  }, [token]);

  const loadQuote = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/quotes/view/${token}`);
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Quote not found');
        }
        throw new Error('Failed to load quote');
      }
      const data = await response.json();
      setQuote(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleResponse = async (action: 'accept' | 'reject') => {
    if (!quote) return;

    setResponseStatus('loading');

    try {
      const response = await fetch(`${API_BASE_URL}/quotes/view/${token}/respond`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action,
          rejectionReason: action === 'reject' ? rejectionReason : undefined,
        }),
      });

      const result = await response.json();

      if (result.success) {
        setResponseStatus('success');
        setResponseMessage(result.message);
        // Reload quote to get updated status
        loadQuote();
      } else {
        setResponseStatus('error');
        setResponseMessage(result.message);
      }
    } catch {
      setResponseStatus('error');
      setResponseMessage('Failed to submit response. Please try again.');
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[var(--grey-50)] flex items-center justify-center">
        <div className="animate-pulse text-center">
          <div className="w-16 h-16 bg-[var(--grey-200)] rounded-full mx-auto mb-4" />
          <div className="h-4 bg-[var(--grey-200)] rounded w-32 mx-auto" />
        </div>
      </div>
    );
  }

  if (error || !quote) {
    return (
      <div className="min-h-screen bg-[var(--grey-50)] flex items-center justify-center p-4">
        <div className="bg-white rounded-xl border border-[var(--grey-200)] p-8 max-w-md text-center">
          <AlertTriangle className="w-16 h-16 text-amber-500 mx-auto mb-4" />
          <h1 className="text-xl font-bold text-[var(--grey-900)] mb-2">Quote Not Found</h1>
          <p className="text-[var(--grey-600)]">
            {error || 'This quote may have been removed or the link is invalid.'}
          </p>
        </div>
      </div>
    );
  }

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-GB', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
    });
  };

  const getStatusBadge = () => {
    const statusConfig: Record<string, { color: string; label: string; icon: React.ReactNode }> = {
      DRAFT: { color: 'bg-[var(--grey-100)] text-[var(--grey-600)]', label: 'Draft', icon: null },
      SENT: { color: 'bg-blue-100 text-blue-700', label: 'Sent', icon: null },
      VIEWED: { color: 'bg-purple-100 text-purple-700', label: 'Viewed', icon: null },
      ACCEPTED: { color: 'bg-green-100 text-green-700', label: 'Accepted', icon: <CheckCircle className="w-4 h-4" /> },
      REJECTED: { color: 'bg-red-100 text-red-700', label: 'Rejected', icon: <XCircle className="w-4 h-4" /> },
      EXPIRED: { color: 'bg-amber-100 text-amber-700', label: 'Expired', icon: <Clock className="w-4 h-4" /> },
      CONVERTED: { color: 'bg-green-100 text-green-700', label: 'Converted to Job', icon: <CheckCircle className="w-4 h-4" /> },
    };

    const config = statusConfig[quote.status] || statusConfig.DRAFT;

    return (
      <span className={cn('inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium', config.color)}>
        {config.icon}
        {config.label}
      </span>
    );
  };

  return (
    <div className="min-h-screen bg-[var(--grey-50)] py-8 px-4">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-xl border border-[var(--grey-200)] p-6 mb-6">
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center gap-4">
              {quote.businessLogoUrl ? (
                <img
                  src={quote.businessLogoUrl}
                  alt={quote.businessName}
                  className="w-16 h-16 object-contain"
                />
              ) : (
                <div className="w-16 h-16 bg-[var(--brand-primary-light)] rounded-lg flex items-center justify-center">
                  <Building2 className="w-8 h-8 text-[var(--brand-primary)]" />
                </div>
              )}
              <div>
                <h2 className="text-lg font-bold text-[var(--grey-900)]">{quote.businessName}</h2>
                <div className="flex items-center gap-4 text-sm text-[var(--grey-600)] mt-1">
                  {quote.businessPhone && (
                    <span className="flex items-center gap-1">
                      <Phone className="w-4 h-4" />
                      {quote.businessPhone}
                    </span>
                  )}
                  {quote.businessEmail && (
                    <span className="flex items-center gap-1">
                      <Mail className="w-4 h-4" />
                      {quote.businessEmail}
                    </span>
                  )}
                </div>
              </div>
            </div>
            {getStatusBadge()}
          </div>

          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-[var(--grey-900)]">Quote #{quote.quoteNumber}</h1>
              <p className="text-[var(--grey-600)]">{quote.title}</p>
            </div>
            {quote.pdfUrl && (
              <a
                href={quote.pdfUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-4 py-2 bg-[var(--grey-100)] hover:bg-[var(--grey-200)] rounded-lg text-sm font-medium text-[var(--grey-700)] transition-colors"
              >
                <Download className="w-4 h-4" />
                Download PDF
              </a>
            )}
          </div>
        </div>

        {/* Validity Notice */}
        {quote.isExpired ? (
          <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 mb-6">
            <div className="flex items-center gap-2">
              <Clock className="w-5 h-5 text-amber-600" />
              <p className="text-amber-700 font-medium">
                This quote expired on {formatDate(quote.validUntil)}
              </p>
            </div>
          </div>
        ) : (
          <div className="bg-green-50 border border-green-200 rounded-xl p-4 mb-6">
            <div className="flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-green-600" />
              <p className="text-green-700">
                Valid until <strong>{formatDate(quote.validUntil)}</strong>
              </p>
            </div>
          </div>
        )}

        {/* Quote Details */}
        <div className="bg-white rounded-xl border border-[var(--grey-200)] p-6 mb-6">
          <h3 className="font-semibold text-[var(--grey-900)] mb-4">Quote Details</h3>

          {/* Customer */}
          <div className="mb-4 p-4 bg-[var(--grey-50)] rounded-lg">
            <p className="text-sm text-[var(--grey-500)] mb-1">Prepared for</p>
            <p className="font-medium text-[var(--grey-900)]">{quote.customerName}</p>
            {quote.customerAddress && (
              <p className="text-sm text-[var(--grey-600)]">{quote.customerAddress}</p>
            )}
          </div>

          {/* Description */}
          {quote.description && (
            <div className="mb-4 p-4 bg-green-50 rounded-lg">
              <p className="text-green-700">{quote.description}</p>
            </div>
          )}

          {/* Line Items */}
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-[var(--grey-200)]">
                  <th className="text-left py-3 text-sm font-medium text-[var(--grey-600)]">Description</th>
                  <th className="text-center py-3 text-sm font-medium text-[var(--grey-600)]">Qty</th>
                  <th className="text-right py-3 text-sm font-medium text-[var(--grey-600)]">Unit Price</th>
                  <th className="text-right py-3 text-sm font-medium text-[var(--grey-600)]">Amount</th>
                </tr>
              </thead>
              <tbody>
                {quote.lineItems.map((item, index) => (
                  <tr key={index} className="border-b border-[var(--grey-100)]">
                    <td className="py-3 text-[var(--grey-900)]">{item.description}</td>
                    <td className="py-3 text-center text-[var(--grey-700)]">{item.quantity}</td>
                    <td className="py-3 text-right text-[var(--grey-700)]">{formatCurrency(item.unitPrice)}</td>
                    <td className="py-3 text-right font-medium text-[var(--grey-900)]">{formatCurrency(item.amount)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Totals */}
          <div className="mt-4 pt-4 border-t border-[var(--grey-200)]">
            <div className="flex justify-end">
              <div className="w-64">
                <div className="flex justify-between py-2">
                  <span className="text-[var(--grey-600)]">Subtotal</span>
                  <span className="text-[var(--grey-900)]">{formatCurrency(quote.subtotal)}</span>
                </div>
                <div className="flex justify-between py-2">
                  <span className="text-[var(--grey-600)]">VAT ({(quote.vatRate * 100).toFixed(0)}%)</span>
                  <span className="text-[var(--grey-900)]">{formatCurrency(quote.vatAmount)}</span>
                </div>
                <div className="flex justify-between py-3 border-t-2 border-[var(--grey-900)]">
                  <span className="font-bold text-[var(--grey-900)]">Total</span>
                  <span className="font-bold text-2xl text-green-600">{formatCurrency(quote.total)}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Terms */}
        {quote.quoteTerms && (
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-6 mb-6">
            <h3 className="font-semibold text-[var(--grey-900)] mb-2">Terms & Conditions</h3>
            <p className="text-sm text-[var(--grey-600)] whitespace-pre-line">{quote.quoteTerms}</p>
          </div>
        )}

        {/* Response Section */}
        {responseStatus === 'success' ? (
          <div className="bg-green-50 border border-green-200 rounded-xl p-6 text-center">
            <CheckCircle className="w-16 h-16 text-green-600 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-green-700 mb-2">Thank You!</h3>
            <p className="text-green-600">{responseMessage}</p>
          </div>
        ) : responseStatus === 'error' ? (
          <div className="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
            <XCircle className="w-16 h-16 text-red-600 mx-auto mb-4" />
            <p className="text-red-700">{responseMessage}</p>
            <Button onClick={() => setResponseStatus('idle')} className="mt-4">
              Try Again
            </Button>
          </div>
        ) : quote.canAccept || quote.canReject ? (
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-6">
            <h3 className="font-semibold text-[var(--grey-900)] mb-4 text-center">
              What would you like to do?
            </h3>

            {showRejectForm ? (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-[var(--grey-700)] mb-1">
                    Reason for declining (optional)
                  </label>
                  <textarea
                    value={rejectionReason}
                    onChange={(e) => setRejectionReason(e.target.value)}
                    placeholder="Please let us know why you're declining this quote..."
                    rows={3}
                    className="w-full px-4 py-2 border border-[var(--grey-200)] rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)]"
                  />
                </div>
                <div className="flex gap-3">
                  <Button
                    variant="secondary"
                    onClick={() => setShowRejectForm(false)}
                    className="flex-1"
                  >
                    Cancel
                  </Button>
                  <Button
                    onClick={() => handleResponse('reject')}
                    disabled={responseStatus === 'loading'}
                    className="flex-1 bg-red-600 hover:bg-red-700"
                  >
                    {responseStatus === 'loading' ? 'Submitting...' : 'Confirm Decline'}
                  </Button>
                </div>
              </div>
            ) : (
              <div className="flex gap-4 justify-center">
                {quote.canAccept && (
                  <Button
                    onClick={() => handleResponse('accept')}
                    disabled={responseStatus === 'loading'}
                    size="lg"
                    className="px-8"
                  >
                    {responseStatus === 'loading' ? 'Processing...' : 'Accept Quote'}
                  </Button>
                )}
                {quote.canReject && (
                  <Button
                    variant="secondary"
                    onClick={() => setShowRejectForm(true)}
                    disabled={responseStatus === 'loading'}
                    size="lg"
                    className="px-8"
                  >
                    Decline
                  </Button>
                )}
              </div>
            )}
          </div>
        ) : quote.status === 'ACCEPTED' ? (
          <div className="bg-green-50 border border-green-200 rounded-xl p-6 text-center">
            <CheckCircle className="w-16 h-16 text-green-600 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-green-700 mb-2">Quote Accepted</h3>
            <p className="text-green-600">
              Thank you! We'll be in touch shortly to schedule the work.
            </p>
          </div>
        ) : quote.status === 'REJECTED' ? (
          <div className="bg-[var(--grey-50)] border border-[var(--grey-200)] rounded-xl p-6 text-center">
            <XCircle className="w-16 h-16 text-[var(--grey-400)] mx-auto mb-4" />
            <h3 className="text-xl font-bold text-[var(--grey-700)] mb-2">Quote Declined</h3>
            <p className="text-[var(--grey-600)]">
              Thank you for letting us know. Feel free to contact us if you change your mind.
            </p>
          </div>
        ) : null}

        {/* Footer */}
        <p className="text-center text-sm text-[var(--grey-400)] mt-8">
          Quote #{quote.quoteNumber} from {quote.businessName}
        </p>
      </div>
    </div>
  );
}
