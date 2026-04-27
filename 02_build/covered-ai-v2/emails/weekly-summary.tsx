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

interface WeeklySummaryEmailProps {
  ownerName: string;
  businessName: string;
  weekEnding: string;
  stats: {
    callsHandled: number;
    jobsCompleted: number;
    revenueCollected: number;
    newCustomers: number;
    reviewsReceived: number;
  };
  insight?: string;
  dashboardLink: string;
}

export const WeeklySummaryEmail = ({
  ownerName = "Ralph",
  businessName = "Your Business",
  weekEnding = new Date().toLocaleDateString(),
  stats = {
    callsHandled: 12,
    jobsCompleted: 8,
    revenueCollected: 2450,
    newCustomers: 3,
    reviewsReceived: 2,
  },
  insight,
  dashboardLink = "https://app.covered.ai",
}: WeeklySummaryEmailProps) => {
  const previewText = `Your weekly summary: ${stats.callsHandled} calls, £${stats.revenueCollected} collected`;

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

          {/* Greeting */}
          <Section style={greetingSection}>
            <Text style={greeting}>👋 Hi {ownerName},</Text>
            <Text style={paragraph}>
              Here's your weekly summary for the week ending {weekEnding}:
            </Text>
          </Section>

          {/* Stats Grid */}
          <Section style={statsSection}>
            <table style={statsTable}>
              <tbody>
                <tr>
                  <td style={statBox}>
                    <Text style={statIcon}>📞</Text>
                    <Text style={statValue}>{stats.callsHandled}</Text>
                    <Text style={statLabel}>Calls handled</Text>
                  </td>
                  <td style={statBox}>
                    <Text style={statIcon}>💼</Text>
                    <Text style={statValue}>{stats.jobsCompleted}</Text>
                    <Text style={statLabel}>Jobs completed</Text>
                  </td>
                </tr>
                <tr>
                  <td style={statBox}>
                    <Text style={statIcon}>💷</Text>
                    <Text style={statValue}>
                      £{stats.revenueCollected.toLocaleString()}
                    </Text>
                    <Text style={statLabel}>Collected</Text>
                  </td>
                  <td style={statBox}>
                    <Text style={statIcon}>👥</Text>
                    <Text style={statValue}>{stats.newCustomers}</Text>
                    <Text style={statLabel}>New customers</Text>
                  </td>
                </tr>
                <tr>
                  <td style={statBoxFull} colSpan={2}>
                    <Text style={statIcon}>⭐</Text>
                    <Text style={statValue}>{stats.reviewsReceived}</Text>
                    <Text style={statLabel}>Reviews received</Text>
                  </td>
                </tr>
              </tbody>
            </table>
          </Section>

          {/* Insight */}
          {insight && (
            <Section style={insightSection}>
              <Text style={insightText}>💡 {insight}</Text>
            </Section>
          )}

          {/* CTA Button */}
          <Section style={buttonSection}>
            <Button style={button} href={dashboardLink}>
              View Full Dashboard
            </Button>
          </Section>

          <Hr style={hr} />

          {/* Footer */}
          <Text style={footerText}>
            Have a great week,
            <br />
            Gemma
          </Text>

          <Text style={footerSmall}>Powered by Covered AI</Text>
        </Container>
      </Body>
    </Html>
  );
};

export default WeeklySummaryEmail;

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

const greetingSection = {
  padding: "24px 32px 0",
};

const greeting = {
  fontSize: "20px",
  fontWeight: "bold",
  color: "#1f2937",
  margin: "0 0 16px",
};

const paragraph = {
  color: "#374151",
  fontSize: "16px",
  lineHeight: "24px",
  margin: "0 0 16px",
};

const statsSection = {
  padding: "0 32px",
};

const statsTable = {
  width: "100%",
  borderCollapse: "separate" as const,
  borderSpacing: "8px",
};

const statBox = {
  backgroundColor: "#f9fafb",
  borderRadius: "8px",
  padding: "16px",
  textAlign: "center" as const,
  width: "50%",
};

const statBoxFull = {
  ...statBox,
  width: "100%",
};

const statIcon = {
  fontSize: "24px",
  margin: "0 0 8px",
};

const statValue = {
  fontSize: "24px",
  fontWeight: "bold",
  color: "#1f2937",
  margin: "0 0 4px",
};

const statLabel = {
  fontSize: "14px",
  color: "#6b7280",
  margin: "0",
};

const insightSection = {
  backgroundColor: "#dbeafe",
  borderRadius: "8px",
  padding: "16px",
  margin: "16px 32px",
};

const insightText = {
  fontSize: "16px",
  color: "#1e40af",
  margin: "0",
};

const buttonSection = {
  padding: "24px 32px",
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

const hr = {
  borderColor: "#e5e7eb",
  margin: "24px 32px",
};

const footerText = {
  color: "#374151",
  fontSize: "16px",
  margin: "0 32px 16px",
};

const footerSmall = {
  fontSize: "12px",
  color: "#9ca3af",
  textAlign: "center" as const,
  margin: "0 32px",
};
