---
title: "Covered AI — Trigger.dev Jobs Specification"
id: "14-trigger-jobs"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Covered AI — Trigger.dev Jobs Specification

## Document Info
- **Version**: 1.0
- **Created**: 2025-01-27
- **Purpose**: Complete job definitions for background processing
- **Stack**: Trigger.dev v3, Prisma, Resend

---

# JOB INDEX

| # | Job ID | Trigger | Purpose |
|---|--------|---------|---------|
| 1 | `process-vapi-call` | Webhook | Process incoming Vapi call data |
| 2 | `send-whatsapp-notification` | Event | Send WhatsApp summary to owner |
| 3 | `check-missed-callbacks` | Cron (2hr) | Find overdue callbacks |
| 4 | `send-invoice` | Event | Email invoice to customer |
| 5 | `invoice-reminder-sequence` | Cron (daily) | Send invoice reminders |
| 6 | `process-invoice-payment` | Webhook | Handle Stripe payment |
| 7 | `update-cash-metrics` | Cron (hourly) | Calculate cash flow metrics |
| 8 | `identify-customer` | Event | Find or create customer record |
| 9 | `calculate-unit-economics` | Cron (daily) | Calculate LTV, CAC, ratio |
| 10 | `request-review` | Cron (daily) | Send review requests |
| 11 | `check-new-reviews` | Cron (6hr) | Poll Google for new reviews |
| 12 | `process-nurture-step` | Cron (daily) | Send nurture sequence messages |
| 13 | `generate-weekly-summary` | Cron (weekly) | Email weekly report |
| 14 | `generate-attention-items` | Cron (15min) | Score and rank priorities |
| 15 | `calculate-dashboard-stats` | Cron (hourly) | Update today's stats |
| 16 | `process-monthly-billing` | Cron (monthly) | Create Stripe invoices |
| 17 | `handle-failed-payment` | Webhook | Handle payment failures |
| 18 | `sync-xero-invoice` | Event | Push invoice to Xero |
| 19 | `generate-invoice-pdf` | Event | Create PDF for invoice |
| 20 | `process-quote-response` | Webhook | Handle quote accept/reject |

---

# JOB 1: PROCESS VAPI CALL

## File
`src/trigger/calls/process-vapi-call.ts`

## Trigger
Webhook from Vapi on call completion

## Purpose
Extract call data, create/update customer, log call, send notification

## Implementation

```typescript
import { task } from "@trigger.dev/sdk/v3";
import { prisma } from "@/lib/prisma";
import { classifyIntent, classifyUrgency } from "@/lib/ai/classify";

interface VapiCallPayload {
  call_id: string;
  phone_number: string;
  duration: number;
  started_at: string;
  ended_at: string;
  transcript: string;
  summary: string;
  caller_name?: string;
  caller_phone: string;
  caller_email?: string;
  recording_url?: string;
}

export const processVapiCall = task({
  id: "process-vapi-call",
  retry: {
    maxAttempts: 3,
    minTimeoutInMs: 1000,
    maxTimeoutInMs: 10000,
  },
  run: async (payload: VapiCallPayload, { ctx }) => {
    const { call_id, caller_phone, transcript, summary } = payload;
    
    // 1. Find client by Covered number
    const client = await prisma.client.findFirst({
      where: { coveredNumber: payload.phone_number },
    });
    
    if (!client) {
      throw new Error(`No client found for number ${payload.phone_number}`);
    }
    
    // 2. Classify intent and urgency using AI
    const [intent, urgency] = await Promise.all([
      classifyIntent(transcript, summary),
      classifyUrgency(transcript, summary, client.emergencyKeywords),
    ]);
    
    // 3. Find or create customer
    const customer = await findOrCreateCustomer({
      clientId: client.id,
      phone: caller_phone,
      name: payload.caller_name,
      email: payload.caller_email,
    });
    
    // 4. Determine if callback needed
    const callbackRequired = 
      urgency === 'EMERGENCY' ||
      urgency === 'URGENT' ||
      intent === 'NEW_ENQUIRY' ||
      intent === 'BOOKING' ||
      intent === 'COMPLAINT';
    
    // 5. Create call record
    const call = await prisma.call.create({
      data: {
        clientId: client.id,
        vapiCallId: call_id,
        direction: 'INBOUND',
        fromNumber: caller_phone,
        toNumber: payload.phone_number,
        callerName: payload.caller_name || 'Unknown',
        callerPhone: caller_phone,
        callerEmail: payload.caller_email,
        summary,
        transcript,
        intent,
        urgency,
        status: 'COMPLETED',
        callbackRequired,
        startedAt: new Date(payload.started_at),
        endedAt: new Date(payload.ended_at),
        duration: payload.duration,
        customerId: customer?.id,
      },
    });
    
    // 6. Create attention item if needed
    if (callbackRequired) {
      await prisma.attentionItem.create({
        data: {
          clientId: client.id,
          type: urgency === 'EMERGENCY' ? 'EMERGENCY' : 'CALLBACK',
          title: payload.caller_name || 'Unknown caller',
          subtitle: summary.slice(0, 100),
          priority: urgency === 'EMERGENCY' ? 100 : 70,
          callId: call.id,
          expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000), // 24 hours
        },
      });
    }
    
    // 7. Trigger WhatsApp notification
    await sendWhatsappNotification.trigger({
      clientId: client.id,
      callId: call.id,
      callerName: payload.caller_name || 'Unknown',
      callerPhone: caller_phone,
      summary,
      urgency,
      callbackRequired,
    });
    
    // 8. Update customer last contact
    if (customer) {
      await prisma.customerRecord.update({
        where: { id: customer.id },
        data: { lastContactDate: new Date() },
      });
    }
    
    return { callId: call.id, customerId: customer?.id };
  },
});

async function findOrCreateCustomer({
  clientId,
  phone,
  name,
  email,
}: {
  clientId: string;
  phone: string;
  name?: string;
  email?: string;
}) {
  // Try to find by phone first
  let customer = await prisma.customerRecord.findFirst({
    where: { clientId, phone },
  });
  
  if (customer) {
    // Update name/email if we have better data
    if ((name && !customer.name) || (email && !customer.email)) {
      customer = await prisma.customerRecord.update({
        where: { id: customer.id },
        data: {
          name: name || customer.name,
          email: email || customer.email,
        },
      });
    }
    return customer;
  }
  
  // Try email
  if (email) {
    customer = await prisma.customerRecord.findFirst({
      where: { clientId, email },
    });
    if (customer) return customer;
  }
  
  // Create new customer
  return prisma.customerRecord.create({
    data: {
      clientId,
      name: name || 'Unknown',
      phone,
      email,
      firstContactDate: new Date(),
      lastContactDate: new Date(),
      acquisitionSource: 'GEMMA_CALL',
      status: 'LEAD',
    },
  });
}
```

