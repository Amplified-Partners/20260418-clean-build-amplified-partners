---
title: "GitHub API Notes"
id: "github-api-notes"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "2026-04-17-githubapi.txt"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

#!/bin/bash

GH_USER="ewan-dot"
GH_TOKEN="PASTE_YOUR_TOKEN_HERE" # Only needed for API authentication

API_URL="https://api.github.com/user/repos?per_page=100&type=owner"

curl -s -u "$GH_USER:$GH_TOKEN" "$API_URL" |
  grep -o '"ssh_url": *"[^"]*"' |
  sed 's/"ssh_url": "//;s/"$//' |
  while read repo; do
    echo "Cloning $repo ..."
    git clone "$repo"
  done

echo "Done!"