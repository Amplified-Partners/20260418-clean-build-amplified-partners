'use client';

import { useState } from 'react';
import { FileText, Download, ExternalLink, Loader2, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui';

interface InvoicePdfPreviewProps {
  invoiceId: string;
  invoiceNumber: string;
  pdfUrl?: string | null;
  pdfGeneratedAt?: string | null;
  onGeneratePdf?: () => Promise<void>;
  isGenerating?: boolean;
}

export function InvoicePdfPreview({
  invoiceId,
  invoiceNumber,
  pdfUrl,
  pdfGeneratedAt,
  onGeneratePdf,
  isGenerating = false,
}: InvoicePdfPreviewProps) {
  const [showPreview, setShowPreview] = useState(false);

  const handleDownload = () => {
    if (pdfUrl) {
      window.open(pdfUrl, '_blank');
    }
  };

  const handleOpenInNewTab = () => {
    if (pdfUrl) {
      window.open(pdfUrl, '_blank');
    }
  };

  // PDF not yet generated
  if (!pdfUrl) {
    return (
      <div className="bg-white rounded-xl border border-[var(--grey-200)] p-6">
        <div className="text-center">
          <div className="w-12 h-12 bg-[var(--grey-100)] rounded-full flex items-center justify-center mx-auto mb-3">
            <FileText className="w-6 h-6 text-[var(--grey-400)]" />
          </div>
          <h4 className="font-medium text-[var(--grey-900)] mb-1">PDF Not Generated</h4>
          <p className="text-sm text-[var(--grey-500)] mb-4">
            Generate a PDF to preview, download, or send to your customer.
          </p>
          {onGeneratePdf && (
            <Button
              onClick={onGeneratePdf}
              disabled={isGenerating}
              className="inline-flex items-center gap-2"
            >
              {isGenerating ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <FileText className="w-4 h-4" />
                  Generate PDF
                </>
              )}
            </Button>
          )}
        </div>
      </div>
    );
  }

  // PDF exists
  return (
    <div className="bg-white rounded-xl border border-[var(--grey-200)] overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-[var(--grey-200)]">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
            <FileText className="w-5 h-5 text-red-600" />
          </div>
          <div>
            <h4 className="font-medium text-[var(--grey-900)]">{invoiceNumber}.pdf</h4>
            {pdfGeneratedAt && (
              <p className="text-xs text-[var(--grey-500)]">
                Generated {new Date(pdfGeneratedAt).toLocaleDateString('en-GB', {
                  day: 'numeric',
                  month: 'short',
                  year: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </p>
            )}
          </div>
        </div>
        <div className="flex items-center gap-2">
          {onGeneratePdf && (
            <button
              onClick={onGeneratePdf}
              disabled={isGenerating}
              className="p-2 text-[var(--grey-400)] hover:text-[var(--grey-600)] hover:bg-[var(--grey-100)] rounded-lg transition-colors disabled:opacity-50"
              title="Regenerate PDF"
            >
              {isGenerating ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <RefreshCw className="w-5 h-5" />
              )}
            </button>
          )}
          <button
            onClick={handleDownload}
            className="p-2 text-[var(--grey-400)] hover:text-[var(--grey-600)] hover:bg-[var(--grey-100)] rounded-lg transition-colors"
            title="Download PDF"
          >
            <Download className="w-5 h-5" />
          </button>
          <button
            onClick={handleOpenInNewTab}
            className="p-2 text-[var(--grey-400)] hover:text-[var(--grey-600)] hover:bg-[var(--grey-100)] rounded-lg transition-colors"
            title="Open in new tab"
          >
            <ExternalLink className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Preview toggle */}
      <button
        onClick={() => setShowPreview(!showPreview)}
        className="w-full p-3 text-sm text-[var(--brand-primary)] hover:bg-[var(--grey-50)] transition-colors text-center"
      >
        {showPreview ? 'Hide Preview' : 'Show Preview'}
      </button>

      {/* PDF Preview iframe */}
      {showPreview && (
        <div className="border-t border-[var(--grey-200)]">
          <iframe
            src={pdfUrl}
            className="w-full h-[500px]"
            title={`Invoice ${invoiceNumber} PDF Preview`}
          />
        </div>
      )}
    </div>
  );
}

export default InvoicePdfPreview;