---

# JOB 2: SEND WHATSAPP NOTIFICATION

## File
`src/trigger/notifications/send-whatsapp.ts`

## Trigger
Event from process-vapi-call

## Implementation

```typescript
import { task } from "@trigger.dev/sdk/v3";
import { prisma } from "@/lib/prisma";
import { sendWhatsApp } from "@/lib/twilio";

interface WhatsAppPayload {
  clientId: string;
  callId: string;
  callerName: string;
  callerPhone: string;
  summary: string;
  urgency: string;
  callbackRequired: boolean;
}

export const sendWhatsappNotification = task({
  id: "send-whatsapp-notification",
  retry: {
    maxAttempts: 3,
  },
  run: async (payload: WhatsAppPayload) => {
    const client = await prisma.client.findUnique({
      where: { id: payload.clientId },
      include: { owner: true },
    });
    
    if (!client?.owner?.phone) {
      throw new Error("No owner phone number found");
    }
    
    const urgencyEmoji = payload.urgency === 'EMERGENCY' ? '🚨' : 
                         payload.urgency === 'URGENT' ? '⚡' : '📞';
    
    const message = `${urgencyEmoji} New call handled

Caller: ${payload.callerName}
Phone: ${payload.callerPhone}

Summary: ${payload.summary}

${payload.callbackRequired ? 'Reply:\n1 - Call back\n2 - Create job\n3 - Send quote' : ''}`;
    
    await sendWhatsApp({
      to: client.owner.phone,
      body: message,
    });
    
    return { sent: true };
  },
});
```

---

# JOB 3: CHECK MISSED CALLBACKS

## File
`src/trigger/calls/check-missed-callbacks.ts`

## Trigger
Cron: Every 2 hours

## Implementation

```typescript
import { task, schedules } from "@trigger.dev/sdk/v3";
import { prisma } from "@/lib/prisma";
import { sendEmail } from "@/lib/resend";
import { MissedCallbackEmail } from "@/emails/calls/missed-callback";

export const checkMissedCallbacks = schedules.task({
  id: "check-missed-callbacks",
  cron: "0 */2 * * *", // Every 2 hours
  run: async () => {
    const fourHoursAgo = new Date(Date.now() - 4 * 60 * 60 * 1000);
    const twentyFourHoursAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
    
    // Find callbacks pending > 4 hours
    const pendingCallbacks = await prisma.call.findMany({
      where: {
        callbackRequired: true,
        callbackCompleted: false,
        createdAt: {
          lt: fourHoursAgo,
          gt: twentyFourHoursAgo,
        },
        reminderSentAt: null,
      },
      include: {
        client: {
          include: { owner: true },
        },
      },
    });
    
    for (const call of pendingCallbacks) {
      if (!call.client.owner?.email) continue;
      
      const hoursWaiting = Math.round(
        (Date.now() - call.createdAt.getTime()) / (1000 * 60 * 60)
      );
      
      // Send reminder email
      await sendEmail({
        to: call.client.owner.email,
        subject: `Don't forget: ${call.callerName} is waiting for your call`,
        react: MissedCallbackEmail({
          businessName: call.client.businessName,
          ownerName: call.client.owner.name,
          callerName: call.callerName,
          callerPhone: call.callerPhone,
          callSummary: call.summary,
          hoursWaiting,
          dashboardLink: `${process.env.APP_URL}/dashboard/calls/${call.id}`,
        }),
      });
      
      // Mark reminder sent
      await prisma.call.update({
        where: { id: call.id },
        data: { reminderSentAt: new Date() },
      });
    }
    
    // Find callbacks pending > 24 hours - escalate
    const escalatedCallbacks = await prisma.call.findMany({
      where: {
        callbackRequired: true,
        callbackCompleted: false,
        createdAt: { lt: twentyFourHoursAgo },
        escalatedAt: null,
      },
      include: {
        client: { include: { owner: true } },
      },
    });
    
    for (const call of escalatedCallbacks) {
      // Send SMS escalation
      if (call.client.owner?.phone) {
        await sendSMS({
          to: call.client.owner.phone,
          body: `⚠️ ${call.callerName} has been waiting 24+ hours for a callback. Please respond ASAP.`,
        });
      }
      
      await prisma.call.update({
        where: { id: call.id },
        data: { escalatedAt: new Date() },
      });
    }
    
    return {
      reminders: pendingCallbacks.length,
      escalations: escalatedCallbacks.length,
    };
  },
});
```

---

# JOB 4: SEND INVOICE

## File
`src/trigger/invoices/send-invoice.ts`

## Trigger
Event when invoice created with sendNow=true or manual send

## Implementation

```typescript
import { task } from "@trigger.dev/sdk/v3";
import { prisma } from "@/lib/prisma";
import { sendEmail } from "@/lib/resend";
import { InvoiceSentEmail } from "@/emails/invoice/invoice-sent";
import { generateInvoicePdf } from "./generate-invoice-pdf";

