/**
 * Covered AI - HeyGen MCP Server Tools
 *
 * AI video generation tools via HeyGen API.
 */

// HeyGen API base URL
const HEYGEN_API_BASE = "https://api.heygen.com";
const apiKey = process.env.HEYGEN_API_KEY;

if (!apiKey) {
  console.error("Warning: HEYGEN_API_KEY must be set");
}

// Types
export interface CreateVideoParams {
  templateId: string;
  variables: Record<string, string>;
  title?: string;
  test?: boolean; // Use test mode for development
}

export interface GetVideoStatusParams {
  videoId: string;
}

// Video template IDs by vertical
export const VIDEO_TEMPLATES: Record<string, string> = {
  trades: process.env.HEYGEN_TEMPLATE_TRADES || "trades-intro-v1",
  vet: process.env.HEYGEN_TEMPLATE_MEDICAL || "medical-intro-v1",
  dental: process.env.HEYGEN_TEMPLATE_MEDICAL || "medical-intro-v1",
  aesthetics: process.env.HEYGEN_TEMPLATE_BEAUTY || "beauty-intro-v1",
  salon: process.env.HEYGEN_TEMPLATE_BEAUTY || "beauty-intro-v1",
  physio: process.env.HEYGEN_TEMPLATE_MEDICAL || "medical-intro-v1",
  optometry: process.env.HEYGEN_TEMPLATE_MEDICAL || "medical-intro-v1",
  fitness: process.env.HEYGEN_TEMPLATE_FITNESS || "fitness-intro-v1",
  default: process.env.HEYGEN_TEMPLATE_DEFAULT || "generic-intro-v1",
};

// Helper for HeyGen API calls
async function heygenRequest(
  endpoint: string,
  method: "GET" | "POST" = "GET",
  body?: Record<string, any>
): Promise<any> {
  if (!apiKey) {
    throw new Error("HEYGEN_API_KEY not configured");
  }

  const url = `${HEYGEN_API_BASE}${endpoint}`;

  const options: RequestInit = {
    method,
    headers: {
      "X-Api-Key": apiKey,
      "Content-Type": "application/json",
    },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(url, options);

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`HeyGen API error (${response.status}): ${errorText}`);
  }

  return response.json();
}

// Tool implementations

export async function createVideo(params: CreateVideoParams) {
  const { templateId, variables, title, test = false } = params;

  // Create video from template
  const result = await heygenRequest("/v2/template/{template_id}/generate".replace("{template_id}", templateId), "POST", {
    test,
    title: title || `Covered AI Video - ${new Date().toISOString()}`,
    variables: Object.entries(variables).map(([key, value]) => ({
      name: key,
      type: "text",
      properties: {
        content: value,
      },
    })),
  });

  return {
    success: true,
    videoId: result.data?.video_id,
    status: "pending",
    message: "Video generation started",
  };
}

export async function getVideoStatus(params: GetVideoStatusParams) {
  const { videoId } = params;

  const result = await heygenRequest(`/v1/video_status.get?video_id=${videoId}`);

  const data = result.data || {};

  return {
    videoId,
    status: data.status, // pending, processing, completed, failed
    videoUrl: data.video_url,
    thumbnailUrl: data.thumbnail_url,
    duration: data.duration,
    gifUrl: data.gif_url,
    error: data.error,
  };
}

export async function getVideoUrl(videoId: string) {
  const status = await getVideoStatus({ videoId });

  if (status.status !== "completed") {
    throw new Error(`Video not ready. Current status: ${status.status}`);
  }

  return {
    videoId,
    videoUrl: status.videoUrl,
    thumbnailUrl: status.thumbnailUrl,
    duration: status.duration,
  };
}

export async function listTemplates() {
  const result = await heygenRequest("/v2/templates");

  const templates =
    result.data?.templates?.map((t: any) => ({
      id: t.template_id,
      name: t.name,
      thumbnail: t.thumbnail_url,
    })) || [];

  return {
    templates,
    count: templates.length,
  };
}

export async function getTemplateDetails(templateId: string) {
  const result = await heygenRequest(`/v2/template/${templateId}`);

  const data = result.data || {};

  return {
    id: data.template_id,
    name: data.name,
    thumbnail: data.thumbnail_url,
    variables: data.variables?.map((v: any) => ({
      name: v.name,
      type: v.type,
    })),
  };
}

export async function listAvatars() {
  const result = await heygenRequest("/v2/avatars");

  const avatars =
    result.data?.avatars?.map((a: any) => ({
      id: a.avatar_id,
      name: a.avatar_name,
      gender: a.gender,
      preview: a.preview_image_url,
    })) || [];

  return {
    avatars,
    count: avatars.length,
  };
}

export async function listVoices() {
  const result = await heygenRequest("/v2/voices");

  const voices =
    result.data?.voices?.map((v: any) => ({
      id: v.voice_id,
      name: v.display_name,
      language: v.language,
      gender: v.gender,
      preview: v.preview_audio,
    })) || [];

  return {
    voices,
    count: voices.length,
  };
}

// Create video with text-to-speech (alternative to template)
export async function createTalkingAvatarVideo(params: {
  avatarId: string;
  voiceId: string;
  script: string;
  title?: string;
  test?: boolean;
}) {
  const { avatarId, voiceId, script, title, test = false } = params;

  const result = await heygenRequest("/v2/video/generate", "POST", {
    test,
    title: title || `Covered AI Video - ${new Date().toISOString()}`,
    video_inputs: [
      {
        character: {
          type: "avatar",
          avatar_id: avatarId,
          avatar_style: "normal",
        },
        voice: {
          type: "text",
          input_text: script,
          voice_id: voiceId,
        },
      },
    ],
  });

  return {
    success: true,
    videoId: result.data?.video_id,
    status: "pending",
    message: "Video generation started",
  };
}

// Poll for video completion (useful for Trigger.dev jobs)
export async function waitForVideo(videoId: string, maxWaitMs: number = 180000) {
  const startTime = Date.now();
  const pollIntervalMs = 5000; // 5 seconds

  while (Date.now() - startTime < maxWaitMs) {
    const status = await getVideoStatus({ videoId });

    if (status.status === "completed") {
      return {
        success: true,
        videoId,
        videoUrl: status.videoUrl,
        thumbnailUrl: status.thumbnailUrl,
        duration: status.duration,
      };
    }

    if (status.status === "failed") {
      throw new Error(`Video generation failed: ${status.error}`);
    }

    // Wait before next poll
    await new Promise((resolve) => setTimeout(resolve, pollIntervalMs));
  }

  throw new Error(`Video generation timed out after ${maxWaitMs}ms`);
}

// Helper to get template ID for a vertical
export function getTemplateForVertical(vertical: string): string {
  return VIDEO_TEMPLATES[vertical] || VIDEO_TEMPLATES.default;
}
