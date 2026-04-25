---
name: vault-monitor
description: Monitor Claude Code output, check vault health, and report on ingestion progress every 10 minutes
---

You are monitoring the Amplified Partners vault ingestion pipeline. Check three things and report concisely:

1. **Claude Code output**: Check ~/Downloads/_working/ and ~/Downloads/_master-docs/ for any new files Claude Code has produced. List any new or changed files since last check.

2. **FalkorDB ingestion**: SSH to Beast (ssh -i ~/.ssh/claude-code-beast-key root@135.181.161.131) and check:
   - Is the ingestion process still running? `ps aux | grep ingest_vault | grep -v grep`
   - How many files done? `tail -5 /opt/backups/agent-stack/graphiti-ingestion/ingestion_output_beast_r3.log`
   - Any errors? `grep -c "Failed\|Error\|timed out" /opt/backups/agent-stack/graphiti-ingestion/ingestion_output_beast_r3.log`

3. **Porch status**: Check if any files are in /opt/amplified-machine/porch/incoming/ on Beast. If there are, run: `cd /opt/amplified-machine/porch && python3 porch_watcher.py`

4. **Vault health**: Quick counts:
   - Qdrant: `curl -s http://localhost:6333/collections/amplified_knowledge | python3 -c 'import json,sys; print(json.load(sys.stdin).get("result",{}).get("points_count","unknown"))'`
   - FalkorDB: `docker exec falkordb redis-cli GRAPH.QUERY business_knowledge 'MATCH (n) RETURN count(n)'`

Report format: Keep it short. Numbers and status only. Flag anything that looks wrong.