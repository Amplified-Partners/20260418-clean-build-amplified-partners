-- CreateEnum
CREATE TYPE "Vertical" AS ENUM ('trades', 'vet', 'dental', 'aesthetics', 'salon', 'physio', 'optometry', 'auto', 'legal', 'accountant', 'fitness');

-- CreateEnum
CREATE TYPE "SubscriptionPlan" AS ENUM ('starter', 'growth', 'scale');

-- CreateEnum
CREATE TYPE "SubscriptionStatus" AS ENUM ('trial', 'active', 'past_due', 'cancelled', 'paused');

-- CreateEnum
CREATE TYPE "LeadStatus" AS ENUM ('new', 'contacted', 'nurturing', 'qualified', 'booked', 'converted', 'dismissed', 'lost');

-- CreateEnum
CREATE TYPE "Urgency" AS ENUM ('emergency', 'urgent', 'routine');

-- CreateEnum
CREATE TYPE "JobStatus" AS ENUM ('scheduled', 'confirmed', 'in_progress', 'completed', 'cancelled', 'no_show');

-- CreateEnum
CREATE TYPE "NotificationChannel" AS ENUM ('email', 'sms', 'whatsapp');

-- CreateEnum
CREATE TYPE "NotificationStatus" AS ENUM ('pending', 'sent', 'delivered', 'failed');

-- CreateEnum
CREATE TYPE "NurtureStatus" AS ENUM ('active', 'paused', 'completed', 'stopped');

