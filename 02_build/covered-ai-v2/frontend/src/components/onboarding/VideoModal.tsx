'use client';

import { useState, useEffect, useRef } from 'react';
import { X, Volume2, VolumeX } from 'lucide-react';

interface VideoModalProps {
  videoUrl: string;
  title: string;
  onClose: () => void;
  onComplete: () => void;
  autoPlay?: boolean;
  clientId?: string;
  videoId?: string;
}

export function VideoModal({
  videoUrl,
  title,
  onClose,
  onComplete,
  autoPlay = true,
  clientId,
  videoId
}: VideoModalProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const lastUpdateRef = useRef<number>(0);
  const lastSecondsRef = useRef<number>(0);
  const [muted, setMuted] = useState(autoPlay);
  const [progress, setProgress] = useState(0);
  const [canSkip, setCanSkip] = useState(false);
  const [watchId, setWatchId] = useState<string | null>(null);
  const [skipCountdown, setSkipCountdown] = useState(5);

  // Start watch tracking
  useEffect(() => {
    if (clientId && videoId) {
      const token = localStorage.getItem('auth_token');
      fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/training/videos/watch`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {})
        },
        body: JSON.stringify({
          clientId,
          videoId,
          trigger: 'modal',
          location: window.location.pathname
        })
      })
        .then(res => res.json())
        .then(data => setWatchId(data.watchId))
        .catch(console.error);
    }
  }, [clientId, videoId]);

  // Allow skip after 5 seconds with countdown
  useEffect(() => {
    const interval = setInterval(() => {
      setSkipCountdown(prev => {
        if (prev <= 1) {
          setCanSkip(true);
          clearInterval(interval);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  // Track video progress - throttled to 1 API call per 5 seconds
  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleTimeUpdate = () => {
      const percent = (video.currentTime / video.duration) * 100;
      setProgress(percent);

      // Throttle API updates to every 5 seconds AND only if seconds changed
      const now = Date.now();
      const currentSeconds = Math.floor(video.currentTime);
      const shouldUpdate =
        watchId &&
        video.currentTime > 0 &&
        (now - lastUpdateRef.current >= 5000) &&
        (currentSeconds !== lastSecondsRef.current);

      if (shouldUpdate) {
        lastUpdateRef.current = now;
        lastSecondsRef.current = currentSeconds;

        const token = localStorage.getItem('auth_token');
        fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/training/videos/watch/${watchId}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            ...(token ? { Authorization: `Bearer ${token}` } : {})
          },
          body: JSON.stringify({
            watchedSeconds: currentSeconds,
            completed: percent >= 90
          })
        }).catch(console.error);
      }

      if (percent >= 90) {
        onComplete();
      }
    };

    video.addEventListener('timeupdate', handleTimeUpdate);
    return () => video.removeEventListener('timeupdate', handleTimeUpdate);
  }, [onComplete, watchId]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
      <div className="bg-white rounded-2xl overflow-hidden max-w-lg w-full mx-4 shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <h3 className="font-semibold text-gray-900">{title}</h3>
          {canSkip && (
            <button
              onClick={onClose}
              className="p-1 hover:bg-gray-100 rounded-full transition-colors"
            >
              <X className="w-5 h-5 text-gray-500" />
            </button>
          )}
        </div>

        {/* Video */}
        <div className="relative aspect-video bg-black">
          <video
            ref={videoRef}
            src={videoUrl}
            autoPlay={autoPlay}
            muted={muted}
            playsInline
            className="w-full h-full"
          />

          {/* Unmute prompt */}
          {muted && (
            <button
              onClick={() => setMuted(false)}
              className="absolute bottom-4 right-4 flex items-center gap-2
                         bg-white/90 px-3 py-2 rounded-full text-sm font-medium
                         hover:bg-white transition-colors shadow-lg"
            >
              <VolumeX className="w-4 h-4" />
              Tap for sound
            </button>
          )}

          {/* Progress bar */}
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-white/30">
            <div
              className="h-full bg-white transition-all"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Footer */}
        <div className="p-4">
          {!canSkip ? (
            <p className="text-center text-sm text-gray-500">
              Skip available in {skipCountdown}s...
            </p>
          ) : (
            <button
              onClick={onClose}
              className="w-full py-3 bg-blue-600 text-white rounded-xl
                         font-medium hover:bg-blue-700 transition-colors"
            >
              Continue
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
