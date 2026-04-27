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

interface QuoteLineItem {
  description: string;
  quantity: number;
  unitPrice: number;
  total: number;
}

interface QuoteEmailProps {
  customerName: string;
  businessName: string;
  quoteNumber: string;
  title: string;
  description?: string;
  lineItems: QuoteLineItem[];
  subtotal: number;
  vatRate: number;
  vatAmount: number;
  total: number;
  validUntil: string;
  viewLink?: string;
  acceptLink?: string;
  businessPhone?: string;
  businessEmail?: string;
  personalMessage?: string;
}

export const QuoteEmail = ({
  customerName = "Customer",
  businessName = "Your Business",
  quoteNumber = "QT-001",
  title = "Service Quote",
  description,
  lineItems = [{ description: "Service", quantity: 1, unitPrice: 100, total: 100 }],
  subtotal = 100,
  vatRate = 20,
  vatAmount = 20,
  total = 120,
  validUntil = new Date().toLocaleDateString(),
  viewLink,
  acceptLink,
  businessPhone,
  businessEmail,
  personalMessage,
}: QuoteEmailProps) => {
  const previewText = `Quote ${quoteNumber}: ${title} from ${businessName}`;

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

          {/* Quote Title */}
          <Section style={quoteHeader}>
            <Heading style={h1}>Quote</Heading>
            <Text style={quoteNumberText}>#{quoteNumber}</Text>
          </Section>

          <Hr style={hr} />

          {/* Greeting */}
          <Text style={paragraph}>Hi {customerName},</Text>
          <Text style={paragraph}>
            Thank you for your enquiry. Please find our quote for{" "}
            <strong>{title}</strong> below.
          </Text>

          {personalMessage && (
            <Text style={messageBox}>{personalMessage}</Text>
          )}

          {description && (
            <Text style={descriptionText}>{description}</Text>
          )}

          {/* Validity Notice */}
          <Section style={validitySection}>
            <Text style={validityText}>
              This quote is valid until <strong>{validUntil}</strong>
            </Text>
          </Section>

          {/* Line Items */}
          <Section style={itemsSection}>
            <table style={itemsTable}>
              <thead>
                <tr>
                  <th style={itemHeaderCell}>Description</th>
                  <th style={itemHeaderCellCenter}>Qty</th>
                  <th style={itemHeaderCellRight}>Unit Price</th>
                  <th style={itemHeaderCellRight}>Total</th>
                </tr>
              </thead>
              <tbody>
                {lineItems.map((item, index) => (
                  <tr key={index}>
                    <td style={itemCell}>{item.description}</td>
                    <td style={itemCellCenter}>{item.quantity}</td>
                    <td style={itemCellRight}>£{item.unitPrice.toFixed(2)}</td>
                    <td style={itemCellRight}>£{item.total.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Section>

          {/* Totals */}
          <Section style={totalsSection}>
            <table style={totalsTable}>
              <tbody>
                <tr>
                  <td style={totalLabel}>Subtotal:</td>
                  <td style={totalValue}>£{subtotal.toFixed(2)}</td>
                </tr>
                <tr>
                  <td style={totalLabel}>VAT ({vatRate}%):</td>
                  <td style={totalValue}>£{vatAmount.toFixed(2)}</td>
                </tr>
                <tr>
                  <td style={grandTotalLabel}>Quote Total:</td>
                  <td style={grandTotalValue}>£{total.toFixed(2)}</td>
                </tr>
              </tbody>
            </table>
          </Section>

          {/* Action Buttons */}
          <Section style={buttonSection}>
            {acceptLink && (
              <Button style={buttonPrimary} href={acceptLink}>
                Accept Quote
              </Button>
            )}
            {viewLink && (
              <Button style={buttonSecondary} href={viewLink}>
                View Full Quote
              </Button>
            )}
          </Section>

          <Hr style={hr} />

          {/* What's Next */}
          <Section style={nextStepsSection}>
            <Text style={nextStepsTitle}>What happens next?</Text>
            <Text style={nextStepsText}>
              1. Review the quote details above
              <br />
              2. Click "Accept Quote" to approve
              <br />
              3. We'll contact you to schedule the work
            </Text>
          </Section>

          <Hr style={hr} />

          {/* Footer */}
          <Text style={footerText}>
            Have questions? Contact us
            {businessEmail && ` at ${businessEmail}`}
            {businessPhone && ` or call ${businessPhone}`}.
          </Text>

          <Text style={footerSignature}>
            Best regards,
            <br />
            {businessName}
          </Text>
        </Container>
      </Body>
    </Html>
  );
};

export default QuoteEmail;

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

const quoteHeader = {
  padding: "32px 32px 0",
  textAlign: "center" as const,
};

const h1 = {
  color: "#1f2937",
  fontSize: "28px",
  fontWeight: "bold",
  margin: "0 0 8px",
};

const quoteNumberText = {
  color: "#6b7280",
  fontSize: "16px",
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

const messageBox = {
  backgroundColor: "#f0f9ff",
  borderLeft: "4px solid #0891b2",
  padding: "16px",
  margin: "0 32px 16px",
  color: "#374151",
  fontSize: "15px",
  lineHeight: "22px",
  borderRadius: "0 8px 8px 0",
};

const descriptionText = {
  color: "#6b7280",
  fontSize: "14px",
  lineHeight: "22px",
  margin: "0 32px 16px",
};

const validitySection = {
  padding: "0 32px",
  marginBottom: "16px",
};

const validityText = {
  backgroundColor: "#fef3c7",
  color: "#92400e",
  fontSize: "14px",
  padding: "12px 16px",
  borderRadius: "8px",
  margin: "0",
  textAlign: "center" as const,
};

const itemsSection = {
  padding: "0 32px",
};

const itemsTable = {
  width: "100%",
  borderCollapse: "collapse" as const,
};

const itemHeaderCell = {
  color: "#6b7280",
  fontSize: "12px",
  fontWeight: "600",
  textTransform: "uppercase" as const,
  padding: "12px 0",
  borderBottom: "2px solid #e5e7eb",
  textAlign: "left" as const,
};

const itemHeaderCellCenter = {
  ...itemHeaderCell,
  textAlign: "center" as const,
  width: "60px",
};

const itemHeaderCellRight = {
  ...itemHeaderCell,
  textAlign: "right" as const,
  width: "90px",
};

const itemCell = {
  color: "#374151",
  fontSize: "14px",
  padding: "16px 0",
  borderBottom: "1px solid #f3f4f6",
};

const itemCellCenter = {
  ...itemCell,
  textAlign: "center" as const,
};

const itemCellRight = {
  ...itemCell,
  textAlign: "right" as const,
  fontWeight: "500",
};

const totalsSection = {
  padding: "16px 32px 0",
};

const totalsTable = {
  width: "100%",
};

const totalLabel = {
  color: "#6b7280",
  fontSize: "14px",
  padding: "8px 0",
  textAlign: "right" as const,
  paddingRight: "16px",
};

const totalValue = {
  color: "#374151",
  fontSize: "14px",
  fontWeight: "500",
  padding: "8px 0",
  textAlign: "right" as const,
  width: "100px",
};

const grandTotalLabel = {
  ...totalLabel,
  color: "#1f2937",
  fontSize: "16px",
  fontWeight: "600",
  paddingTop: "16px",
  borderTop: "2px solid #e5e7eb",
};

const grandTotalValue = {
  ...totalValue,
  color: "#0891b2",
  fontSize: "20px",
  fontWeight: "bold",
  paddingTop: "16px",
  borderTop: "2px solid #e5e7eb",
};

const buttonSection = {
  padding: "24px 32px",
  textAlign: "center" as const,
};

const buttonPrimary = {
  backgroundColor: "#0891b2",
  borderRadius: "8px",
  color: "#ffffff",
  fontSize: "16px",
  fontWeight: "600",
  textDecoration: "none",
  textAlign: "center" as const,
  display: "inline-block",
  padding: "14px 32px",
  marginRight: "12px",
};

const buttonSecondary = {
  backgroundColor: "#ffffff",
  border: "2px solid #0891b2",
  borderRadius: "8px",
  color: "#0891b2",
  fontSize: "16px",
  fontWeight: "600",
  textDecoration: "none",
  textAlign: "center" as const,
  display: "inline-block",
  padding: "12px 24px",
};

const nextStepsSection = {
  padding: "0 32px",
};

const nextStepsTitle = {
  color: "#1f2937",
  fontSize: "16px",
  fontWeight: "600",
  margin: "0 0 12px",
};

const nextStepsText = {
  color: "#6b7280",
  fontSize: "14px",
  lineHeight: "24px",
  margin: "0",
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