-- CreateTable
CREATE TABLE "clients" (
    "id" TEXT NOT NULL,
    "business_name" TEXT NOT NULL,
    "owner_name" TEXT NOT NULL,
    "phone" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "address" TEXT,
    "postcode" TEXT,
    "website" TEXT,
    "covered_number" TEXT,
    "vapi_assistant_id" TEXT,
    "google_place_id" TEXT,
    "vertical" "Vertical" NOT NULL DEFAULT 'trades',
    "subscription_plan" "SubscriptionPlan" NOT NULL DEFAULT 'starter',
    "subscription_status" "SubscriptionStatus" NOT NULL DEFAULT 'trial',
    "stripe_customer_id" TEXT,
    "trial_ends_at" TIMESTAMP(3),
    "notification_phone" TEXT,
    "notification_email" TEXT,
    "notify_via_whatsapp" BOOLEAN NOT NULL DEFAULT true,
    "notify_via_sms" BOOLEAN NOT NULL DEFAULT false,
    "notify_via_email" BOOLEAN NOT NULL DEFAULT true,
    "crm_type" TEXT,
    "crm_sheet_id" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "clients_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "customers" (
    "id" TEXT NOT NULL,
    "client_id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "phone" TEXT NOT NULL,
    "email" TEXT,
    "address" TEXT,
    "postcode" TEXT,
    "source" TEXT,
    "tags" TEXT[] DEFAULT ARRAY[]::TEXT[],
    "notes" TEXT,
    "crm_customer_id" TEXT,
    "crm_synced_at" TIMESTAMP(3),
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "customers_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "leads" (
    "id" TEXT NOT NULL,
    "client_id" TEXT NOT NULL,
    "customer_id" TEXT,
    "call_id" TEXT,
    "caller_phone" TEXT NOT NULL,
    "call_duration" INTEGER,
    "recording_url" TEXT,
    "transcript" TEXT,
    "summary" TEXT,
    "customer_name" TEXT,
    "address" TEXT,
    "postcode" TEXT,
    "job_type" TEXT,
    "urgency" "Urgency" NOT NULL DEFAULT 'routine',
    "status" "LeadStatus" NOT NULL DEFAULT 'new',
    "qualified_at" TIMESTAMP(3),
    "booked_at" TIMESTAMP(3),
    "converted_at" TIMESTAMP(3),
    "dismissed_at" TIMESTAMP(3),
    "dismiss_reason" TEXT,
    "nurture_sequence_id" TEXT,
    "crm_lead_id" TEXT,
    "crm_deep_link" TEXT,
    "crm_pushed_at" TIMESTAMP(3),
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "leads_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "jobs" (
    "id" TEXT NOT NULL,
    "client_id" TEXT NOT NULL,
    "customer_id" TEXT NOT NULL,
    "lead_id" TEXT,
    "title" TEXT NOT NULL,
    "description" TEXT,
    "job_type" TEXT,
    "address" TEXT NOT NULL,
    "postcode" TEXT,
    "scheduled_date" TIMESTAMP(3) NOT NULL,
    "scheduled_time" TEXT,
    "estimated_duration" INTEGER,
    "assigned_to" TEXT,
    "status" "JobStatus" NOT NULL DEFAULT 'scheduled',
    "confirmed_at" TIMESTAMP(3),
    "started_at" TIMESTAMP(3),
    "completed_at" TIMESTAMP(3),
    "cancelled_at" TIMESTAMP(3),
    "cancel_reason" TEXT,
    "quoted_amount" DECIMAL(10,2),
    "final_amount" DECIMAL(10,2),
    "paid_at" TIMESTAMP(3),
    "review_requested" BOOLEAN NOT NULL DEFAULT false,
    "review_requested_at" TIMESTAMP(3),
    "review_received" BOOLEAN NOT NULL DEFAULT false,
    "review_rating" INTEGER,
    "crm_job_id" TEXT,
    "crm_synced_at" TIMESTAMP(3),
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "jobs_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "nurture_sequences" (
    "id" TEXT NOT NULL,
    "lead_id" TEXT NOT NULL,
    "current_touch" INTEGER NOT NULL DEFAULT 0,
    "status" "NurtureStatus" NOT NULL DEFAULT 'active',
    "touch_1_sent_at" TIMESTAMP(3),
    "touch_2_sent_at" TIMESTAMP(3),
    "touch_3_sent_at" TIMESTAMP(3),
    "touch_4_sent_at" TIMESTAMP(3),
    "touch_5_sent_at" TIMESTAMP(3),
    "touch_5_video_url" TEXT,
    "touch_6_sent_at" TIMESTAMP(3),
    "touch_7_sent_at" TIMESTAMP(3),
    "touch_8_sent_at" TIMESTAMP(3),
    "touch_9_sent_at" TIMESTAMP(3),
    "touch_10_sent_at" TIMESTAMP(3),
    "touch_11_sent_at" TIMESTAMP(3),
    "touch_12_sent_at" TIMESTAMP(3),
    "next_touch_at" TIMESTAMP(3),
    "next_touch_number" INTEGER,
    "completed_at" TIMESTAMP(3),
    "stopped_at" TIMESTAMP(3),
    "stop_reason" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "nurture_sequences_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "notifications" (
    "id" TEXT NOT NULL,
    "client_id" TEXT NOT NULL,
    "lead_id" TEXT,
    "job_id" TEXT,
    "type" TEXT NOT NULL,
    "channel" "NotificationChannel" NOT NULL,
    "recipient" TEXT NOT NULL,
    "subject" TEXT,
    "message" TEXT NOT NULL,
    "status" "NotificationStatus" NOT NULL DEFAULT 'pending',
    "sent_at" TIMESTAMP(3),
    "delivered_at" TIMESTAMP(3),
    "failed_at" TIMESTAMP(3),
    "error" TEXT,
    "external_id" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "notifications_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "video_generations" (
    "id" TEXT NOT NULL,
    "lead_id" TEXT NOT NULL,
    "heygen_video_id" TEXT,
    "template_id" TEXT NOT NULL,
    "variables" JSONB NOT NULL,
    "status" TEXT NOT NULL DEFAULT 'pending',
    "video_url" TEXT,
    "thumbnail_url" TEXT,
    "duration" INTEGER,
    "requested_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "completed_at" TIMESTAMP(3),
    "failed_at" TIMESTAMP(3),
    "error" TEXT,

    CONSTRAINT "video_generations_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "customers_client_id_idx" ON "customers"("client_id");

-- CreateIndex
CREATE INDEX "customers_phone_idx" ON "customers"("phone");

-- CreateIndex
CREATE UNIQUE INDEX "customers_client_id_phone_key" ON "customers"("client_id", "phone");

-- CreateIndex
CREATE INDEX "leads_client_id_idx" ON "leads"("client_id");

-- CreateIndex
CREATE INDEX "leads_customer_id_idx" ON "leads"("customer_id");

-- CreateIndex
CREATE INDEX "leads_status_idx" ON "leads"("status");

-- CreateIndex
CREATE INDEX "leads_created_at_idx" ON "leads"("created_at");

-- CreateIndex
CREATE UNIQUE INDEX "jobs_lead_id_key" ON "jobs"("lead_id");

-- CreateIndex
CREATE INDEX "jobs_client_id_idx" ON "jobs"("client_id");

-- CreateIndex
CREATE INDEX "jobs_customer_id_idx" ON "jobs"("customer_id");

-- CreateIndex
CREATE INDEX "jobs_status_idx" ON "jobs"("status");

-- CreateIndex
CREATE INDEX "jobs_scheduled_date_idx" ON "jobs"("scheduled_date");

-- CreateIndex
CREATE UNIQUE INDEX "nurture_sequences_lead_id_key" ON "nurture_sequences"("lead_id");

-- CreateIndex
CREATE INDEX "nurture_sequences_status_idx" ON "nurture_sequences"("status");

-- CreateIndex
CREATE INDEX "nurture_sequences_next_touch_at_idx" ON "nurture_sequences"("next_touch_at");

-- CreateIndex
CREATE INDEX "notifications_client_id_idx" ON "notifications"("client_id");

-- CreateIndex
CREATE INDEX "notifications_lead_id_idx" ON "notifications"("lead_id");

-- CreateIndex
CREATE INDEX "notifications_type_idx" ON "notifications"("type");

-- CreateIndex
CREATE INDEX "notifications_created_at_idx" ON "notifications"("created_at");

-- CreateIndex
CREATE INDEX "video_generations_lead_id_idx" ON "video_generations"("lead_id");

-- CreateIndex
CREATE INDEX "video_generations_status_idx" ON "video_generations"("status");

-- AddForeignKey
ALTER TABLE "customers" ADD CONSTRAINT "customers_client_id_fkey" FOREIGN KEY ("client_id") REFERENCES "clients"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "leads" ADD CONSTRAINT "leads_client_id_fkey" FOREIGN KEY ("client_id") REFERENCES "clients"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "leads" ADD CONSTRAINT "leads_customer_id_fkey" FOREIGN KEY ("customer_id") REFERENCES "customers"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "leads" ADD CONSTRAINT "leads_nurture_sequence_id_fkey" FOREIGN KEY ("nurture_sequence_id") REFERENCES "nurture_sequences"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "jobs" ADD CONSTRAINT "jobs_client_id_fkey" FOREIGN KEY ("client_id") REFERENCES "clients"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "jobs" ADD CONSTRAINT "jobs_customer_id_fkey" FOREIGN KEY ("customer_id") REFERENCES "customers"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "jobs" ADD CONSTRAINT "jobs_lead_id_fkey" FOREIGN KEY ("lead_id") REFERENCES "leads"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "notifications" ADD CONSTRAINT "notifications_client_id_fkey" FOREIGN KEY ("client_id") REFERENCES "clients"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "notifications" ADD CONSTRAINT "notifications_lead_id_fkey" FOREIGN KEY ("lead_id") REFERENCES "leads"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "notifications" ADD CONSTRAINT "notifications_job_id_fkey" FOREIGN KEY ("job_id") REFERENCES "jobs"("id") ON DELETE SET NULL ON UPDATE CASCADE;
