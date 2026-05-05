---
title: "Module 9: Landing Page & Marketing Site"
id: "09-landing-page"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Module 9: Landing Page & Marketing Site

## Overview
The main covered.ai website. Focused entirely on conversion - getting visitors to call 0800 COVERED.

## Expert Panel Input

**Conversion Expert**: One goal only - get them to call. Every element should push toward that action. Remove everything that doesn't.

**Copywriting Expert**: Lead with pain, show the solution, prove it works, make the action obvious. No corporate fluff.

**SEO Expert**: Target "AI receptionist", "phone answering service UK", "24/7 call answering" and vertical-specific terms.

**Trust Expert**: Social proof early and often. Real numbers, real testimonials, real results.

---

## Pages

### 1. Homepage (`/`)
- Hero with phone number
- Problem/solution
- How it works (3 steps)
- Pricing
- Testimonials
- FAQ
- Final CTA

### 2. Verticals (`/for/[vertical]`)
- Plumber, electrician, salon, vet, etc.
- Vertical-specific copy
- Vertical-specific testimonials
- Same structure, different words

### 3. Pricing (`/pricing`)
- Simple pricing
- Feature comparison
- FAQ about pricing

### 4. About (`/about`)
- Ewan's story
- Why Covered exists
- Team (AI-enhanced photos)

---

## Files to Create

### 1. frontend/src/app/(marketing)/page.tsx

