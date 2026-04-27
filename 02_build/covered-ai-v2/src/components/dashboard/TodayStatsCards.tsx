/**
 * TodayStatsCards Component
 *
 * 3 metric cards showing:
 * - Calls today (with trend vs yesterday)
 * - Revenue this week (with trend vs last week)
 * - Reviews this week (with trend vs last week)
 */

import React from "react";

interface TodayStats {
  calls_today: number;
  calls_today_trend: number;
  revenue_this_week: number;
  revenue_this_week_trend: number;
  reviews_this_week: number;
  reviews_this_week_trend: number;
}

interface TodayStatsCardsProps {
  stats: TodayStats;
  isLoading?: boolean;
}

const TrendBadge: React.FC<{ value: number; suffix?: string }> = ({ value, suffix = "%" }) => {
  if (value === 0) {
    return (
      <span className="text-xs text-gray-400">No change</span>
    );
  }

  const isPositive = value > 0;
  return (
    <span className={`flex items-center text-xs font-medium ${isPositive ? "text-green-600" : "text-red-600"}`}>
      <svg
        className={`w-3 h-3 mr-0.5 ${isPositive ? "" : "rotate-180"}`}
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
      </svg>
      {Math.abs(value)}{suffix}
    </span>
  );
};

export const TodayStatsCards: React.FC<TodayStatsCardsProps> = ({
  stats,
  isLoading = false,
}) => {
  if (isLoading) {
    return (
      <div className="grid grid-cols-3 gap-3">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="bg-white rounded-lg shadow p-4">
            <div className="h-4 bg-gray-200 rounded w-16 animate-pulse mb-2"></div>
            <div className="h-8 bg-gray-200 rounded w-12 animate-pulse mb-1"></div>
            <div className="h-3 bg-gray-200 rounded w-10 animate-pulse"></div>
          </div>
        ))}
      </div>
    );
  }

  const cards = [
    {
      label: "Calls Today",
      value: stats.calls_today,
      trend: stats.calls_today_trend,
      trendLabel: "vs yesterday",
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
        </svg>
      ),
      iconBg: "bg-blue-100",
      iconColor: "text-blue-600",
      format: (v: number) => v.toString(),
    },
    {
      label: "Revenue",
      sublabel: "This Week",
      value: stats.revenue_this_week,
      trend: stats.revenue_this_week_trend,
      trendLabel: "vs last week",
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      iconBg: "bg-green-100",
      iconColor: "text-green-600",
      format: (v: number) => `£${v >= 1000 ? `${(v / 1000).toFixed(1)}k` : v.toFixed(0)}`,
    },
    {
      label: "Reviews",
      sublabel: "This Week",
      value: stats.reviews_this_week,
      trend: stats.reviews_this_week_trend,
      trendLabel: "vs last week",
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
        </svg>
      ),
      iconBg: "bg-yellow-100",
      iconColor: "text-yellow-600",
      format: (v: number) => v.toString(),
    },
  ];

  return (
    <div className="grid grid-cols-3 gap-3">
      {cards.map((card) => (
        <div key={card.label} className="bg-white rounded-lg shadow p-3">
          <div className="flex items-center gap-2 mb-2">
            <div className={`p-1.5 rounded-lg ${card.iconBg} ${card.iconColor}`}>
              {card.icon}
            </div>
          </div>
          <div className="text-2xl font-bold text-gray-900">
            {card.format(card.value)}
          </div>
          <div className="text-xs text-gray-500 mb-1">
            {card.label}
            {card.sublabel && <span className="block text-gray-400">{card.sublabel}</span>}
          </div>
          <TrendBadge value={card.trend} />
        </div>
      ))}
    </div>
  );
};

export default TodayStatsCards;
