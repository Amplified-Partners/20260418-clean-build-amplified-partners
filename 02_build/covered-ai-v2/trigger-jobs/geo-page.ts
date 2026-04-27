/**
 * GEO Page Generation Jobs
 * Generates AI-optimized local service pages for each business
 * Works with the actual Prisma schema: GeoPage, GeoFaq, AiCitation
 */
import { task, schedules } from "@trigger.dev/sdk/v3";
import { PrismaClient } from "@prisma/client";
import OpenAI from "openai";

const prisma = new PrismaClient();
const openai = new OpenAI();

// Utility function to create URL-friendly slug
function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

// Get schema.org business type from vertical
function getBusinessType(vertical: string): string {
  const types: Record<string, string> = {
    trades: "HomeAndConstructionBusiness",
    vet: "VeterinaryCare",
    salon: "BeautySalon",
    dental: "Dentist",
    physio: "PhysicalTherapy",
    legal: "LegalService",
    accounting: "AccountingService",
  };
  return types[vertical?.toLowerCase()] || "LocalBusiness";
}

// Generate page title
function generatePageTitle(service: string, area: string | null, postcode: string, businessName: string): string {
  const areaDisplay = area || postcode;
  return `${service.charAt(0).toUpperCase() + service.slice(1)} in ${areaDisplay} | ${businessName}`;
}

// Generate meta description
function generateMetaDescription(service: string, area: string | null, postcode: string, businessName: string): string {
  const areaDisplay = area || postcode;
  return `Professional ${service.toLowerCase()} services in ${areaDisplay} (${postcode}). ${businessName} offers reliable, affordable ${service.toLowerCase()} with fast response times. Call now for a free quote!`;
}

// Generate page content
function generatePageContent(
  postcode: string,
  service: string,
  area: string | null,
  businessName: string,
  vertical: string
): string {
  const areaDisplay = area || postcode;

  return `# ${service.charAt(0).toUpperCase() + service.slice(1)} Services in ${areaDisplay}

Looking for professional ${service.toLowerCase()} services in ${areaDisplay}? ${businessName} provides reliable, high-quality ${service.toLowerCase()} services throughout the ${postcode} area.

## Why Choose ${businessName}?

- **Local Expertise**: We know the ${areaDisplay} area inside out
- **Fast Response**: Same-day service available for urgent needs
- **Trusted Professionals**: Fully qualified and insured team
- **Fair Pricing**: Transparent quotes with no hidden fees

## Our ${service.charAt(0).toUpperCase() + service.slice(1)} Services

We offer a comprehensive range of ${service.toLowerCase()} services in ${areaDisplay}:

- Emergency callouts and repairs
- Routine maintenance and servicing
- New installations
- Upgrades and replacements
- Free quotes and assessments

## Service Area

We cover all of ${postcode} and surrounding areas including ${areaDisplay}. Whether you're in the town centre or the outskirts, we can help.

## Get in Touch

Ready to book or need a quote? Give us a call or fill out our enquiry form. We aim to respond within 15 minutes during business hours.

**Covering ${postcode} | ${areaDisplay} | Available 24/7 for Emergencies**`;
}

