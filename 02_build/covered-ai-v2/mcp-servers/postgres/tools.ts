/**
 * Covered AI - PostgreSQL MCP Server Tools
 *
 * Database query tools for leads, clients, jobs, and dashboard stats.
 */

import { PrismaClient, Prisma } from "@prisma/client";

const prisma = new PrismaClient();

// Types for tool parameters
export interface QueryLeadsParams {
  clientId: string;
  status?: string;
  urgency?: string;
  limit?: number;
  offset?: number;
}

export interface CreateLeadParams {
  clientId: string;
  callerPhone: string;
  callId?: string;
  callDuration?: number;
  recordingUrl?: string;
  transcript?: string;
  summary?: string;
  customerName?: string;
  address?: string;
  postcode?: string;
  jobType?: string;
  urgency?: "emergency" | "urgent" | "routine";
}

export interface UpdateLeadParams {
  id: string;
  status?: string;
  dismissReason?: string;
}

export interface CreateCustomerParams {
  clientId: string;
  name: string;
  phone: string;
  email?: string;
  address?: string;
  postcode?: string;
}

export interface CreateJobParams {
  clientId: string;
  customerId: string;
  leadId?: string;
  title: string;
  description?: string;
  jobType?: string;
  address: string;
  postcode?: string;
  scheduledDate: Date;
  scheduledTime?: string;
  estimatedDuration?: number;
  quotedAmount?: number;
}

export interface UpdateJobParams {
  id: string;
  status?: string;
  finalAmount?: number;
  completedAt?: Date;
}

export interface CreateNurtureSequenceParams {
  leadId: string;
}

export interface UpdateNurtureProgressParams {
  leadId: string;
  touchNumber: number;
}

// Tool implementations

export async function queryLeads(params: QueryLeadsParams) {
  const { clientId, status, urgency, limit = 50, offset = 0 } = params;

  const where: Prisma.LeadWhereInput = {
    clientId,
    ...(status && { status: status as any }),
    ...(urgency && { urgency: urgency as any }),
  };

  const [leads, total] = await Promise.all([
    prisma.lead.findMany({
      where,
      include: {
        customer: true,
        nurtureSequence: true,
      },
      orderBy: { createdAt: "desc" },
      take: limit,
      skip: offset,
    }),
    prisma.lead.count({ where }),
  ]);

  return { leads, total, limit, offset };
}

export async function getLead(id: string) {
  const lead = await prisma.lead.findUnique({
    where: { id },
    include: {
      customer: true,
      client: true,
      nurtureSequence: true,
      notifications: {
        orderBy: { createdAt: "desc" },
        take: 10,
      },
    },
  });

  return lead;
}

export async function createLead(params: CreateLeadParams) {
  const lead = await prisma.lead.create({
    data: {
      clientId: params.clientId,
      callerPhone: params.callerPhone,
      callId: params.callId,
      callDuration: params.callDuration,
      recordingUrl: params.recordingUrl,
      transcript: params.transcript,
      summary: params.summary,
      customerName: params.customerName,
      address: params.address,
      postcode: params.postcode,
      jobType: params.jobType,
      urgency: params.urgency || "routine",
      status: "new",
    },
    include: {
      client: true,
    },
  });

  return lead;
}

export async function updateLead(params: UpdateLeadParams) {
  const { id, status, dismissReason } = params;

  const updateData: Prisma.LeadUpdateInput = {};

  if (status) {
    updateData.status = status as any;

    // Set timestamps based on status
    if (status === "booked") {
      updateData.bookedAt = new Date();
    } else if (status === "converted") {
      updateData.convertedAt = new Date();
    } else if (status === "dismissed") {
      updateData.dismissedAt = new Date();
      updateData.dismissReason = dismissReason;
    } else if (status === "qualified") {
      updateData.qualifiedAt = new Date();
    }
  }

  const lead = await prisma.lead.update({
    where: { id },
    data: updateData,
  });

  return lead;
}

