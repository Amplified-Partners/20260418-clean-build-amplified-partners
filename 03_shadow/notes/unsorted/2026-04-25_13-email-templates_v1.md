---
title: "Covered AI — Email Templates"
id: "13-email-templates"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Covered AI — Email Templates

## Document Info
- **Version**: 1.0
- **Created**: 2025-01-27
- **Purpose**: All email templates for Resend
- **Stack**: React Email components

---

# EMAIL DESIGN SYSTEM

## Brand Colours
```
Primary Blue: #2563eb
Success Green: #16a34a
Warning Amber: #ca8a04
Danger Red: #dc2626
Text Dark: #111827
Text Grey: #6b7280
Background: #f9fafb
White: #ffffff
```

## Typography
- Font: Arial, sans-serif (safe for email)
- Heading: 24px, bold, #111827
- Body: 16px, normal, #374151
- Small: 14px, normal, #6b7280

## Layout
- Max width: 600px
- Padding: 40px
- Border radius: 8px
- Background: #f9fafb (outer), #ffffff (content)

---

# TEMPLATE 1: INVOICE SENT

## File
`src/emails/invoice/invoice-sent.tsx`

## Variables
```typescript
interface InvoiceSentProps {
  businessName: string;
  customerName: string;
  invoiceNumber: string;
  amount: string;
  dueDate: string;
  description: string;
  paymentLink: string;
  bankDetails?: {
    accountName: string;
    sortCode: string;
    accountNumber: string;
  };
}
```

## Subject
`Invoice {{invoiceNumber}} from {{businessName}}`

## Template

```tsx
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
} from '@react-email/components';

export default function InvoiceSent({
  businessName,
  customerName,
  invoiceNumber,
  amount,
  dueDate,
  description,
  paymentLink,
  bankDetails,
}: InvoiceSentProps) {
  return (
    <Html>
      <Head />
      <Preview>Invoice {invoiceNumber} for {amount} from {businessName}</Preview>
      <Body style={main}>
        <Container style={container}>
          <Heading style={heading}>{businessName}</Heading>
          
          <Text style={paragraph}>Hi {customerName},</Text>
          
          <Text style={paragraph}>
            Please find your invoice below.
          </Text>
          
          <Section style={invoiceBox}>
            <Text style={invoiceLabel}>Invoice</Text>
            <Text style={invoiceNumber}>{invoiceNumber}</Text>
            
            <Hr style={divider} />
            
            <Text style={descriptionText}>{description}</Text>
            
            <Hr style={divider} />
            
            <table style={table}>
              <tr>
                <td style={tableLabel}>Amount due</td>
                <td style={tableValue}>{amount}</td>
              </tr>
              <tr>
                <td style={tableLabel}>Due date</td>
                <td style={tableValue}>{dueDate}</td>
              </tr>
            </table>
          </Section>
          
          <Section style={buttonSection}>
            <Button style={button} href={paymentLink}>
              Pay Now
            </Button>
          </Section>
          
          {bankDetails && (
            <Section style={bankSection}>
              <Text style={smallHeading}>Bank Transfer Details</Text>
              <Text style={smallText}>
                Account name: {bankDetails.accountName}<br />
                Sort code: {bankDetails.sortCode}<br />
                Account number: {bankDetails.accountNumber}<br />
                Reference: {invoiceNumber}
              </Text>
            </Section>
          )}
          
          <Hr style={divider} />
          
          <Text style={footer}>
            Thanks,<br />
            {businessName}
          </Text>
        </Container>
      </Body>
    </Html>
  );
}

const main = {
  backgroundColor: '#f9fafb',
  fontFamily: 'Arial, sans-serif',
};

const container = {
  backgroundColor: '#ffffff',
  margin: '40px auto',
  padding: '40px',
  borderRadius: '8px',
  maxWidth: '600px',
};

const heading = {
  fontSize: '24px',
  fontWeight: 'bold',
  color: '#111827',
  marginBottom: '24px',
};

const paragraph = {
  fontSize: '16px',
  lineHeight: '24px',
  color: '#374151',
  marginBottom: '16px',
};

const invoiceBox = {
  backgroundColor: '#f9fafb',
  borderRadius: '8px',
  padding: '24px',
  marginBottom: '24px',
};

const invoiceLabel = {
  fontSize: '14px',
  color: '#6b7280',
  marginBottom: '4px',
};

const invoiceNumberStyle = {
  fontSize: '20px',
  fontWeight: 'bold',
  color: '#111827',
  marginBottom: '16px',
};

const descriptionText = {
  fontSize: '16px',
  color: '#374151',
  margin: '16px 0',
};

const divider = {
  borderColor: '#e5e7eb',
  margin: '16px 0',
};

const table = {
  width: '100%',
};

const tableLabel = {
  fontSize: '14px',
  color: '#6b7280',
  padding: '8px 0',
};

const tableValue = {
  fontSize: '16px',
  fontWeight: 'bold',
  color: '#111827',
  textAlign: 'right' as const,
  padding: '8px 0',
};

const buttonSection = {
  textAlign: 'center' as const,
  marginBottom: '24px',
};

const button = {
  backgroundColor: '#2563eb',
  color: '#ffffff',
  fontSize: '16px',
  fontWeight: 'bold',
  padding: '12px 32px',
  borderRadius: '8px',
  textDecoration: 'none',
};

const bankSection = {
  backgroundColor: '#f9fafb',
  borderRadius: '8px',
  padding: '16px',
  marginBottom: '24px',
};

const smallHeading = {
  fontSize: '14px',
  fontWeight: 'bold',
  color: '#374151',
  marginBottom: '8px',
};

const smallText = {
  fontSize: '14px',
  color: '#6b7280',
  lineHeight: '20px',
};

const footer = {
  fontSize: '16px',
  color: '#374151',
};
```