interface SendInvoicePayload {
  invoiceId: string;
}

export const sendInvoice = task({
  id: "send-invoice",
  retry: {
    maxAttempts: 3,
  },
  run: async (payload: SendInvoicePayload) => {
    const invoice = await prisma.invoice.findUnique({
      where: { id: payload.invoiceId },
      include: {
        client: true,
      },
    });
    
    if (!invoice) {
      throw new Error(`Invoice ${payload.invoiceId} not found`);
    }
    
    if (!invoice.customerEmail) {
      throw new Error("No customer email on invoice");
    }
    
    // Generate PDF
    const pdfResult = await generateInvoicePdf.triggerAndWait({
      invoiceId: invoice.id,
    });
    
    // Create payment link
    const paymentLink = invoice.stripePaymentLink || 
      `${process.env.APP_URL}/pay/${invoice.id}`;
    
    // Send email
    await sendEmail({
      to: invoice.customerEmail,
      subject: `Invoice ${invoice.invoiceNumber} from ${invoice.client.businessName}`,
      react: InvoiceSentEmail({
        businessName: invoice.client.businessName,
        customerName: invoice.customerName,
        invoiceNumber: invoice.invoiceNumber,
        amount: formatCurrency(invoice.amount),
        dueDate: formatDate(invoice.dueDate),
        description: invoice.description || 'Services rendered',
        paymentLink,
        bankDetails: invoice.client.bankDetails,
      }),
      attachments: pdfResult?.pdfUrl ? [{
        filename: `${invoice.invoiceNumber}.pdf`,
        path: pdfResult.pdfUrl,
      }] : undefined,
    });
    
    // Update invoice status
    await prisma.invoice.update({
      where: { id: invoice.id },
      data: {
        status: 'SENT',
        sentAt: new Date(),
      },
    });
    
    return { sent: true, invoiceId: invoice.id };
  },
});
```

---

# JOB 5: INVOICE REMINDER SEQUENCE

## File
`src/trigger/invoices/invoice-reminder-sequence.ts`

## Trigger
Cron: Daily at 9am

## Implementation

```typescript
import { schedules } from "@trigger.dev/sdk/v3";
import { prisma } from "@/lib/prisma";
import { sendEmail } from "@/lib/resend";
import { InvoiceReminder1 } from "@/emails/invoice/reminder-1";
import { InvoiceReminder2 } from "@/emails/invoice/reminder-2";
import { InvoiceFinalNotice } from "@/emails/invoice/final-notice";

export const invoiceReminderSequence = schedules.task({
  id: "invoice-reminder-sequence",
  cron: "0 9 * * *", // Daily at 9am
  run: async () => {
    const now = new Date();
    
    // Get all unpaid invoices
    const unpaidInvoices = await prisma.invoice.findMany({
      where: {
        status: { in: ['SENT', 'REMINDED', 'OVERDUE'] },
      },
      include: { client: true },
    });
    
    const results = {
      reminder1: 0,
      reminder2: 0,
      finalNotice: 0,
    };
    
    for (const invoice of unpaidInvoices) {
      if (!invoice.customerEmail || !invoice.sentAt) continue;
      
      const daysSinceSent = Math.floor(
        (now.getTime() - invoice.sentAt.getTime()) / (1000 * 60 * 60 * 24)
      );
      
      const paymentLink = invoice.stripePaymentLink || 
        `${process.env.APP_URL}/pay/${invoice.id}`;
      
      // Day 7: First reminder
      if (daysSinceSent >= 7 && !invoice.reminder1SentAt) {
        await sendEmail({
          to: invoice.customerEmail,
          subject: `Friendly reminder: Invoice ${invoice.invoiceNumber}`,
          react: InvoiceReminder1({
            businessName: invoice.client.businessName,
            customerName: invoice.customerName,
            invoiceNumber: invoice.invoiceNumber,
            amount: formatCurrency(invoice.amount),
            dueDate: formatDate(invoice.dueDate),
            paymentLink,
          }),
        });
        
        await prisma.invoice.update({
          where: { id: invoice.id },
          data: { reminder1SentAt: now },
        });
        
        results.reminder1++;
      }
      
      // Day 14: Second reminder (now overdue)
      else if (daysSinceSent >= 14 && !invoice.reminder2SentAt) {
        await sendEmail({
          to: invoice.customerEmail,
          subject: `Invoice ${invoice.invoiceNumber} is now overdue`,
          react: InvoiceReminder2({
            businessName: invoice.client.businessName,
            customerName: invoice.customerName,
            invoiceNumber: invoice.invoiceNumber,
            amount: formatCurrency(invoice.amount),
            originalDueDate: formatDate(invoice.dueDate),
            paymentLink,
          }),
        });
        
        await prisma.invoice.update({
          where: { id: invoice.id },
          data: {
            reminder2SentAt: now,
            status: 'OVERDUE',
          },
        });
        
        results.reminder2++;
      }
      
      // Day 21: Final notice
      else if (daysSinceSent >= 21 && !invoice.finalNoticeSentAt) {
        const daysOverdue = daysSinceSent - 14; // Assuming 14-day terms
        
        await sendEmail({
          to: invoice.customerEmail,
          subject: `Final notice: Invoice ${invoice.invoiceNumber}`,
          react: InvoiceFinalNotice({
            businessName: invoice.client.businessName,
            customerName: invoice.customerName,
            invoiceNumber: invoice.invoiceNumber,
            amount: formatCurrency(invoice.amount),
            daysOverdue,
            paymentLink,
          }),
        });
        
        await prisma.invoice.update({
          where: { id: invoice.id },
          data: { finalNoticeSentAt: now },
        });
        
        results.finalNotice++;
      }
    }
    
    return results;
  },
});
```

---

# JOB 6: PROCESS INVOICE PAYMENT

## File
`src/trigger/invoices/process-payment.ts`

## Trigger
Webhook from Stripe

## Implementation

```typescript
import { task } from "@trigger.dev/sdk/v3";
import { prisma } from "@/lib/prisma";
import { sendEmail } from "@/lib/resend";
import { PaymentReceiptEmail } from "@/emails/invoice/receipt";
import { updateCashMetrics } from "./update-cash-metrics";

