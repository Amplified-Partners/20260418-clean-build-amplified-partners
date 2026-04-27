"use client";

import React, { useEffect, useState } from "react";
import { RefreshCw, ChevronDown, ChevronRight, RotateCcw } from "lucide-react";
import { eventsApi, EventLogItem } from "@/lib/api";

export default function AdminEventsPage() {
  const [events, setEvents] = useState<EventLogItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState({ source: "", status: "" });
  const [expandedId, setExpandedId] = useState<string | null>(null);

  useEffect(() => {
    loadEvents();
  }, [filter]);

  const loadEvents = async () => {
    setLoading(true);
    try {
      const data = await eventsApi.list({
        source: filter.source || undefined,
        status: filter.status || undefined,
        limit: 100,
      });
      setEvents(data.events || []);
    } catch (err) {
      console.error(err);
      setEvents([]);
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = async (eventId: string) => {
    try {
      await eventsApi.retry(eventId);
      loadEvents();
    } catch (err) {
      console.error("Failed to retry event:", err);
    }
  };

  const sourceColors: Record<string, string> = {
    vapi: "bg-purple-100 text-purple-800",
    twilio: "bg-red-100 text-red-800",
    stripe: "bg-blue-100 text-blue-800",
    resend: "bg-green-100 text-green-800",
  };

  const statusColors: Record<string, string> = {
    received: "bg-yellow-100 text-yellow-800",
    processed: "bg-green-100 text-green-800",
    failed: "bg-red-100 text-red-800",
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Event Log</h1>
          <p className="text-gray-500">Webhook events and processing status</p>
        </div>
        <button
          onClick={loadEvents}
          className="flex items-center gap-2 px-4 py-2 bg-white border rounded-lg hover:bg-gray-50"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          Refresh
        </button>
      </div>

      {/* Filters */}
      <div className="flex gap-4">
        <select
          value={filter.source}
          onChange={(e) => setFilter({ ...filter, source: e.target.value })}
          className="px-3 py-2 border rounded-lg"
        >
          <option value="">All Sources</option>
          <option value="vapi">Vapi</option>
          <option value="twilio">Twilio</option>
          <option value="stripe">Stripe</option>
          <option value="resend">Resend</option>
        </select>
        <select
          value={filter.status}
          onChange={(e) => setFilter({ ...filter, status: e.target.value })}
          className="px-3 py-2 border rounded-lg"
        >
          <option value="">All Statuses</option>
          <option value="received">Received</option>
          <option value="processed">Processed</option>
          <option value="failed">Failed</option>
        </select>
      </div>

      {/* Events List */}
      <div className="bg-white rounded-xl shadow-sm divide-y">
        {events.map((event) => (
          <div key={event.id}>
            <div
              className="px-4 py-3 flex items-center gap-4 hover:bg-gray-50 cursor-pointer"
              onClick={() => setExpandedId(expandedId === event.id ? null : event.id)}
            >
              {expandedId === event.id ? (
                <ChevronDown className="w-4 h-4 text-gray-400" />
              ) : (
                <ChevronRight className="w-4 h-4 text-gray-400" />
              )}
              <span className={`px-2 py-1 rounded text-xs font-medium ${sourceColors[event.source] || "bg-gray-100"}`}>
                {event.source}
              </span>
              <span className="flex-1 text-sm font-mono text-gray-900">
                {event.event_type}
              </span>
              <span className={`px-2 py-1 rounded text-xs font-medium ${statusColors[event.status] || "bg-gray-100"}`}>
                {event.status}
              </span>
              <span className="text-sm text-gray-500">
                {new Date(event.created_at).toLocaleTimeString()}
              </span>
            </div>
            {expandedId === event.id && (
              <div className="px-4 py-3 bg-gray-50 border-t">
                <pre className="text-xs overflow-auto max-h-96 p-3 bg-gray-900 text-gray-100 rounded-lg">
                  {JSON.stringify(event.payload, null, 2)}
                </pre>
                {event.error && (
                  <div className="mt-2 p-3 bg-red-50 text-red-800 rounded-lg text-sm flex items-center justify-between">
                    <div>
                      <strong>Error:</strong> {event.error}
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleRetry(event.id);
                      }}
                      className="flex items-center gap-1 px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700"
                    >
                      <RotateCcw className="w-3 h-3" />
                      Retry
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}

        {events.length === 0 && (
          <div className="p-12 text-center text-gray-500">
            {loading ? "Loading..." : "No events found"}
          </div>
        )}
      </div>
    </div>
  );
}