---

# TEMPLATE 2: INVOICE REMINDER 1 (Day 7)

## File
`src/emails/invoice/reminder-1.tsx`

## Subject
`Friendly reminder: Invoice {{invoiceNumber}}`

## Template

```tsx
export default function InvoiceReminder1({
  businessName,
  customerName,
  invoiceNumber,
  amount,
  dueDate,
  paymentLink,
}: InvoiceReminderProps) {
  return (
    <Html>
      <Head />
      <Preview>Reminder: Invoice {invoiceNumber} for {amount} due {dueDate}</Preview>
      <Body style={main}>
        <Container style={container}>
          <Heading style={heading}>{businessName}</Heading>
          
          <Text style={paragraph}>Hi {customerName},</Text>
          
          <Text style={paragraph}>
            Just a quick reminder that invoice <strong>{invoiceNumber}</strong> for <strong>{amount}</strong> is due on <strong>{dueDate}</strong>.
          </Text>
          
          <Section style={buttonSection}>
            <Button style={button} href={paymentLink}>
              Pay Now
            </Button>
          </Section>
          
          <Text style={smallText}>
            If you've already paid, please ignore this reminder.
          </Text>
          
          <Hr style={divider} />
          
          <Text style={footer}>
            Thanks,<br />
            {businessName}
          </Text>
        </Container>
      </Body>
    </Html>
  );
}
```

---

# TEMPLATE 3: INVOICE REMINDER 2 (Day 14)

## File
`src/emails/invoice/reminder-2.tsx`

## Subject
`Invoice {{invoiceNumber}} is now overdue`

## Template

