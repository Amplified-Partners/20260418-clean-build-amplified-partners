"use client";

import React, { useEffect, useState } from "react";
import { Plus, RefreshCw, Play, Pause, Download } from "lucide-react";
import { outreachApi, OutreachCampaign } from "@/lib/api";

export default function AdminOutreachPage() {
  const [campaigns, setCampaigns] = useState<OutreachCampaign[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCampaigns();
  }, []);

  const loadCampaigns = async () => {
    setLoading(true);
    try {
      const data = await outreachApi.listCampaigns();
      setCampaigns(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleStart = async (id: string) => {
    await outreachApi.startCampaign(id);
    loadCampaigns();
  };

  const handlePause = async (id: string) => {
    await outreachApi.pauseCampaign(id);
    loadCampaigns();
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Outreach Campaigns</h1>
          <p className="text-gray-500">Email campaigns and tracking</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={loadCampaigns}
            className="flex items-center gap-2 px-4 py-2 bg-white border rounded-lg hover:bg-gray-50"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            Refresh
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            <Plus className="w-4 h-4" />
            New Campaign
          </button>
        </div>
      </div>

      {/* Campaigns Table */}
      <div className="bg-white rounded-xl shadow-sm overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Campaign</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Leads</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Sent</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Opened</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Replied</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Converted</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {campaigns.map((campaign) => (
              <tr key={campaign.id} className="hover:bg-gray-50">
                <td className="px-4 py-3">
                  <p className="font-medium text-gray-900">{campaign.name}</p>
                  <p className="text-sm text-gray-500">{campaign.template}</p>
                </td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    campaign.status === "active" ? "bg-green-100 text-green-800" :
                    campaign.status === "paused" ? "bg-yellow-100 text-yellow-800" :
                    campaign.status === "completed" ? "bg-blue-100 text-blue-800" :
                    "bg-gray-100 text-gray-800"
                  }`}>
                    {campaign.status}
                  </span>
                </td>
                <td className="px-4 py-3 text-sm text-gray-600">{campaign.total_leads}</td>
                <td className="px-4 py-3 text-sm text-gray-600">{campaign.sent}</td>
                <td className="px-4 py-3 text-sm text-gray-600">
                  {campaign.opened} ({campaign.sent ? Math.round(campaign.opened / campaign.sent * 100) : 0}%)
                </td>
                <td className="px-4 py-3 text-sm text-gray-600">{campaign.replied}</td>
                <td className="px-4 py-3 text-sm text-gray-600">{campaign.converted}</td>
                <td className="px-4 py-3">
                  <div className="flex gap-1">
                    {campaign.status === "active" ? (
                      <button
                        onClick={() => handlePause(campaign.id)}
                        className="p-2 hover:bg-gray-100 rounded-lg"
                        title="Pause"
                      >
                        <Pause className="w-4 h-4 text-gray-500" />
                      </button>
                    ) : campaign.status === "draft" || campaign.status === "paused" ? (
                      <button
                        onClick={() => handleStart(campaign.id)}
                        className="p-2 hover:bg-gray-100 rounded-lg"
                        title="Start"
                      >
                        <Play className="w-4 h-4 text-gray-500" />
                      </button>
                    ) : null}
                    <a
                      href={outreachApi.exportCampaign(campaign.id)}
                      className="p-2 hover:bg-gray-100 rounded-lg"
                      title="Export CSV"
                    >
                      <Download className="w-4 h-4 text-gray-500" />
                    </a>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {campaigns.length === 0 && (
          <div className="p-12 text-center text-gray-500">
            {loading ? "Loading..." : "No campaigns found"}
          </div>
        )}
      </div>
    </div>
  );
}
