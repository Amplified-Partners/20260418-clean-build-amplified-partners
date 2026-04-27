import {
  Body,
  Button,
  Container,
  Head,
  Heading,
  Hr,
  Html,
  Preview,
  Section,
  Text,
} from "@react-email/components";
import * as React from "react";

interface LeadAcknowledgmentEmailProps {
  customerName: string;
  businessName: string;
  ownerName?: string;
  jobType: string;
  urgency: "emergency" | "urgent" | "routine";
  callbackTime?: string;
  businessPhone?: string;
  businessEmail?: string;
  vertical?: string;
}

export const LeadAcknowledgmentEmail = ({
  customerName = "Customer",
  businessName = "Your Business",
  ownerName,
  jobType = "service enquiry",
  urgency = "routine",
  callbackTime = "within 2 hours",
  businessPhone,
  businessEmail,
  vertical = "trades",
}: LeadAcknowledgmentEmailProps) => {
  const previewText = `We've received your ${jobType} request - ${businessName}`;

  // Urgency-specific messaging
  const urgencyConfig = {
    emergency: {
      title: "We're on it!",
      message: `We understand this is urgent. ${ownerName || "Our team"} has been immediately notified and will contact you ${callbackTime || "within 15 minutes"}.`,
      color: "#dc2626",
    },
    urgent: {
      title: "Message received!",
      message: `${ownerName || "Our team"} will get back to you ${callbackTime || "within 30 minutes"} to discuss your ${jobType}.`,
      color: "#f59e0b",
    },
    routine: {
      title: "Thank you for getting in touch!",
      message: `${ownerName || "Our team"} will be in touch ${callbackTime || "soon"} to discuss your requirements.`,
      color: "#0891b2",
    },
  };

  const config = urgencyConfig[urgency];

  return (
    <Html>
      <Head />
      <Preview>{previewText}</Preview>
      <Body style={main}>
        <Container style={container}>
          {/* Header */}
          <Section style={{ ...header, backgroundColor: config.color }}>
            <Heading style={logo}>{businessName}</Heading>
          </Section>

          {/* Checkmark Icon */}
          <Section style={iconSection}>
            <div style={{ ...checkCircle, borderColor: config.color }}>
              <Text style={{ ...checkMark, color: config.color }}>&#10003;</Text>
            </div>
          </Section>

          {/* Title */}
          <Section style={titleSection}>
            <Heading style={h1}>{config.title}</Heading>
            <Text style={subtitle}>
              We've received your request for {jobType}
            </Text>
          </Section>

          <Hr style={hr} />

          {/* Greeting */}
          <Text style={paragraph}>Hi {customerName},</Text>
          <Text style={paragraph}>{config.message}</Text>

          {/* What We Captured */}
          <Section style={capturedSection}>
            <Text style={capturedTitle}>What we noted from your call:</Text>
            <div style={capturedBox}>
              <div style={capturedRow}>
                <Text style={capturedLabel}>Service Type</Text>
                <Text style={capturedValue}>{jobType}</Text>
              </div>
              <div style={capturedRow}>
                <Text style={capturedLabel}>Priority</Text>
                <Text style={{ ...capturedValue, color: config.color, fontWeight: "600" }}>
                  {urgency.charAt(0).toUpperCase() + urgency.slice(1)}
                </Text>
              </div>
            </div>
          </Section>

          {/* Contact Info */}
          {(businessPhone || businessEmail) && (
            <Section style={contactSection}>
              <Text style={contactTitle}>Need to reach us sooner?</Text>
              {businessPhone && (
                <Button style={phoneButton} href={`tel:${businessPhone}`}>
                  Call {businessPhone}
                </Button>
              )}
              {businessEmail && (
                <Text style={emailText}>
                  Or email us at <a href={`mailto:${businessEmail}`} style={emailLink}>{businessEmail}</a>
                </Text>
              )}
            </Section>
          )}

          <Hr style={hr} />

          {/* What to Expect */}
          <Section style={expectSection}>
            <Text style={expectTitle}>What to expect next</Text>
            <div style={timelineContainer}>
              <div style={timelineItem}>
                <div style={timelineDot}></div>
                <div style={timelineContent}>
                  <Text style={timelineStep}>1. Callback</Text>
                  <Text style={timelineDesc}>
                    {ownerName || "We"}'ll call to discuss your requirements
                  </Text>
                </div>
              </div>
              <div style={timelineItem}>
                <div style={timelineDot}></div>
                <div style={timelineContent}>
                  <Text style={timelineStep}>2. Quote</Text>
                  <Text style={timelineDesc}>
                    You'll receive a clear, no-obligation quote
                  </Text>
                </div>
              </div>
              <div style={timelineItem}>
                <div style={timelineDot}></div>
                <div style={timelineContent}>
                  <Text style={timelineStep}>3. Schedule</Text>
                  <Text style={timelineDesc}>
                    We'll arrange a time that works for you
                  </Text>
                </div>
              </div>
            </div>
          </Section>

          <Hr style={hr} />

          {/* Footer */}
          <Text style={footerText}>
            This email was sent because you contacted {businessName}. If you didn't
            make this enquiry, please let us know.
          </Text>

          <Text style={footerSignature}>
            Looking forward to helping you,
            <br />
            {ownerName ? `${ownerName} at ` : ""}{businessName}
          </Text>
        </Container>
      </Body>
    </Html>
  );
};

