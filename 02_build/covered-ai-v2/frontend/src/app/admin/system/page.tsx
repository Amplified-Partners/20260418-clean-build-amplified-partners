"use client";

import React, { useEffect, useState } from "react";
import { CheckCircle, XCircle, RefreshCw, Server, Database, Phone, Mail, CreditCard, LucideIcon } from "lucide-react";

interface ServiceStatus {
  status: string;
  latency?: number;
  connections?: number;
  balance?: number;
  assistants?: number;
}

interface SystemStatus {
  api: ServiceStatus;
  database: ServiceStatus;
  twilio: ServiceStatus;
  vapi: ServiceStatus;
  resend: ServiceStatus;
  stripe: ServiceStatus;
}

export default function AdminSystemPage() {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkStatus();
  }, []);

  const checkStatus = async () => {
    setLoading(true);
    // TODO: Implement actual health checks via API
    setStatus({
      api: { status: "healthy", latency: 45 },
      database: { status: "healthy", connections: 2 },
      twilio: { status: "healthy", balance: 50.0 },
      vapi: { status: "healthy", assistants: 3 },
      resend: { status: "healthy" },
      stripe: { status: "healthy" },
    });
    setLoading(false);
  };

  const services: { key: keyof SystemStatus; label: string; icon: LucideIcon; extra: string | null }[] = [
    { key: "api", label: "API Server", icon: Server, extra: status?.api.latency ? `${status.api.latency}ms` : null },
    { key: "database", label: "Database", icon: Database, extra: status?.database.connections ? `${status.database.connections} connections` : null },
    { key: "twilio", label: "Twilio", icon: Phone, extra: status?.twilio.balance ? `$${status.twilio.balance.toFixed(2)} balance` : null },
    { key: "vapi", label: "Vapi", icon: Phone, extra: status?.vapi.assistants ? `${status.vapi.assistants} assistants` : null },
    { key: "resend", label: "Resend", icon: Mail, extra: null },
    { key: "stripe", label: "Stripe", icon: CreditCard, extra: null },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">System Status</h1>
          <p className="text-gray-500">Service health and configuration</p>
        </div>
        <button
          onClick={checkStatus}
          className="flex items-center gap-2 px-4 py-2 bg-white border rounded-lg hover:bg-gray-50"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          Check Status
        </button>
      </div>

      {/* Service Status Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {services.map((service) => {
          const serviceStatus = status?.[service.key];
          const isHealthy = serviceStatus?.status === "healthy";

          return (
            <div key={service.key} className="bg-white rounded-xl shadow-sm p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className={`p-2 rounded-lg ${isHealthy ? "bg-green-50" : "bg-red-50"}`}>
                    <service.icon className={`w-5 h-5 ${isHealthy ? "text-green-600" : "text-red-600"}`} />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{service.label}</p>
                    {service.extra && (
                      <p className="text-sm text-gray-500">{service.extra}</p>
                    )}
                  </div>
                </div>
                {isHealthy ? (
                  <CheckCircle className="w-5 h-5 text-green-600" />
                ) : (
                  <XCircle className="w-5 h-5 text-red-600" />
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Environment Info */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h2 className="font-semibold text-gray-900 mb-4">Environment</h2>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-gray-500">API URL</p>
            <p className="font-mono text-gray-900">{process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}</p>
          </div>
          <div>
            <p className="text-gray-500">Environment</p>
            <p className="font-mono text-gray-900">{process.env.NODE_ENV}</p>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h2 className="font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="flex gap-3 flex-wrap">
          <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 text-sm">
            Clear Cache
          </button>
          <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 text-sm">
            Refresh Tokens
          </button>
          <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 text-sm">
            Run Migrations
          </button>
          <button className="px-4 py-2 bg-red-50 text-red-700 rounded-lg hover:bg-red-100 text-sm">
            Expire Demo Numbers
          </button>
        </div>
      </div>
    </div>
  );
}