```tsx
export default function InvoiceReminder2({
  businessName,
  customerName,
  invoiceNumber,
  amount,
  originalDueDate,
  paymentLink,
}: InvoiceReminderProps) {
  return (
    <Html>
      <Head />
      <Preview>Invoice {invoiceNumber} for {amount} is now overdue</Preview>
      <Body style={main}>
        <Container style={container}>
          <Heading style={heading}>{businessName}</Heading>
          
          <Text style={paragraph}>Hi {customerName},</Text>
          
          <Text style={paragraph}>
            Invoice <strong>{invoiceNumber}</strong> for <strong>{amount}</strong> was due on {originalDueDate} and is now overdue.
          </Text>
          
          <Text style={paragraph}>
            Please arrange payment at your earliest convenience.
          </Text>
          
          <Section style={buttonSection}>
            <Button style={buttonUrgent} href={paymentLink}>
              Pay Now
            </Button>
          </Section>
          
          <Text style={smallText}>
            If there's an issue with this invoice, please get in touch so we can resolve it.
          </Text>
          
          <Hr style={divider} />
          
          <Text style={footer}>
            Thanks,<br />
            {businessName}
          </Text>
        </Container>
      </Body>
    </Html>
  );
}

const buttonUrgent = {
  backgroundColor: '#ca8a04',
  color: '#ffffff',
  fontSize: '16px',
  fontWeight: 'bold',
  padding: '12px 32px',
  borderRadius: '8px',
  textDecoration: 'none',
};
```

---

# TEMPLATE 4: INVOICE FINAL NOTICE (Day 21)

## File
`src/emails/invoice/final-notice.tsx`

## Subject
`Final notice: Invoice {{invoiceNumber}}`

## Template

```tsx
export default function InvoiceFinalNotice({
  businessName,
  customerName,
  invoiceNumber,
  amount,
  daysOverdue,
  paymentLink,
}: InvoiceFinalNoticeProps) {
  return (
    <Html>
      <Head />
      <Preview>Final notice: Invoice {invoiceNumber} for {amount} requires immediate attention</Preview>
      <Body style={main}>
        <Container style={container}>
          <Heading style={heading}>{businessName}</Heading>
          
          <Text style={paragraph}>Hi {customerName},</Text>
          
          <Text style={paragraph}>
            This is a final reminder that invoice <strong>{invoiceNumber}</strong> for <strong>{amount}</strong> remains unpaid and is now <strong>{daysOverdue} days overdue</strong>.
          </Text>
          
          <Text style={paragraph}>
            Please arrange payment immediately to avoid any further action.
          </Text>
          
          <Section style={buttonSection}>
            <Button style={buttonDanger} href={paymentLink}>
              Pay Now
            </Button>
          </Section>
          
          <Text style={smallText}>
            If you're experiencing difficulties, please contact us to discuss payment arrangements.
          </Text>
          
          <Hr style={divider} />
          
          <Text style={footer}>
            Thanks,<br />
            {businessName}
          </Text>
        </Container>
      </Body>
    </Html>
  );
}

const buttonDanger = {
  backgroundColor: '#dc2626',
  color: '#ffffff',
  fontSize: '16px',
  fontWeight: 'bold',
  padding: '12px 32px',
  borderRadius: '8px',
  textDecoration: 'none',
};
```

---

# TEMPLATE 5: PAYMENT RECEIPT

## File
`src/emails/invoice/receipt.tsx`

## Subject
`Payment received - Thank you!`

## Template

```tsx
export default function PaymentReceipt({
  businessName,
  customerName,
  invoiceNumber,
  amount,
  paymentDate,
}: PaymentReceiptProps) {
  return (
    <Html>
      <Head />
      <Preview>Payment of {amount} received - Thank you!</Preview>
      <Body style={main}>
        <Container style={container}>
          <Heading style={heading}>{businessName}</Heading>
          
          <Section style={successBox}>
            <Text style={successIcon}>✓</Text>
            <Text style={successText}>Payment Received</Text>
          </Section>
          
          <Text style={paragraph}>Hi {customerName},</Text>
          
          <Text style={paragraph}>
            Thank you for your payment of <strong>{amount}</strong> for invoice <strong>{invoiceNumber}</strong>.
          </Text>
          
          <Section style={receiptBox}>
            <table style={table}>
              <tr>
                <td style={tableLabel}>Amount paid</td>
                <td style={tableValue}>{amount}</td>
              </tr>
              <tr>
                <td style={tableLabel}>Invoice</td>
                <td style={tableValue}>{invoiceNumber}</td>
              </tr>
              <tr>
                <td style={tableLabel}>Date</td>
                <td style={tableValue}>{paymentDate}</td>
              </tr>
            </table>
          </Section>
          
          <Text style={paragraph}>
            This email confirms your payment has been received.
          </Text>
          
          <Hr style={divider} />
          
          <Text style={footer}>
            Thanks for your business,<br />
            {businessName}
          </Text>
        </Container>
      </Body>
    </Html>
  );
}

const successBox = {
  textAlign: 'center' as const,
  marginBottom: '24px',
};

const successIcon = {
  fontSize: '48px',
  color: '#16a34a',
  marginBottom: '8px',
};

const successText = {
  fontSize: '20px',
  fontWeight: 'bold',
  color: '#16a34a',
};

const receiptBox = {
  backgroundColor: '#f0fdf4',
  borderRadius: '8px',
  padding: '24px',
  marginBottom: '24px',
};
```