export default LeadAcknowledgmentEmail;

// Styles
const main = {
  backgroundColor: "#f6f9fc",
  fontFamily:
    '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Ubuntu, sans-serif',
};

const container = {
  backgroundColor: "#ffffff",
  margin: "0 auto",
  padding: "20px 0 48px",
  marginBottom: "64px",
  maxWidth: "600px",
};

const header = {
  padding: "24px 32px",
};

const logo = {
  color: "#ffffff",
  fontSize: "24px",
  fontWeight: "bold",
  margin: "0",
};

const iconSection = {
  padding: "32px 32px 0",
  textAlign: "center" as const,
};

const checkCircle = {
  width: "64px",
  height: "64px",
  borderRadius: "50%",
  border: "3px solid",
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  margin: "0 auto",
};

const checkMark = {
  fontSize: "32px",
  fontWeight: "bold",
  lineHeight: "64px",
  margin: "0",
};

const titleSection = {
  padding: "16px 32px 0",
  textAlign: "center" as const,
};

const h1 = {
  color: "#1f2937",
  fontSize: "28px",
  fontWeight: "bold",
  margin: "0 0 8px",
};

const subtitle = {
  color: "#6b7280",
  fontSize: "16px",
  margin: "0",
  lineHeight: "24px",
};

const hr = {
  borderColor: "#e5e7eb",
  margin: "24px 32px",
};

const paragraph = {
  color: "#374151",
  fontSize: "16px",
  lineHeight: "24px",
  margin: "0 32px 16px",
};

const capturedSection = {
  padding: "0 32px",
};

const capturedTitle = {
  color: "#1f2937",
  fontSize: "14px",
  fontWeight: "600",
  margin: "0 0 12px",
};

const capturedBox = {
  backgroundColor: "#f9fafb",
  borderRadius: "8px",
  padding: "16px",
  border: "1px solid #e5e7eb",
};

const capturedRow = {
  display: "flex",
  justifyContent: "space-between",
  padding: "8px 0",
};

const capturedLabel = {
  color: "#6b7280",
  fontSize: "14px",
  margin: "0",
};

const capturedValue = {
  color: "#1f2937",
  fontSize: "14px",
  fontWeight: "500",
  margin: "0",
  textAlign: "right" as const,
};

const contactSection = {
  padding: "0 32px",
  textAlign: "center" as const,
  marginTop: "24px",
};

const contactTitle = {
  color: "#1f2937",
  fontSize: "16px",
  fontWeight: "600",
  margin: "0 0 16px",
};

const phoneButton = {
  backgroundColor: "#0891b2",
  borderRadius: "8px",
  color: "#ffffff",
  fontSize: "16px",
  fontWeight: "600",
  textDecoration: "none",
  textAlign: "center" as const,
  display: "inline-block",
  padding: "14px 32px",
};

const emailText = {
  color: "#6b7280",
  fontSize: "14px",
  margin: "16px 0 0",
};

const emailLink = {
  color: "#0891b2",
  textDecoration: "none",
};

const expectSection = {
  padding: "0 32px",
};

const expectTitle = {
  color: "#1f2937",
  fontSize: "16px",
  fontWeight: "600",
  margin: "0 0 16px",
};

const timelineContainer = {
  paddingLeft: "8px",
};

const timelineItem = {
  display: "flex",
  marginBottom: "16px",
  alignItems: "flex-start",
};

const timelineDot = {
  width: "8px",
  height: "8px",
  borderRadius: "50%",
  backgroundColor: "#0891b2",
  marginTop: "6px",
  marginRight: "16px",
  flexShrink: 0,
};

const timelineContent = {
  flex: 1,
};

const timelineStep = {
  color: "#1f2937",
  fontSize: "14px",
  fontWeight: "600",
  margin: "0 0 4px",
};

const timelineDesc = {
  color: "#6b7280",
  fontSize: "14px",
  margin: "0",
  lineHeight: "20px",
};

const footerText = {
  color: "#9ca3af",
  fontSize: "13px",
  lineHeight: "20px",
  margin: "0 32px 8px",
};

const footerSignature = {
  color: "#374151",
  fontSize: "14px",
  lineHeight: "22px",
  margin: "16px 32px 0",
};
