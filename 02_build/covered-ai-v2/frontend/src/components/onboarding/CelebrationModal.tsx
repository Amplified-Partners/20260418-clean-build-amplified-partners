'use client';

import { useEffect, useState } from 'react';
import { Star, ArrowRight, PartyPopper, Sparkles } from 'lucide-react';
import Link from 'next/link';

interface CelebrationModalProps {
  title: string;
  message: string;
  icon?: 'star' | 'party' | 'sparkles';
  nextAction?: {
    label: string;
    href: string;
  };
  onClose: () => void;
}

export function CelebrationModal({
  title,
  message,
  icon = 'star',
  nextAction,
  onClose
}: CelebrationModalProps) {
  const [showContent, setShowContent] = useState(false);

  useEffect(() => {
    // Fire confetti
    fireConfetti();

    // Animate content in
    setTimeout(() => setShowContent(true), 300);
  }, []);

  const fireConfetti = async () => {
    // Dynamic import to avoid SSR issues
    try {
      const confetti = (await import('canvas-confetti')).default;

      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });

      // Second burst
      setTimeout(() => {
        confetti({
          particleCount: 50,
          angle: 60,
          spread: 55,
          origin: { x: 0 }
        });
        confetti({
          particleCount: 50,
          angle: 120,
          spread: 55,
          origin: { x: 1 }
        });
      }, 250);
    } catch (error) {
      // Confetti not available, that's ok
      console.log('Confetti not available');
    }
  };

  const IconComponent = {
    star: Star,
    party: PartyPopper,
    sparkles: Sparkles
  }[icon];

  const iconColors = {
    star: 'bg-yellow-100 text-yellow-500',
    party: 'bg-purple-100 text-purple-500',
    sparkles: 'bg-blue-100 text-blue-500'
  }[icon];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div
        className={`
          bg-white rounded-2xl p-8 max-w-sm w-full mx-4 text-center
          transform transition-all duration-500 shadow-2xl
          ${showContent ? 'scale-100 opacity-100' : 'scale-90 opacity-0'}
        `}
      >
        <div
          className={`
            w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4
            ${iconColors}
          `}
        >
          <IconComponent className="w-8 h-8 fill-current" />
        </div>

        <h2 className="text-xl font-bold text-gray-900 mb-2">{title}</h2>

        <p className="text-gray-600 mb-6">{message}</p>

        {nextAction ? (
          <Link
            href={nextAction.href}
            onClick={onClose}
            className="inline-flex items-center gap-2 px-6 py-3
                       bg-blue-600 text-white rounded-xl font-medium
                       hover:bg-blue-700 transition-colors"
          >
            {nextAction.label}
            <ArrowRight className="w-4 h-4" />
          </Link>
        ) : (
          <button
            onClick={onClose}
            className="px-6 py-3 bg-blue-600 text-white rounded-xl
                       font-medium hover:bg-blue-700 transition-colors"
          >
            Continue
          </button>
        )}
      </div>
    </div>
  );
}