// Generate schema markup for a GEO page
function generateSchemaMarkup(input: {
  page: { slug: string; postcode: string; area: string | null; service: string; title: string; metaDescription: string };
  client: { businessName: string; vertical: string | null; coveredNumber: string | null; email: string };
  faqs: Array<{ question: string; answer: string }>;
}): object {
  const { page, client, faqs } = input;
  const baseUrl = `https://covered.ai/find/${page.slug}`;

  const graph: object[] = [];

  // 1. LocalBusiness Schema
  const localBusiness: Record<string, unknown> = {
    "@type": getBusinessType(client.vertical || ""),
    "@id": `${baseUrl}#business`,
    name: client.businessName,
    url: baseUrl,
    telephone: client.coveredNumber || "",
    email: client.email,
    description: page.metaDescription,
    priceRange: "££",
    paymentAccepted: ["Cash", "Credit Card", "Bank Transfer"],
    currenciesAccepted: "GBP",
    areaServed: {
      "@type": "PostalAddress",
      postalCode: page.postcode,
      addressLocality: page.area || page.postcode,
      addressCountry: "GB",
    },
  };

  graph.push(localBusiness);

  // 2. FAQPage Schema
  if (faqs.length > 0) {
    graph.push({
      "@type": "FAQPage",
      "@id": `${baseUrl}#faq`,
      mainEntity: faqs.map((faq) => ({
        "@type": "Question",
        name: faq.question,
        acceptedAnswer: {
          "@type": "Answer",
          text: faq.answer,
        },
      })),
    });
  }

  // 3. Service Schema
  graph.push({
    "@type": "Service",
    "@id": `${baseUrl}#service`,
    name: page.service,
    description: `Professional ${page.service} services in ${page.area || page.postcode}`,
    provider: { "@id": `${baseUrl}#business` },
    areaServed: {
      "@type": "Place",
      address: {
        "@type": "PostalAddress",
        postalCode: page.postcode,
        addressCountry: "GB",
      },
    },
  });

  // 4. WebPage with Speakable
  graph.push({
    "@type": "WebPage",
    "@id": baseUrl,
    name: page.title,
    description: page.metaDescription,
    speakable: {
      "@type": "SpeakableSpecification",
      cssSelector: [".business-description", ".faq-answer", ".service-description"],
    },
    mainEntity: { "@id": `${baseUrl}#business` },
  });

  return {
    "@context": "https://schema.org",
    "@graph": graph,
  };
}

// Generate default FAQs for a service/area
function generateDefaultFaqs(
  service: string,
  area: string | null,
  postcode: string,
  businessName: string
): Array<{ question: string; answer: string }> {
  const areaDisplay = area || postcode;

  return [
    {
      question: `How quickly can you provide ${service.toLowerCase()} services in ${areaDisplay}?`,
      answer: `We typically respond within 2 hours for standard requests and offer same-day emergency service throughout ${postcode}.`,
    },
    {
      question: `How much does ${service.toLowerCase()} cost in ${areaDisplay}?`,
      answer: `Prices vary depending on the specific job. We offer free, no-obligation quotes and transparent pricing with no hidden fees.`,
    },
    {
      question: `Are your ${service.toLowerCase()} professionals qualified and insured?`,
      answer: `Yes, all our team members are fully qualified, certified, and comprehensively insured for your peace of mind.`,
    },
    {
      question: `Do you offer emergency ${service.toLowerCase()} services in ${postcode}?`,
      answer: `Yes, we provide 24/7 emergency callout services throughout ${areaDisplay} and the wider ${postcode} area.`,
    },
    {
      question: `What areas do you cover near ${areaDisplay}?`,
      answer: `We cover all of ${postcode} and surrounding postcodes. Contact us to confirm we service your specific location.`,
    },
  ];
}

/**
 * Generate GEO pages for all service areas of a client
 */
export const generateGeoPages = schedules.task({
  id: "generate-geo-pages",
  cron: "0 3 * * *", // 3am daily
  run: async () => {
    const clients = await prisma.client.findMany({
      where: { subscriptionStatus: "active" },
    });

    let generated = 0;
    let updated = 0;

    for (const client of clients) {
      try {
        // Get service areas from client (default to their postcode area)
        const serviceAreas = client.serviceAreas || [];
        const defaultPostcode = client.postcode?.substring(0, 4)?.toUpperCase() || "";

        // Get common services for their vertical
        const services = getServicesForVertical(client.vertical || "trades");

        // For each postcode area + service combination, create/update a GEO page
        const postcodes = serviceAreas.length > 0 ? serviceAreas : [defaultPostcode];

        for (const postcode of postcodes) {
          if (!postcode) continue;

          for (const service of services) {
            const slug = slugify(`${service}-${postcode}`);

            // Check if page exists
            const existingPage = await prisma.geoPage.findFirst({
              where: { clientId: client.id, slug },
            });

            const title = generatePageTitle(service, null, postcode, client.businessName);
            const metaDescription = generateMetaDescription(service, null, postcode, client.businessName);
            const content = generatePageContent(postcode, service, null, client.businessName, client.vertical || "trades");

            // Get existing FAQs for this page
            let faqs: Array<{ question: string; answer: string }> = [];
            if (existingPage) {
              const existingFaqs = await prisma.geoFaq.findMany({
                where: { pageId: existingPage.id },
              });
              faqs = existingFaqs.map((f) => ({ question: f.question, answer: f.answer }));
            }

            // Generate schema markup
            const schemaMarkup = generateSchemaMarkup({
              page: { slug, postcode, area: null, service, title, metaDescription },
              client: {
                businessName: client.businessName,
                vertical: client.vertical,
                coveredNumber: client.coveredNumber,
                email: client.email,
              },
              faqs,
            });

            if (existingPage) {
              // Update existing page
              await prisma.geoPage.update({
                where: { id: existingPage.id },
                data: {
                  title,
                  metaDescription,
                  content,
                  schemaMarkup,
                },
              });
              updated++;
            } else {
              // Create new page
              const newPage = await prisma.geoPage.create({
                data: {
                  clientId: client.id,
                  slug,
                  postcode,
                  service,
                  title,
                  metaDescription,
                  content,
                  schemaMarkup,
                  status: "DRAFT",
                },
              });

              // Create default FAQs
              const defaultFaqs = generateDefaultFaqs(service, null, postcode, client.businessName);
              for (const faq of defaultFaqs) {
                await prisma.geoFaq.create({
                  data: {
                    pageId: newPage.id,
                    clientId: client.id,
                    question: faq.question,
                    answer: faq.answer,
                    sourceType: "ai_generated",
                  },
                });
              }

              generated++;
            }
          }
        }
      } catch (error) {
        console.error(`Failed to generate GEO pages for ${client.id}:`, error);
      }
    }

    return { generated, updated };
  },
});