interface PaymentPayload {
  invoiceId: string;
  stripePaymentIntentId: string;
  amountPaid: number;
  paymentMethod: string;
}

export const processInvoicePayment = task({
  id: "process-invoice-payment",
  run: async (payload: PaymentPayload) => {
    const invoice = await prisma.invoice.findUnique({
      where: { id: payload.invoiceId },
      include: { client: true },
    });
    
    if (!invoice) {
      throw new Error(`Invoice ${payload.invoiceId} not found`);
    }
    
    // Update invoice
    await prisma.invoice.update({
      where: { id: invoice.id },
      data: {
        status: 'PAID',
        paidAt: new Date(),
        paymentMethod: payload.paymentMethod,
        paymentReference: payload.stripePaymentIntentId,
      },
    });
    
    // Send receipt
    if (invoice.customerEmail) {
      await sendEmail({
        to: invoice.customerEmail,
        subject: `Payment received - Thank you!`,
        react: PaymentReceiptEmail({
          businessName: invoice.client.businessName,
          customerName: invoice.customerName,
          invoiceNumber: invoice.invoiceNumber,
          amount: formatCurrency(invoice.amount),
          paymentDate: formatDate(new Date()),
        }),
      });
    }
    
    // Update cash metrics
    await updateCashMetrics.trigger({ clientId: invoice.clientId });
    
    // Remove from attention items
    await prisma.attentionItem.deleteMany({
      where: {
        clientId: invoice.clientId,
        invoiceId: invoice.id,
      },
    });
    
    return { paid: true, invoiceId: invoice.id };
  },
});
```

---

# JOB 7: UPDATE CASH METRICS

## File
`src/trigger/metrics/update-cash-metrics.ts`

## Trigger
Cron: Hourly + Event on payment

## Implementation

```typescript
import { task, schedules } from "@trigger.dev/sdk/v3";
import { prisma } from "@/lib/prisma";

interface UpdateCashMetricsPayload {
  clientId: string;
}

export const updateCashMetrics = task({
  id: "update-cash-metrics",
  run: async (payload: UpdateCashMetricsPayload) => {
    const { clientId } = payload;
    
    const now = new Date();
    const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
    const startOfLastMonth = new Date(now.getFullYear(), now.getMonth() - 1, 1);
    const endOfLastMonth = new Date(now.getFullYear(), now.getMonth(), 0);
    
    // Calculate metrics
    const [
      totalOutstanding,
      totalOverdue,
      collectedThisMonth,
      collectedLastMonth,
      paidInvoices,
    ] = await Promise.all([
      // Outstanding: All unpaid invoices
      prisma.invoice.aggregate({
        where: {
          clientId,
          status: { in: ['SENT', 'REMINDED', 'OVERDUE'] },
        },
        _sum: { amount: true },
      }),
      
      // Overdue: Status = OVERDUE
      prisma.invoice.aggregate({
        where: {
          clientId,
          status: 'OVERDUE',
        },
        _sum: { amount: true },
      }),
      
      // Collected this month
      prisma.invoice.aggregate({
        where: {
          clientId,
          status: 'PAID',
          paidAt: { gte: startOfMonth },
        },
        _sum: { amount: true },
      }),
      
      // Collected last month
      prisma.invoice.aggregate({
        where: {
          clientId,
          status: 'PAID',
          paidAt: {
            gte: startOfLastMonth,
            lte: endOfLastMonth,
          },
        },
        _sum: { amount: true },
      }),
      
      // For DSO calculation
      prisma.invoice.findMany({
        where: {
          clientId,
          status: 'PAID',
          paidAt: { gte: startOfMonth },
          sentAt: { not: null },
        },
        select: {
          sentAt: true,
          paidAt: true,
        },
      }),
    ]);
    
    // Calculate average DSO
    let averageDSO = 0;
    if (paidInvoices.length > 0) {
      const totalDays = paidInvoices.reduce((sum, inv) => {
        if (inv.sentAt && inv.paidAt) {
          return sum + Math.floor(
            (inv.paidAt.getTime() - inv.sentAt.getTime()) / (1000 * 60 * 60 * 24)
          );
        }
        return sum;
      }, 0);
      averageDSO = Math.round(totalDays / paidInvoices.length);
    }
    
    // Upsert metrics
    await prisma.clientCashMetrics.upsert({
      where: { clientId },
      create: {
        clientId,
        totalOutstanding: totalOutstanding._sum.amount || 0,
        totalOverdue: totalOverdue._sum.amount || 0,
        collectedThisMonth: collectedThisMonth._sum.amount || 0,
        collectedLastMonth: collectedLastMonth._sum.amount || 0,
        averageDSO,
        updatedAt: now,
      },
      update: {
        totalOutstanding: totalOutstanding._sum.amount || 0,
        totalOverdue: totalOverdue._sum.amount || 0,
        collectedThisMonth: collectedThisMonth._sum.amount || 0,
        collectedLastMonth: collectedLastMonth._sum.amount || 0,
        averageDSO,
        updatedAt: now,
      },
    });
    
    return { clientId, updated: true };
  },
});

