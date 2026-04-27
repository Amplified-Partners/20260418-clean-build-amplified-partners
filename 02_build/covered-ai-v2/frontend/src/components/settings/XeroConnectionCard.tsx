'use client';

import { useState } from 'react';
import {
  CheckCircle,
  XCircle,
  ExternalLink,
  Loader2,
  AlertCircle,
  RefreshCw,
  FileText,
  CloudOff,
} from 'lucide-react';
import { Button, Switch } from '@/components/ui';
import { xeroApi, type XeroConnectionStatus } from '@/lib/api';

interface XeroConnectionCardProps {
  clientId: string;
  status: XeroConnectionStatus | null;
  onStatusChange: () => void;
}

export function XeroConnectionCard({
  clientId,
  status,
  onStatusChange,
}: XeroConnectionCardProps) {
  const [isConnecting, setIsConnecting] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);
  const [isTogglingAutoSync, setIsTogglingAutoSync] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [syncResult, setSyncResult] = useState<{
    succeeded: number;
    failed: number;
  } | null>(null);

  const handleConnectXero = async () => {
    setIsConnecting(true);
    setError(null);
    try {
      const response = await xeroApi.connect(clientId);
      // Redirect to Xero OAuth
      window.location.href = response.redirect_url;
    } catch (err: unknown) {
      const error = err as { data?: { detail?: string } };
      setError(error.data?.detail || 'Failed to connect to Xero');
      setIsConnecting(false);
    }
  };

  const handleDisconnect = async () => {
    if (
      !confirm(
        'Are you sure you want to disconnect Xero? Invoice sync will stop.'
      )
    ) {
      return;
    }

    try {
      await xeroApi.disconnect(clientId);
      onStatusChange();
    } catch (err) {
      setError('Failed to disconnect Xero');
    }
  };

  const handleToggleAutoSync = async (enabled: boolean) => {
    setIsTogglingAutoSync(true);
    try {
      await xeroApi.toggleAutoSync(clientId, enabled);
      onStatusChange();
    } catch (err) {
      setError('Failed to update auto-sync setting');
    } finally {
      setIsTogglingAutoSync(false);
    }
  };

  const handleSyncAll = async () => {
    setIsSyncing(true);
    setError(null);
    setSyncResult(null);
    try {
      const result = await xeroApi.syncAllInvoices(clientId);
      setSyncResult({
        succeeded: result.succeeded,
        failed: result.failed,
      });
      onStatusChange();
    } catch (err: unknown) {
      const error = err as { data?: { detail?: string } };
      setError(error.data?.detail || 'Failed to sync invoices');
    } finally {
      setIsSyncing(false);
    }
  };

  // Format the last sync date
  const formatLastSync = (date: string | null) => {
    if (!date) return 'Never';
    const d = new Date(date);
    return d.toLocaleDateString('en-GB', {
      day: 'numeric',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="bg-white rounded-xl border border-[var(--grey-200)] overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-[var(--grey-200)]">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 bg-[#13B5EA] rounded-lg flex items-center justify-center">
            <svg
              viewBox="0 0 24 24"
              className="w-6 h-6 text-white"
              fill="currentColor"
            >
              <path d="M11.526 8.206c.198 0 .404.024.614.075l-.56.826c-.154-.034-.312-.05-.474-.05-.67 0-1.234.222-1.692.666-.459.444-.688.984-.688 1.622 0 .638.229 1.178.688 1.622.458.444 1.022.666 1.692.666.162 0 .32-.017.474-.05l.56.826a3.5 3.5 0 01-.614.075c-.896 0-1.658-.316-2.286-.948-.628-.632-.942-1.396-.942-2.29 0-.896.314-1.66.942-2.292.628-.632 1.39-.948 2.286-.948zm1.464 2.916c0-.292.094-.542.281-.75.188-.208.416-.312.686-.312.27 0 .498.104.686.312.187.208.28.458.28.75 0 .292-.093.542-.28.75-.188.208-.416.312-.686.312-.27 0-.498-.104-.686-.312-.187-.208-.281-.458-.281-.75z" />
            </svg>
          </div>
          <div>
            <h3 className="font-semibold text-[var(--grey-900)]">Xero</h3>
            <p className="text-sm text-[var(--grey-500)]">
              Sync invoices to your accounting software
            </p>
          </div>
        </div>
      </div>

      {/* Error message */}
      {error && (
        <div className="mx-4 mt-4 p-3 bg-red-50 rounded-lg flex items-start gap-2">
          <XCircle className="w-4 h-4 text-red-600 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      {/* Sync result message */}
      {syncResult && (
        <div className="mx-4 mt-4 p-3 bg-blue-50 rounded-lg flex items-start gap-2">
          <CheckCircle className="w-4 h-4 text-blue-600 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-blue-700">
            Synced {syncResult.succeeded} invoice{syncResult.succeeded !== 1 && 's'}
            {syncResult.failed > 0 && ` (${syncResult.failed} failed)`}
          </p>
        </div>
      )}

      {/* Status */}
      <div className="p-4">
        {!status?.connected ? (
          // Not connected
          <div className="text-center py-6">
            <div className="w-16 h-16 bg-[var(--grey-100)] rounded-full flex items-center justify-center mx-auto mb-4">
              <CloudOff className="w-8 h-8 text-[var(--grey-400)]" />
            </div>
            <h4 className="font-medium text-[var(--grey-900)] mb-2">
              Connect your Xero account
            </h4>
            <p className="text-sm text-[var(--grey-500)] mb-6 max-w-sm mx-auto">
              Automatically sync your invoices to Xero. Keep your books up to
              date without manual entry.
            </p>
            <Button
              onClick={handleConnectXero}
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
                  <FileText className="w-4 h-4" />
                  Connect to Xero
                </>
              )}
            </Button>
          </div>
        ) : (
          // Connected
          <div className="space-y-4">
            {/* Connection status */}
            <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
              <CheckCircle className="w-5 h-5 text-green-600" />
              <div className="flex-1">
                <p className="font-medium text-green-900">Connected to Xero</p>
                <p className="text-sm text-green-700">
                  {status.tenant_name || 'Organization'}
                </p>
              </div>
            </div>

            {/* Sync error warning */}
            {status.last_sync_error && (
              <div className="flex items-start gap-3 p-3 bg-amber-50 rounded-lg">
                <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="font-medium text-amber-900">Sync issue</p>
                  <p className="text-sm text-amber-700">
                    {status.last_sync_error}
                  </p>
                </div>
              </div>
            )}

            {/* Info */}
            <div className="grid grid-cols-2 gap-4">
              <div className="p-3 bg-[var(--grey-50)] rounded-lg">
                <p className="text-xs text-[var(--grey-500)] mb-1">Last Sync</p>
                <p className="text-sm font-medium text-[var(--grey-900)]">
                  {formatLastSync(status.last_sync_at)}
                </p>
              </div>
              <div className="p-3 bg-[var(--grey-50)] rounded-lg">
                <p className="text-xs text-[var(--grey-500)] mb-1">
                  Organization
                </p>
                <p className="text-sm font-medium text-[var(--grey-900)] truncate">
                  {status.tenant_name || 'N/A'}
                </p>
              </div>
            </div>

            {/* Auto-sync toggle */}
            <div className="flex items-center justify-between p-3 bg-[var(--grey-50)] rounded-lg">
              <div>
                <p className="font-medium text-[var(--grey-900)]">
                  Auto-sync invoices
                </p>
                <p className="text-sm text-[var(--grey-500)]">
                  Automatically sync new invoices to Xero
                </p>
              </div>
              <Switch
                checked={status.auto_sync_invoices}
                onChange={handleToggleAutoSync}
                disabled={isTogglingAutoSync}
              />
            </div>

            {/* Actions */}
            <div className="flex flex-col gap-2">
              <Button
                variant="secondary"
                onClick={handleSyncAll}
                disabled={isSyncing}
                className="w-full inline-flex items-center justify-center gap-2"
              >
                {isSyncing ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Syncing...
                  </>
                ) : (
                  <>
                    <RefreshCw className="w-4 h-4" />
                    Sync All Unsynced Invoices
                  </>
                )}
              </Button>
              <a
                href="https://go.xero.com"
                target="_blank"
                rel="noopener noreferrer"
                className="w-full inline-flex items-center justify-center gap-2 px-4 py-2 text-sm border border-[var(--grey-200)] rounded-lg text-[var(--grey-700)] hover:bg-[var(--grey-50)]"
              >
                <ExternalLink className="w-4 h-4" />
                Open Xero
              </a>
            </div>
          </div>
        )}
      </div>

      {/* Disconnect button */}
      {status?.connected && (
        <div className="px-4 pb-4">
          <button
            onClick={handleDisconnect}
            className="w-full text-sm text-red-600 hover:text-red-700 py-2"
          >
            Disconnect Xero
          </button>
        </div>
      )}
    </div>
  );
}
