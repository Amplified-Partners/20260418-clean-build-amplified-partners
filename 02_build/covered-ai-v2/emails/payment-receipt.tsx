import {
  Body,
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

interface PaymentReceiptEmailProps {
  customerName: string;
  businessName: string;
  invoiceNumber: string;
  amount: string;
  paymentDate: string;
  paymentMethod?: string;
  businessPhone?: string;
  businessEmail?: string;
}

export const PaymentReceiptEmail = ({
  customerName = "Customer",
  businessName = "Your Business",
  invoiceNumber = "INV-001",
  amount = "£100.00",
  paymentDate = new Date().toLocaleDateString(),
  paymentMethod = "Card",
  businessPhone,
  businessEmail,
}: PaymentReceiptEmailProps) => {
  const previewText = `Payment of ${amount} received - Thank you!`;

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

          {/* Success Banner */}
          <Section style={successBanner}>
            <Text style={successIcon}>✓</Text>
            <Heading style={successHeading}>Payment Received</Heading>
          </Section>

          <Hr style={hr} />

          {/* Greeting */}
          <Text style={paragraph}>Hi {customerName},</Text>
          <Text style={paragraph}>
            Thank you for your payment of <strong>{amount}</strong> for invoice{" "}
            <strong>{invoiceNumber}</strong>.
          </Text>

          {/* Receipt Details */}
          <Section style={receiptBox}>
            <table style={receiptTable}>
              <tbody>
                <tr>
                  <td style={receiptLabel}>Amount paid</td>
                  <td style={receiptValue}>{amount}</td>
                </tr>
                <tr>
                  <td style={receiptLabel}>Invoice</td>
                  <td style={receiptValue}>{invoiceNumber}</td>
                </tr>
                <tr>
                  <td style={receiptLabel}>Date</td>
                  <td style={receiptValue}>{paymentDate}</td>
                </tr>
                {paymentMethod && (
                  <tr>
                    <td style={receiptLabel}>Payment method</td>
                    <td style={receiptValue}>{paymentMethod}</td>
                  </tr>
                )}
              </tbody>
            </table>
          </Section>

          <Text style={paragraph}>
            This email confirms your payment has been received.
          </Text>

          <Hr style={hr} />

          {/* Footer */}
          <Text style={footerText}>
            If you have any questions, please contact us
            {businessEmail && ` at ${businessEmail}`}
            {businessPhone && ` or call ${businessPhone}`}.
          </Text>

          <Text style={footerText}>Thanks for your business!</Text>

          <Text style={footerSignature}>{businessName}</Text>
        </Container>
      </Body>
    </Html>
  );
};

export default PaymentReceiptEmail;

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

const successBanner = {
  padding: "32px",
  textAlign: "center" as const,
  backgroundColor: "#f0fdf4",
};

const successIcon = {
  fontSize: "48px",
  color: "#16a34a",
  margin: "0 0 8px",
};

const successHeading = {
  color: "#16a34a",
  fontSize: "24px",
  fontWeight: "bold",
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

const receiptBox = {
  backgroundColor: "#f0fdf4",
  borderRadius: "8px",
  padding: "24px",
  margin: "16px 32px",
};

const receiptTable = {
  width: "100%",
};

const receiptLabel = {
  color: "#6b7280",
  fontSize: "14px",
  padding: "8px 0",
};

const receiptValue = {
  color: "#1f2937",
  fontSize: "14px",
  fontWeight: "600",
  padding: "8px 0",
  textAlign: "right" as const,
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
  fontWeight: "600",
  margin: "16px 32px 0",
};