---

# TEMPLATE 6: REVIEW REQUEST

## File
`src/emails/review/review-request.tsx`

## Subject
`How did we do, {{customerName}}?`

## Template

```tsx
export default function ReviewRequest({
  businessName,
  ownerName,
  customerName,
  jobType,
  reviewLink,
}: ReviewRequestProps) {
  return (
    <Html>
      <Head />
      <Preview>We'd love your feedback on our recent {jobType}</Preview>
      <Body style={main}>
        <Container style={container}>
          <Heading style={heading}>{businessName}</Heading>
          
          <Text style={paragraph}>Hi {customerName},</Text>
          
          <Text style={paragraph}>
            Thanks for choosing {businessName} for your recent <strong>{jobType}</strong>.
          </Text>
          
          <Text style={paragraph}>
            We'd really appreciate your feedback:
          </Text>
          
          <Section style={buttonSection}>
            <Button style={button} href={reviewLink}>
              ⭐⭐⭐⭐⭐ Leave a Review
            </Button>
          </Section>
          
          <Text style={smallText}>
            It only takes 30 seconds and helps other customers find us.
          </Text>
          
          <Hr style={divider} />
          
          <Text style={footer}>
            Thanks,<br />
            {ownerName}<br />
            {businessName}
          </Text>
        </Container>
      </Body>
    </Html>
  );
}
```

---

# TEMPLATE 7: WEEKLY SUMMARY

## File
`src/emails/reports/weekly-summary.tsx`

## Subject
`Your week with Covered AI`

## Template

```tsx
export default function WeeklySummary({
  businessName,
  ownerName,
  weekEnding,
  stats,
  insight,
  dashboardLink,
}: WeeklySummaryProps) {
  return (
    <Html>
      <Head />
      <Preview>Your weekly summary: {stats.callsHandled} calls, £{stats.revenueCollected} collected</Preview>
      <Body style={main}>
        <Container style={container}>
          <Text style={gemmaGreeting}>👋 Hi {ownerName},</Text>
          
          <Text style={paragraph}>
            Here's your weekly summary for the week ending {weekEnding}:
          </Text>
          
          <Section style={statsGrid}>
            <table style={statsTable}>
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
                  <Text style={statValue}>£{stats.revenueCollected}</Text>
                  <Text style={statLabel}>Collected</Text>
                </td>
                <td style={statBox}>
                  <Text style={statIcon}>👥</Text>
                  <Text style={statValue}>{stats.newCustomers}</Text>
                  <Text style={statLabel}>New customers</Text>
                </td>
              </tr>
              <tr>
                <td style={statBox} colSpan={2}>
                  <Text style={statIcon}>⭐</Text>
                  <Text style={statValue}>{stats.reviewsReceived}</Text>
                  <Text style={statLabel}>Reviews received</Text>
                </td>
              </tr>
            </table>
          </Section>
          
          {insight && (
            <Section style={insightBox}>
              <Text style={insightText}>💡 {insight}</Text>
            </Section>
          )}
          
          <Section style={buttonSection}>
            <Button style={button} href={dashboardLink}>
              View Full Dashboard
            </Button>
          </Section>
          
          <Hr style={divider} />
          
          <Text style={footer}>
            Have a great week,<br />
            Gemma
          </Text>
          
          <Text style={footerSmall}>
            Powered by Covered AI
          </Text>
        </Container>
      </Body>
    </Html>
  );
}

const gemmaGreeting = {
  fontSize: '20px',
  fontWeight: 'bold',
  color: '#111827',
  marginBottom: '16px',
};

const statsGrid = {
  marginBottom: '24px',
};

const statsTable = {
  width: '100%',
  borderCollapse: 'collapse' as const,
};

const statBox = {
  backgroundColor: '#f9fafb',
  borderRadius: '8px',
  padding: '16px',
  textAlign: 'center' as const,
  margin: '4px',
};

const statIcon = {
  fontSize: '24px',
  marginBottom: '8px',
};

const statValue = {
  fontSize: '24px',
  fontWeight: 'bold',
  color: '#111827',
  marginBottom: '4px',
};

const statLabel = {
  fontSize: '14px',
  color: '#6b7280',
};

const insightBox = {
  backgroundColor: '#dbeafe',
  borderRadius: '8px',
  padding: '16px',
  marginBottom: '24px',
};

const insightText = {
  fontSize: '16px',
  color: '#1e40af',
};

const footerSmall = {
  fontSize: '12px',
  color: '#9ca3af',
  textAlign: 'center' as const,
};
```

