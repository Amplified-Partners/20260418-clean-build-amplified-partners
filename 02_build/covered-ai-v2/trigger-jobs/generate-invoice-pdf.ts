/**
 * Generate Invoice PDF Job
 * Renders invoice to PDF and uploads to storage
 */
import { task, logger } from "@trigger.dev/sdk/v3";
import React from "react";
import { renderToBuffer } from "@react-pdf/renderer";
import { PrismaClient } from "@prisma/client";
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { InvoicePdf, InvoicePdfData, InvoiceLineItem } from "./lib/pdf/invoice-template";
import crypto from "crypto";

const prisma = new PrismaClient();

// S3/R2 client for PDF storage
const s3Client = new S3Client({
  region: process.env.AWS_REGION || "eu-west-2",
  endpoint: process.env.S3_ENDPOINT, // For R2 compatibility
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID || "",
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || "",
  },
});

const PDF_BUCKET = process.env.PDF_STORAGE_BUCKET || "covered-invoices";
const PDF_CDN_URL = process.env.PDF_CDN_URL || `https://${PDF_BUCKET}.s3.amazonaws.com`;

interface GenerateInvoicePdfInput {
  invoiceId: string;
  regenerate?: boolean; // Force regenerate even if PDF exists
}

export const generateInvoicePdf = task({
  id: "generate-invoice-pdf",
  run: async (payload: GenerateInvoicePdfInput) => {
    const { invoiceId, regenerate = false } = payload;

    logger.info("Starting invoice PDF generation", { invoiceId, regenerate });

    // Fetch invoice with client data
    const invoice = await prisma.invoice.findUnique({
      where: { id: invoiceId },
      include: {
        client: true,
        job: true,
      },
    });

    if (!invoice) {
      throw new Error(`Invoice ${invoiceId} not found`);
    }

    // Check if PDF already exists and we're not forcing regeneration
    if (invoice.pdfUrl && !regenerate) {
      logger.info("PDF already exists, skipping generation", {
        invoiceId,
        pdfUrl: invoice.pdfUrl
      });
      return {
        success: true,
        pdfUrl: invoice.pdfUrl,
        cached: true,
      };
    }

    // Generate view token if not exists
    let viewToken = invoice.viewToken;
    if (!viewToken) {
      viewToken = crypto.randomBytes(32).toString("hex");
      await prisma.invoice.update({
        where: { id: invoiceId },
        data: { viewToken },
      });
    }

    // Build line items from description (for now, single line item)
    // In future, could store structured line items in JSON column
    const lineItems: InvoiceLineItem[] = [{
      description: invoice.description,
      quantity: 1,
      unitPrice: Number(invoice.amount) / 1.2, // Remove VAT for unit price
      amount: Number(invoice.amount) / 1.2,
    }];

    const subtotal = lineItems.reduce((sum, item) => sum + item.amount, 0);
    const vatRate = 0.20;
    const vatAmount = subtotal * vatRate;
    const total = subtotal + vatAmount;

    // Build PDF data
    const pdfData: InvoicePdfData = {
      invoiceNumber: invoice.invoiceNumber,
      issueDate: invoice.createdAt.toISOString(),
      dueDate: invoice.dueDate.toISOString(),

      // Business details
      businessName: invoice.client.businessName,
      businessAddress: invoice.client.address || undefined,
      businessPhone: invoice.client.phone,
      businessEmail: invoice.client.email,
      businessLogoUrl: invoice.client.logoUrl || undefined,
      vatNumber: invoice.client.vatNumber || undefined,

      // Customer details
      customerName: invoice.customerName,
      customerEmail: invoice.customerEmail || undefined,
      customerPhone: invoice.customerPhone || undefined,

      // Line items
      lineItems,

      // Totals
      subtotal,
      vatRate,
      vatAmount,
      total,

      // Payment details
      paymentLinkUrl: invoice.paymentLinkUrl || undefined,
      bankAccountName: invoice.client.bankAccountName || undefined,
      bankSortCode: invoice.client.bankSortCode || undefined,
      bankAccountNumber: invoice.client.bankAccountNumber || undefined,
      paymentTerms: invoice.client.invoiceTerms || "Payment due within 30 days",
    };

    logger.info("Rendering PDF", { invoiceNumber: pdfData.invoiceNumber });

    // Render PDF to buffer
    const pdfBuffer = await renderToBuffer(
      React.createElement(InvoicePdf, { data: pdfData })
    );

    // Generate unique filename
    const filename = `invoices/${invoice.client.id}/${invoice.invoiceNumber}-${Date.now()}.pdf`;

    logger.info("Uploading PDF to storage", { filename, bucket: PDF_BUCKET });

    // Upload to S3/R2
    await s3Client.send(
      new PutObjectCommand({
        Bucket: PDF_BUCKET,
        Key: filename,
        Body: pdfBuffer,
        ContentType: "application/pdf",
        ContentDisposition: `inline; filename="${invoice.invoiceNumber}.pdf"`,
        // Cache for 1 year (immutable once generated)
        CacheControl: "public, max-age=31536000, immutable",
      })
    );

    const pdfUrl = `${PDF_CDN_URL}/${filename}`;

    // Update invoice with PDF URL
    await prisma.invoice.update({
      where: { id: invoiceId },
      data: {
        pdfUrl,
        pdfGeneratedAt: new Date(),
      },
    });

    logger.info("Invoice PDF generated successfully", {
      invoiceId,
      invoiceNumber: invoice.invoiceNumber,
      pdfUrl,
    });

    return {
      success: true,
      pdfUrl,
      invoiceNumber: invoice.invoiceNumber,
      viewToken,
      cached: false,
    };
  },
});

// Export for use in other tasks
export type { GenerateInvoicePdfInput };
