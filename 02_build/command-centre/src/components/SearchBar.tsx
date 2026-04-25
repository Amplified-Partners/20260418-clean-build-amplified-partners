import React, { useState, useRef, useEffect } from 'react';

interface SearchResult {
  title: string;
  url: string;
  content: string;
  engine: string;
}

interface SearchResponse {
  query: string;
  results: SearchResult[];
  total: number;
  error?: string;
}

const BASE_URL = 'http://localhost:8001';

export default function SearchBar() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [total, setTotal] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Close results when clicking outside
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setShowResults(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Keyboard shortcut: Cmd+K to focus search
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        inputRef.current?.focus();
      }
      if (e.key === 'Escape') {
        setShowResults(false);
        inputRef.current?.blur();
      }
    }
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setShowResults(true);

    try {
      const res = await fetch(`${BASE_URL}/api/search?q=${encodeURIComponent(query.trim())}`);
      const data: SearchResponse = await res.json();
      setResults(data.results || []);
      setTotal(data.total || 0);
    } catch (err) {
      setResults([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  }

  function getDomain(url: string): string {
    try {
      return new URL(url).hostname.replace('www.', '');
    } catch {
      return url;
    }
  }

  return (
    <div className="search-container" ref={containerRef}>
      <form className="search-form" onSubmit={handleSearch}>
        <div className="search-input-wrapper">
          <svg className="search-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8" />
            <path d="M21 21l-4.35-4.35" />
          </svg>
          <input
            ref={inputRef}
            type="text"
            className="search-input"
            placeholder="Search via Beast SearXNG… ⌘K"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onFocus={() => results.length > 0 && setShowResults(true)}
          />
          {loading && <div className="search-spinner" />}
          {query && !loading && (
            <button
              type="button"
              className="search-clear"
              onClick={() => { setQuery(''); setResults([]); setShowResults(false); }}
            >
              ✕
            </button>
          )}
        </div>
      </form>

      {showResults && (
        <div className="search-results">
          {loading ? (
            <div className="search-results__loading">
              Searching via Beast (10 Gbit)…
            </div>
          ) : results.length === 0 ? (
            <div className="search-results__empty">
              No results for "{query}"
            </div>
          ) : (
            <>
              <div className="search-results__count">
                {total} results via SearXNG
              </div>
              {results.map((r, i) => (
                <a
                  key={i}
                  href={r.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="search-result"
                >
                  <div className="search-result__domain">{getDomain(r.url)}</div>
                  <div className="search-result__title">{r.title}</div>
                  {r.content && (
                    <div className="search-result__snippet">{r.content}</div>
                  )}
                </a>
              ))}
            </>
          )}
        </div>
      )}
    </div>
  );
}