// Scheduled version for all clients
export const updateAllCashMetrics = schedules.task({
  id: "update-all-cash-metrics",
  cron: "0 * * * *", // Hourly
  run: async () => {
    const clients = await prisma.client.findMany({
      where: { status: 'ACTIVE' },
      select: { id: true },
    });
    
    for (const client of clients) {
      await updateCashMetrics.trigger({ clientId: client.id });
    }
    
    return { clientsUpdated: clients.length };
  },
});
```

---

# JOB 8: IDENTIFY CUSTOMER

## File
`src/trigger/customers/identify-customer.ts`

## Trigger
Event on job completion

## Implementation

```typescript
import { task } from "@trigger.dev/sdk/v3";
import { prisma } from "@/lib/prisma";

interface IdentifyCustomerPayload {
  clientId: string;
  phone?: string;
  email?: string;
  name?: string;
  jobId?: string;
}

export const identifyCustomer = task({
  id: "identify-customer",
  run: async (payload: IdentifyCustomerPayload) => {
    const { clientId, phone, email, name, jobId } = payload;
    
    let customer = null;
    
    // Try phone first
    if (phone) {
      customer = await prisma.customerRecord.findFirst({
        where: { clientId, phone },
      });
    }
    
    // Try email
    if (!customer && email) {
      customer = await prisma.customerRecord.findFirst({
        where: { clientId, email },
      });
    }
    
    if (customer) {
      // Update with any new info
      customer = await prisma.customerRecord.update({
        where: { id: customer.id },
        data: {
          name: name || customer.name,
          email: email || customer.email,
          phone: phone || customer.phone,
          lastContactDate: new Date(),
          totalJobs: { increment: 1 },
        },
      });
    } else {
      // Create new
      customer = await prisma.customerRecord.create({
        data: {
          clientId,
          name: name || 'Unknown',
          phone,
          email,
          firstContactDate: new Date(),
          lastContactDate: new Date(),
          totalJobs: 1,
          acquisitionSource: 'GEMMA_CALL',
          status: 'ACTIVE',
        },
      });
    }
    
    // Link job to customer
    if (jobId) {
      await prisma.job.update({
        where: { id: jobId },
        data: { customerId: customer.id },
      });
      
      // Update customer revenue
      const job = await prisma.job.findUnique({
        where: { id: jobId },
        select: { actualValue: true, estimatedValue: true },
      });
      
      if (job) {
        const revenue = job.actualValue || job.estimatedValue || 0;
        await prisma.customerRecord.update({
          where: { id: customer.id },
          data: {
            totalRevenue: { increment: revenue },
          },
        });
      }
    }
    
    return { customerId: customer.id, isNew: !customer.id };
  },
});
```

---

# JOB 9: CALCULATE UNIT ECONOMICS

## File
`src/trigger/metrics/calculate-unit-economics.ts`

## Trigger
Cron: Daily at midnight + on-demand

## Implementation

```typescript
import { task, schedules } from "@trigger.dev/sdk/v3";
import { prisma } from "@/lib/prisma";

interface CalculateUnitEconomicsPayload {
  clientId: string;
}

export const calculateUnitEconomics = task({
  id: "calculate-unit-economics",
  run: async (payload: CalculateUnitEconomicsPayload) => {
    const { clientId } = payload;
    
    const now = new Date();
    const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
    
    // Get customer stats
    const [
      totalCustomers,
      repeatCustomers,
      customerStats,
      marketingSpend,
      newCustomersThisMonth,
    ] = await Promise.all([
      prisma.customerRecord.count({
        where: { clientId, status: 'ACTIVE' },
      }),
      
      prisma.customerRecord.count({
        where: { clientId, totalJobs: { gte: 2 } },
      }),
      
      prisma.customerRecord.aggregate({
        where: { clientId, status: 'ACTIVE' },
        _avg: { totalJobs: true, totalRevenue: true },
      }),
      
      prisma.marketingSpend.aggregate({
        where: {
          clientId,
          month: {
            gte: startOfMonth,
          },
        },
        _sum: { amount: true },
      }),
      
      prisma.customerRecord.count({
        where: {
          clientId,
          firstContactDate: { gte: startOfMonth },
        },
      }),
    ]);
    
    // Calculate metrics
    const repeatRate = totalCustomers > 0 
      ? Math.round((repeatCustomers / totalCustomers) * 100) 
      : 0;
    
    const avgJobValue = customerStats._avg.totalRevenue && customerStats._avg.totalJobs
      ? Math.round(customerStats._avg.totalRevenue / customerStats._avg.totalJobs)
      : 0;
    
    const avgJobsPerCustomer = customerStats._avg.totalJobs || 0;
    
    const customerLTV = Math.round(avgJobValue * avgJobsPerCustomer);
    
    const totalMarketingSpend = marketingSpend._sum.amount || 0;
    
    const avgCAC = newCustomersThisMonth > 0
      ? Math.round(totalMarketingSpend / newCustomersThisMonth)
      : 0;
    
    const ltvCacRatio = avgCAC > 0
      ? Math.round((customerLTV / avgCAC) * 10) / 10
      : 0;
    
    // Get last month's ratio for trend
    const lastMetrics = await prisma.clientUnitEconomics.findUnique({
      where: { clientId },
      select: { ltvCacRatio: true },
    });
    
    const ltvCacTrend = lastMetrics
      ? ltvCacRatio > lastMetrics.ltvCacRatio ? 'UP'
        : ltvCacRatio < lastMetrics.ltvCacRatio ? 'DOWN'
        : 'STABLE'
      : 'STABLE';
    
    // Upsert metrics
    await prisma.clientUnitEconomics.upsert({
      where: { clientId },
      create: {
        clientId,
        totalCustomers,
        repeatCustomers,
        repeatRate,
        avgJobValue,
        avgJobsPerCustomer,
        customerLTV,
        totalMarketingSpend,
        newCustomersThisMonth,
        avgCAC,
        ltvCacRatio,
        ltvCacLastMonth: 0,
        ltvCacTrend,
        updatedAt: now,
      },
      update: {
        totalCustomers,
        repeatCustomers,
        repeatRate,
        avgJobValue,
        avgJobsPerCustomer,
        customerLTV,
        totalMarketingSpend,
        newCustomersThisMonth,
        avgCAC,
        ltvCacLastMonth: lastMetrics?.ltvCacRatio || 0,
        ltvCacRatio,
        ltvCacTrend,
        updatedAt: now,
      },
    });
    
    return { clientId, ltvCacRatio };
  },
});