```tsx
import Link from "next/link";
import { Phone, Clock, CheckCircle, Star, ArrowRight, Play } from "lucide-react";

export default function HomePage() {
  return (
    <main>
      {/* Hero */}
      <section className="relative bg-gradient-to-b from-blue-50 to-white pt-20 pb-32">
        <div className="max-w-6xl mx-auto px-4">
          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium mb-6">
              <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              Gemma is answering calls right now
            </div>
            
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
              Never miss a call.
              <br />
              <span className="text-blue-600">Never miss a job.</span>
            </h1>
            
            <p className="text-xl text-gray-600 mb-8 max-w-2xl">
              Gemma is your AI receptionist. She answers every call, 24/7, captures the details, 
              and forwards emergencies to you immediately. No more missed opportunities.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4">
              <a 
                href="tel:08002683733"
                className="inline-flex items-center justify-center gap-2 bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-blue-700 transition-colors"
              >
                <Phone className="w-5 h-5" />
                Call 0800 COVERED
              </a>
              <a 
                href="#how-it-works"
                className="inline-flex items-center justify-center gap-2 border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-xl font-semibold text-lg hover:border-gray-400 transition-colors"
              >
                <Play className="w-5 h-5" />
                See How It Works
              </a>
            </div>
            
            <p className="mt-4 text-sm text-gray-500">
              Call now and experience Gemma for yourself. It's free.
            </p>
          </div>
        </div>
        
        {/* Trust indicators */}
        <div className="max-w-6xl mx-auto px-4 mt-16">
          <div className="flex flex-wrap items-center justify-center gap-8 text-gray-500">
            <div className="flex items-center gap-2">
              <Clock className="w-5 h-5" />
              <span>24/7 availability</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="w-5 h-5" />
              <span>Set up in 5 minutes</span>
            </div>
            <div className="flex items-center gap-2">
              <Star className="w-5 h-5 text-yellow-500" />
              <span>4.9/5 from 50+ businesses</span>
            </div>
          </div>
        </div>
      </section>

      {/* Problem/Agitation */}
      <section className="py-20 bg-gray-900 text-white">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Every missed call is a missed job
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            You're busy working. The phone rings. You can't answer. 
            That caller? They're already dialling your competitor.
          </p>
          <div className="grid md:grid-cols-3 gap-8 mt-12">
            <div className="text-center">
              <p className="text-4xl font-bold text-red-400">62%</p>
              <p className="text-gray-400 mt-2">of callers won't leave a voicemail</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-red-400">85%</p>
              <p className="text-gray-400 mt-2">of people won't call back</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-red-400">£4,200</p>
              <p className="text-gray-400 mt-2">lost per month (avg trade)</p>
            </div>
          </div>
        </div>
      </section>

      {/* Solution */}
      <section id="how-it-works" className="py-20">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Gemma answers. You work.
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Set up in 5 minutes. Gemma handles every call professionally, 24/7.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-blue-600">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Forward your calls</h3>
              <p className="text-gray-600">
                Dial a simple code on your phone. Takes 30 seconds.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-blue-600">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Gemma answers</h3>
              <p className="text-gray-600">
                Every call, day or night. She captures names, numbers, and reasons.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-blue-600">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">You get the leads</h3>
              <p className="text-gray-600">
                Instant notifications. Call them back when you're ready.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Social Proof */}
      <section className="py-20 bg-blue-50">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Trusted by tradespeople across the UK
            </h2>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <TestimonialCard
              quote="47 calls in 3 weeks. 12 emergency callouts I would have missed. That's £4,200 extra revenue."
              name="Ralph"
              business="Titan Plumbing, Newcastle"
              avatar="/testimonials/ralph.jpg"
            />
            <TestimonialCard
              quote="I was sceptical about AI answering my phone. But Gemma sounds natural. Clients don't even realise."
              name="Sarah"
              business="Glow Aesthetics, Manchester"
              avatar="/testimonials/sarah.jpg"
            />
            <TestimonialCard
              quote="Set it up in my van on a lunch break. Best business decision I've made this year."
              name="Dave"
              business="Dave's Electrical, Leeds"
              avatar="/testimonials/dave.jpg"
            />
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="py-20">
        <div className="max-w-4xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Simple pricing. No surprises.
            </h2>
            <p className="text-xl text-gray-600">
              One plan. Everything included. Cancel anytime.
            </p>
          </div>
          
          <div className="bg-white rounded-2xl shadow-xl border p-8 md:p-12">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6 mb-8">
              <div>
                <h3 className="text-2xl font-bold text-gray-900">Covered Pro</h3>
                <p className="text-gray-600">Everything you need</p>
              </div>
              <div className="text-right">
                <p className="text-4xl font-bold text-gray-900">£297<span className="text-lg font-normal text-gray-500">/month</span></p>
                <p className="text-sm text-gray-500">+ VAT. No setup fees.</p>
              </div>
            </div>
            
            <div className="grid md:grid-cols-2 gap-4 mb-8">
              {[
                "24/7 AI receptionist",
                "Unlimited calls",
                "Instant notifications",
                "Call recordings",
                "Lead capture",
                "Emergency forwarding",
                "Custom greeting",
                "Dashboard access",
              ].map((feature) => (
                <div key={feature} className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <span>{feature}</span>
                </div>
              ))}
            </div>
            
            <div className="flex flex-col sm:flex-row gap-4">
              <a 
                href="tel:08002683733"
                className="flex-1 inline-flex items-center justify-center gap-2 bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-blue-700"
              >
                <Phone className="w-5 h-5" />
                Call to Start
              </a>
              <Link 
                href="/pricing"
                className="flex-1 inline-flex items-center justify-center gap-2 border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-xl font-semibold hover:border-gray-400"
              >
                Compare Plans
                <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-3xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
            Frequently Asked Questions
          </h2>
          
          <div className="space-y-4">
            <FAQItem
              question="How does Gemma sound?"
              answer="Gemma has a friendly Northern British accent. She sounds natural and professional - most callers don't realise they're speaking to AI. Call 0800 COVERED to hear her yourself."
            />
            <FAQItem
              question="How quickly can I set this up?"
              answer="About 5 minutes. You'll get a dedicated phone number, dial a forwarding code on your phone, and you're live. We help you every step of the way."
            />
            <FAQItem
              question="What happens with urgent calls?"
              answer="Gemma recognises emergency keywords (flood, burst, gas leak, etc.) and can immediately forward those calls to your mobile. You set the keywords."
            />
            <FAQItem
              question="Can I keep my existing number?"
              answer="Yes! You can either forward your existing number to Covered, or we can port your number over completely. Both work."
            />
            <FAQItem
              question="Is there a contract?"
              answer="No. Pay monthly, cancel anytime. No setup fees, no hidden costs."
            />
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-20 bg-blue-600">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to stop missing calls?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Call now. Gemma will answer. Experience it for yourself.
          </p>
          <a 
            href="tel:08002683733"
            className="inline-flex items-center gap-3 bg-white text-blue-600 px-10 py-5 rounded-xl font-bold text-xl hover:bg-blue-50 transition-colors"
          >
            <Phone className="w-6 h-6" />
            0800 COVERED
          </a>
          <p className="mt-4 text-blue-200 text-sm">
            That's 0800 268 3733 • Free to call
          </p>
        </div>
      </section>
    </main>
  );
}

function TestimonialCard({ 
  quote, 
  name, 
  business, 
  avatar 
}: { 
  quote: string; 
  name: string; 
  business: string; 
  avatar: string;
}) {
  return (
    <div className="bg-white rounded-xl p-6 shadow-sm">
      <div className="flex gap-1 mb-4">
        {[1, 2, 3, 4, 5].map((i) => (
          <Star key={i} className="w-5 h-5 text-yellow-400 fill-yellow-400" />
        ))}
      </div>
      <p className="text-gray-700 mb-4">"{quote}"</p>
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 bg-gray-200 rounded-full" />
        <div>
          <p className="font-semibold text-gray-900">{name}</p>
          <p className="text-sm text-gray-500">{business}</p>
        </div>
      </div>
    </div>
  );
}

function FAQItem({ question, answer }: { question: string; answer: string }) {
  return (
    <details className="group bg-white rounded-xl shadow-sm">
      <summary className="flex items-center justify-between p-6 cursor-pointer">
        <h3 className="font-semibold text-gray-900 pr-4">{question}</h3>
        <span className="text-2xl text-gray-400 group-open:rotate-45 transition-transform">+</span>
      </summary>
      <div className="px-6 pb-6">
        <p className="text-gray-600">{answer}</p>
      </div>
    </details>
  );
}
```

