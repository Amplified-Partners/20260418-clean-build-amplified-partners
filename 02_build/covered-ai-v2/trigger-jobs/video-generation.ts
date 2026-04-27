/**
 * Covered AI - Video Generation Job
 * 
 * Generates personalized videos via HeyGen API.
 * Used by the nurture sequence for Touch 5.
 */

import { task } from "@trigger.dev/sdk/v3";

interface VideoRequest {
  leadId: string;
  customerName: string;
  businessName: string;
  vertical: string;
  templateId?: string;
}

interface VideoResult {
  videoId: string;
  videoUrl: string;
  thumbnailUrl: string;
  duration: number;
}

// HeyGen API configuration
const HEYGEN_API_URL = "https://api.heygen.com/v2";
const HEYGEN_API_KEY = process.env.HEYGEN_API_KEY;

// Template mapping by vertical
const TEMPLATES: Record<string, string> = {
  trades: "YOUR_TRADES_TEMPLATE_ID",
  vet: "YOUR_MEDICAL_TEMPLATE_ID",
  dental: "YOUR_MEDICAL_TEMPLATE_ID",
  aesthetics: "YOUR_BEAUTY_TEMPLATE_ID",
  salon: "YOUR_BEAUTY_TEMPLATE_ID",
  default: "YOUR_GENERIC_TEMPLATE_ID",
};

export const generateVideoJob = task({
  id: "generate-video",
  retry: {
    maxAttempts: 2,
  },
  run: async (payload: VideoRequest): Promise<VideoResult> => {
    const { leadId, customerName, businessName, vertical, templateId } = payload;
    
    console.log(`🎬 Generating video for ${customerName}`);
    
    const template = templateId || TEMPLATES[vertical] || TEMPLATES.default;
    
    // 1. Create video via HeyGen API
    const createResponse = await fetch(`${HEYGEN_API_URL}/video/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Api-Key": HEYGEN_API_KEY!,
      },
      body: JSON.stringify({
        video_inputs: [
          {
            character: {
              type: "avatar",
              avatar_id: template,
            },
            voice: {
              type: "text",
              input_text: generateScript(customerName, businessName, vertical),
            },
          },
        ],
        dimension: {
          width: 1280,
          height: 720,
        },
      }),
    });
    
    if (!createResponse.ok) {
      const error = await createResponse.text();
      throw new Error(`HeyGen API error: ${error}`);
    }
    
    const createData = await createResponse.json();
    const videoId = createData.data.video_id;
    
    console.log(`   Video ID: ${videoId}`);
    
    // 2. Poll for completion
    let attempts = 0;
    const maxAttempts = 60; // 5 minutes max
    
    while (attempts < maxAttempts) {
      await new Promise(resolve => setTimeout(resolve, 5000)); // Wait 5 seconds
      
      const statusResponse = await fetch(`${HEYGEN_API_URL}/video_status.get?video_id=${videoId}`, {
        headers: {
          "X-Api-Key": HEYGEN_API_KEY!,
        },
      });
      
      const statusData = await statusResponse.json();
      const status = statusData.data.status;
      
      console.log(`   Status: ${status}`);
      
      if (status === "completed") {
        const result: VideoResult = {
          videoId,
          videoUrl: statusData.data.video_url,
          thumbnailUrl: statusData.data.thumbnail_url,
          duration: statusData.data.duration,
        };
        
        // Save to database
        await saveVideoGeneration(leadId, result);
        
        console.log(`✅ Video ready: ${result.videoUrl}`);
        return result;
      }
      
      if (status === "failed") {
        throw new Error(`Video generation failed: ${statusData.data.error}`);
      }
      
      attempts++;
    }
    
    throw new Error("Video generation timed out");
  },
});

function generateScript(customerName: string, businessName: string, vertical: string): string {
  const scripts: Record<string, string> = {
    trades: `Hi ${customerName}! Thanks for reaching out to ${businessName}. 
We know how frustrating it can be when something breaks down at home. 
That's why we're here to help - 24/7, whenever you need us.
Our team is ready to get your issue sorted quickly and professionally.
Looking forward to helping you out!`,
    
    vet: `Hello ${customerName}! Thank you for contacting ${businessName}.
We understand how important your pet's health is to you.
Our team of caring professionals is here to provide the best possible care.
We'll be in touch soon to discuss how we can help your furry family member.`,
    
    dental: `Hi ${customerName}! Thanks for getting in touch with ${businessName}.
We know visiting the dentist can sometimes feel daunting, but we're here to make it as comfortable as possible.
Our friendly team is dedicated to giving you the best care in a relaxed environment.
We look forward to seeing you soon!`,
    
    aesthetics: `Hello ${customerName}! Thank you for your enquiry to ${businessName}.
We're passionate about helping you look and feel your absolute best.
Our expert team will work with you to achieve natural, beautiful results.
Can't wait to welcome you for your consultation!`,
    
    salon: `Hi ${customerName}! Thanks for reaching out to ${businessName}.
We love helping our clients look and feel amazing.
Our talented team is ready to give you an experience you'll love.
Looking forward to seeing you in the salon soon!`,
    
    default: `Hi ${customerName}! Thank you for contacting ${businessName}.
We really appreciate you reaching out to us.
Our team is dedicated to providing excellent service and we're here to help.
We'll be in touch very soon to discuss how we can assist you.`,
  };
  
  return scripts[vertical] || scripts.default;
}

async function saveVideoGeneration(leadId: string, result: VideoResult): Promise<void> {
  const API_URL = process.env.API_URL || "http://localhost:8000";
  
  // TODO: Save to video_generations table via API
  console.log(`   Saved video generation for lead ${leadId}`);
}