---

# TEMPLATE 8: WELCOME EMAIL

## File
`src/emails/onboarding/welcome.tsx`

## Subject
`Welcome to Covered AI! 🎉`

## Template

```tsx
export default function Welcome({
  businessName,
  ownerName,
  coveredNumber,
  dashboardLink,
}: WelcomeProps) {
  return (
    <Html>
      <Head />
      <Preview>Gemma is ready to answer your calls</Preview>
      <Body style={main}>
        <Container style={container}>
          <Section style={heroSection}>
            <Text style={heroEmoji}>🎉</Text>
            <Heading style={heroHeading}>Welcome to Covered AI!</Heading>
          </Section>
          
          <Text style={paragraph}>Hi {ownerName},</Text>
          
          <Text style={paragraph}>
            You're all set up. Gemma is now ready to answer calls for <strong>{businessName}</strong>.
          </Text>
          
          <Section style={numberBox}>
            <Text style={numberLabel}>Your Covered AI number</Text>
            <Text style={numberValue}>{coveredNumber}</Text>
          </Section>
          
          <Text style={paragraph}>
            <strong>What happens now:</strong>
          </Text>
          
          <Section style={stepsSection}>
            <Text style={stepText}>
              <strong>1. 📞 Calls come in</strong><br />
              Gemma answers professionally, 24/7
            </Text>
            <Text style={stepText}>
              <strong>2. 💬 You get summaries</strong><br />
              WhatsApp notifications after each call
            </Text>
            <Text style={stepText}>
              <strong>3. 📊 Track everything</strong><br />
              Your dashboard shows all activity
            </Text>
          </Section>
          
          <Section style={buttonSection}>
            <Button style={button} href={dashboardLink}>
              Go to Dashboard
            </Button>
          </Section>
          
          <Hr style={divider} />
          
          <Text style={footer}>
            Questions? Just reply to this email.<br /><br />
            Welcome aboard,<br />
            The Covered AI Team
          </Text>
        </Container>
      </Body>
    </Html>
  );
}

const heroSection = {
  textAlign: 'center' as const,
  marginBottom: '24px',
};

const heroEmoji = {
  fontSize: '48px',
  marginBottom: '16px',
};

const heroHeading = {
  fontSize: '28px',
  fontWeight: 'bold',
  color: '#111827',
};

const numberBox = {
  backgroundColor: '#dbeafe',
  borderRadius: '8px',
  padding: '24px',
  textAlign: 'center' as const,
  marginBottom: '24px',
};

const numberLabel = {
  fontSize: '14px',
  color: '#1e40af',
  marginBottom: '8px',
};

const numberValue = {
  fontSize: '28px',
  fontWeight: 'bold',
  color: '#1e40af',
};

const stepsSection = {
  marginBottom: '24px',
};

const stepText = {
  fontSize: '16px',
  color: '#374151',
  marginBottom: '16px',
  lineHeight: '24px',
};
```

