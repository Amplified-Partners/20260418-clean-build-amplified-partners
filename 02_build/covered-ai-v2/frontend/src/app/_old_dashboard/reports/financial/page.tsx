'use client';

import { useState, useEffect, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { Loader2 } from 'lucide-react';
import {
  ArrowLeft,
  Download,
  Calendar,
  TrendingUp,
  TrendingDown,
  Minus,
  PoundSterling,
  FileText,
} from 'lucide-react';
import Link from 'next/link';
import { Button } from '@/components/ui';
import { cn, formatCurrency } from '@/lib/utils';
import { financialApi } from '@/lib/api';
import type { CashFlowReport, VatReport } from '@/lib/api';

type TabType = 'cash-flow' | 'vat';

function FinancialReportsContent() {
  const searchParams = useSearchParams();
  const [activeTab, setActiveTab] = useState<TabType>('cash-flow');
  const [isLoading, setIsLoading] = useState(true);

  // Cash flow state
  const [cashFlowData, setCashFlowData] = useState<CashFlowReport | null>(null);
  const [startDate, setStartDate] = useState(() => {
    const date = new Date();
    date.setMonth(date.getMonth() - 3);
    return date.toISOString().split('T')[0];
  });
  const [endDate, setEndDate] = useState(() => {
    return new Date().toISOString().split('T')[0];
  });

  // VAT state
  const [vatData, setVatData] = useState<VatReport | null>(null);
  const [vatQuarter, setVatQuarter] = useState(() => {
    const now = new Date();
    return Math.ceil((now.getMonth() + 1) / 3);
  });
  const [vatYear, setVatYear] = useState(() => new Date().getFullYear());

  // Get client ID from URL params or use default
  const clientId = searchParams.get('client_id') || '06d733ac-96e9-4455-970d-99cb3f5b9b8e';

  useEffect(() => {
    if (activeTab === 'cash-flow') {
      loadCashFlowData();
    } else {
      loadVatData();
    }
  }, [activeTab, startDate, endDate, vatQuarter, vatYear, clientId]);

  const loadCashFlowData = async () => {
    setIsLoading(true);
    try {
      const data = await financialApi.getCashFlowReport(clientId, startDate, endDate);
      setCashFlowData(data);
    } catch (error) {
      console.error('Failed to load cash flow data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadVatData = async () => {
    setIsLoading(true);
    try {
      const data = await financialApi.getVatReport(clientId, vatQuarter, vatYear);
      setVatData(data);
    } catch (error) {
      console.error('Failed to load VAT data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleExportCashFlow = () => {
    const url = financialApi.exportCashFlowCsv(clientId, startDate, endDate);
    window.open(url, '_blank');
  };

  const handleExportVat = () => {
    const url = financialApi.exportVatCsv(clientId, vatQuarter, vatYear);
    window.open(url, '_blank');
  };

  const getQuarterLabel = (quarter: number) => {
    const quarters = ['Q1 (Jan-Mar)', 'Q2 (Apr-Jun)', 'Q3 (Jul-Sep)', 'Q4 (Oct-Dec)'];
    return quarters[quarter - 1] || `Q${quarter}`;
  };

  return (
    <div className="min-h-screen bg-[var(--grey-50)] p-6">
      {/* Header */}
      <div className="mb-6">
        <Link
          href="/reports"
          className="inline-flex items-center gap-2 text-[var(--grey-600)] hover:text-[var(--grey-900)] mb-4"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Reports
        </Link>
        <h1 className="text-2xl font-bold text-[var(--grey-900)]">Financial Reports</h1>
        <p className="text-[var(--grey-600)]">Cash flow analysis and VAT reporting</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6">
        <button
          onClick={() => setActiveTab('cash-flow')}
          className={cn(
            'px-4 py-2 rounded-lg font-medium transition-colors',
            activeTab === 'cash-flow'
              ? 'bg-[var(--brand-primary)] text-white'
              : 'bg-white text-[var(--grey-600)] hover:bg-[var(--grey-100)]'
          )}
        >
          <span className="flex items-center gap-2">
            <TrendingUp className="w-4 h-4" />
            Cash Flow
          </span>
        </button>
        <button
          onClick={() => setActiveTab('vat')}
          className={cn(
            'px-4 py-2 rounded-lg font-medium transition-colors',
            activeTab === 'vat'
              ? 'bg-[var(--brand-primary)] text-white'
              : 'bg-white text-[var(--grey-600)] hover:bg-[var(--grey-100)]'
          )}
        >
          <span className="flex items-center gap-2">
            <FileText className="w-4 h-4" />
            VAT Report
          </span>
        </button>
      </div>

      {/* Cash Flow Tab */}
      {activeTab === 'cash-flow' && (
        <div className="space-y-6">
          {/* Filters */}
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
            <div className="flex flex-wrap items-end gap-4">
              <div>
                <label className="block text-sm font-medium text-[var(--grey-700)] mb-1">
                  Start Date
                </label>
                <input
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  className="px-3 py-2 border border-[var(--grey-200)] rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)]"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-[var(--grey-700)] mb-1">
                  End Date
                </label>
                <input
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  className="px-3 py-2 border border-[var(--grey-200)] rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)]"
                />
              </div>
              <Button onClick={handleExportCashFlow} variant="secondary">
                <Download className="w-4 h-4 mr-2" />
                Export CSV
              </Button>
            </div>
          </div>

          {isLoading ? (
            <div className="bg-white rounded-xl border border-[var(--grey-200)] p-8 animate-pulse">
              <div className="h-8 bg-[var(--grey-100)] rounded w-1/3 mb-4" />
              <div className="space-y-3">
                {[1, 2, 3, 4].map((i) => (
                  <div key={i} className="h-6 bg-[var(--grey-100)] rounded" />
                ))}
              </div>
            </div>
          ) : cashFlowData ? (
            <>
              {/* Summary Cards */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <SummaryCard
                  label="Total Invoiced"
                  value={formatCurrency(cashFlowData.summary.total_invoiced)}
                  icon={<FileText className="w-5 h-5" />}
                  color="grey"
                />
                <SummaryCard
                  label="Total Collected"
                  value={formatCurrency(cashFlowData.summary.total_collected)}
                  icon={<PoundSterling className="w-5 h-5" />}
                  color="green"
                />
                <SummaryCard
                  label="Outstanding"
                  value={formatCurrency(cashFlowData.summary.total_outstanding)}
                  icon={<Calendar className="w-5 h-5" />}
                  color="amber"
                />
                <SummaryCard
                  label="Net Cash Flow"
                  value={formatCurrency(cashFlowData.summary.net_cash_flow)}
                  icon={
                    cashFlowData.summary.net_cash_flow >= 0 ? (
                      <TrendingUp className="w-5 h-5" />
                    ) : (
                      <TrendingDown className="w-5 h-5" />
                    )
                  }
                  color={cashFlowData.summary.net_cash_flow >= 0 ? 'green' : 'red'}
                />
              </div>

              {/* Monthly Breakdown */}
              <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
                <h3 className="font-semibold text-[var(--grey-900)] mb-4">Monthly Breakdown</h3>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-[var(--grey-200)]">
                        <th className="text-left py-3 px-4 text-sm font-medium text-[var(--grey-600)]">
                          Month
                        </th>
                        <th className="text-right py-3 px-4 text-sm font-medium text-[var(--grey-600)]">
                          Invoiced
                        </th>
                        <th className="text-right py-3 px-4 text-sm font-medium text-[var(--grey-600)]">
                          Collected
                        </th>
                        <th className="text-right py-3 px-4 text-sm font-medium text-[var(--grey-600)]">
                          Outstanding
                        </th>
                        <th className="text-right py-3 px-4 text-sm font-medium text-[var(--grey-600)]">
                          Collection Rate
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {cashFlowData.breakdown.map((row, index) => (
                        <tr
                          key={index}
                          className="border-b border-[var(--grey-100)] hover:bg-[var(--grey-50)]"
                        >
                          <td className="py-3 px-4 font-medium text-[var(--grey-900)]">
                            {row.month}
                          </td>
                          <td className="py-3 px-4 text-right text-[var(--grey-700)]">
                            {formatCurrency(row.invoiced)}
                          </td>
                          <td className="py-3 px-4 text-right text-green-600 font-medium">
                            {formatCurrency(row.collected)}
                          </td>
                          <td className="py-3 px-4 text-right text-[var(--grey-700)]">
                            {formatCurrency(row.outstanding)}
                          </td>
                          <td className="py-3 px-4 text-right">
                            <span
                              className={cn(
                                'font-medium',
                                row.collection_rate >= 80
                                  ? 'text-green-600'
                                  : row.collection_rate >= 50
                                  ? 'text-amber-600'
                                  : 'text-red-600'
                              )}
                            >
                              {row.collection_rate.toFixed(1)}%
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </>
          ) : (
            <div className="bg-white rounded-xl border border-[var(--grey-200)] p-8 text-center text-[var(--grey-500)]">
              No cash flow data available for the selected period
            </div>
          )}
        </div>
      )}

      {/* VAT Tab */}
      {activeTab === 'vat' && (
        <div className="space-y-6">
          {/* Filters */}
          <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
            <div className="flex flex-wrap items-end gap-4">
              <div>
                <label className="block text-sm font-medium text-[var(--grey-700)] mb-1">
                  Quarter
                </label>
                <select
                  value={vatQuarter}
                  onChange={(e) => setVatQuarter(Number(e.target.value))}
                  className="px-3 py-2 border border-[var(--grey-200)] rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)]"
                >
                  <option value={1}>Q1 (Jan-Mar)</option>
                  <option value={2}>Q2 (Apr-Jun)</option>
                  <option value={3}>Q3 (Jul-Sep)</option>
                  <option value={4}>Q4 (Oct-Dec)</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-[var(--grey-700)] mb-1">
                  Year
                </label>
                <select
                  value={vatYear}
                  onChange={(e) => setVatYear(Number(e.target.value))}
                  className="px-3 py-2 border border-[var(--grey-200)] rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)]"
                >
                  {[2023, 2024, 2025].map((year) => (
                    <option key={year} value={year}>
                      {year}
                    </option>
                  ))}
                </select>
              </div>
              <Button onClick={handleExportVat} variant="secondary">
                <Download className="w-4 h-4 mr-2" />
                Export CSV
              </Button>
            </div>
          </div>

          {isLoading ? (
            <div className="bg-white rounded-xl border border-[var(--grey-200)] p-8 animate-pulse">
              <div className="h-8 bg-[var(--grey-100)] rounded w-1/3 mb-4" />
              <div className="space-y-3">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="h-6 bg-[var(--grey-100)] rounded" />
                ))}
              </div>
            </div>
          ) : vatData ? (
            <>
              {/* VAT Summary */}
              <div className="bg-white rounded-xl border border-[var(--grey-200)] p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-semibold text-[var(--grey-900)]">
                    VAT Summary - {getQuarterLabel(vatData.quarter)} {vatData.year}
                  </h3>
                  <span className="text-sm text-[var(--grey-500)]">
                    {vatData.start_date} to {vatData.end_date}
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="p-4 bg-[var(--grey-50)] rounded-lg">
                    <p className="text-sm text-[var(--grey-600)] mb-1">Total Sales (excl. VAT)</p>
                    <p className="text-2xl font-bold text-[var(--grey-900)]">
                      {formatCurrency(vatData.summary.total_sales)}
                    </p>
                  </div>
                  <div className="p-4 bg-[var(--grey-50)] rounded-lg">
                    <p className="text-sm text-[var(--grey-600)] mb-1">VAT Collected (Output)</p>
                    <p className="text-2xl font-bold text-[var(--brand-primary)]">
                      {formatCurrency(vatData.summary.vat_collected)}
                    </p>
                  </div>
                  <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                    <p className="text-sm text-green-600 mb-1">VAT Due to HMRC</p>
                    <p className="text-2xl font-bold text-green-700">
                      {formatCurrency(vatData.summary.vat_due)}
                    </p>
                  </div>
                </div>
              </div>

              {/* Invoice Breakdown */}
              <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
                <h3 className="font-semibold text-[var(--grey-900)] mb-4">Invoice Breakdown</h3>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-[var(--grey-200)]">
                        <th className="text-left py-3 px-4 text-sm font-medium text-[var(--grey-600)]">
                          Invoice
                        </th>
                        <th className="text-left py-3 px-4 text-sm font-medium text-[var(--grey-600)]">
                          Customer
                        </th>
                        <th className="text-left py-3 px-4 text-sm font-medium text-[var(--grey-600)]">
                          Date
                        </th>
                        <th className="text-right py-3 px-4 text-sm font-medium text-[var(--grey-600)]">
                          Net Amount
                        </th>
                        <th className="text-right py-3 px-4 text-sm font-medium text-[var(--grey-600)]">
                          VAT ({vatData.vat_rate}%)
                        </th>
                        <th className="text-right py-3 px-4 text-sm font-medium text-[var(--grey-600)]">
                          Gross
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {vatData.invoices.map((invoice, index) => (
                        <tr
                          key={index}
                          className="border-b border-[var(--grey-100)] hover:bg-[var(--grey-50)]"
                        >
                          <td className="py-3 px-4 font-medium text-[var(--brand-primary)]">
                            <Link href={`/invoices/${invoice.id}`} className="hover:underline">
                              {invoice.invoice_number}
                            </Link>
                          </td>
                          <td className="py-3 px-4 text-[var(--grey-700)]">
                            {invoice.customer_name}
                          </td>
                          <td className="py-3 px-4 text-[var(--grey-600)]">
                            {new Date(invoice.date).toLocaleDateString('en-GB')}
                          </td>
                          <td className="py-3 px-4 text-right text-[var(--grey-700)]">
                            {formatCurrency(invoice.net_amount)}
                          </td>
                          <td className="py-3 px-4 text-right text-[var(--brand-primary)]">
                            {formatCurrency(invoice.vat_amount)}
                          </td>
                          <td className="py-3 px-4 text-right font-medium text-[var(--grey-900)]">
                            {formatCurrency(invoice.gross_amount)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                    <tfoot>
                      <tr className="bg-[var(--grey-50)]">
                        <td colSpan={3} className="py-3 px-4 font-semibold text-[var(--grey-900)]">
                          Totals
                        </td>
                        <td className="py-3 px-4 text-right font-semibold text-[var(--grey-900)]">
                          {formatCurrency(vatData.summary.total_sales)}
                        </td>
                        <td className="py-3 px-4 text-right font-semibold text-[var(--brand-primary)]">
                          {formatCurrency(vatData.summary.vat_collected)}
                        </td>
                        <td className="py-3 px-4 text-right font-semibold text-[var(--grey-900)]">
                          {formatCurrency(vatData.summary.total_sales + vatData.summary.vat_collected)}
                        </td>
                      </tr>
                    </tfoot>
                  </table>
                </div>
                {vatData.invoices.length === 0 && (
                  <div className="text-center py-8 text-[var(--grey-500)]">
                    No invoices found for this quarter
                  </div>
                )}
              </div>
            </>
          ) : (
            <div className="bg-white rounded-xl border border-[var(--grey-200)] p-8 text-center text-[var(--grey-500)]">
              No VAT data available for the selected quarter
            </div>
          )}
        </div>
      )}
    </div>
  );
}

interface SummaryCardProps {
  label: string;
  value: string;
  icon: React.ReactNode;
  color: 'grey' | 'green' | 'amber' | 'red';
}

function SummaryCard({ label, value, icon, color }: SummaryCardProps) {
  const colorClasses = {
    grey: 'bg-[var(--grey-100)] text-[var(--grey-600)]',
    green: 'bg-green-100 text-green-600',
    amber: 'bg-amber-100 text-amber-600',
    red: 'bg-red-100 text-red-600',
  };

  return (
    <div className="bg-white rounded-xl border border-[var(--grey-200)] p-4">
      <div className={cn('w-10 h-10 rounded-lg flex items-center justify-center mb-3', colorClasses[color])}>
        {icon}
      </div>
      <p className="text-sm text-[var(--grey-600)] mb-1">{label}</p>
      <p className="text-xl font-bold text-[var(--grey-900)]">{value}</p>
    </div>
  );
}

export default function FinancialReportsPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-[var(--grey-50)] flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-[var(--brand-primary)]" />
      </div>
    }>
      <FinancialReportsContent />
    </Suspense>
  );
}
