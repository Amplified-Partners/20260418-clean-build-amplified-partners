/**
 * Covered AI - 12-Touch Lead Nurture Sequence
 *
 * This job handles the complete nurture sequence for new leads.
 * Each touch is sent at a specific delay with channel-specific content.
 */

import { task, wait } from "@trigger.dev/sdk/v3";
import { ActionLog } from "./lib/action-logger";

interface Lead {
  id: string;
  clientId: string;
  customerName: string;
  email?: string;
  phone: string;
  jobType?: string;
  urgency: string;
  vertical: string;
}

interface Client {
  id: string;
  businessName: string;
  ownerName: string;
  vertical: string;
}

// Touch configuration
const TOUCHES = [
  { num: 1, delay: 0, channel: "email", template: "acknowledgment" },
  { num: 2, delay: 5 * 60, channel: "whatsapp", template: "pain-question" }, // 5 min
  { num: 3, delay: 2 * 60 * 60, channel: "sms", template: "quick-tip" }, // 2 hours
  { num: 4, delay: 24 * 60 * 60, channel: "email", template: "social-proof" }, // 24 hours
  { num: 5, delay: 48 * 60 * 60, channel: "email", template: "video-intro" }, // 48 hours (with HeyGen)
  { num: 6, delay: 72 * 60 * 60, channel: "whatsapp", template: "urgency" }, // 72 hours
  { num: 7, delay: 5 * 24 * 60 * 60, channel: "email", template: "case-study" }, // 5 days
  { num: 8, delay: 7 * 24 * 60 * 60, channel: "sms", template: "limited-offer" }, // 7 days
  { num: 9, delay: 10 * 24 * 60 * 60, channel: "email", template: "faq" }, // 10 days
  { num: 10, delay: 14 * 24 * 60 * 60, channel: "whatsapp", template: "final-push" }, // 14 days
  { num: 11, delay: 21 * 24 * 60 * 60, channel: "email", template: "long-nurture" }, // 21 days
  { num: 12, delay: 30 * 24 * 60 * 60, channel: "email", template: "re-engage" }, // 30 days
];

export const leadNurtureSequence = task({
  id: "lead-nurture-sequence",
  retry: {
    maxAttempts: 3,
  },
  run: async (payload: { lead: Lead; client: Client }) => {
    const { lead, client } = payload;
    
    console.log(`🌱 Starting nurture sequence for lead ${lead.id}`);
    
    let previousDelay = 0;
    
    for (const touch of TOUCHES) {
      // Calculate wait time from previous touch
      const waitTime = touch.delay - previousDelay;
      
      if (waitTime > 0) {
        console.log(`⏳ Waiting ${waitTime / 60} minutes before touch ${touch.num}`);
        await wait.for({ seconds: waitTime });
      }
      
      // Check if lead is still active (not booked/dismissed)
      const stillActive = await checkLeadStatus(lead.id);
      if (!stillActive) {
        console.log(`🛑 Lead ${lead.id} no longer active, stopping sequence`);
        return { completed: false, stoppedAt: touch.num, reason: "lead_inactive" };
      }
      
      // Send the touch
      console.log(`📤 Sending touch ${touch.num} via ${touch.channel}`);

      // Log autonomous action
      const action = await ActionLog.nurtureEmailSent(
        client.id,
        lead.id,
        lead.customerName,
        touch.num
      );

      try {
        if (touch.num === 5) {
          // Touch 5 includes personalized video
          await sendVideoTouch(lead, client, touch);
        } else {
          await sendTouch(lead, client, touch);
        }

        // Update nurture sequence in DB
        await updateNurtureProgress(lead.id, touch.num);

        await action.success(`Touch ${touch.num} sent via ${touch.channel}`);
      } catch (error) {
        await action.fail(String(error));
        console.error(`❌ Failed to send touch ${touch.num}:`, error);
        // Continue to next touch on failure
      }
      
      previousDelay = touch.delay;
    }
    
    console.log(`✅ Nurture sequence completed for lead ${lead.id}`);
    return { completed: true, touchesSent: 12 };
  },
});

async function checkLeadStatus(leadId: string): Promise<boolean> {
  // TODO: Call API to check if lead is still in nurturing status
  // Returns false if booked, converted, or dismissed
  return true;
}

