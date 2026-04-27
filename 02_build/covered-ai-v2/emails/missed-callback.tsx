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

interface MissedCallbackEmailProps {
  ownerName: string;
  businessName: string;
  callerName: string;
  callerPhone: string;
  callSummary: string;
  hoursWaiting: number;
  dashboardLink: string;
}

export const MissedCallbackEmail = ({
  ownerName = "Ralph",
  businessName = "Your Business",
  callerName = "John Smith",
  callerPhone = "+44 7700 900123",
  callSummary = "Burst pipe in kitchen, needs urgent attention",
  hoursWaiting = 4,
  dashboardLink = "https://app.covered.ai",
}: MissedCallbackEmailProps) => {
  const previewText = `${callerName} has been waiting ${hoursWaiting} hours for your callback`;

  return (
    <Html>
      <Head />
      <Preview>{previewText}</Preview>
      <Body style={main}>
        <Container style={container}>
          {/* Header */}
          <Section style={header}>
            <Text style={headerText}>Covered AI</Text>
          </Section>

          {/* Warning Banner */}
          <Section style={warningBanner}>
            <Text style={warningText}>⏰ Callback Reminder</Text>
          </Section>

          <Hr style={hr} />

          {/* Greeting */}
          <Text style={paragraph}>Hi {ownerName},</Text>
          <Text style={paragraph}>
            <strong>{callerName}</strong> called {hoursWaiting} hours ago and is
            still waiting for a callback.
          </Text>

          {/* Call Details Box */}
          <Section style={callBox}>
            <Text style={callLabel}>Phone</Text>
            <Text style={callValue}>{callerPhone}</Text>

            <Hr style={callDivider} />

            <Text style={callLabel}>Summary</Text>
            <Text style={callSummaryText}>{callSummary}</Text>
          </Section>

          {/* CTA Buttons */}
          <Section style={buttonSection}>
            <Button style={buttonCall} href={`tel:${callerPhone}`}>
              📞 Call Now
            </Button>
          </Section>

          <Section style={buttonSectionSecondary}>
            <Button style={buttonSecondary} href={dashboardLink}>
              View in Dashboard
            </Button>
          </Section>

          <Hr style={hr} />

          {/* Footer */}
          <Text style={footerSignature}>{businessName}</Text>
        </Container>
      </Body>
    </Html>
  );
};

export default MissedCallbackEmail;

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
  backgroundColor: "#0891b2",
  textAlign: "center" as const,
};

const headerText = {
  color: "#ffffff",
  fontSize: "20px",
  fontWeight: "bold",
  margin: "0",
};

const warningBanner = {
  backgroundColor: "#fef3c7",
  borderRadius: "8px",
  padding: "12px",
  textAlign: "center" as const,
  margin: "24px 32px 0",
};

const warningText = {
  fontSize: "16px",
  fontWeight: "bold",
  color: "#92400e",
  margin: "0",
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

const callBox = {
  backgroundColor: "#f9fafb",
  borderRadius: "8px",
  padding: "24px",
  margin: "0 32px 24px",
};

const callLabel = {
  fontSize: "12px",
  color: "#6b7280",
  textTransform: "uppercase" as const,
  margin: "0 0 4px",
};

const callValue = {
  fontSize: "20px",
  fontWeight: "bold",
  color: "#1f2937",
  margin: "0 0 16px",
};

const callDivider = {
  borderColor: "#e5e7eb",
  margin: "16px 0",
};

const callSummaryText = {
  fontSize: "16px",
  color: "#374151",
  lineHeight: "24px",
  margin: "0",
};

const buttonSection = {
  padding: "0 32px",
  textAlign: "center" as const,
};

const buttonSectionSecondary = {
  padding: "12px 32px",
  textAlign: "center" as const,
};

const buttonCall = {
  backgroundColor: "#16a34a",
  borderRadius: "8px",
  color: "#ffffff",
  fontSize: "16px",
  fontWeight: "600",
  textDecoration: "none",
  textAlign: "center" as const,
  display: "inline-block",
  padding: "14px 32px",
};

const buttonSecondary = {
  backgroundColor: "#ffffff",
  borderRadius: "8px",
  color: "#374151",
  fontSize: "14px",
  fontWeight: "500",
  textDecoration: "none",
  textAlign: "center" as const,
  display: "inline-block",
  padding: "10px 24px",
  border: "1px solid #d1d5db",
};

const footerSignature = {
  color: "#374151",
  fontSize: "14px",
  fontWeight: "600",
  margin: "0 32px",
};