export async function findOrCreateCustomer(params: CreateCustomerParams) {
  const { clientId, name, phone, email, address, postcode } = params;

  // Try to find existing customer by phone
  let customer = await prisma.customer.findUnique({
    where: {
      clientId_phone: {
        clientId,
        phone,
      },
    },
  });

  if (!customer) {
    customer = await prisma.customer.create({
      data: {
        clientId,
        name,
        phone,
        email,
        address,
        postcode,
        source: "phone_call",
      },
    });
  }

  return customer;
}

export async function createJob(params: CreateJobParams) {
  const job = await prisma.job.create({
    data: {
      clientId: params.clientId,
      customerId: params.customerId,
      leadId: params.leadId,
      title: params.title,
      description: params.description,
      jobType: params.jobType,
      address: params.address,
      postcode: params.postcode,
      scheduledDate: params.scheduledDate,
      scheduledTime: params.scheduledTime,
      estimatedDuration: params.estimatedDuration,
      quotedAmount: params.quotedAmount,
      status: "scheduled",
    },
    include: {
      customer: true,
      lead: true,
    },
  });

  return job;
}

export async function updateJob(params: UpdateJobParams) {
  const { id, status, finalAmount, completedAt } = params;

  const updateData: Prisma.JobUpdateInput = {};

  if (status) {
    updateData.status = status as any;

    if (status === "completed") {
      updateData.completedAt = completedAt || new Date();
    } else if (status === "cancelled") {
      updateData.cancelledAt = new Date();
    } else if (status === "in_progress") {
      updateData.startedAt = new Date();
    } else if (status === "confirmed") {
      updateData.confirmedAt = new Date();
    }
  }

  if (finalAmount !== undefined) {
    updateData.finalAmount = finalAmount;
  }

  const job = await prisma.job.update({
    where: { id },
    data: updateData,
    include: {
      customer: true,
      client: true,
    },
  });

  return job;
}

export async function getJob(id: string) {
  const job = await prisma.job.findUnique({
    where: { id },
    include: {
      customer: true,
      client: true,
      lead: true,
    },
  });

  return job;
}

export async function createNurtureSequence(params: CreateNurtureSequenceParams) {
  const sequence = await prisma.nurtureSequence.create({
    data: {
      leadId: params.leadId,
      currentTouch: 0,
      status: "active",
      nextTouchAt: new Date(),
      nextTouchNumber: 1,
    },
  });

  // Link to lead
  await prisma.lead.update({
    where: { id: params.leadId },
    data: {
      nurtureSequenceId: sequence.id,
      status: "nurturing",
    },
  });

  return sequence;
}

export async function updateNurtureProgress(params: UpdateNurtureProgressParams) {
  const { leadId, touchNumber } = params;

  // Find the nurture sequence for this lead
  const lead = await prisma.lead.findUnique({
    where: { id: leadId },
    include: { nurtureSequence: true },
  });

  if (!lead?.nurtureSequence) {
    throw new Error(`No nurture sequence found for lead ${leadId}`);
  }

  const touchField = `touch${touchNumber}SentAt` as const;
  const updateData: any = {
    currentTouch: touchNumber,
    [touchField]: new Date(),
  };

  // Set next touch or complete sequence
  if (touchNumber >= 12) {
    updateData.status = "completed";
    updateData.completedAt = new Date();
    updateData.nextTouchAt = null;
    updateData.nextTouchNumber = null;
  } else {
    updateData.nextTouchNumber = touchNumber + 1;
    // Next touch timing is handled by the job scheduler
  }

  const sequence = await prisma.nurtureSequence.update({
    where: { id: lead.nurtureSequence.id },
    data: updateData,
  });

  return sequence;
}

export async function getNurtureSequence(leadId: string) {
  const lead = await prisma.lead.findUnique({
    where: { id: leadId },
    include: { nurtureSequence: true },
  });

  return lead?.nurtureSequence;
}