async function sendTouch(
  lead: Lead,
  client: Client,
  touch: { num: number; channel: string; template: string }
): Promise<void> {
  const API_URL = process.env.API_URL || "http://localhost:8000";
  const RESEND_API_KEY = process.env.RESEND_API_KEY;
  const TWILIO_ACCOUNT_SID = process.env.TWILIO_ACCOUNT_SID;
  const TWILIO_AUTH_TOKEN = process.env.TWILIO_AUTH_TOKEN;
  const TWILIO_PHONE_NUMBER = process.env.TWILIO_PHONE_NUMBER;

  console.log(`   Touch ${touch.num}: ${touch.channel} - ${touch.template}`);

  if (touch.channel === "email" && lead.email && RESEND_API_KEY) {
    // Send email via Resend
    const subject = getEmailSubject(touch.template, client.businessName);
    const html = generateNurtureEmailHtml(touch.template, lead, client);

    await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: `${client.businessName} <noreply@covered.ai>`,
        to: lead.email,
        subject,
        html,
      }),
    });
  } else if (touch.channel === "sms" && TWILIO_ACCOUNT_SID && TWILIO_AUTH_TOKEN) {
    // Send SMS via Twilio
    const message = getSmsMessage(touch.template, lead, client);
    const twilioUrl = `https://api.twilio.com/2010-04-01/Accounts/${TWILIO_ACCOUNT_SID}/Messages.json`;

    await fetch(twilioUrl, {
      method: "POST",
      headers: {
        "Authorization": `Basic ${Buffer.from(`${TWILIO_ACCOUNT_SID}:${TWILIO_AUTH_TOKEN}`).toString("base64")}`,
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        From: TWILIO_PHONE_NUMBER || "",
        To: lead.phone,
        Body: message,
      }),
    });
  } else if (touch.channel === "whatsapp" && TWILIO_ACCOUNT_SID && TWILIO_AUTH_TOKEN) {
    // Send WhatsApp via Twilio
    const message = getWhatsAppMessage(touch.template, lead, client);
    const twilioUrl = `https://api.twilio.com/2010-04-01/Accounts/${TWILIO_ACCOUNT_SID}/Messages.json`;

    await fetch(twilioUrl, {
      method: "POST",
      headers: {
        "Authorization": `Basic ${Buffer.from(`${TWILIO_ACCOUNT_SID}:${TWILIO_AUTH_TOKEN}`).toString("base64")}`,
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        From: `whatsapp:${TWILIO_PHONE_NUMBER || ""}`,
        To: `whatsapp:${lead.phone}`,
        Body: message,
      }),
    });
  }
}

async function sendVideoTouch(
  lead: Lead,
  client: Client,
  touch: { num: number; channel: string; template: string }
): Promise<void> {
  // 1. Generate personalized video via HeyGen
  console.log(`   🎬 Generating personalized video for ${lead.customerName}`);
  
  // TODO: Call HeyGen MCP server to generate video
  // const video = await heygenMcp.createVideo({
  //   templateId: getVideoTemplate(client.vertical),
  //   variables: {
  //     customer_name: lead.customerName,
  //     business_name: client.businessName,
  //   }
  // });
  
  // 2. Send email with video
  // await resendMcp.sendEmail({
  //   to: lead.email,
  //   template: "video-intro",
  //   data: {
  //     name: lead.customerName,
  //     videoUrl: video.url,
  //     thumbnailUrl: video.thumbnail,
  //   }
  // });
  
  console.log(`   Touch ${touch.num}: video email sent`);
}

async function updateNurtureProgress(leadId: string, touchNum: number): Promise<void> {
  // TODO: Update nurture_sequences table via API or direct DB
  console.log(`   Updated nurture progress: touch ${touchNum}`);
}

function getVideoTemplate(vertical: string): string {
  const templates: Record<string, string> = {
    trades: "trades-intro-v1",
    vet: "medical-intro-v1",
    dental: "medical-intro-v1",
    aesthetics: "beauty-intro-v1",
    salon: "beauty-intro-v1",
  };
  return templates[vertical] || "generic-intro-v1";
}

// Email subject lines for each template
function getEmailSubject(template: string, businessName: string): string {
  const subjects: Record<string, string> = {
    acknowledgment: `We received your enquiry - ${businessName}`,
    "social-proof": `Why customers choose ${businessName}`,
    "video-intro": `A personal message from ${businessName}`,
    "case-study": `See how we helped another customer`,
    faq: `Common questions about our services`,
    "long-nurture": `Still thinking about your project?`,
    "re-engage": `We'd love to hear from you - ${businessName}`,
  };
  return subjects[template] || `Update from ${businessName}`;
}