---

# TEMPLATE 9: MISSED CALLBACK REMINDER

## File
`src/emails/calls/missed-callback.tsx`

## Subject
`Don't forget: {{callerName}} is waiting for your call`

## Template

```tsx
export default function MissedCallback({
  businessName,
  ownerName,
  callerName,
  callerPhone,
  callSummary,
  hoursWaiting,
  dashboardLink,
}: MissedCallbackProps) {
  return (
    <Html>
      <Head />
      <Preview>{callerName} has been waiting {hoursWaiting} hours for your callback</Preview>
      <Body style={main}>
        <Container style={container}>
          <Section style={warningBanner}>
            <Text style={warningText}>⏰ Callback Reminder</Text>
          </Section>
          
          <Text style={paragraph}>Hi {ownerName},</Text>
          
          <Text style={paragraph}>
            <strong>{callerName}</strong> called {hoursWaiting} hours ago and is still waiting for a callback.
          </Text>
          
          <Section style={callBox}>
            <Text style={callLabel}>Phone</Text>
            <Text style={callValue}>{callerPhone}</Text>
            
            <Hr style={divider} />
            
            <Text style={callLabel}>Summary</Text>
            <Text style={callSummaryText}>{callSummary}</Text>
          </Section>
          
          <Section style={buttonSection}>
            <Button style={buttonCall} href={`tel:${callerPhone}`}>
              📞 Call Now
            </Button>
          </Section>
          
          <Section style={buttonSection}>
            <Button style={buttonSecondary} href={dashboardLink}>
              View in Dashboard
            </Button>
          </Section>
          
          <Hr style={divider} />
          
          <Text style={footer}>
            {businessName}
          </Text>
        </Container>
      </Body>
    </Html>
  );
}

const warningBanner = {
  backgroundColor: '#fef3c7',
  borderRadius: '8px',
  padding: '12px',
  textAlign: 'center' as const,
  marginBottom: '24px',
};

const warningText = {
  fontSize: '16px',
  fontWeight: 'bold',
  color: '#92400e',
};

const callBox = {
  backgroundColor: '#f9fafb',
  borderRadius: '8px',
  padding: '24px',
  marginBottom: '24px',
};

const callLabel = {
  fontSize: '12px',
  color: '#6b7280',
  textTransform: 'uppercase' as const,
  marginBottom: '4px',
};

const callValue = {
  fontSize: '20px',
  fontWeight: 'bold',
  color: '#111827',
  marginBottom: '16px',
};

const callSummaryText = {
  fontSize: '16px',
  color: '#374151',
  lineHeight: '24px',
};

const buttonCall = {
  backgroundColor: '#16a34a',
  color: '#ffffff',
  fontSize: '16px',
  fontWeight: 'bold',
  padding: '12px 32px',
  borderRadius: '8px',
  textDecoration: 'none',
};

const buttonSecondary = {
  backgroundColor: '#ffffff',
  color: '#374151',
  fontSize: '14px',
  padding: '8px 24px',
  borderRadius: '8px',
  textDecoration: 'none',
  border: '1px solid #d1d5db',
};
```

---

# CLAUDE CODE PROMPT

```
Create all email templates for Covered AI using React Email.

Install dependencies:
npm install @react-email/components resend

Create these files:

src/emails/invoice/invoice-sent.tsx
src/emails/invoice/reminder-1.tsx
src/emails/invoice/reminder-2.tsx
src/emails/invoice/final-notice.tsx
src/emails/invoice/receipt.tsx
src/emails/review/review-request.tsx
src/emails/reports/weekly-summary.tsx
src/emails/onboarding/welcome.tsx
src/emails/calls/missed-callback.tsx

Use the exact templates from /specs/13-EMAIL-TEMPLATES.md

Create a shared styles file:
src/emails/styles.ts

Export all common styles (main, container, heading, paragraph, button, etc.)

Then import in each template:
import { main, container, heading, ... } from '../styles';
```
