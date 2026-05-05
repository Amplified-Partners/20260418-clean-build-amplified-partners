---
title: "Technical Decisions - Melanin Design Platform"
id: "technical-decisions"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "tech-decision"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Technical Decisions - Melanin Design Platform

## Confirmed Technology Stack

### Backend
- **Runtime**: Node.js with Express
- **Language**: TypeScript
- **Database**: PostgreSQL
- **ORM**: Prisma
- **Authentication**: JWT with bcryptjs for password hashing
- **API Architecture**: RESTful with Express

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS with custom melanin color palette
- **State Management**: Zustand
- **Data Fetching**: React Query
- **Canvas Library**: **Fabric.js** - Mature, proven for design tools
- **Routing**: React Router

### AI Integration
- **Service**: **OpenAI DALL-E 3**
  - Cost: $0.04-0.12 per image
  - Quality: Highest available
  - API: Official OpenAI API
  - Prompt tokens included in generation cost

### Authentication Strategy
- **Method**: **Email/Password with JWT tokens**
  - Simple, traditional auth flow
  - JWT stored in httpOnly cookies or localStorage
  - Refresh token rotation for security
  - Password requirements: min 8 chars, complexity rules

### Deployment (Future)
- **Backend**: Railway or Render
- **Frontend**: Vercel
- **Database**: Supabase or Railway PostgreSQL
- **Image Storage**: AWS S3 or Cloudflare R2
- **CDN**: Cloudflare

## Implementation Priorities

1. **Phase 1**: Foundation ✅ (Complete)
2. **Phase 2**: Authentication & Core API (Next)
3. **Phase 3**: Design Canvas with Fabric.js
4. **Phase 4**: AI Integration (DALL-E 3)
5. **Phase 5**: Learning System
6. **Phase 6**: Export & Deployment

## Key Integration Points

### DALL-E 3 Integration
```typescript
// Prompt structure for melanin-focused designs
interface DesignPrompt {
  style: string[];           // "modern", "traditional", "abstract"
  colors: string[];          // Melanin-focused color palette
  themes: string[];          // "celebration", "daily-life", etc.
  culturalElements: string[]; // "geometric-patterns", "natural-textures"
  productType: string;       // "mug", "t-shirt", "poster", etc.
}
```

### Fabric.js Canvas Structure
- Interactive canvas for element manipulation
- Drag-and-drop functionality
- Layer management
- Export to various formats
- Real-time preview

### Authentication Flow
1. User registers with email/password
2. Password hashed with bcryptjs (10 rounds)
3. JWT token generated on login
4. Token validated on protected routes
5. Refresh token for extended sessions