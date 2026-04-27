import {
  Body,
  Button,
  Container,
  Head,
  Heading,
  Hr,
  Html,
  Img,
  Preview,
  Section,
  Text,
} from "@react-email/components";
import * as React from "react";

interface InvoiceEmailProps {
  customerName: string;
  businessName: string;
  invoiceNumber: string;
  invoiceDate: string;
  dueDate: string;
  lineItems: { description: string; amount: number }[];
  subtotal: number;
  vatRate: number;
  vatAmount: number;
  total: number;
  paymentLink?: string;
  businessPhone?: string;
  businessEmail?: string;
}

export const InvoiceEmail = ({
  customerName = "Customer",
  businessName = "Your Business",
  invoiceNumber = "INV-001",
  invoiceDate = new Date().toLocaleDateString(),
  dueDate = new Date().toLocaleDateString(),
  lineItems = [{ description: "Service", amount: 100 }],
  subtotal = 100,
  vatRate = 20,
  vatAmount = 20,
  total = 120,
  paymentLink,
  businessPhone,
  businessEmail,
}: InvoiceEmailProps) => {
  const previewText = `Invoice ${invoiceNumber} from ${businessName}`;

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

          {/* Invoice Title */}
          <Section style={invoiceHeader}>
            <Heading style={h1}>Invoice</Heading>
            <Text style={invoiceNumberText}>#{invoiceNumber}</Text>
          </Section>

          <Hr style={hr} />

          {/* Greeting */}
          <Text style={paragraph}>Hi {customerName},</Text>
          <Text style={paragraph}>
            Please find your invoice details below. Payment is due by{" "}
            <strong>{dueDate}</strong>.
          </Text>

          {/* Invoice Details */}
          <Section style={detailsSection}>
            <table style={detailsTable}>
              <tbody>
                <tr>
                  <td style={detailLabel}>Invoice Date:</td>
                  <td style={detailValue}>{invoiceDate}</td>
                </tr>
                <tr>
                  <td style={detailLabel}>Due Date:</td>
                  <td style={detailValue}>{dueDate}</td>
                </tr>
              </tbody>
            </table>
          </Section>

          {/* Line Items */}
          <Section style={itemsSection}>
            <table style={itemsTable}>
              <thead>
                <tr>
                  <th style={itemHeaderCell}>Description</th>
                  <th style={itemHeaderCellRight}>Amount</th>
                </tr>
              </thead>
              <tbody>
                {lineItems.map((item, index) => (
                  <tr key={index}>
                    <td style={itemCell}>{item.description}</td>
                    <td style={itemCellRight}>
                      £{item.amount.toFixed(2)}
                    </td>
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
                  <td style={grandTotalLabel}>Total Due:</td>
                  <td style={grandTotalValue}>£{total.toFixed(2)}</td>
                </tr>
              </tbody>
            </table>
          </Section>

          {/* Payment Button */}
          {paymentLink && (
            <Section style={buttonSection}>
              <Button style={button} href={paymentLink}>
                Pay Now
              </Button>
            </Section>
          )}

          <Hr style={hr} />

          {/* Footer */}
          <Text style={footerText}>
            If you have any questions about this invoice, please contact us
            {businessEmail && ` at ${businessEmail}`}
            {businessPhone && ` or call ${businessPhone}`}.
          </Text>

          <Text style={footerText}>
            Thank you for your business!
          </Text>

          <Text style={footerSignature}>{businessName}</Text>
        </Container>
      </Body>
    </Html>
  );
};

export default InvoiceEmail;

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

const invoiceHeader = {
  padding: "32px 32px 0",
  textAlign: "center" as const,
};

const h1 = {
  color: "#1f2937",
  fontSize: "28px",
  fontWeight: "bold",
  margin: "0 0 8px",
};

const invoiceNumberText = {
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

const detailsSection = {
  padding: "0 32px",
};

const detailsTable = {
  width: "100%",
  marginBottom: "16px",
};

const detailLabel = {
  color: "#6b7280",
  fontSize: "14px",
  padding: "4px 0",
  width: "120px",
};

const detailValue = {
  color: "#1f2937",
  fontSize: "14px",
  fontWeight: "500",
  padding: "4px 0",
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

const itemHeaderCellRight = {
  ...itemHeaderCell,
  textAlign: "right" as const,
};

const itemCell = {
  color: "#374151",
  fontSize: "14px",
  padding: "16px 0",
  borderBottom: "1px solid #f3f4f6",
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
  margin: "0 32px 8px",
};

const footerSignature = {
  color: "#374151",
  fontSize: "14px",
  fontWeight: "600",
  margin: "16px 32px 0",
};
