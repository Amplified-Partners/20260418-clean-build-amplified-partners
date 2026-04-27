import { defineConfig } from "@trigger.dev/sdk/v3";

export default defineConfig({
  // Production project ID: d7f5f3ee-e04e-4559-bbe4-a97c75d87ce0
  project: "proj_mzlahtbhkhkroxbcabis",
  logLevel: "log",
  maxDuration: 300, // 5 minutes max for nurture sequence processing
  retries: {
    enabledInDev: true,
    default: {
      maxAttempts: 3,
      minTimeoutInMs: 1000,
      maxTimeoutInMs: 10000,
      factor: 2,
      randomize: true,
    },
  },
  dirs: ["./trigger-jobs"],
});
