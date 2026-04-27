import { Metadata } from "next";
import { notFound } from "next/navigation";
import { Phone, Mail, MapPin, Clock, ChevronDown } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface GeoPageData {
  id: string;
  slug: string;
  title: string;
  meta_description: string;
  content: string;
  postcode: string;
  area: string | null;
  service: string;
  schema_markup: Record<string, unknown> | null;
  faqs: Array<{ question: string; answer: string }>;
  business: {
    name: string;
    phone: string;
    email: string;
    vertical: string;
  };
  published_at: string;
}

async function getGeoPage(slug: string): Promise<GeoPageData | null> {
  try {
    const res = await fetch(`${API_URL}/api/v1/geo/public/${slug}`, {
      next: { revalidate: 3600 }, // Cache for 1 hour
    });

    if (!res.ok) {
      return null;
    }

    return res.json();
  } catch {
    return null;
  }
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const page = await getGeoPage(slug);

  if (!page) {
    return {
      title: "Page Not Found",
    };
  }

  return {
    title: page.title,
    description: page.meta_description,
    openGraph: {
      title: page.title,
      description: page.meta_description,
      type: "website",
    },
  };
}

function FaqAccordion({ faqs }: { faqs: Array<{ question: string; answer: string }> }) {
  return (
    <div className="space-y-3">
      {faqs.map((faq, index) => (
        <details
          key={index}
          className="group bg-white rounded-lg border border-gray-200 overflow-hidden"
        >
          <summary className="flex items-center justify-between cursor-pointer px-5 py-4 text-left font-medium text-gray-900 hover:bg-gray-50">
            <span className="faq-answer">{faq.question}</span>
            <ChevronDown className="w-5 h-5 text-gray-500 transition-transform group-open:rotate-180" />
          </summary>
          <div className="px-5 pb-4 text-gray-600 service-description">
            {faq.answer}
          </div>
        </details>
      ))}
    </div>
  );
}

