/**
 * Client App - Help Page
 * 
 * Support and guides.
 * Simple, searchable, helpful.
 */

"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Search, MessageCircle, Phone, Mail } from "lucide-react";
import { Header } from "@/components/client-app";

const helpArticles = [
  {
    id: "setup",
    category: "Getting Started",
    title: "How to set up call forwarding",
    summary: "Step-by-step guide for all UK networks",
  },
  {
    id: "emergency",
    category: "Getting Started",
    title: "Setting up emergency keywords",
    summary: "Tell Gemma what counts as urgent",
  },
  {
    id: "greeting",
    category: "Getting Started",
    title: "Customising your greeting",
    summary: "Make Gemma sound like your business",
  },
  {
    id: "callbacks",
    category: "Using Covered",
    title: "Managing callbacks",
    summary: "Never miss a follow-up",
  },
  {
    id: "invoices",
    category: "Using Covered",
    title: "Creating and sending invoices",
    summary: "Get paid faster",
  },
  {
    id: "reviews",
    category: "Using Covered",
    title: "Getting more Google reviews",
    summary: "Build your reputation automatically",
  },
  {
    id: "billing",
    category: "Account",
    title: "Managing your subscription",
    summary: "Plans, billing, and invoices",
  },
  {
    id: "cancel",
    category: "Account",
    title: "How to cancel",
    summary: "We're sorry to see you go",
  },
];

const categories = [...new Set(helpArticles.map(a => a.category))];

export default function HelpPage() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("");
  
  const filteredArticles = helpArticles.filter(article =>
    article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    article.summary.toLowerCase().includes(searchQuery.toLowerCase())
  );
  
  const groupedArticles = categories.reduce((acc, category) => {
    const articles = filteredArticles.filter(a => a.category === category);
    if (articles.length > 0) {
      acc[category] = articles;
    }
    return acc;
  }, {} as Record<string, typeof helpArticles>);
  
  return (
    <div className="min-h-screen bg-neutral-50">
      <Header
        title="Help"
        showBack
        onBack={() => router.back()}
      />
      
      {/* Search */}
      <div className="px-5 py-4 bg-white border-b border-neutral-200">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-400" />
          <input
            type="text"
            placeholder="Search help articles..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-3 bg-neutral-100 rounded-xl text-neutral-900 placeholder:text-neutral-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
      
      {/* Articles */}
      <div className="pb-8">
        {Object.entries(groupedArticles).map(([category, articles]) => (
          <div key={category}>
            <h2 className="px-5 py-3 text-xs font-semibold text-neutral-500 uppercase tracking-wider">
              {category}
            </h2>
            <div className="bg-white border-y border-neutral-200">
              {articles.map((article, i) => (
                <React.Fragment key={article.id}>
                  <button
                    onClick={() => router.push(`/more/help/${article.id}`)}
                    className="w-full px-5 py-4 text-left hover:bg-neutral-50 transition-colors"
                  >
                    <p className="font-medium text-neutral-900">{article.title}</p>
                    <p className="text-sm text-neutral-500 mt-0.5">{article.summary}</p>
                  </button>
                  {i < articles.length - 1 && (
                    <div className="h-px bg-neutral-100 mx-5" />
                  )}
                </React.Fragment>
              ))}
            </div>
          </div>
        ))}
        
        {filteredArticles.length === 0 && (
          <div className="px-5 py-12 text-center">
            <p className="text-neutral-500">No articles found</p>
          </div>
        )}
      </div>
      
      {/* Contact Support */}
      <div className="px-5 pb-8">
        <h2 className="text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-3">
          Still need help?
        </h2>
        <div className="bg-white rounded-2xl border border-neutral-200 overflow-hidden">
          <a
            href="mailto:support@covered.ai"
            className="flex items-center gap-4 px-5 py-4 hover:bg-neutral-50 transition-colors"
          >
            <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
              <Mail className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <p className="font-medium text-neutral-900">Email support</p>
              <p className="text-sm text-neutral-500">support@covered.ai</p>
            </div>
          </a>
          <div className="h-px bg-neutral-100 mx-5" />
          <a
            href="tel:+441onal917432732"
            className="flex items-center gap-4 px-5 py-4 hover:bg-neutral-50 transition-colors"
          >
            <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
              <Phone className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <p className="font-medium text-neutral-900">Call us</p>
              <p className="text-sm text-neutral-500">Mon-Fri, 9am-5pm</p>
            </div>
          </a>
        </div>
      </div>
    </div>
  );
}
