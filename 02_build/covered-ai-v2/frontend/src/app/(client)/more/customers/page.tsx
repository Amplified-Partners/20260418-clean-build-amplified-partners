/**
 * Client App - Customers Page
 * 
 * Your customer list.
 * Search, view, and manage customers.
 */

"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Search, Phone, Plus } from "lucide-react";
import { Header, EmptyState } from "@/components/client-app";

// Mock data
const mockCustomers = [
  {
    id: "1",
    name: "Mrs Thompson",
    phone: "+447712345678",
    email: "thompson@email.com",
    address: "42 Oak Road, NE3 4AB",
    totalJobs: 3,
    totalSpend: 892,
    lastJob: "2 days ago",
  },
  {
    id: "2",
    name: "Dave Wilson",
    phone: "+447712345679",
    address: "15 High Street, NE1 2XY",
    totalJobs: 1,
    totalSpend: 340,
    lastJob: "1 week ago",
  },
  {
    id: "3",
    name: "Sarah Jones",
    phone: "+447712345680",
    email: "sarah.j@email.com",
    address: "7 Park Lane, NE4 5CD",
    totalJobs: 5,
    totalSpend: 2150,
    lastJob: "2 weeks ago",
  },
  {
    id: "4",
    name: "Mr Abbas",
    phone: "+447712345681",
    address: "82 High Street, NE1 2XY",
    totalJobs: 2,
    totalSpend: 460,
    lastJob: "Today",
  },
  {
    id: "5",
    name: "Mrs Chen",
    phone: "+447712345682",
    email: "mchen@email.com",
    address: "14 Park Road, NE3 4AB",
    totalJobs: 1,
    totalSpend: 180,
    lastJob: "Today",
  },
  {
    id: "6",
    name: "Johnson family",
    phone: "+447712345683",
    address: "7 Oak Avenue, NE4 5CD",
    totalJobs: 2,
    totalSpend: 3400,
    lastJob: "Tomorrow",
  },
];

export default function CustomersPage() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("");
  
  const filteredCustomers = mockCustomers.filter(customer =>
    customer.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    customer.phone.includes(searchQuery) ||
    customer.address?.toLowerCase().includes(searchQuery.toLowerCase())
  );
  
  // Sort by last job (most recent first)
  const sortedCustomers = [...filteredCustomers].sort((a, b) => {
    const order = ["Today", "Tomorrow", "2 days ago", "1 week ago", "2 weeks ago"];
    return order.indexOf(a.lastJob) - order.indexOf(b.lastJob);
  });
  
  return (
    <div className="min-h-screen bg-neutral-50">
      <Header
        title="Customers"
        showBack
        onBack={() => router.back()}
        rightContent={
          <button
            onClick={() => router.push("/more/customers/new")}
            className="p-2 text-blue-600"
          >
            <Plus className="w-6 h-6" />
          </button>
        }
      />
      
      {/* Search */}
      <div className="px-5 py-4 bg-white border-b border-neutral-200">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-400" />
          <input
            type="text"
            placeholder="Search customers..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-3 bg-neutral-100 rounded-xl text-neutral-900 placeholder:text-neutral-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
      
      {/* Stats */}
      <div className="px-5 py-4 flex gap-4">
        <div className="flex-1 bg-white rounded-xl p-4 border border-neutral-200">
          <p className="text-2xl font-bold text-neutral-900">{mockCustomers.length}</p>
          <p className="text-xs text-neutral-500">Total customers</p>
        </div>
        <div className="flex-1 bg-white rounded-xl p-4 border border-neutral-200">
          <p className="text-2xl font-bold text-neutral-900">
            £{mockCustomers.reduce((sum, c) => sum + c.totalSpend, 0).toLocaleString()}
          </p>
          <p className="text-xs text-neutral-500">Total revenue</p>
        </div>
      </div>
      
      {/* Customer list */}
      {sortedCustomers.length === 0 ? (
        <EmptyState
          icon="👥"
          title={searchQuery ? "No customers found" : "No customers yet"}
          description={searchQuery ? "Try a different search" : "Customers will appear here after their first job."}
        />
      ) : (
        <div className="px-5 pb-8">
          <div className="bg-white rounded-2xl border border-neutral-200 overflow-hidden">
            {sortedCustomers.map((customer, i) => (
              <React.Fragment key={customer.id}>
                <button
                  onClick={() => router.push(`/more/customers/${customer.id}`)}
                  className="w-full p-4 text-left hover:bg-neutral-50 transition-colors"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="font-medium text-neutral-900">{customer.name}</p>
                      <p className="text-sm text-neutral-500 mt-0.5">
                        {customer.totalJobs} job{customer.totalJobs !== 1 ? "s" : ""} • £{customer.totalSpend.toLocaleString()}
                      </p>
                    </div>
                    <a
                      href={`tel:${customer.phone}`}
                      onClick={(e) => e.stopPropagation()}
                      className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                    >
                      <Phone className="w-5 h-5" />
                    </a>
                  </div>
                  <p className="text-xs text-neutral-400 mt-2">
                    Last job: {customer.lastJob}
                  </p>
                </button>
                {i < sortedCustomers.length - 1 && (
                  <div className="h-px bg-neutral-100 mx-4" />
                )}
              </React.Fragment>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
