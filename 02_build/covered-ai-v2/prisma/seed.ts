/**
 * Covered AI - Database Seed
 * Seeds initial data including Ralph (Titan Plumbing)
 */

import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  console.log("🌱 Seeding database...");

  // Create Ralph - Titan Plumbing
  const ralph = await prisma.client.upsert({
    where: { id: "06d733ac-96e9-4455-970d-99cb3f5b9b8e" },
    update: {},
    create: {
      id: "06d733ac-96e9-4455-970d-99cb3f5b9b8e",
      businessName: "Titan Plumbing Solutions",
      ownerName: "Ralph",
      phone: "+447738676932",
      email: "ralph@titanplumbing.co.uk",
      address: "Cullercoats, North Tyneside",
      postcode: "NE30",
      website: "https://titan-plumbing.netlify.app",
      coveredNumber: "+441917432732",
      vapiAssistantId: "0630abf5-9bc3-4b54-b362-e212f1c133a0",
      googlePlaceId: "ChIJdd4hrwug2EcRmSrV3Vo6llI",
      vertical: "trades",
      subscriptionPlan: "starter",
      subscriptionStatus: "active",
      notificationPhone: "+447738676932",
      notificationEmail: "ewan@bykerbusinesshelp.ai",
      notifyViaWhatsapp: true,
      notifyViaSms: false,
      notifyViaEmail: true,
      crmType: "sheets",
    },
  });

  console.log(`✅ Created client: ${ralph.businessName}`);

  // Create Harriet - Facial Aesthetics (Pilot)
  const harriet = await prisma.client.upsert({
    where: { id: "harriet-aesthetics-001" },
    update: {},
    create: {
      id: "harriet-aesthetics-001",
      businessName: "Harriet Bramley Aesthetics",
      ownerName: "Harriet",
      phone: "+447980500161",
      email: "harriet@aesthetics.co.uk",
      address: "Newcastle upon Tyne",
      postcode: "NE1",
      vertical: "aesthetics",
      subscriptionPlan: "starter",
      subscriptionStatus: "trial",
      notificationEmail: "harriet@aesthetics.co.uk",
      notifyViaEmail: true,
    },
  });

  console.log(`✅ Created client: ${harriet.businessName}`);

  // Create Callum - Groundworks (Pilot)
  const callum = await prisma.client.upsert({
    where: { id: "callum-groundworks-001" },
    update: {},
    create: {
      id: "callum-groundworks-001",
      businessName: "Callum's Groundworks",
      ownerName: "Callum",
      phone: "+447000000000",
      email: "callum@groundworks.co.uk",
      address: "Newcastle upon Tyne",
      postcode: "NE1",
      vertical: "trades",
      subscriptionPlan: "starter",
      subscriptionStatus: "trial",
      notifyViaEmail: true,
    },
  });

  console.log(`✅ Created client: ${callum.businessName}`);

  console.log("\n🎉 Seeding complete!");
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
