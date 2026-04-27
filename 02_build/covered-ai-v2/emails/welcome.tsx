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

interface WelcomeEmailProps {
  ownerName: string;
  businessName: string;
  coveredNumber: string;
  dashboardLink: string;
}

export const WelcomeEmail = ({
  ownerName = "Ralph",
  businessName = "Your Business",
  coveredNumber = "+44 191 743 2732",
  dashboardLink = "https://app.covered.ai",
}: WelcomeEmailProps) => {
  const previewText = "Gemma is ready to answer your calls";

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

          {/* Hero Section */}
          <Section style={heroSection}>
            <Text style={heroEmoji}>🎉</Text>
            <Heading style={heroHeading}>Welcome to Covered AI!</Heading>
          </Section>

          <Hr style={hr} />

          {/* Greeting */}
          <Text style={paragraph}>Hi {ownerName},</Text>
          <Text style={paragraph}>
            You're all set up. Gemma is now ready to answer calls for{" "}
            <strong>{businessName}</strong>.
          </Text>

          {/* Covered Number Box */}
          <Section style={numberBox}>
            <Text style={numberLabel}>Your Covered AI number</Text>
            <Text style={numberValue}>{coveredNumber}</Text>
          </Section>

          {/* What Happens Now */}
          <Text style={sectionHeading}>What happens now:</Text>

          <Section style={stepsSection}>
            <Text style={stepText}>
              <strong>1. 📞 Calls come in</strong>
              <br />
              Gemma answers professionally, 24/7
            </Text>
            <Text style={stepText}>
              <strong>2. 💬 You get summaries</strong>
              <br />
              WhatsApp notifications after each call
            </Text>
            <Text style={stepText}>
              <strong>3. 📊 Track everything</strong>
              <br />
              Your dashboard shows all activity
            </Text>
          </Section>

          {/* CTA Button */}
          <Section style={buttonSection}>
            <Button style={button} href={dashboardLink}>
              Go to Dashboard
            </Button>
          </Section>

          <Hr style={hr} />

          {/* Footer */}
          <Text style={footerText}>
            Questions? Just reply to this email.
          </Text>

          <Text style={footerSignature}>
            Welcome aboard,
            <br />
            The Covered AI Team
          </Text>
        </Container>
      </Body>
    </Html>
  );
};

export default WelcomeEmail;

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

const heroSection = {
  textAlign: "center" as const,
  padding: "32px",
};

const heroEmoji = {
  fontSize: "48px",
  margin: "0 0 16px",
};

const heroHeading = {
  fontSize: "28px",
  fontWeight: "bold",
  color: "#1f2937",
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

const numberBox = {
  backgroundColor: "#dbeafe",
  borderRadius: "8px",
  padding: "24px",
  textAlign: "center" as const,
  margin: "16px 32px",
};

const numberLabel = {
  fontSize: "14px",
  color: "#1e40af",
  margin: "0 0 8px",
};

const numberValue = {
  fontSize: "28px",
  fontWeight: "bold",
  color: "#1e40af",
  margin: "0",
};

const sectionHeading = {
  fontSize: "16px",
  fontWeight: "bold",
  color: "#1f2937",
  margin: "0 32px 16px",
};

const stepsSection = {
  margin: "0 32px 24px",
};

const stepText = {
  fontSize: "16px",
  color: "#374151",
  lineHeight: "24px",
  margin: "0 0 16px",
};

const buttonSection = {
  padding: "0 32px 24px",
  textAlign: "center" as const,
};

const button = {
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

const footerText = {
  color: "#6b7280",
  fontSize: "14px",
  lineHeight: "20px",
  margin: "0 32px 16px",
};

const footerSignature = {
  color: "#374151",
  fontSize: "14px",
  fontWeight: "500",
  margin: "0 32px",
  lineHeight: "20px",
};
