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

interface ReviewRequestEmailProps {
  customerName: string;
  businessName: string;
  jobTitle: string;
  completedDate: string;
  reviewLink: string;
  businessPhone?: string;
  businessEmail?: string;
}

export const ReviewRequestEmail = ({
  customerName = "Customer",
  businessName = "Your Business",
  jobTitle = "Recent Service",
  completedDate = new Date().toLocaleDateString(),
  reviewLink = "https://g.page/review",
  businessPhone,
  businessEmail,
}: ReviewRequestEmailProps) => {
  const previewText = `How was your experience with ${businessName}?`;

  return (
    <Html>
      <Head />
      <Preview>{previewText}</Preview>
      <Body style={main}>
        <Container style={container}>
          {/* Header */}
          <Section style={header}>
            <Heading style={logo}>{businessName}</Heading>
          </Section>

          {/* Stars Icon */}
          <Section style={starsSection}>
            <Text style={starsText}>
              <span style={starIcon}>&#9733;</span>
              <span style={starIcon}>&#9733;</span>
              <span style={starIcon}>&#9733;</span>
              <span style={starIcon}>&#9733;</span>
              <span style={starIcon}>&#9733;</span>
            </Text>
          </Section>

          {/* Title */}
          <Section style={titleSection}>
            <Heading style={h1}>How did we do?</Heading>
            <Text style={subtitle}>
              Your feedback helps us improve and helps others find great service
            </Text>
          </Section>

          <Hr style={hr} />

          {/* Greeting */}
          <Text style={paragraph}>Hi {customerName},</Text>
          <Text style={paragraph}>
            Thank you for choosing {businessName} for your recent{" "}
            <strong>{jobTitle}</strong> on {completedDate}.
          </Text>
          <Text style={paragraph}>
            We'd really appreciate it if you could take a moment to share your
            experience. Your review helps other customers make informed decisions
            and helps us continue to provide excellent service.
          </Text>

          {/* Review Button */}
          <Section style={buttonSection}>
            <Button style={button} href={reviewLink}>
              Leave a Review
            </Button>
            <Text style={timeText}>Takes less than 2 minutes</Text>
          </Section>

          <Hr style={hr} />

          {/* Why Reviews Matter */}
          <Section style={whySection}>
            <Text style={whyTitle}>Why your review matters</Text>
            <div style={benefitsList}>
              <Text style={benefitItem}>
                <span style={checkmark}>&#10003;</span>
                Helps other customers find quality service
              </Text>
              <Text style={benefitItem}>
                <span style={checkmark}>&#10003;</span>
                Supports local businesses in your community
              </Text>
              <Text style={benefitItem}>
                <span style={checkmark}>&#10003;</span>
                Helps us understand what we're doing well
              </Text>
            </div>
          </Section>

          <Hr style={hr} />

          {/* Footer */}
          <Text style={footerText}>
            Had an issue? We'd love the chance to make it right.
            {businessEmail && ` Contact us at ${businessEmail}`}
            {businessPhone && ` or call ${businessPhone}`}.
          </Text>

          <Text style={footerSignature}>
            Thank you for your support,
            <br />
            The {businessName} Team
          </Text>
        </Container>
      </Body>
    </Html>
  );
};

export default ReviewRequestEmail;

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
};

const logo = {
  color: "#ffffff",
  fontSize: "24px",
  fontWeight: "bold",
  margin: "0",
};

const starsSection = {
  padding: "32px 32px 0",
  textAlign: "center" as const,
};

const starsText = {
  margin: "0",
  lineHeight: "1",
};

const starIcon = {
  color: "#fbbf24",
  fontSize: "36px",
  margin: "0 4px",
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

const buttonSection = {
  padding: "8px 32px 24px",
  textAlign: "center" as const,
};

const button = {
  backgroundColor: "#0891b2",
  borderRadius: "8px",
  color: "#ffffff",
  fontSize: "18px",
  fontWeight: "600",
  textDecoration: "none",
  textAlign: "center" as const,
  display: "inline-block",
  padding: "16px 48px",
};

const timeText = {
  color: "#9ca3af",
  fontSize: "13px",
  margin: "12px 0 0",
};

const whySection = {
  padding: "0 32px",
};

const whyTitle = {
  color: "#1f2937",
  fontSize: "16px",
  fontWeight: "600",
  margin: "0 0 16px",
};

const benefitsList = {
  margin: "0",
};

const benefitItem = {
  color: "#6b7280",
  fontSize: "14px",
  lineHeight: "20px",
  margin: "0 0 12px",
  paddingLeft: "8px",
};

const checkmark = {
  color: "#10b981",
  fontWeight: "bold",
  marginRight: "10px",
};

const footerText = {
  color: "#6b7280",
  fontSize: "14px",
  lineHeight: "20px",
  margin: "0 32px 8px",
};

const footerSignature = {
  color: "#374151",
  fontSize: "14px",
  lineHeight: "22px",
  margin: "16px 32px 0",
};
