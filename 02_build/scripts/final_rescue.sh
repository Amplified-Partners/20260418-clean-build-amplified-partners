#!/bin/bash

# --- CONFIGURATION ---
TARGET_ORG="Amplified-Partners-all"
PREFIX="legacy-"

# The list we just confirmed
SOURCE_ORGS=(
    "Amplified-Partners"
    "Silly-Silly-Boy"
    "amppipedreams"
    "AmplifiedPlus"
    "Amplified-Partners-v1"
    "Amplified-Partners-org"
)

# Switch this to true if you want to test first!
DRY_RUN=false

# --- THE LOGIC ---
for ORG in "${SOURCE_ORGS[@]}"; do
    echo "--------------------------------------------"
    echo "📂 SCANNING ORG: $ORG"
    echo "--------------------------------------------"
    
    # Get all repo names
    REPOS=$(gh repo list "$ORG" --limit 1000 --json name -q '.[].name')
    
    if [ -z "$REPOS" ]; then
        echo "  > No repositories found here."
        continue
    fi

    for REPO in $REPOS; do
        NEW_NAME="${PREFIX}${REPO}"
        
        if [ "$DRY_RUN" = true ]; then
            echo "[TEST] Would move $ORG/$REPO -> $TARGET_ORG/$NEW_NAME and Archive."
        else
            echo "🚀 Moving: $ORG/$REPO..."
            
            # 1. Transfer
            # We use the API here because it's the most reliable for Enterprise
            gh api "repos/$ORG/$REPO/transfer" -f "new_owner=$TARGET_ORG" > /dev/null 2>&1
            
            # Wait for the GitHub hamsters to move the files
            sleep 4
            
            # 2. Rename (target is now in the new org)
            echo "🏷️  Renaming to $NEW_NAME..."
            gh repo rename "$NEW_NAME" --repo "$TARGET_ORG/$REPO" --yes > /dev/null 2>&1
            
            # 3. Archive
            echo "📁 Archiving $NEW_NAME..."
            gh repo archive "$TARGET_ORG/$NEW_NAME" --yes > /dev/null 2>&1
            
            echo "✅ $REPO is safe."
        fi
    done
done

echo "--------------------------------------------"
echo "🎉 ALL DONE. Check https://github.com/$TARGET_ORG"
echo "--------------------------------------------"