export async function stopNurtureSequence(leadId: string, reason: string) {
  const lead = await prisma.lead.findUnique({
    where: { id: leadId },
    include: { nurtureSequence: true },
  });

  if (!lead?.nurtureSequence) {
    throw new Error(`No nurture sequence found for lead ${leadId}`);
  }

  const sequence = await prisma.nurtureSequence.update({
    where: { id: lead.nurtureSequence.id },
    data: {
      status: "stopped",
      stoppedAt: new Date(),
      stopReason: reason,
      nextTouchAt: null,
      nextTouchNumber: null,
    },
  });

  return sequence;
}

export async function getDashboardStats(clientId: string) {
  const now = new Date();
  const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const weekStart = new Date(todayStart);
  weekStart.setDate(weekStart.getDate() - weekStart.getDay());
  const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);

  const [
    leadsToday,
    leadsThisWeek,
    leadsThisMonth,
    totalLeads,
    convertedLeads,
    jobsScheduled,
    jobsCompleted,
    revenue,
  ] = await Promise.all([
    prisma.lead.count({
      where: { clientId, createdAt: { gte: todayStart } },
    }),
    prisma.lead.count({
      where: { clientId, createdAt: { gte: weekStart } },
    }),
    prisma.lead.count({
      where: { clientId, createdAt: { gte: monthStart } },
    }),
    prisma.lead.count({
      where: { clientId, createdAt: { gte: monthStart } },
    }),
    prisma.lead.count({
      where: {
        clientId,
        createdAt: { gte: monthStart },
        status: { in: ["booked", "converted"] },
      },
    }),
    prisma.job.count({
      where: {
        clientId,
        status: "scheduled",
        scheduledDate: { gte: now },
      },
    }),
    prisma.job.count({
      where: {
        clientId,
        status: "completed",
        completedAt: { gte: monthStart },
      },
    }),
    prisma.job.aggregate({
      where: {
        clientId,
        status: "completed",
        completedAt: { gte: monthStart },
      },
      _sum: { finalAmount: true },
    }),
  ]);

  const conversionRate = totalLeads > 0 ? (convertedLeads / totalLeads) * 100 : 0;

  return {
    leadsToday,
    leadsThisWeek,
    leadsThisMonth,
    conversionRate: Math.round(conversionRate * 10) / 10,
    jobsScheduled,
    jobsCompleted,
    revenueThisMonth: revenue._sum.finalAmount?.toNumber() || 0,
  };
}

export async function getClient(clientId: string) {
  const client = await prisma.client.findUnique({
    where: { id: clientId },
  });

  return client;
}

export async function getClientByPhone(coveredNumber: string) {
  const client = await prisma.client.findFirst({
    where: { coveredNumber },
  });

  return client;
}

export async function createNotification(params: {
  clientId: string;
  leadId?: string;
  jobId?: string;
  type: string;
  channel: "email" | "sms" | "whatsapp";
  recipient: string;
  subject?: string;
  message: string;
  externalId?: string;
}) {
  const notification = await prisma.notification.create({
    data: {
      clientId: params.clientId,
      leadId: params.leadId,
      jobId: params.jobId,
      type: params.type,
      channel: params.channel,
      recipient: params.recipient,
      subject: params.subject,
      message: params.message,
      status: "pending",
      externalId: params.externalId,
    },
  });

  return notification;
}

export async function updateNotificationStatus(
  id: string,
  status: "sent" | "delivered" | "failed",
  error?: string
) {
  const updateData: Prisma.NotificationUpdateInput = {
    status,
  };

  if (status === "sent") {
    updateData.sentAt = new Date();
  } else if (status === "delivered") {
    updateData.deliveredAt = new Date();
  } else if (status === "failed") {
    updateData.failedAt = new Date();
    updateData.error = error;
  }

  const notification = await prisma.notification.update({
    where: { id },
    data: updateData,
  });

  return notification;
}

// Cleanup
export async function disconnect() {
  await prisma.$disconnect();
}