// Scheduled version
export const calculateAllUnitEconomics = schedules.task({
  id: "calculate-all-unit-economics",
  cron: "0 0 * * *", // Daily at midnight
  run: async () => {
    const clients = await prisma.client.findMany({
      where: { status: 'ACTIVE' },
      select: { id: true },
    });
    
    for (const client of clients) {
      await calculateUnitEconomics.trigger({ clientId: client.id });
    }
    
    return { clientsUpdated: clients.length };
  },
});
```

---

# JOB 10: REQUEST REVIEW

## File
`src/trigger/reviews/request-review.ts`

## Trigger
Cron: Daily at 10am

## Implementation

```typescript
import { schedules } from "@trigger.dev/sdk/v3";
import { prisma } from "@/lib/prisma";
import { sendEmail } from "@/lib/resend";
import { ReviewRequestEmail } from "@/emails/review/review-request";

export const requestReviews = schedules.task({
  id: "request-reviews",
  cron: "0 10 * * *", // Daily at 10am
  run: async () => {
    const twoDaysAgo = new Date(Date.now() - 48 * 60 * 60 * 1000);
    const threeDaysAgo = new Date(Date.now() - 72 * 60 * 60 * 1000);
    
    // Find completed jobs without review requests
    const eligibleJobs = await prisma.job.findMany({
      where: {
        status: 'COMPLETED',
        completedAt: {
          gte: threeDaysAgo,
          lte: twoDaysAgo,
        },
        reviews: {
          none: {},
        },
        customer: {
          email: { not: null },
        },
      },
      include: {
        client: true,
        customer: true,
      },
    });
    
    let sent = 0;
    
    for (const job of eligibleJobs) {
      if (!job.customer?.email) continue;
      
      // Create review record
      const review = await prisma.review.create({
        data: {
          clientId: job.clientId,
          customerId: job.customerId,
          jobId: job.id,
          requestedAt: new Date(),
          requestMethod: 'EMAIL',
          status: 'REQUESTED',
        },
      });
      
      // Generate review link
      const reviewLink = `${process.env.APP_URL}/r/${review.id}`;
      
      // Send email
      await sendEmail({
        to: job.customer.email,
        subject: `How did we do, ${job.customer.name}?`,
        react: ReviewRequestEmail({
          businessName: job.client.businessName,
          ownerName: job.client.owner?.name || 'The team',
          customerName: job.customer.name,
          jobType: job.title,
          reviewLink,
        }),
      });
      
      sent++;
    }
    
    return { reviewsSent: sent };
  },
});
```

---

# JOB 11: CHECK NEW REVIEWS

## File
`src/trigger/reviews/check-new-reviews.ts`

## Trigger
Cron: Every 6 hours

## Implementation

```typescript
import { schedules } from "@trigger.dev/sdk/v3";
import { prisma } from "@/lib/prisma";
import { getGoogleReviews } from "@/lib/google-places";

export const checkNewReviews = schedules.task({
  id: "check-new-reviews",
  cron: "0 */6 * * *", // Every 6 hours
  run: async () => {
    const clients = await prisma.client.findMany({
      where: {
        status: 'ACTIVE',
        googlePlaceId: { not: null },
      },
      select: {
        id: true,
        googlePlaceId: true,
      },
    });
    
    let newReviews = 0;
    
    for (const client of clients) {
      if (!client.googlePlaceId) continue;
      
      // Fetch reviews from Google
      const reviews = await getGoogleReviews(client.googlePlaceId);
      
      for (const review of reviews) {
        // Check if we already have this review
        const existing = await prisma.review.findFirst({
          where: {
            clientId: client.id,
            platformReviewId: review.review_id,
          },
        });
        
        if (!existing) {
          // Try to match to customer
          const customer = await prisma.customerRecord.findFirst({
            where: {
              clientId: client.id,
              name: { contains: review.author_name, mode: 'insensitive' },
            },
          });
          
          // Create review record
          await prisma.review.create({
            data: {
              clientId: client.id,
              customerId: customer?.id,
              platform: 'GOOGLE',
              platformReviewId: review.review_id,
              platformUrl: review.review_url,
              rating: review.rating,
              reviewText: review.text,
              status: 'COMPLETED',
              createdAt: new Date(review.time * 1000),
            },
          });
          
          newReviews++;
        }
      }
    }
    
    return { newReviews };
  },
});
```

---

# JOB 12: PROCESS NURTURE STEP

## File
`src/trigger/nurture/process-nurture-step.ts`

## Trigger
Cron: Daily at 10am

## Implementation

```typescript
import { schedules } from "@trigger.dev/sdk/v3";
import { prisma } from "@/lib/prisma";
import { sendEmail } from "@/lib/resend";
import { sendSMS } from "@/lib/twilio";

