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

interface InvoiceReminderEmailProps {
  customerName: string;
  businessName: string;
  invoiceNumber: string;
  dueDate: string;
  total: number;
  isOverdue: boolean;
  daysOverdue?: number;
  paymentLink?: string;
  businessPhone?: string;
  businessEmail?: string;
}

export const InvoiceReminderEmail = ({
  customerName = "Customer",
  businessName = "Your Business",
  invoiceNumber = "INV-001",
  dueDate = new Date().toLocaleDateString(),
  total = 120,
  isOverdue = false,
  daysOverdue = 0,
  paymentLink,
  businessPhone,
  businessEmail,
}: InvoiceReminderEmailProps) => {
  const previewText = isOverdue
    ? `Overdue: Invoice ${invoiceNumber} from ${businessName}`
    : `Reminder: Invoice ${invoiceNumber} due soon`;

  return (
    <Html>
      <Head />
      <Preview>{previewText}</Preview>
      <Body style={main}>
        <Container style={container}>
          {/* Header */}
          <Section style={isOverdue ? headerOverdue : header}>
            <Heading style={logo}>{businessName}</Heading>
          </Section>

          {/* Title */}
          <Section style={titleSection}>
            <Heading style={h1}>
              {isOverdue ? "Payment Overdue" : "Payment Reminder"}
            </Heading>
            {isOverdue && daysOverdue > 0 && (
              <Text style={overdueText}>
                {daysOverdue} {daysOverdue === 1 ? "day" : "days"} overdue
              </Text>
            )}
          </Section>

          <Hr style={hr} />

          {/* Greeting */}
          <Text style={paragraph}>Hi {customerName},</Text>

          {isOverdue ? (
            <>
              <Text style={paragraph}>
                Your invoice <strong>#{invoiceNumber}</strong> was due on{" "}
                <strong>{dueDate}</strong> and is now overdue.
              </Text>
              <Text style={paragraph}>
                Please arrange payment at your earliest convenience to avoid any
                service interruptions.
              </Text>
            </>
          ) : (
            <Text style={paragraph}>
              This is a friendly reminder that invoice{" "}
              <strong>#{invoiceNumber}</strong> is due on{" "}
              <strong>{dueDate}</strong>.
            </Text>
          )}

          {/* Amount Box */}
          <Section style={amountSection}>
            <div style={amountBox}>
              <Text style={amountLabel}>Amount Due</Text>
              <Text style={amountValue}>£{total.toFixed(2)}</Text>
            </div>
          </Section>

          {/* Payment Button */}
          {paymentLink && (
            <Section style={buttonSection}>
              <Button style={isOverdue ? buttonOverdue : button} href={paymentLink}>
                Pay Now
              </Button>
            </Section>
          )}

          <Hr style={hr} />

          {/* Footer */}
          <Text style={footerText}>
            If you've already made this payment, please disregard this email.
          </Text>

          <Text style={footerText}>
            Questions? Contact us
            {businessEmail && ` at ${businessEmail}`}
            {businessPhone && ` or call ${businessPhone}`}.
          </Text>

          <Text style={footerSignature}>
            Thank you,
            <br />
            {businessName}
          </Text>
        </Container>
      </Body>
    </Html>
  );
};

export default InvoiceReminderEmail;

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

const headerOverdue = {
  padding: "24px 32px",
  backgroundColor: "#dc2626",
};

const logo = {
  color: "#ffffff",
  fontSize: "24px",
  fontWeight: "bold",
  margin: "0",
};

const titleSection = {
  padding: "32px 32px 0",
  textAlign: "center" as const,
};

const h1 = {
  color: "#1f2937",
  fontSize: "28px",
  fontWeight: "bold",
  margin: "0 0 8px",
};

const overdueText = {
  color: "#dc2626",
  fontSize: "14px",
  fontWeight: "600",
  margin: "0",
  textTransform: "uppercase" as const,
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

const amountSection = {
  padding: "0 32px",
};

const amountBox = {
  backgroundColor: "#f9fafb",
  borderRadius: "12px",
  padding: "24px",
  textAlign: "center" as const,
  border: "1px solid #e5e7eb",
};

const amountLabel = {
  color: "#6b7280",
  fontSize: "14px",
  margin: "0 0 8px",
  textTransform: "uppercase" as const,
  fontWeight: "600",
  letterSpacing: "0.5px",
};

const amountValue = {
  color: "#1f2937",
  fontSize: "36px",
  fontWeight: "bold",
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

const buttonOverdue = {
  ...button,
  backgroundColor: "#dc2626",
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
