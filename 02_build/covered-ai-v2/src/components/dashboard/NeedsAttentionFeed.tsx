/**
 * NeedsAttentionFeed Component
 *
 * Priority queue showing items that need action:
 * - Emergency leads (priority: 100)
 * - Callbacks due (priority: 70)
 * - Overdue invoices (priority: 50)
 * - Stale leads (priority: 30)
 *
 * Each item has one-tap action buttons.
 */

import React from "react";

interface AttentionItem {
  id: string;
  item_type: string;
  item_id: string;
  priority: number;
  category: string;
  title: string;
  subtitle?: string;
  action_type: string;
  action_label: string;
  action_data?: Record<string, any>;
  created_at: string;
}

interface NeedsAttentionFeedProps {
  items: AttentionItem[];
  onAction: (item: AttentionItem) => void;
  onDismiss: (itemId: string) => void;
  isLoading?: boolean;
}

const CATEGORY_CONFIG: Record<string, { icon: string; color: string; bgColor: string }> = {
  emergency: {
    icon: "M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z",
    color: "text-red-600",
    bgColor: "bg-red-50 border-red-200",
  },
  callback_due: {
    icon: "M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z",
    color: "text-orange-600",
    bgColor: "bg-orange-50 border-orange-200",
  },
  invoice_overdue: {
    icon: "M9 14l6-6m-5.5.5h.01m4.99 5h.01M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16l3.5-2 3.5 2 3.5-2 3.5 2z",
    color: "text-amber-600",
    bgColor: "bg-amber-50 border-amber-200",
  },
  lead_stale: {
    icon: "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z",
    color: "text-gray-600",
    bgColor: "bg-gray-50 border-gray-200",
  },
};

const ACTION_ICONS: Record<string, string> = {
  call: "M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z",
  chase: "M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z",
  send: "M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z",
  view: "M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z",
};

export const NeedsAttentionFeed: React.FC<NeedsAttentionFeedProps> = ({
  items,
  onAction,
  onDismiss,
  isLoading = false,
}) => {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow">
        <div className="p-4 border-b">
          <div className="h-5 bg-gray-200 rounded w-32 animate-pulse"></div>
        </div>
        <div className="p-4 space-y-3">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="h-20 bg-gray-100 rounded-lg animate-pulse"></div>
          ))}
        </div>
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="text-center">
          <div className="w-12 h-12 mx-auto mb-3 bg-green-100 rounded-full flex items-center justify-center">
            <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h3 className="text-sm font-medium text-gray-900">All caught up!</h3>
          <p className="text-xs text-gray-500 mt-1">No urgent items need your attention</p>
        </div>
      </div>
    );
  }

  const getTimeAgo = (dateStr: string) => {
    const diff = Date.now() - new Date(dateStr).getTime();
    const minutes = Math.floor(diff / 60000);
    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    return `${days}d ago`;
  };

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="p-4 border-b flex justify-between items-center">
        <div className="flex items-center gap-2">
          <span className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
          </span>
          <h2 className="font-semibold text-gray-900">Needs Attention</h2>
        </div>
        <span className="text-sm text-gray-500">{items.length} items</span>
      </div>

      <div className="divide-y divide-gray-100">
        {items.map((item) => {
          const config = CATEGORY_CONFIG[item.category] || CATEGORY_CONFIG.lead_stale;
          const actionIcon = ACTION_ICONS[item.action_type] || ACTION_ICONS.view;

          return (
            <div
              key={item.id}
              className={`p-4 ${config.bgColor} border-l-4`}
            >
              <div className="flex items-start gap-3">
                {/* Icon */}
                <div className={`mt-0.5 ${config.color}`}>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={config.icon.split(" ")[0].startsWith("M") ? config.icon : ""} />
                  </svg>
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <h3 className="text-sm font-medium text-gray-900 truncate">
                        {item.title}
                      </h3>
                      {item.subtitle && (
                        <p className="text-xs text-gray-500 mt-0.5">{item.subtitle}</p>
                      )}
                    </div>
                    <span className="text-xs text-gray-400 whitespace-nowrap">
                      {getTimeAgo(item.created_at)}
                    </span>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2 mt-3">
                    <button
                      onClick={() => onAction(item)}
                      className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-full ${
                        item.category === "emergency"
                          ? "bg-red-600 text-white hover:bg-red-700"
                          : "bg-blue-600 text-white hover:bg-blue-700"
                      } transition-colors`}
                    >
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={actionIcon} />
                      </svg>
                      {item.action_label}
                    </button>
                    <button
                      onClick={() => onDismiss(item.id)}
                      className="px-3 py-1.5 text-xs font-medium text-gray-600 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors"
                    >
                      Dismiss
                    </button>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default NeedsAttentionFeed;
