/**
 * Marketing Spend List Component
 *
 * Displays marketing spend history by month and source.
 */

import React from "react";

interface MarketingSpend {
  id: string;
  month: string;
  amount: number;
  source?: string;
  notes?: string;
  created_at: string;
}

interface MarketingSpendListProps {
  spend: MarketingSpend[];
  isLoading?: boolean;
  onDelete?: (id: string) => Promise<void>;
}

const SOURCE_LABELS: Record<string, string> = {
  google_ads: "Google Ads",
  facebook: "Facebook/Instagram",
  flyers: "Flyers/Print",
  covered_ai: "Covered AI",
  referral: "Referral Program",
  other: "Other",
};

const SOURCE_COLORS: Record<string, string> = {
  google_ads: "bg-blue-500",
  facebook: "bg-indigo-500",
  flyers: "bg-yellow-500",
  covered_ai: "bg-purple-500",
  referral: "bg-green-500",
  other: "bg-gray-500",
};

export const MarketingSpendList: React.FC<MarketingSpendListProps> = ({
  spend,
  isLoading = false,
  onDelete,
}) => {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow">
        <div className="p-4 border-b">
          <div className="h-6 bg-gray-200 rounded w-1/3 animate-pulse"></div>
        </div>
        <div className="p-4 space-y-3">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-16 bg-gray-100 rounded animate-pulse"></div>
          ))}
        </div>
      </div>
    );
  }

  // Group spend by month
  const groupedByMonth = spend.reduce((acc, item) => {
    if (!acc[item.month]) {
      acc[item.month] = [];
    }
    acc[item.month].push(item);
    return acc;
  }, {} as Record<string, MarketingSpend[]>);

  const months = Object.keys(groupedByMonth).sort().reverse();

  const formatMonth = (monthStr: string) => {
    const [year, month] = monthStr.split("-");
    const date = new Date(parseInt(year), parseInt(month) - 1, 1);
    return date.toLocaleDateString("en-GB", {
      month: "long",
      year: "numeric",
    });
  };

  const totalSpend = spend.reduce((sum, s) => sum + s.amount, 0);

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="p-4 border-b flex justify-between items-center">
        <h3 className="text-lg font-semibold text-gray-900">Marketing Spend</h3>
        <div className="text-right">
          <div className="text-sm text-gray-500">Total Spend</div>
          <div className="text-lg font-semibold text-gray-900">£{totalSpend.toFixed(2)}</div>
        </div>
      </div>

      {spend.length === 0 ? (
        <div className="p-8 text-center text-gray-500">
          <svg className="w-12 h-12 mx-auto text-gray-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p>No marketing spend recorded</p>
          <p className="text-sm">Add your marketing expenses to track CAC</p>
        </div>
      ) : (
        <div className="divide-y divide-gray-100">
          {months.map((month) => {
            const items = groupedByMonth[month];
            const monthTotal = items.reduce((sum, i) => sum + i.amount, 0);

            return (
              <div key={month} className="p-4">
                <div className="flex justify-between items-center mb-3">
                  <h4 className="font-medium text-gray-900">{formatMonth(month)}</h4>
                  <span className="font-semibold text-gray-700">£{monthTotal.toFixed(2)}</span>
                </div>
                <div className="space-y-2">
                  {items.map((item) => (
                    <div
                      key={item.id}
                      className="flex items-center justify-between p-2 bg-gray-50 rounded-lg"
                    >
                      <div className="flex items-center gap-3">
                        <div
                          className={`w-2 h-8 rounded-full ${SOURCE_COLORS[item.source ?? "other"]}`}
                        />
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {SOURCE_LABELS[item.source ?? "other"] ?? item.source}
                          </div>
                          {item.notes && (
                            <div className="text-xs text-gray-500">{item.notes}</div>
                          )}
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="font-medium text-gray-900">
                          £{item.amount.toFixed(2)}
                        </span>
                        {onDelete && (
                          <button
                            onClick={() => onDelete(item.id)}
                            className="p-1 text-gray-400 hover:text-red-500 transition-colors"
                            title="Delete"
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default MarketingSpendList;
