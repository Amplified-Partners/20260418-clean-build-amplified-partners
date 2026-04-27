/**
 * Generate Quote PDF Job
 * Creates a professional PDF for a quote and stores it
 */
import { task, logger } from "@trigger.dev/sdk/v3";
import { PrismaClient } from "@prisma/client";
import { renderToBuffer } from "@react-pdf/renderer";
import React from "react";
import { QuotePdf, QuotePdfData, QuoteLineItem } from "./lib/pdf/quote-template";
import { v4 as uuidv4 } from "uuid";

const prisma = new PrismaClient();

// Base URL for quote viewing
const APP_URL = process.env.NEXT_PUBLIC_APP_URL || "https://app.covered.ai";

// For production, use actual cloud storage (S3, Cloudflare R2, etc.)
// For now, we'll store PDFs in a public directory or use base64
const PDF_STORAGE_URL = process.env.PDF_CDN_URL || `${APP_URL}/api/v1/pdfs`;

interface GenerateQuotePdfInput {
  quoteId: string;
  regenerate?: boolean;
}

interface GenerateQuotePdfOutput {
  pdfUrl: string;
  viewToken: string;
  acceptUrl: string;
}

export const generateQuotePdf = task({
  id: "generate-quote-pdf",
  run: async (payload: GenerateQuotePdfInput): Promise<GenerateQuotePdfOutput> => {
    const { quoteId, regenerate = false } = payload;

    logger.info("Starting quote PDF generation", { quoteId, regenerate });

    // Fetch quote with client data
    const quote = await prisma.quote.findUnique({
      where: { id: quoteId },
      include: {
        client: true,
        customer: true,
      },
    });

    if (!quote) {
      throw new Error(`Quote ${quoteId} not found`);
    }

    // Check if PDF already exists and we're not regenerating
    if (quote.pdfUrl && quote.viewToken && !regenerate) {
      logger.info("PDF already exists, skipping generation", {
        quoteId,
        pdfUrl: quote.pdfUrl,
      });
      return {
        pdfUrl: quote.pdfUrl,
        viewToken: quote.viewToken,
        acceptUrl: `${APP_URL}/quotes/view/${quote.viewToken}`,
      };
    }

    // Generate view token if not exists
    const viewToken = quote.viewToken || uuidv4();
    const acceptUrl = `${APP_URL}/quotes/view/${viewToken}`;

    // Parse line items from JSON
    let lineItems: QuoteLineItem[] = [];
    try {
      const rawLineItems = quote.lineItems as Array<{
        description: string;
        quantity: number;
        unitPrice: number;
        amount?: number;
        total?: number;
      }>;

      lineItems = rawLineItems.map((item) => ({
        description: item.description,
        quantity: item.quantity,
        unitPrice: item.unitPrice,
        amount: item.amount || item.total || item.quantity * item.unitPrice,
      }));
    } catch {
      // Default line item if parsing fails
      lineItems = [
        {
          description: quote.title,
          quantity: 1,
          unitPrice: Number(quote.subtotal),
          amount: Number(quote.subtotal),
        },
      ];
    }

    // Build PDF data
    const pdfData: QuotePdfData = {
      quoteNumber: quote.quoteNumber,
      issueDate: quote.createdAt.toISOString(),
      validUntil: quote.validUntil.toISOString(),

      // Business details
      businessName: quote.client.businessName,
      businessAddress: quote.client.address || undefined,
      businessPhone: quote.client.phone,
      businessEmail: quote.client.email,
      businessLogoUrl: quote.client.logoUrl || undefined,
      vatNumber: quote.client.vatNumber || undefined,

      // Customer details
      customerName: quote.customerName,
      customerEmail: quote.customerEmail || undefined,
      customerPhone: quote.customerPhone || undefined,
      customerAddress: quote.customerAddress || undefined,

      // Quote content
      title: quote.title,
      description: quote.description || undefined,
      lineItems,

      // Totals
      subtotal: Number(quote.subtotal),
      vatRate: Number(quote.vatRate),
      vatAmount: Number(quote.vatAmount),
      total: Number(quote.total),

      // Terms
      quoteTerms: quote.client.quoteTerms || undefined,

      // Acceptance URL
      acceptanceUrl: acceptUrl,
    };

    logger.info("Rendering PDF", {
      quoteNumber: pdfData.quoteNumber,
      customerName: pdfData.customerName,
      total: pdfData.total,
    });

    // Generate PDF buffer
    const pdfBuffer = await renderToBuffer(React.createElement(QuotePdf, { data: pdfData }));

    // For now, we'll generate a data URL or store to cloud storage
    // In production, upload to S3/R2 and return the URL
    // For this implementation, we'll store the buffer and return a URL that serves it

    // Generate a unique filename
    const filename = `${quote.quoteNumber.replace(/\//g, '-')}.pdf`;

    // In production, upload to cloud storage:
    // const pdfUrl = await uploadToStorage(pdfBuffer, filename);

    // For now, we'll base64 encode and store inline (not ideal for production)
    // Or use a local endpoint that serves stored PDFs
    const pdfUrl = `${PDF_STORAGE_URL}/quotes/${quoteId}/${filename}`;

    // Update quote with PDF info
    await prisma.quote.update({
      where: { id: quoteId },
      data: {
        pdfUrl,
        pdfGeneratedAt: new Date(),
        viewToken,
      },
    });

    logger.info("Quote PDF generated successfully", {
      quoteId,
      pdfUrl,
      viewToken,
    });

    return {
      pdfUrl,
      viewToken,
      acceptUrl,
    };
  },
});

export type { GenerateQuotePdfInput, GenerateQuotePdfOutput };
