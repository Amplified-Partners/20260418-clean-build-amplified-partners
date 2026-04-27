/**
 * Customer LTV Table Component
 *
 * Displays top customers ranked by lifetime value.
 */

import React from "react";

interface Customer {
  id: string;
  client_id: string;
  name: string;
  phone: string;
  email?: string;
  total_jobs: number;
  total_revenue: number;
  first_job_date?: string;
  last_job_date?: string;
  acquisition_source?: string;
}

interface CustomerLTVTableProps {
  customers: Customer[];
  isLoading?: boolean;
  limit?: number;
}

const SOURCE_LABELS: Record<string, string> = {
  phone: "Phone Call",
  website: "Website",
  referral: "Referral",
  google: "Google",
  facebook: "Facebook",
  walk_in: "Walk-in",
  covered_ai: "Covered AI",
  unknown: "Unknown",
};

export const CustomerLTVTable: React.FC<CustomerLTVTableProps> = ({
  customers,
  isLoading = false,
  limit = 10,
}) => {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow">
        <div className="p-4 border-b">
          <div className="h-6 bg-gray-200 rounded w-1/4 animate-pulse"></div>
        </div>
        <div className="p-4 space-y-3">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-12 bg-gray-100 rounded animate-pulse"></div>
          ))}
        </div>
      </div>
    );
  }

  const displayedCustomers = customers.slice(0, limit);

  const formatDate = (dateStr?: string) => {
    if (!dateStr) return "-";
    return new Date(dateStr).toLocaleDateString("en-GB", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  };

  const getSourceBadge = (source?: string) => {
    const label = SOURCE_LABELS[source ?? "unknown"] ?? source ?? "Unknown";
    const colors: Record<string, string> = {
      covered_ai: "bg-purple-100 text-purple-700",
      referral: "bg-green-100 text-green-700",
      google: "bg-blue-100 text-blue-700",
      facebook: "bg-indigo-100 text-indigo-700",
      phone: "bg-yellow-100 text-yellow-700",
      website: "bg-cyan-100 text-cyan-700",
    };
    const colorClass = colors[source ?? ""] ?? "bg-gray-100 text-gray-700";

    return (
      <span className={`px-2 py-1 text-xs font-medium rounded-full ${colorClass}`}>
        {label}
      </span>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="p-4 border-b flex justify-between items-center">
        <h3 className="text-lg font-semibold text-gray-900">Top Customers by LTV</h3>
        <span className="text-sm text-gray-500">{customers.length} total</span>
      </div>

      {displayedCustomers.length === 0 ? (
        <div className="p-8 text-center text-gray-500">
          <svg className="w-12 h-12 mx-auto text-gray-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <p>No customer data yet</p>
          <p className="text-sm">Customers will appear here as jobs are completed</p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Rank
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Customer
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Total Revenue
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Jobs
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Source
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Last Job
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {displayedCustomers.map((customer, index) => (
                <tr key={customer.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className={`inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold ${
                      index === 0 ? "bg-yellow-100 text-yellow-700" :
                      index === 1 ? "bg-gray-200 text-gray-700" :
                      index === 2 ? "bg-orange-100 text-orange-700" :
                      "bg-gray-100 text-gray-500"
                    }`}>
                      {index + 1}
                    </span>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <div>
                      <div className="font-medium text-gray-900">{customer.name}</div>
                      <div className="text-sm text-gray-500">{customer.phone}</div>
                    </div>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className="font-semibold text-green-600">
                      £{customer.total_revenue.toFixed(2)}
                    </span>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-gray-900">
                    {customer.total_jobs}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    {getSourceBadge(customer.acquisition_source)}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                    {formatDate(customer.last_job_date)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default CustomerLTVTable;
