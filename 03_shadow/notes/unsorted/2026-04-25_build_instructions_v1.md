---
title: "Today Mirror - Build Instructions"
id: "build_instructions"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Today Mirror - Build Instructions

## Prerequisites

1. **macOS 13.0+** (Ventura or later)
2. **Xcode 15.0+** with Command Line Tools
3. **Ollama** with local models installed
4. **Obsidian** (optional, for markdown mirror)

## Quick Start

### 1. Install Ollama and Models

```bash
# Install Ollama
brew install ollama

# Start Ollama service
ollama serve &

# Pull the models (this will take some time - models are large)
ollama pull qwen2.5-coder:14b
ollama pull qwen2.5:14b
ollama pull llama3.2:3b
```

### 2. Create Xcode Project

Since Xcode project files are complex binary/XML files, you'll need to create the project in Xcode:

```bash
cd today-mirror
```

**In Xcode:**
1. Open Xcode
2. File → New → Project
3. Choose "macOS" → "App"
4. Product Name: `TodayMirror`
5. Interface: SwiftUI
6. Language: Swift
7. Save in the `today-mirror` directory (it will create TodayMirror.xcodeproj)

### 3. Add Source Files to Project

In Xcode:
1. Right-click on "TodayMirror" folder in Project Navigator
2. Add Files to "TodayMirror"...
3. Select all the folders:
   - Models/
   - ViewModels/
   - Views/
   - Services/
4. Make sure "Copy items if needed" is UNCHECKED (files are already in place)
5. Make sure "Create groups" is selected
6. Click "Add"

### 4. Configure Project Settings

In Xcode Project Settings:
1. Select TodayMirror target
2. General tab:
   - Minimum Deployments: macOS 13.0
   - Bundle Identifier: com.yourdomain.TodayMirror
3. Signing & Capabilities:
   - Team: Select your Apple Developer account (or use "Sign to Run Locally")

### 5. Build and Run

```bash
# In Xcode: Cmd+R to build and run
# Or from command line:
xcodebuild -project TodayMirror.xcodeproj -scheme TodayMirror -configuration Debug build
```

## Alternative: Command Line Setup

If you prefer command line, here's a script to create the Xcode project:

```bash
#!/bin/bash
# create-xcode-project.sh

cd today-mirror

# Create Xcode project using swift package
swift package init --type executable --name TodayMirror

# Or use xcodegen (install with: brew install xcodegen)
# Create project.yml first, then run: xcodegen generate
```

## Configuration

### First Launch

On first launch, the app will create:
- `~/.today-mirror/config.json` - Configuration file
- `~/.today-mirror/data/` - Data storage directory

### Configure Obsidian (Optional)

1. Create an Obsidian vault (or use existing)
2. Edit `~/.today-mirror/config.json`:
```json
{
  "obsidianVaultPath": "/Users/YOUR_USERNAME/Documents/Obsidian/TodayMirror",
  "llmEndpoint": "http://localhost:11434/api/generate",
  "llmModel": "qwen2.5-coder:14b",
  "defaultMode": "balance",
  "theme": "light"
}
```

## Troubleshooting

### Ollama Not Running
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it:
ollama serve
```

### Build Errors

**"Cannot find type 'Task' in scope"**
- Make sure all source files are added to the Xcode target
- Check that files are in the correct groups

**"Module compiled with Swift X.X cannot be imported"**
- Clean build folder: Cmd+Shift+K
- Rebuild: Cmd+B

### Runtime Errors

**"Failed to connect to LLM"**
- Ensure Ollama is running: `ollama serve`
- Check endpoint in config.json
- Try the fallback: app will use dummy responses

**"Permission denied" for file operations**
- Check that ~/.today-mirror directory exists
- Verify write permissions

## File Structure

```
today-mirror/
├── TodayMirror.xcodeproj/     # Xcode project (you create this)
├── TodayMirror/
│   ├── TodayMirrorApp.swift   # App entry point
│   ├── Models/                # Data models
│   ├── ViewModels/            # Business logic
│   ├── Views/                 # UI components
│   ├── Services/              # Infrastructure
│   └── Info.plist            # App metadata
├── SPEC.md                    # Complete specification
├── IMPLEMENTATION_PLAN.md     # Detailed build plan
├── ARCHITECTURE.md            # System design
└── README.md                  # Project summary
```

## Testing

### Manual Testing
1. Launch app
2. Add 3 tasks manually
3. Mark one as done
4. Verify micro-win animation
5. Check JSON files in ~/.today-mirror/data/
6. Generate daily summary
7. Check Obsidian markdown files (if configured)

### Verify LLM Integration
1. Type something in "What's on your mind?"
2. Click Send
3. Should see suggested tasks (or fallback message if Ollama offline)

## Next Steps

After successful build:
1. Test all three modes (Money-First, Balance, Recovery)
2. Test mode validation (try adding 4th task)
3. Test LLM integration with Ollama
4. Configure Obsidian vault
5. Generate daily summary
6. Review JSON and markdown files

## Support

If you encounter issues:
1. Check Ollama is running: `ollama list`
2. Verify models are installed: `ollama list`
3. Check logs in Xcode console
4. Review ~/.today-mirror/data/ files

## Performance Notes

Your M4 MacBook Air with 24GB RAM is excellent for this app:
- Local LLM models will run fast
- qwen2.5-coder:14b should respond in 2-5 seconds
- App memory usage: ~100-200MB
- Ollama memory usage: ~8-10GB (for 14B models)

Enjoy using Today Mirror!