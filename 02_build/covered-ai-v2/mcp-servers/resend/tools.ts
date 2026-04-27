/**
 * Covered AI - Resend MCP Server Tools
 *
 * Email sending tools via Resend.
 */

import { Resend } from "resend";
import * as fs from "fs";
import * as path from "path";

// Initialize Resend client
const apiKey = process.env.RESEND_API_KEY;

if (!apiKey) {
  console.error("Warning: RESEND_API_KEY must be set");
}

const resend = apiKey ? new Resend(apiKey) : null;

// Default from address
const defaultFrom = process.env.RESEND_FROM_EMAIL || "Covered AI <noreply@covered.ai>";

// Types
export interface SendEmailParams {
  to: string | string[];
  subject: string;
  html: string;
  text?: string;
  from?: string;
  replyTo?: string;
  attachments?: Array<{
    filename: string;
    content: string;
  }>;
}

export interface SendTemplateParams {
  to: string | string[];
  template: string;
  data: Record<string, any>;
  from?: string;
  replyTo?: string;
}

export interface GetEmailStatusParams {
  emailId: string;
}

// Template directory
const TEMPLATE_DIR = path.resolve(process.cwd(), "templates/email");

// Template subjects
const TEMPLATE_SUBJECTS: Record<string, string> = {
  acknowledgment: "Thanks for calling {{business_name}}",
  "social-proof": "See what our customers are saying",
  "video-intro": "{{owner_name}} has a message for you",
  "case-study": "How we helped a customer just like you",
  faq: "Got questions? We've got answers",
  "review-request": "How did we do?",
  "re-engage": "We miss you! Here's a special offer",
  "long-nurture": "Still thinking about it?",
};

// Load and compile template
function loadTemplate(templateName: string): string | null {
  const templatePath = path.join(TEMPLATE_DIR, `${templateName}.html`);

  try {
    if (fs.existsSync(templatePath)) {
      return fs.readFileSync(templatePath, "utf-8");
    }
  } catch (error) {
    console.error(`Failed to load template ${templateName}:`, error);
  }

  return null;
}

// Simple template variable replacement
function compileTemplate(template: string, data: Record<string, any>): string {
  let result = template;

  for (const [key, value] of Object.entries(data)) {
    const regex = new RegExp(`\\{\\{\\s*${key}\\s*\\}\\}`, "g");
    result = result.replace(regex, String(value ?? ""));
  }

  return result;
}

// Tool implementations

export async function sendEmail(params: SendEmailParams) {
  if (!resend) {
    throw new Error("Resend client not initialized. Check RESEND_API_KEY.");
  }

  const { to, subject, html, text, from, replyTo, attachments } = params;

  const result = await resend.emails.send({
    from: from || defaultFrom,
    to: Array.isArray(to) ? to : [to],
    subject,
    html,
    text,
    reply_to: replyTo,
    attachments: attachments?.map((a) => ({
      filename: a.filename,
      content: Buffer.from(a.content, "base64"),
    })),
  });

  if (result.error) {
    throw new Error(result.error.message);
  }

  return {
    success: true,
    id: result.data?.id,
    to,
    subject,
  };
}

export async function sendTemplate(params: SendTemplateParams) {
  if (!resend) {
    throw new Error("Resend client not initialized. Check RESEND_API_KEY.");
  }

  const { to, template, data, from, replyTo } = params;

  // Load template
  const templateHtml = loadTemplate(template);

  if (!templateHtml) {
    throw new Error(`Template not found: ${template}`);
  }

  // Compile template with data
  const html = compileTemplate(templateHtml, data);

  // Get subject from template mapping or use default
  let subject = TEMPLATE_SUBJECTS[template] || `Message from ${data.business_name || "Covered AI"}`;
  subject = compileTemplate(subject, data);

  const result = await resend.emails.send({
    from: from || defaultFrom,
    to: Array.isArray(to) ? to : [to],
    subject,
    html,
    reply_to: replyTo,
  });

  if (result.error) {
    throw new Error(result.error.message);
  }

  return {
    success: true,
    id: result.data?.id,
    to,
    template,
    subject,
  };
}

export async function getEmailStatus(params: GetEmailStatusParams) {
  if (!resend) {
    throw new Error("Resend client not initialized. Check RESEND_API_KEY.");
  }

  const { emailId } = params;

  const result = await resend.emails.get(emailId);

  if (result.error) {
    throw new Error(result.error.message);
  }

  return {
    id: result.data?.id,
    from: result.data?.from,
    to: result.data?.to,
    subject: result.data?.subject,
    created_at: result.data?.created_at,
    last_event: result.data?.last_event,
  };
}

export async function listTemplates() {
  // List available email templates
  const templates: Array<{ name: string; subject: string; exists: boolean }> = [];

  for (const [name, subject] of Object.entries(TEMPLATE_SUBJECTS)) {
    const exists = loadTemplate(name) !== null;
    templates.push({ name, subject, exists });
  }

  return { templates };
}

export async function previewTemplate(template: string, data: Record<string, any>) {
  const templateHtml = loadTemplate(template);

  if (!templateHtml) {
    throw new Error(`Template not found: ${template}`);
  }

  const html = compileTemplate(templateHtml, data);
  let subject = TEMPLATE_SUBJECTS[template] || "Preview";
  subject = compileTemplate(subject, data);

  return {
    template,
    subject,
    html,
    data,
  };
}

// Batch send (useful for nurture sequences)
export async function sendBatch(
  emails: Array<{
    to: string;
    subject: string;
    html: string;
    from?: string;
  }>
) {
  if (!resend) {
    throw new Error("Resend client not initialized. Check RESEND_API_KEY.");
  }

  const results = await Promise.allSettled(
    emails.map((email) =>
      resend.emails.send({
        from: email.from || defaultFrom,
        to: email.to,
        subject: email.subject,
        html: email.html,
      })
    )
  );

  const sent: string[] = [];
  const failed: Array<{ to: string; error: string }> = [];

  results.forEach((result, index) => {
    if (result.status === "fulfilled" && result.value.data?.id) {
      sent.push(result.value.data.id);
    } else {
      const error =
        result.status === "rejected"
          ? result.reason.message
          : result.value.error?.message || "Unknown error";
      failed.push({ to: emails[index].to, error });
    }
  });

  return {
    sent: sent.length,
    failed: failed.length,
    sentIds: sent,
    failures: failed,
  };
}