### 2. frontend/src/app/(marketing)/layout.tsx

```tsx
import Link from "next/link";
import { Phone } from "lucide-react";

export default function MarketingLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 bg-white/95 backdrop-blur-sm border-b z-50">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="text-xl font-bold text-blue-600">
            Covered
          </Link>
          
          <nav className="hidden md:flex items-center gap-6">
            <Link href="/#how-it-works" className="text-gray-600 hover:text-gray-900">
              How It Works
            </Link>
            <Link href="/pricing" className="text-gray-600 hover:text-gray-900">
              Pricing
            </Link>
            <Link href="/about" className="text-gray-600 hover:text-gray-900">
              About
            </Link>
          </nav>
          
          <a 
            href="tel:08002683733"
            className="inline-flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700"
          >
            <Phone className="w-4 h-4" />
            <span className="hidden sm:inline">0800 COVERED</span>
            <span className="sm:hidden">Call</span>
          </a>
        </div>
      </header>
      
      <div className="pt-16">
        {children}
      </div>
      
      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-4">Covered</h3>
              <p className="text-gray-400">
                AI phone answering for UK businesses. Never miss a call again.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/#how-it-works" className="hover:text-white">How It Works</Link></li>
                <li><Link href="/pricing" className="hover:text-white">Pricing</Link></li>
                <li><Link href="/for/plumber" className="hover:text-white">For Plumbers</Link></li>
                <li><Link href="/for/salon" className="hover:text-white">For Salons</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/about" className="hover:text-white">About</Link></li>
                <li><Link href="/contact" className="hover:text-white">Contact</Link></li>
                <li><Link href="/privacy" className="hover:text-white">Privacy</Link></li>
                <li><Link href="/terms" className="hover:text-white">Terms</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Contact</h4>
              <p className="text-gray-400">
                <a href="tel:08002683733" className="hover:text-white">0800 COVERED</a>
                <br />
                <a href="mailto:hello@covered.ai" className="hover:text-white">hello@covered.ai</a>
              </p>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-500 text-sm">
            <p>© 2024 Covered AI Ltd. All rights reserved.</p>
          </div>
        </div>
      </footer>
      
      {/* Mobile sticky CTA */}
      <div className="fixed bottom-0 left-0 right-0 bg-blue-600 p-4 md:hidden z-40">
        <a 
          href="tel:08002683733"
          className="block text-center text-white font-semibold text-lg"
        >
          📞 Call 0800 COVERED
        </a>
      </div>
    </div>
  );
}
```

### 3. frontend/src/app/(marketing)/for/[vertical]/page.tsx

