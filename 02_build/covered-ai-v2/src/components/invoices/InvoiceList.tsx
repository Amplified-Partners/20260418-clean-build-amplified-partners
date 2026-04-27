/**
 * Invoice List Component
 *
 * Displays invoices in a table with:
 * - Invoice number
 * - Customer name
 * - Amount
 * - Status badge (color-coded)
 * - Due date
 * - Actions (view, send, mark paid, etc.)
 */

import React from "react";

type InvoiceStatus =
  | "DRAFT"
  | "SENT"
  | "REMINDED"
  | "OVERDUE"
  | "PAID"
  | "CANCELLED"
  | "WRITTEN_OFF";

interface Invoice {
  id: string;
  invoiceNumber: string;
  customerName: string;
  customerEmail: string;
  amount: number;
  description: string;
  dueDate: string;
  status: InvoiceStatus;
  sentAt?: string;
  paidAt?: string;
  createdAt: string;
}

interface InvoiceListProps {
  invoices: Invoice[];
  loading?: boolean;
  onSend?: (invoiceId: string) => void;
  onMarkPaid?: (invoiceId: string) => void;
  onView?: (invoiceId: string) => void;
  onCancel?: (invoiceId: string) => void;
}

const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency: "GBP",
  }).format(amount);
};

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
};

const StatusBadge: React.FC<{ status: InvoiceStatus }> = ({ status }) => {
  const statusConfig: Record<
    InvoiceStatus,
    { label: string; className: string }
  > = {
    DRAFT: {
      label: "Draft",
      className: "bg-gray-100 text-gray-700",
    },
    SENT: {
      label: "Sent",
      className: "bg-blue-100 text-blue-700",
    },
    REMINDED: {
      label: "Reminded",
      className: "bg-amber-100 text-amber-700",
    },
    OVERDUE: {
      label: "Overdue",
      className: "bg-red-100 text-red-700",
    },
    PAID: {
      label: "Paid",
      className: "bg-green-100 text-green-700",
    },
    CANCELLED: {
      label: "Cancelled",
      className: "bg-gray-100 text-gray-500",
    },
    WRITTEN_OFF: {
      label: "Written Off",
      className: "bg-gray-100 text-gray-500",
    },
  };

  const config = statusConfig[status];

  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${config.className}`}
    >
      {config.label}
    </span>
  );
};

const ActionButton: React.FC<{
  onClick: () => void;
  variant?: "primary" | "secondary" | "success" | "danger";
  children: React.ReactNode;
}> = ({ onClick, variant = "secondary", children }) => {
  const variantClasses = {
    primary: "text-blue-600 hover:text-blue-800",
    secondary: "text-gray-600 hover:text-gray-800",
    success: "text-green-600 hover:text-green-800",
    danger: "text-red-600 hover:text-red-800",
  };

  return (
    <button
      onClick={onClick}
      className={`text-sm font-medium ${variantClasses[variant]} transition-colors`}
    >
      {children}
    </button>
  );
};

export const InvoiceList: React.FC<InvoiceListProps> = ({
  invoices,
  loading = false,
  onSend,
  onMarkPaid,
  onView,
  onCancel,
}) => {
  if (loading) {
    return (
      <div className="rounded-lg border border-gray-200 bg-white">
        <div className="p-8 text-center">
          <div className="mx-auto h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent" />
          <p className="mt-2 text-sm text-gray-500">Loading invoices...</p>
        </div>
      </div>
    );
  }

  if (invoices.length === 0) {
    return (
      <div className="rounded-lg border border-gray-200 bg-white">
        <div className="p-8 text-center">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <p className="mt-2 text-sm text-gray-500">No invoices found</p>
        </div>
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-lg border border-gray-200 bg-white">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
              Invoice
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
              Customer
            </th>
            <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-gray-500">
              Amount
            </th>
            <th className="px-4 py-3 text-center text-xs font-medium uppercase tracking-wider text-gray-500">
              Status
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
              Due Date
            </th>
            <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-gray-500">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200 bg-white">
          {invoices.map((invoice) => {
            const isOverdue =
              new Date(invoice.dueDate) < new Date() &&
              !["PAID", "CANCELLED", "WRITTEN_OFF"].includes(invoice.status);

            return (
              <tr
                key={invoice.id}
                className="hover:bg-gray-50 transition-colors"
              >
                <td className="whitespace-nowrap px-4 py-3">
                  <div>
                    <p className="font-medium text-gray-900">
                      {invoice.invoiceNumber}
                    </p>
                    <p className="text-xs text-gray-500 truncate max-w-[200px]">
                      {invoice.description}
                    </p>
                  </div>
                </td>
                <td className="whitespace-nowrap px-4 py-3">
                  <div>
                    <p className="text-sm text-gray-900">
                      {invoice.customerName}
                    </p>
                    <p className="text-xs text-gray-500">
                      {invoice.customerEmail}
                    </p>
                  </div>
                </td>
                <td className="whitespace-nowrap px-4 py-3 text-right">
                  <p className="font-semibold text-gray-900">
                    {formatCurrency(invoice.amount)}
                  </p>
                </td>
                <td className="whitespace-nowrap px-4 py-3 text-center">
                  <StatusBadge status={invoice.status} />
                </td>
                <td className="whitespace-nowrap px-4 py-3">
                  <p
                    className={`text-sm ${isOverdue ? "text-red-600 font-medium" : "text-gray-700"}`}
                  >
                    {formatDate(invoice.dueDate)}
                  </p>
                  {invoice.paidAt && (
                    <p className="text-xs text-green-600">
                      Paid {formatDate(invoice.paidAt)}
                    </p>
                  )}
                </td>
                <td className="whitespace-nowrap px-4 py-3 text-right">
                  <div className="flex items-center justify-end gap-3">
                    {onView && (
                      <ActionButton onClick={() => onView(invoice.id)}>
                        View
                      </ActionButton>
                    )}
                    {invoice.status === "DRAFT" && onSend && (
                      <ActionButton
                        variant="primary"
                        onClick={() => onSend(invoice.id)}
                      >
                        Send
                      </ActionButton>
                    )}
                    {["SENT", "REMINDED", "OVERDUE"].includes(invoice.status) &&
                      onMarkPaid && (
                        <ActionButton
                          variant="success"
                          onClick={() => onMarkPaid(invoice.id)}
                        >
                          Mark Paid
                        </ActionButton>
                      )}
                    {invoice.status === "DRAFT" && onCancel && (
                      <ActionButton
                        variant="danger"
                        onClick={() => onCancel(invoice.id)}
                      >
                        Cancel
                      </ActionButton>
                    )}
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default InvoiceList;
