/**
 * Ewan Admin - Pipeline View
 * 
 * Demo numbers, outreach, funnel.
 * Track leads to conversion.
 */

"use client";

import React, { useState } from "react";
import { Phone, Mail, Calendar, TrendingUp, Users, Target, ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils";

// Mock data
const mockPipeline = {
  demoNumbers: [
    {
      id: "1",
      number: "+441onal234567001",
      assignedTo: "Newcastle Plumbers Search",
      calls: 12,
      hotLeads: 3,
      lastCall: "2h ago",
      status: "active",
    },
    {
      id: "2",
      number: "+441234567002",
      assignedTo: "Facebook Ad - Tradespeople",
      calls: 8,
      hotLeads: 2,
      lastCall: "5h ago",
      status: "active",
    },
    {
      id: "3",
      number: "+441234567003",
      assignedTo: "Google Ads - Emergency Plumber",
      calls: 24,
      hotLeads: 6,
      lastCall: "30m ago",
      status: "active",
    },
  ],
  outreachCampaigns: [
    {
      id: "1",
      name: "Vet Clinics - Newcastle",
      sent: 150,
      opened: 67,
      replied: 12,
      booked: 4,
      status: "active",
    },
    {
      id: "2",
      name: "Salons - North East",
      sent: 200,
      opened: 89,
      replied: 18,
      booked: 6,
      status: "active",
    },
    {
      id: "3",
      name: "Physios - UK Wide",
      sent: 100,
      opened: 42,
      replied: 8,
      booked: 2,
      status: "paused",
    },
  ],
  funnel: {
    visitors: 1247,
    demos: 89,
    signups: 24,
    paid: 12,
  },
  leads: [
    {
      id: "1",
      name: "Newcastle Vets",
      contact: "Dr. Sarah Wilson",
      source: "Outreach",
      stage: "demo-booked",
      value: 297,
      nextAction: "Demo call tomorrow 2pm",
    },
    {
      id: "2",
      name: "Glamour Hair",
      contact: "Michelle Brown",
      source: "Demo Number",
      stage: "warm",
      value: 197,
      nextAction: "Follow up call needed",
    },
    {
      id: "3",
      name: "Peak Physio",
      contact: "James Taylor",
      source: "Referral",
      stage: "negotiation",
      value: 297,
      nextAction: "Waiting on decision",
    },
  ],
};

const stages = [
  { id: "cold", label: "Cold", color: "bg-neutral-500" },
  { id: "warm", label: "Warm", color: "bg-yellow-500" },
  { id: "demo-booked", label: "Demo Booked", color: "bg-blue-500" },
  { id: "negotiation", label: "Negotiation", color: "bg-purple-500" },
  { id: "closed", label: "Closed", color: "bg-green-500" },
];

export default function PipelinePage() {
  const [activeTab, setActiveTab] = useState<"numbers" | "outreach" | "leads">("numbers");
  const { demoNumbers, outreachCampaigns, funnel, leads } = mockPipeline;
  
  return (
    <div className="p-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">Pipeline</h1>
          <p className="text-neutral-500">Demo numbers, outreach, and leads</p>
        </div>
      </div>
      
      {/* Funnel overview */}
      <div className="bg-neutral-900 rounded-xl border border-neutral-800 p-6 mb-8">
        <h2 className="text-lg font-semibold text-white mb-4">Conversion Funnel</h2>
        <div className="flex items-center justify-between">
          {[
            { label: "Visitors", value: funnel.visitors, color: "text-neutral-400" },
            { label: "Demos", value: funnel.demos, color: "text-blue-500" },
            { label: "Signups", value: funnel.signups, color: "text-yellow-500" },
            { label: "Paid", value: funnel.paid, color: "text-green-500" },
          ].map((stage, i, arr) => (
            <React.Fragment key={stage.label}>
              <div className="text-center">
                <p className={`text-3xl font-bold ${stage.color}`}>{stage.value}</p>
                <p className="text-sm text-neutral-500">{stage.label}</p>
                {i > 0 && (
                  <p className="text-xs text-neutral-600 mt-1">
                    {Math.round((stage.value / arr[i - 1].value) * 100)}% conv
                  </p>
                )}
              </div>
              {i < arr.length - 1 && (
                <ArrowRight className="w-6 h-6 text-neutral-700" />
              )}
            </React.Fragment>
          ))}
        </div>
      </div>
      
      {/* Tabs */}
      <div className="flex gap-2 mb-6">
        {[
          { id: "numbers", label: "Demo Numbers", icon: Phone },
          { id: "outreach", label: "Outreach", icon: Mail },
          { id: "leads", label: "Leads", icon: Users },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as typeof activeTab)}
            className={cn(
              "flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors",
              activeTab === tab.id
                ? "bg-blue-600 text-white"
                : "bg-neutral-900 text-neutral-400 hover:text-white border border-neutral-800"
            )}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
          </button>
        ))}
      </div>
      
      {/* Demo Numbers */}
      {activeTab === "numbers" && (
        <div className="bg-neutral-900 rounded-xl border border-neutral-800 overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b border-neutral-800">
                <th className="text-left px-6 py-4 text-xs font-medium text-neutral-500 uppercase">Number</th>
                <th className="text-left px-6 py-4 text-xs font-medium text-neutral-500 uppercase">Assigned To</th>
                <th className="text-left px-6 py-4 text-xs font-medium text-neutral-500 uppercase">Calls</th>
                <th className="text-left px-6 py-4 text-xs font-medium text-neutral-500 uppercase">Hot Leads</th>
                <th className="text-left px-6 py-4 text-xs font-medium text-neutral-500 uppercase">Last Call</th>
                <th className="text-left px-6 py-4 text-xs font-medium text-neutral-500 uppercase">Status</th>
              </tr>
            </thead>
            <tbody>
              {demoNumbers.map((num) => (
                <tr key={num.id} className="border-b border-neutral-800 hover:bg-neutral-800/50">
                  <td className="px-6 py-4 font-mono text-white">{num.number}</td>
                  <td className="px-6 py-4 text-neutral-300">{num.assignedTo}</td>
                  <td className="px-6 py-4 text-neutral-400">{num.calls}</td>
                  <td className="px-6 py-4">
                    <span className="text-green-500 font-semibold">{num.hotLeads}</span>
                  </td>
                  <td className="px-6 py-4 text-neutral-500">{num.lastCall}</td>
                  <td className="px-6 py-4">
                    <span className={cn(
                      "px-2 py-1 text-xs rounded",
                      num.status === "active" ? "bg-green-500/10 text-green-500" : "bg-neutral-500/10 text-neutral-500"
                    )}>
                      {num.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      
      {/* Outreach Campaigns */}
      {activeTab === "outreach" && (
        <div className="bg-neutral-900 rounded-xl border border-neutral-800 overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b border-neutral-800">
                <th className="text-left px-6 py-4 text-xs font-medium text-neutral-500 uppercase">Campaign</th>
                <th className="text-left px-6 py-4 text-xs font-medium text-neutral-500 uppercase">Sent</th>
                <th className="text-left px-6 py-4 text-xs font-medium text-neutral-500 uppercase">Opened</th>
                <th className="text-left px-6 py-4 text-xs font-medium text-neutral-500 uppercase">Replied</th>
                <th className="text-left px-6 py-4 text-xs font-medium text-neutral-500 uppercase">Booked</th>
                <th className="text-left px-6 py-4 text-xs font-medium text-neutral-500 uppercase">Status</th>
              </tr>
            </thead>
            <tbody>
              {outreachCampaigns.map((campaign) => (
                <tr key={campaign.id} className="border-b border-neutral-800 hover:bg-neutral-800/50">
                  <td className="px-6 py-4 text-white font-medium">{campaign.name}</td>
                  <td className="px-6 py-4 text-neutral-400">{campaign.sent}</td>
                  <td className="px-6 py-4">
                    <span className="text-neutral-300">{campaign.opened}</span>
                    <span className="text-neutral-600 text-sm ml-1">
                      ({Math.round((campaign.opened / campaign.sent) * 100)}%)
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-neutral-300">{campaign.replied}</span>
                    <span className="text-neutral-600 text-sm ml-1">
                      ({Math.round((campaign.replied / campaign.sent) * 100)}%)
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-green-500 font-semibold">{campaign.booked}</span>
                  </td>
                  <td className="px-6 py-4">
                    <span className={cn(
                      "px-2 py-1 text-xs rounded",
                      campaign.status === "active" ? "bg-green-500/10 text-green-500" : "bg-yellow-500/10 text-yellow-500"
                    )}>
                      {campaign.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      
      {/* Leads */}
      {activeTab === "leads" && (
        <div className="space-y-4">
          {/* Stage filters */}
          <div className="flex gap-2 mb-4">
            {stages.map((stage) => (
              <button
                key={stage.id}
                className="flex items-center gap-2 px-3 py-1.5 bg-neutral-800 rounded-lg text-sm text-neutral-400 hover:text-white"
              >
                <div className={`w-2 h-2 rounded-full ${stage.color}`} />
                {stage.label}
              </button>
            ))}
          </div>
          
          {/* Leads list */}
          <div className="bg-neutral-900 rounded-xl border border-neutral-800 overflow-hidden">
            {leads.map((lead, i) => (
              <div
                key={lead.id}
                className={cn(
                  "p-4 hover:bg-neutral-800/50 transition-colors",
                  i < leads.length - 1 && "border-b border-neutral-800"
                )}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-white font-medium">{lead.name}</p>
                    <p className="text-sm text-neutral-500">{lead.contact}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-white font-semibold">£{lead.value}/mo</p>
                    <span className={cn(
                      "px-2 py-0.5 text-xs rounded",
                      lead.stage === "demo-booked" ? "bg-blue-500/10 text-blue-500" :
                      lead.stage === "warm" ? "bg-yellow-500/10 text-yellow-500" :
                      lead.stage === "negotiation" ? "bg-purple-500/10 text-purple-500" :
                      "bg-neutral-500/10 text-neutral-500"
                    )}>
                      {lead.stage.replace("-", " ")}
                    </span>
                  </div>
                </div>
                <div className="flex items-center justify-between mt-3">
                  <span className="text-xs text-neutral-600">Source: {lead.source}</span>
                  <span className="text-xs text-blue-500">{lead.nextAction}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