// Get services based on vertical
function getServicesForVertical(vertical: string): string[] {
  const services: Record<string, string[]> = {
    trades: ["plumber", "emergency plumber", "boiler repair", "heating engineer"],
    vet: ["veterinary care", "pet emergency", "pet vaccinations", "pet health check"],
    salon: ["hair salon", "haircut", "hair colouring", "beauty treatments"],
    dental: ["dentist", "emergency dentist", "teeth cleaning", "dental checkup"],
    physio: ["physiotherapy", "sports massage", "back pain treatment", "injury rehabilitation"],
    legal: ["solicitor", "legal advice", "conveyancing", "family law"],
    accounting: ["accountant", "tax advice", "bookkeeping", "business accounting"],
  };
  return services[vertical?.toLowerCase()] || ["professional services"];
}

/**
 * Generate GEO page for a specific client (on-demand)
 */
export const generateGeoPageForClient = task({
  id: "generate-geo-page-for-client",
  run: async (payload: { clientId: string; postcode?: string; service?: string }) => {
    const client = await prisma.client.findUnique({
      where: { id: payload.clientId },
    });

    if (!client) {
      throw new Error(`Client ${payload.clientId} not found`);
    }

    const postcode = payload.postcode || client.postcode?.substring(0, 4)?.toUpperCase() || "";
    const service = payload.service || getServicesForVertical(client.vertical || "trades")[0];
    const slug = slugify(`${service}-${postcode}`);

    const title = generatePageTitle(service, null, postcode, client.businessName);
    const metaDescription = generateMetaDescription(service, null, postcode, client.businessName);
    const content = generatePageContent(postcode, service, null, client.businessName, client.vertical || "trades");

    const schemaMarkup = generateSchemaMarkup({
      page: { slug, postcode, area: null, service, title, metaDescription },
      client: {
        businessName: client.businessName,
        vertical: client.vertical,
        coveredNumber: client.coveredNumber,
        email: client.email,
      },
      faqs: [],
    });

    const page = await prisma.geoPage.upsert({
      where: {
        clientId_slug: {
          clientId: client.id,
          slug,
        },
      },
      create: {
        clientId: client.id,
        slug,
        postcode,
        service,
        title,
        metaDescription,
        content,
        schemaMarkup,
        status: "DRAFT",
      },
      update: {
        title,
        metaDescription,
        content,
        schemaMarkup,
      },
    });

    // Create default FAQs if new page
    const existingFaqs = await prisma.geoFaq.count({ where: { pageId: page.id } });
    if (existingFaqs === 0) {
      const defaultFaqs = generateDefaultFaqs(service, null, postcode, client.businessName);
      for (const faq of defaultFaqs) {
        await prisma.geoFaq.create({
          data: {
            pageId: page.id,
            clientId: client.id,
            question: faq.question,
            answer: faq.answer,
            sourceType: "ai_generated",
          },
        });
      }
    }

    return { clientId: client.id, pageId: page.id, slug };
  },
});