export const processNurtureSteps = schedules.task({
  id: "process-nurture-steps",
  cron: "0 10 * * *", // Daily at 10am
  run: async () => {
    const now = new Date();
    
    // Find enrollments due for next step
    const dueEnrollments = await prisma.nurtureEnrollment.findMany({
      where: {
        status: 'ACTIVE',
        nextStepAt: { lte: now },
      },
      include: {
        sequence: true,
        customer: true,
        client: true,
      },
    });
    
    let processed = 0;
    
    for (const enrollment of dueEnrollments) {
      const steps = enrollment.sequence.steps as NurtureStep[];
      const currentStepIndex = enrollment.currentStep;
      
      if (currentStepIndex >= steps.length) {
        // Sequence complete
        await prisma.nurtureEnrollment.update({
          where: { id: enrollment.id },
          data: {
            status: 'COMPLETED',
            completedAt: now,
          },
        });
        continue;
      }
      
      const step = steps[currentStepIndex];
      
      // Execute step
      if (step.type === 'email' && enrollment.customer.email) {
        await sendEmail({
          to: enrollment.customer.email,
          subject: replaceVariables(step.subject, enrollment),
          html: replaceVariables(step.content, enrollment),
        });
      } else if (step.type === 'sms' && enrollment.customer.phone) {
        await sendSMS({
          to: enrollment.customer.phone,
          body: replaceVariables(step.content, enrollment),
        });
      }
      
      // Calculate next step time
      const nextStepIndex = currentStepIndex + 1;
      const nextStep = steps[nextStepIndex];
      const nextStepAt = nextStep
        ? new Date(now.getTime() + nextStep.delayDays * 24 * 60 * 60 * 1000)
        : null;
      
      // Update enrollment
      await prisma.nurtureEnrollment.update({
        where: { id: enrollment.id },
        data: {
          currentStep: nextStepIndex,
          lastStepAt: now,
          nextStepAt,
          status: nextStepIndex >= steps.length ? 'COMPLETED' : 'ACTIVE',
          completedAt: nextStepIndex >= steps.length ? now : null,
        },
      });
      
      processed++;
    }
    
    return { processed };
  },
});

function replaceVariables(text: string, enrollment: any): string {
  return text
    .replace(/{{customer_name}}/g, enrollment.customer.name)
    .replace(/{{business_name}}/g, enrollment.client.businessName)
    .replace(/{{first_name}}/g, enrollment.customer.name.split(' ')[0]);
}
```

---

# JOB 13: GENERATE WEEKLY SUMMARY

## File
`src/trigger/reports/weekly-summary.ts`

## Trigger
Cron: Monday 8am

## Implementation

```typescript
import { schedules } from "@trigger.dev/sdk/v3";
import { prisma } from "@/lib/prisma";
import { sendEmail } from "@/lib/resend";
import { WeeklySummaryEmail } from "@/emails/reports/weekly-summary";

export const generateWeeklySummary = schedules.task({
  id: "generate-weekly-summary",
  cron: "0 8 * * 1", // Monday 8am
  run: async () => {
    const now = new Date();
    const weekStart = new Date(now);
    weekStart.setDate(weekStart.getDate() - 7);
    
    const clients = await prisma.client.findMany({
      where: { status: 'ACTIVE' },
      include: { owner: true },
    });
    
    let sent = 0;
    
    for (const client of clients) {
      if (!client.owner?.email) continue;
      
      // Gather stats
      const [calls, jobs, invoices, customers, reviews] = await Promise.all([
        prisma.call.count({
          where: { clientId: client.id, createdAt: { gte: weekStart } },
        }),
        prisma.job.count({
          where: { clientId: client.id, status: 'COMPLETED', completedAt: { gte: weekStart } },
        }),
        prisma.invoice.aggregate({
          where: { clientId: client.id, status: 'PAID', paidAt: { gte: weekStart } },
          _sum: { amount: true },
        }),
        prisma.customerRecord.count({
          where: { clientId: client.id, firstContactDate: { gte: weekStart } },
        }),
        prisma.review.count({
          where: { clientId: client.id, status: 'COMPLETED', createdAt: { gte: weekStart } },
        }),
      ]);
      
      // Generate insight
      const insight = generateInsight({
        calls,
        jobs,
        revenue: invoices._sum.amount || 0,
        newCustomers: customers,
        reviews,
      });
      
      await sendEmail({
        to: client.owner.email,
        subject: `Your week with Covered AI`,
        react: WeeklySummaryEmail({
          businessName: client.businessName,
          ownerName: client.owner.name,
          weekEnding: formatDate(now),
          stats: {
            callsHandled: calls,
            jobsCompleted: jobs,
            revenueCollected: invoices._sum.amount || 0,
            newCustomers: customers,
            reviewsReceived: reviews,
          },
          insight,
          dashboardLink: `${process.env.APP_URL}/dashboard`,
        }),
      });
      
      sent++;
    }
    
    return { sent };
  },
});