```tsx
import { notFound } from "next/navigation";
import Link from "next/link";
import { Phone, CheckCircle, Star, ArrowRight } from "lucide-react";

const verticals = {
  plumber: {
    title: "AI Receptionist for Plumbers",
    headline: "Never miss an emergency callout again",
    description: "Burst pipes don't wait for office hours. Gemma answers every call, 24/7, and forwards emergencies to you immediately.",
    pain_points: [
      "Missing calls while under a sink",
      "Losing emergency jobs to competitors",
      "Customers going to voicemail and not leaving messages",
    ],
    testimonial: {
      quote: "47 calls in 3 weeks. 12 emergency callouts I would have missed. That's £4,200 extra revenue.",
      name: "Ralph",
      business: "Titan Plumbing, Newcastle",
    },
    keywords: ["flood", "burst pipe", "leak", "no hot water", "boiler", "blocked drain"],
  },
  electrician: {
    title: "AI Receptionist for Electricians",
    headline: "Answer every call. Win every job.",
    description: "When someone's power goes out, they need help now. Gemma ensures you never miss that call.",
    pain_points: [
      "Missing calls on jobs",
      "Losing urgent rewire work",
      "After-hours emergencies going unanswered",
    ],
    testimonial: {
      quote: "Set it up in my van on a lunch break. Best business decision I've made this year.",
      name: "Dave",
      business: "Dave's Electrical, Leeds",
    },
    keywords: ["power out", "no electricity", "tripped fuse", "emergency", "rewire"],
  },
  salon: {
    title: "AI Receptionist for Salons",
    headline: "Never miss a booking again",
    description: "Your stylists are busy. Gemma handles every call, captures bookings, and keeps your chairs full.",
    pain_points: [
      "Missing calls while with clients",
      "Losing bookings to competitors",
      "Staff distracted from clients",
    ],
    testimonial: {
      quote: "I was sceptical about AI answering my phone. But Gemma sounds natural. Clients don't even realise.",
      name: "Sarah",
      business: "Glow Aesthetics, Manchester",
    },
    keywords: ["appointment", "booking", "haircut", "colour", "cancel"],
  },
  vet: {
    title: "AI Receptionist for Vets",
    headline: "Every pet owner. Every call. Answered.",
    description: "When someone's pet is sick, they need reassurance. Gemma handles calls with empathy and urgency.",
    pain_points: [
      "Missing emergency calls during consultations",
      "Staff overwhelmed at reception",
      "After-hours emergencies going to voicemail",
    ],
    testimonial: {
      quote: "Gemma handles our after-hours calls perfectly. She knows when it's urgent.",
      name: "Dr. Claire",
      business: "Riverside Vets, Bristol",
    },
    keywords: ["emergency", "sick", "injured", "not eating", "collapsed"],
  },
};

export default function VerticalPage({ params }: { params: { vertical: string } }) {
  const data = verticals[params.vertical as keyof typeof verticals];
  
  if (!data) {
    notFound();
  }
  
  return (
    <main>
      {/* Hero */}
      <section className="bg-gradient-to-b from-blue-50 to-white pt-20 pb-32">
        <div className="max-w-6xl mx-auto px-4">
          <div className="max-w-3xl">
            <p className="text-blue-600 font-medium mb-4">{data.title}</p>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              {data.headline}
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              {data.description}
            </p>
            <a 
              href="tel:08002683733"
              className="inline-flex items-center gap-2 bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-blue-700"
            >
              <Phone className="w-5 h-5" />
              Call 0800 COVERED
            </a>
          </div>
        </div>
      </section>

      {/* Pain Points */}
      <section className="py-20">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-gray-900 mb-8">Sound familiar?</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {data.pain_points.map((point, i) => (
              <div key={i} className="bg-red-50 border border-red-100 rounded-xl p-6">
                <p className="text-red-800">❌ {point}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Solution */}
      <section className="py-20 bg-blue-600 text-white">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-3xl font-bold mb-8">With Gemma, you never miss a call</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {data.pain_points.map((point, i) => (
              <div key={i} className="bg-white/10 rounded-xl p-6">
                <p className="text-blue-100">
                  ✅ {point.replace("Missing", "Catching every").replace("Losing", "Winning every")}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonial */}
      <section className="py-20">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <div className="flex justify-center gap-1 mb-6">
            {[1, 2, 3, 4, 5].map((i) => (
              <Star key={i} className="w-6 h-6 text-yellow-400 fill-yellow-400" />
            ))}
          </div>
          <blockquote className="text-2xl text-gray-900 mb-6">
            "{data.testimonial.quote}"
          </blockquote>
          <p className="font-semibold">{data.testimonial.name}</p>
          <p className="text-gray-500">{data.testimonial.business}</p>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-gray-900 text-white">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-6">
            Ready to stop missing calls?
          </h2>
          <a 
            href="tel:08002683733"
            className="inline-flex items-center gap-3 bg-blue-600 text-white px-10 py-5 rounded-xl font-bold text-xl hover:bg-blue-700"
          >
            <Phone className="w-6 h-6" />
            0800 COVERED
          </a>
        </div>
      </section>
    </main>
  );
}

export function generateStaticParams() {
  return Object.keys(verticals).map((vertical) => ({ vertical }));
}
```

---

## SEO Configuration

### frontend/src/app/(marketing)/layout.tsx metadata

```tsx
import { Metadata } from "next";

export const metadata: Metadata = {
  title: {
    default: "Covered - AI Phone Answering for UK Businesses",
    template: "%s | Covered",
  },
  description: "Never miss a call again. Gemma, your AI receptionist, answers every call 24/7. Set up in 5 minutes. From £297/month.",
  keywords: ["AI receptionist", "phone answering service", "24/7 call answering", "virtual receptionist UK"],
  openGraph: {
    type: "website",
    locale: "en_GB",
    url: "https://covered.ai",
    siteName: "Covered",
    images: [
      {
        url: "https://covered.ai/og-image.jpg",
        width: 1200,
        height: 630,
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    site: "@coveredai",
  },
  robots: {
    index: true,
    follow: true,
  },
};
```

### Schema.org for homepage

Add to homepage:
```tsx
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{
    __html: JSON.stringify({
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "name": "Covered AI",
      "applicationCategory": "BusinessApplication",
      "operatingSystem": "Web",
      "description": "AI phone answering service for UK businesses",
      "offers": {
        "@type": "Offer",
        "price": "297",
        "priceCurrency": "GBP",
        "priceValidUntil": "2025-12-31",
      },
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "50",
      },
    }),
  }}
/>
```
