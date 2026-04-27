/**
 * Covered AI - Twilio MCP Server Tools
 *
 * SMS and WhatsApp messaging tools via Twilio.
 */

import Twilio from "twilio";

// Initialize Twilio client
const accountSid = process.env.TWILIO_ACCOUNT_SID;
const authToken = process.env.TWILIO_AUTH_TOKEN;
const twilioPhoneNumber = process.env.TWILIO_PHONE_NUMBER;
const whatsappNumber = process.env.TWILIO_WHATSAPP_NUMBER || `whatsapp:${twilioPhoneNumber}`;

if (!accountSid || !authToken) {
  console.error("Warning: TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN must be set");
}

const client = accountSid && authToken ? Twilio(accountSid, authToken) : null;

// Types
export interface SendSmsParams {
  to: string;
  message: string;
  from?: string;
}

export interface SendWhatsAppParams {
  to: string;
  message: string;
  mediaUrl?: string;
}

export interface GetCallsParams {
  phoneNumber?: string;
  limit?: number;
  startDate?: string;
  endDate?: string;
}

export interface GetMessagesParams {
  to?: string;
  from?: string;
  limit?: number;
  dateSent?: string;
}

// Utility to format UK phone numbers
function formatUkPhone(phone: string): string {
  // Remove all non-digits
  let cleaned = phone.replace(/\D/g, "");

  // Handle UK numbers
  if (cleaned.startsWith("44")) {
    return `+${cleaned}`;
  } else if (cleaned.startsWith("0")) {
    return `+44${cleaned.substring(1)}`;
  } else if (!cleaned.startsWith("+")) {
    // Assume UK number without prefix
    return `+44${cleaned}`;
  }

  return phone;
}

// Tool implementations

export async function sendSms(params: SendSmsParams) {
  if (!client) {
    throw new Error("Twilio client not initialized. Check TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN.");
  }

  const { to, message, from } = params;
  const formattedTo = formatUkPhone(to);
  const formattedFrom = from || twilioPhoneNumber;

  if (!formattedFrom) {
    throw new Error("TWILIO_PHONE_NUMBER environment variable not set");
  }

  const result = await client.messages.create({
    body: message,
    to: formattedTo,
    from: formattedFrom,
  });

  return {
    success: true,
    sid: result.sid,
    to: result.to,
    from: result.from,
    status: result.status,
    dateCreated: result.dateCreated,
  };
}

export async function sendWhatsApp(params: SendWhatsAppParams) {
  if (!client) {
    throw new Error("Twilio client not initialized. Check TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN.");
  }

  const { to, message, mediaUrl } = params;
  const formattedTo = formatUkPhone(to);

  // WhatsApp numbers need the whatsapp: prefix
  const whatsappTo = formattedTo.startsWith("whatsapp:")
    ? formattedTo
    : `whatsapp:${formattedTo}`;

  const messageOptions: {
    body: string;
    to: string;
    from: string;
    mediaUrl?: string[];
  } = {
    body: message,
    to: whatsappTo,
    from: whatsappNumber!,
  };

  if (mediaUrl) {
    messageOptions.mediaUrl = [mediaUrl];
  }

  const result = await client.messages.create(messageOptions);

  return {
    success: true,
    sid: result.sid,
    to: result.to,
    from: result.from,
    status: result.status,
    dateCreated: result.dateCreated,
  };
}

export async function getCalls(params: GetCallsParams) {
  if (!client) {
    throw new Error("Twilio client not initialized. Check TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN.");
  }

  const { phoneNumber, limit = 20, startDate, endDate } = params;

  const filters: {
    to?: string;
    from?: string;
    startTime?: Date;
    endTime?: Date;
  } = {};

  if (phoneNumber) {
    const formatted = formatUkPhone(phoneNumber);
    filters.to = formatted;
  }

  if (startDate) {
    filters.startTime = new Date(startDate);
  }

  if (endDate) {
    filters.endTime = new Date(endDate);
  }

  const calls = await client.calls.list({
    ...filters,
    limit,
  });

  return {
    calls: calls.map((call) => ({
      sid: call.sid,
      from: call.from,
      to: call.to,
      status: call.status,
      direction: call.direction,
      duration: call.duration,
      startTime: call.startTime,
      endTime: call.endTime,
    })),
    count: calls.length,
  };
}

export async function getMessages(params: GetMessagesParams) {
  if (!client) {
    throw new Error("Twilio client not initialized. Check TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN.");
  }

  const { to, from, limit = 20, dateSent } = params;

  const filters: {
    to?: string;
    from?: string;
    dateSent?: Date;
  } = {};

  if (to) {
    filters.to = formatUkPhone(to);
  }

  if (from) {
    filters.from = formatUkPhone(from);
  }

  if (dateSent) {
    filters.dateSent = new Date(dateSent);
  }

  const messages = await client.messages.list({
    ...filters,
    limit,
  });

  return {
    messages: messages.map((msg) => ({
      sid: msg.sid,
      from: msg.from,
      to: msg.to,
      body: msg.body,
      status: msg.status,
      direction: msg.direction,
      dateCreated: msg.dateCreated,
      dateSent: msg.dateSent,
    })),
    count: messages.length,
  };
}

export async function getMessageStatus(sid: string) {
  if (!client) {
    throw new Error("Twilio client not initialized. Check TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN.");
  }

  const message = await client.messages(sid).fetch();

  return {
    sid: message.sid,
    status: message.status,
    to: message.to,
    from: message.from,
    body: message.body,
    dateCreated: message.dateCreated,
    dateSent: message.dateSent,
    dateUpdated: message.dateUpdated,
    errorCode: message.errorCode,
    errorMessage: message.errorMessage,
  };
}

export async function lookupPhoneNumber(phone: string) {
  if (!client) {
    throw new Error("Twilio client not initialized. Check TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN.");
  }

  const formatted = formatUkPhone(phone);

  try {
    const lookup = await client.lookups.v2.phoneNumbers(formatted).fetch({
      fields: "line_type_intelligence",
    });

    return {
      phoneNumber: lookup.phoneNumber,
      nationalFormat: lookup.nationalFormat,
      countryCode: lookup.countryCode,
      valid: lookup.valid,
      callerName: lookup.callerName,
      lineTypeIntelligence: lookup.lineTypeIntelligence,
    };
  } catch (error) {
    return {
      phoneNumber: formatted,
      valid: false,
      error: error instanceof Error ? error.message : "Lookup failed",
    };
  }
}