export default async function GeoPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const page = await getGeoPage(slug);

  if (!page) {
    notFound();
  }

  const areaDisplay = page.area || page.postcode;

  return (
    <>
      {/* Schema.org JSON-LD */}
      {page.schema_markup && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(page.schema_markup),
          }}
        />
      )}

      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-cyan-600 text-white">
          <div className="max-w-4xl mx-auto px-4 py-8">
            <div className="flex items-center gap-2 text-cyan-100 text-sm mb-2">
              <MapPin className="w-4 h-4" />
              <span>{areaDisplay} | {page.postcode}</span>
            </div>
            <h1 className="text-3xl md:text-4xl font-bold business-description">
              {page.title}
            </h1>
            <p className="mt-3 text-cyan-100 text-lg">
              {page.meta_description}
            </p>
          </div>
        </header>

        {/* Contact Bar */}
        <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
          <div className="max-w-4xl mx-auto px-4 py-4">
            <div className="flex flex-col sm:flex-row items-center gap-4 justify-between">
              <div className="flex items-center gap-6">
                <a
                  href={`tel:${page.business.phone}`}
                  className="flex items-center gap-2 text-gray-700 hover:text-cyan-600 transition-colors"
                >
                  <Phone className="w-5 h-5" />
                  <span className="font-medium">{page.business.phone}</span>
                </a>
                <a
                  href={`mailto:${page.business.email}`}
                  className="flex items-center gap-2 text-gray-700 hover:text-cyan-600 transition-colors"
                >
                  <Mail className="w-5 h-5" />
                  <span className="font-medium hidden sm:inline">{page.business.email}</span>
                </a>
              </div>
              <a
                href={`tel:${page.business.phone}`}
                className="w-full sm:w-auto bg-cyan-600 hover:bg-cyan-700 text-white font-semibold py-3 px-6 rounded-lg text-center transition-colors"
              >
                Call Now for a Free Quote
              </a>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <main className="max-w-4xl mx-auto px-4 py-8">
          {/* About Section */}
          <section className="bg-white rounded-xl border border-gray-200 p-6 mb-8">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 bg-cyan-100 rounded-full flex items-center justify-center">
                <span className="text-2xl">
                  {page.business.vertical === "trades" && "🔧"}
                  {page.business.vertical === "vet" && "🐾"}
                  {page.business.vertical === "dental" && "🦷"}
                  {page.business.vertical === "salon" && "💇"}
                  {page.business.vertical === "physio" && "💪"}
                  {page.business.vertical === "legal" && "⚖️"}
                  {page.business.vertical === "accounting" && "📊"}
                  {!page.business.vertical && "🏢"}
                </span>
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-900">{page.business.name}</h2>
                <p className="text-gray-500 text-sm capitalize">{page.business.vertical || "Local Service"}</p>
              </div>
            </div>

            {/* Content rendered as markdown-style text */}
            <div className="prose prose-gray max-w-none">
              {page.content.split("\n").map((paragraph, index) => {
                if (paragraph.startsWith("# ")) {
                  return (
                    <h2 key={index} className="text-2xl font-bold text-gray-900 mt-6 mb-3">
                      {paragraph.replace("# ", "")}
                    </h2>
                  );
                }
                if (paragraph.startsWith("## ")) {
                  return (
                    <h3 key={index} className="text-xl font-semibold text-gray-900 mt-5 mb-2">
                      {paragraph.replace("## ", "")}
                    </h3>
                  );
                }
                if (paragraph.startsWith("- ")) {
                  return (
                    <li key={index} className="text-gray-600 ml-4">
                      {paragraph.replace("- ", "")}
                    </li>
                  );
                }
                if (paragraph.startsWith("**") && paragraph.endsWith("**")) {
                  return (
                    <p key={index} className="font-semibold text-gray-900 mt-4">
                      {paragraph.replace(/\*\*/g, "")}
                    </p>
                  );
                }
                if (paragraph.trim()) {
                  return (
                    <p key={index} className="text-gray-600 mt-3 leading-relaxed">
                      {paragraph}
                    </p>
                  );
                }
                return null;
              })}
            </div>
          </section>

          {/* Service Areas */}
          <section className="bg-white rounded-xl border border-gray-200 p-6 mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Service Area</h2>
            <div className="flex items-center gap-3 text-gray-600">
              <MapPin className="w-5 h-5 text-cyan-600" />
              <span>Covering <strong>{page.postcode}</strong> and surrounding areas{page.area && ` including ${page.area}`}</span>
            </div>
            <div className="flex items-center gap-3 text-gray-600 mt-3">
              <Clock className="w-5 h-5 text-cyan-600" />
              <span>24/7 Emergency Service Available</span>
            </div>
          </section>

          {/* FAQs */}
          {page.faqs.length > 0 && (
            <section className="mb-8">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Frequently Asked Questions</h2>
              <FaqAccordion faqs={page.faqs} />
            </section>
          )}

          {/* CTA */}
          <section className="bg-cyan-600 rounded-xl p-8 text-center text-white">
            <h2 className="text-2xl font-bold mb-3">Ready to Get Started?</h2>
            <p className="text-cyan-100 mb-6">
              Contact {page.business.name} today for professional {page.service} services in {areaDisplay}.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <a
                href={`tel:${page.business.phone}`}
                className="w-full sm:w-auto bg-white text-cyan-600 font-semibold py-3 px-8 rounded-lg hover:bg-cyan-50 transition-colors"
              >
                Call {page.business.phone}
              </a>
              <a
                href={`mailto:${page.business.email}`}
                className="w-full sm:w-auto border-2 border-white text-white font-semibold py-3 px-8 rounded-lg hover:bg-white/10 transition-colors"
              >
                Send Email
              </a>
            </div>
          </section>
        </main>

        {/* Footer */}
        <footer className="bg-gray-900 text-gray-400 py-8 mt-12">
          <div className="max-w-4xl mx-auto px-4 text-center">
            <p className="text-sm">
              {page.business.name} - Professional {page.service} services in {areaDisplay}
            </p>
            <p className="text-xs mt-2">
              Powered by <a href="https://covered.ai" className="text-cyan-400 hover:underline">Covered AI</a>
            </p>
          </div>
        </footer>
      </div>
    </>
  );
}
