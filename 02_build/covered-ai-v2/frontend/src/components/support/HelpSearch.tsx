'use client';

import { useState, useCallback, useRef, useEffect } from 'react';
import { Search, Book, PlayCircle, MessageCircle, ExternalLink } from 'lucide-react';
import Link from 'next/link';

interface SearchResult {
  id: string;
  title: string;
  snippet: string;
  type: 'article' | 'video' | 'action';
  category: string;
  videoId?: string;
  duration?: number;
}

interface HelpSearchProps {
  onVideoClick?: (videoId: string) => void;
  placeholder?: string;
}

// API URL constant
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export function HelpSearch({
  onVideoClick,
  placeholder = 'Search help articles, videos, or ask a question...'
}: HelpSearchProps) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      abortControllerRef.current?.abort();
    };
  }, []);

  // Memoized search function with proper debounce
  const performSearch = useCallback(async (q: string) => {
    if (q.length < 2) {
      setResults([]);
      setLoading(false);
      return;
    }

    // Cancel any pending request
    abortControllerRef.current?.abort();
    abortControllerRef.current = new AbortController();

    try {
      const token = localStorage.getItem('auth_token');
      const res = await fetch(`${API_URL}/api/v1/training/help/search?q=${encodeURIComponent(q)}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        signal: abortControllerRef.current.signal
      });
      const data = await res.json();
      setResults(data.results);
    } catch (error) {
      if (error instanceof Error && error.name === 'AbortError') return;
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);

    // Clear existing timeout
    if (timeoutRef.current) clearTimeout(timeoutRef.current);

    if (value.length >= 2) {
      setLoading(true);
      // Debounce the search
      timeoutRef.current = setTimeout(() => performSearch(value), 300);
    } else {
      setResults([]);
      setLoading(false);
    }
  }, [performSearch]);

  const getIcon = (type: string) => {
    switch (type) {
      case 'video':
        return <PlayCircle className="w-5 h-5 text-blue-500" />;
      case 'action':
        return <ExternalLink className="w-5 h-5 text-green-500" />;
      default:
        return <Book className="w-5 h-5 text-gray-400" />;
    }
  };

  return (
    <div className="relative">
      <div className="relative">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="text"
          value={query}
          onChange={handleChange}
          onFocus={() => setShowResults(true)}
          onBlur={() => setTimeout(() => setShowResults(false), 200)}
          placeholder={placeholder}
          className="w-full pl-12 pr-4 py-3 border border-gray-200 rounded-xl
                     focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                     outline-none transition-all"
        />
      </div>

      {/* Results dropdown */}
      {showResults && (results.length > 0 || loading) && query.length >= 2 && (
        <div
          className="absolute top-full left-0 right-0 mt-2 bg-white
                      rounded-xl border border-gray-200 shadow-lg z-10
                      max-h-96 overflow-auto"
        >
          {loading ? (
            <div className="p-4 text-center text-gray-500">Searching...</div>
          ) : (
            <div className="p-2">
              {results.map((result) => (
                <div key={result.id}>
                  {result.type === 'video' && onVideoClick ? (
                    <button
                      onClick={() => onVideoClick(result.videoId!)}
                      className="w-full flex items-start gap-3 p-3 rounded-lg
                                 hover:bg-gray-50 transition-colors text-left"
                    >
                      <div className="mt-0.5">{getIcon(result.type)}</div>
                      <div className="flex-1 min-w-0">
                        <h4 className="font-medium text-gray-900 truncate">
                          {result.title}
                        </h4>
                        <p className="text-sm text-gray-500 line-clamp-2">
                          {result.snippet}
                        </p>
                        {result.duration && (
                          <span className="text-xs text-gray-400 mt-1">
                            {Math.round(result.duration / 60)} min video
                          </span>
                        )}
                      </div>
                    </button>
                  ) : (
                    <Link
                      href={`/help/${result.id}`}
                      className="flex items-start gap-3 p-3 rounded-lg
                                 hover:bg-gray-50 transition-colors"
                    >
                      <div className="mt-0.5">{getIcon(result.type)}</div>
                      <div className="flex-1 min-w-0">
                        <h4 className="font-medium text-gray-900 truncate">
                          {result.title}
                        </h4>
                        <p className="text-sm text-gray-500 line-clamp-2">
                          {result.snippet}
                        </p>
                      </div>
                    </Link>
                  )}
                </div>
              ))}

              {/* Can't find what you need? */}
              <div className="border-t border-gray-100 mt-2 pt-2">
                <Link
                  href="/support/chat"
                  className="flex items-center gap-3 p-3 rounded-lg
                             hover:bg-gray-50 transition-colors"
                >
                  <MessageCircle className="w-5 h-5 text-blue-500" />
                  <span className="text-sm font-medium text-blue-600">
                    Chat with support
                  </span>
                </Link>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