function generateInsight(stats: any): string {
  if (stats.calls > 50) {
    return "Busy week! Gemma handled a high volume of calls for you.";
  }
  if (stats.revenue > 5000) {
    return "Great revenue week! Your cash flow is looking healthy.";
  }
  if (stats.reviews >= 3) {
    return "Nice work on the reviews! Social proof builds trust.";
  }
  if (stats.newCustomers >= 5) {
    return "Strong customer acquisition this week. Keep it up!";
  }
  return "Steady week. Small consistent progress adds up!";
}
```

---

# JOB 14: GENERATE ATTENTION ITEMS

## File
`src/trigger/dashboard/generate-attention-items.ts`

## Trigger
Cron: Every 15 minutes

## Implementation

```typescript
import { schedules } from "@trigger.dev/sdk/v3";
import { prisma } from "@/lib/prisma";

export const generateAttentionItems = schedules.task({
  id: "generate-attention-items",
  cron: "*/15 * * * *", // Every 15 minutes
  run: async () => {
    const clients = await prisma.client.findMany({
      where: { status: 'ACTIVE' },
      select: { id: true },
    });
    
    for (const client of clients) {
      // Clear old items
      await prisma.attentionItem.deleteMany({
        where: {
          clientId: client.id,
          expiresAt: { lt: new Date() },
        },
      });
      
      // Emergency calls (not already in attention items)
      const emergencyCalls = await prisma.call.findMany({
        where: {
          clientId: client.id,
          urgency: 'EMERGENCY',
          callbackRequired: true,
          callbackCompleted: false,
          attentionItems: { none: {} },
        },
      });
      
      for (const call of emergencyCalls) {
        await prisma.attentionItem.upsert({
          where: {
            clientId_type_referenceId: {
              clientId: client.id,
              type: 'EMERGENCY',
              referenceId: call.id,
            },
          },
          create: {
            clientId: client.id,
            type: 'EMERGENCY',
            title: call.callerName,
            subtitle: call.summary.slice(0, 100),
            priority: 100,
            referenceId: call.id,
            callId: call.id,
            expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000),
          },
          update: {
            priority: 100,
          },
        });
      }
      
      // Pending callbacks
      const callbackCalls = await prisma.call.findMany({
        where: {
          clientId: client.id,
          callbackRequired: true,
          callbackCompleted: false,
          urgency: { not: 'EMERGENCY' },
        },
      });
      
      for (const call of callbackCalls) {
        const hoursOld = (Date.now() - call.createdAt.getTime()) / (1000 * 60 * 60);
        const priority = 70 + (hoursOld > 2 ? 20 : 0);
        
        await prisma.attentionItem.upsert({
          where: {
            clientId_type_referenceId: {
              clientId: client.id,
              type: 'CALLBACK',
              referenceId: call.id,
            },
          },
          create: {
            clientId: client.id,
            type: 'CALLBACK',
            title: call.callerName,
            subtitle: call.summary.slice(0, 100),
            priority,
            referenceId: call.id,
            callId: call.id,
            expiresAt: new Date(Date.now() + 48 * 60 * 60 * 1000),
          },
          update: { priority },
        });
      }
      
      // Overdue invoices
      const overdueInvoices = await prisma.invoice.findMany({
        where: {
          clientId: client.id,
          status: 'OVERDUE',
        },
      });
      
      for (const invoice of overdueInvoices) {
        const daysOverdue = Math.floor(
          (Date.now() - invoice.dueDate.getTime()) / (1000 * 60 * 60 * 24)
        );
        const priority = 50 + (daysOverdue >= 14 ? 30 : daysOverdue >= 7 ? 15 : 0);
        
        await prisma.attentionItem.upsert({
          where: {
            clientId_type_referenceId: {
              clientId: client.id,
              type: 'OVERDUE_INVOICE',
              referenceId: invoice.id,
            },
          },
          create: {
            clientId: client.id,
            type: 'OVERDUE_INVOICE',
            title: `Invoice ${invoice.invoiceNumber} overdue`,
            subtitle: `${invoice.customerName} — £${invoice.amount} • ${daysOverdue} days`,
            priority,
            referenceId: invoice.id,
            invoiceId: invoice.id,
            expiresAt: null, // Never expires until paid
          },
          update: { priority, subtitle: `${invoice.customerName} — £${invoice.amount} • ${daysOverdue} days` },
        });
      }
    }
    
    return { clientsProcessed: clients.length };
  },
});
```

---

# CLAUDE CODE PROMPT

```
Create all Trigger.dev jobs for Covered AI using the specifications in /specs/14-TRIGGER-JOBS.md

Install:
npm install @trigger.dev/sdk

Create these files:

src/trigger/calls/process-vapi-call.ts
src/trigger/calls/check-missed-callbacks.ts
src/trigger/notifications/send-whatsapp.ts
src/trigger/invoices/send-invoice.ts
src/trigger/invoices/invoice-reminder-sequence.ts
src/trigger/invoices/process-payment.ts
src/trigger/invoices/generate-invoice-pdf.ts
src/trigger/metrics/update-cash-metrics.ts
src/trigger/metrics/calculate-unit-economics.ts
src/trigger/customers/identify-customer.ts
src/trigger/reviews/request-review.ts
src/trigger/reviews/check-new-reviews.ts
src/trigger/nurture/process-nurture-step.ts
src/trigger/reports/weekly-summary.ts
src/trigger/dashboard/generate-attention-items.ts
src/trigger/dashboard/calculate-dashboard-stats.ts
src/trigger/billing/process-monthly-billing.ts
src/trigger/billing/handle-failed-payment.ts

Use exact implementations from spec. Register all jobs in src/trigger/index.ts
```