/**
 * Extract FAQs from call transcripts using AI
 */
export const extractFaqsFromCalls = schedules.task({
  id: "extract-faqs-from-calls",
  cron: "0 2 * * 0", // Sunday 2am
  run: async () => {
    const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);

    const clients = await prisma.client.findMany({
      where: { subscriptionStatus: "active" },
      include: {
        calls: {
          where: {
            createdAt: { gte: thirtyDaysAgo },
            transcript: { not: null },
          },
          select: {
            id: true,
            transcript: true,
            summary: true,
          },
          take: 50,
        },
      },
    });

    let totalFaqs = 0;

    for (const client of clients) {
      if (client.calls.length < 5) continue;

      try {
        // Extract questions from transcripts
        const callData = client.calls.map((c) => ({
          summary: c.summary || "",
          questions: extractQuestionsFromTranscript(c.transcript || ""),
        }));

        // Generate FAQs with AI
        const response = await openai.chat.completions.create({
          model: "gpt-4o-mini",
          messages: [
            {
              role: "system",
              content: `You are analysing customer call data for a ${client.vertical || "service"} business named ${client.businessName}.

Generate 5-8 helpful FAQs based on the call patterns. Each FAQ should:
1. Address a real question customers ask
2. Have a helpful, professional answer (2-3 sentences)

Output JSON: {"faqs": [{"question": "...", "answer": "..."}]}`,
            },
            {
              role: "user",
              content: `Call data:\n${JSON.stringify(callData.slice(0, 30), null, 2)}`,
            },
          ],
          response_format: { type: "json_object" },
          temperature: 0.3,
        });

        const result = JSON.parse(response.choices[0].message.content || '{"faqs":[]}');

        // Find GEO pages for this client
        const geoPages = await prisma.geoPage.findMany({
          where: { clientId: client.id },
          include: { faqs: true },
        });

        for (const geoPage of geoPages) {
          const existingQuestions = geoPage.faqs.map((f) => normalizeQuestion(f.question));

          // Add new FAQs that don't already exist
          for (const faq of result.faqs) {
            if (!existingQuestions.includes(normalizeQuestion(faq.question))) {
              await prisma.geoFaq.create({
                data: {
                  pageId: geoPage.id,
                  clientId: client.id,
                  question: faq.question,
                  answer: faq.answer,
                  sourceType: "call_transcript",
                },
              });
              totalFaqs++;
            }
          }
        }
      } catch (error) {
        console.error(`Failed to extract FAQs for ${client.id}:`, error);
      }
    }

    return { faqsGenerated: totalFaqs };
  },
});

// Helper function to extract questions from transcript
function extractQuestionsFromTranscript(transcript: string): string[] {
  const questions = transcript.match(/[^.!?]*\?/g) || [];
  return questions.slice(0, 5);
}

// Helper function to normalize questions for comparison
function normalizeQuestion(q: string): string {
  return q.toLowerCase().replace(/[^a-z0-9]/g, "");
}

/**
 * Monitor AI citations for clients
 * Placeholder for future integration with AI search APIs
 */
export const monitorAiCitations = schedules.task({
  id: "monitor-ai-citations",
  cron: "0 6 * * *", // 6am daily
  run: async () => {
    // This job would check AI platforms (Perplexity, ChatGPT, etc.)
    // for mentions of client businesses
    // For now, just log activity

    const clients = await prisma.client.findMany({
      where: { subscriptionStatus: "active" },
    });

    let checked = 0;

    for (const client of clients) {
      try {
        // Get recent citation count for this client
        const recentCitations = await prisma.aiCitation.count({
          where: {
            clientId: client.id,
            detectedAt: {
              gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
            },
          },
        });

        // In the future, this would:
        // 1. Query AI search APIs with business-related queries
        // 2. Check if the client is mentioned in responses
        // 3. Record new citations in the AiCitation table

        console.log(`Client ${client.businessName}: ${recentCitations} citations in last 30 days`);
        checked++;
      } catch (error) {
        console.error(`Failed to check citations for ${client.id}:`, error);
      }
    }

    return { checked };
  },
});