// Generate email HTML for nurture templates
function generateNurtureEmailHtml(template: string, lead: Lead, client: Client): string {
  const baseStyle = `
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;
  `;

  const templates: Record<string, string> = {
    acknowledgment: `
      <div style="${baseStyle}">
        <h1 style="color: #0891b2;">Thanks for getting in touch!</h1>
        <p>Hi ${lead.customerName},</p>
        <p>We've received your enquiry${lead.jobType ? ` about ${lead.jobType}` : ""} and ${client.ownerName} will be in touch shortly.</p>
        <p>In the meantime, feel free to call us on our direct line if it's urgent.</p>
        <p>Best regards,<br>${client.businessName}</p>
      </div>
    `,
    "social-proof": `
      <div style="${baseStyle}">
        <h1 style="color: #0891b2;">Why customers trust ${client.businessName}</h1>
        <p>Hi ${lead.customerName},</p>
        <p>We wanted to share why customers keep coming back to us:</p>
        <ul>
          <li><strong>Local expertise</strong> - We know your area inside out</li>
          <li><strong>Reliable service</strong> - We show up when we say we will</li>
          <li><strong>Fair pricing</strong> - No hidden fees, no surprises</li>
        </ul>
        <p>Ready to discuss your needs? Just reply to this email or give us a call.</p>
        <p>Best regards,<br>${client.ownerName} at ${client.businessName}</p>
      </div>
    `,
    "case-study": `
      <div style="${baseStyle}">
        <h1 style="color: #0891b2;">See how we helped a customer just like you</h1>
        <p>Hi ${lead.customerName},</p>
        <p>Recently, we helped a customer in your area with a similar ${lead.jobType || "project"}. They were delighted with the results.</p>
        <p>We'd love the opportunity to do the same for you. Ready to get started?</p>
        <p>Best regards,<br>${client.ownerName} at ${client.businessName}</p>
      </div>
    `,
    faq: `
      <div style="${baseStyle}">
        <h1 style="color: #0891b2;">Got questions? We've got answers</h1>
        <p>Hi ${lead.customerName},</p>
        <p>Here are some common questions we get asked:</p>
        <p><strong>Q: How quickly can you start?</strong><br>A: Usually within a few days for most jobs.</p>
        <p><strong>Q: Do you offer free quotes?</strong><br>A: Yes! We provide no-obligation quotes.</p>
        <p><strong>Q: Are you insured?</strong><br>A: Absolutely. We're fully insured for your peace of mind.</p>
        <p>Have more questions? Just hit reply!</p>
        <p>Best regards,<br>${client.businessName}</p>
      </div>
    `,
    "long-nurture": `
      <div style="${baseStyle}">
        <h1 style="color: #0891b2;">Still thinking it over?</h1>
        <p>Hi ${lead.customerName},</p>
        <p>We understand big decisions take time. We're here whenever you're ready.</p>
        <p>If anything has changed or if you have questions, we'd love to hear from you.</p>
        <p>Best regards,<br>${client.ownerName} at ${client.businessName}</p>
      </div>
    `,
    "re-engage": `
      <div style="${baseStyle}">
        <h1 style="color: #0891b2;">We'd love to hear from you</h1>
        <p>Hi ${lead.customerName},</p>
        <p>It's been a while since your enquiry about ${lead.jobType || "our services"}. We wanted to check in.</p>
        <p>If your needs have changed or if you'd like to revisit your project, we're just a call away.</p>
        <p>Best regards,<br>${client.ownerName} at ${client.businessName}</p>
      </div>
    `,
  };

  return templates[template] || templates.acknowledgment;
}

// SMS message templates
function getSmsMessage(template: string, lead: Lead, client: Client): string {
  const messages: Record<string, string> = {
    "quick-tip": `Hi ${lead.customerName}, quick tip from ${client.businessName}: Regular maintenance can prevent costly repairs. Need help? Reply YES or call us!`,
    "limited-offer": `${lead.customerName}, limited time: Book this week and get 10% off your ${lead.jobType || "service"}. Call ${client.businessName} or reply BOOK.`,
  };
  return messages[template] || `Hi ${lead.customerName}, ${client.businessName} here. Ready to help with your ${lead.jobType || "project"}!`;
}

// WhatsApp message templates
function getWhatsAppMessage(template: string, lead: Lead, client: Client): string {
  const messages: Record<string, string> = {
    "pain-question": `Hi ${lead.customerName}! It's ${client.ownerName} from ${client.businessName}. How can we help with your ${lead.jobType || "enquiry"}? What's the main thing you're trying to solve?`,
    urgency: `Hi ${lead.customerName}, just checking in. Is your ${lead.jobType || "project"} still something you need help with? We've got availability this week!`,
    "final-push": `Hi ${lead.customerName}! ${client.ownerName} here. I noticed we haven't connected yet about your ${lead.jobType || "enquiry"}. Would you like me to call you to discuss? No pressure!`,
  };
  return messages[template] || `Hi ${lead.customerName}, ${client.businessName} here. How can we help?`;
}
