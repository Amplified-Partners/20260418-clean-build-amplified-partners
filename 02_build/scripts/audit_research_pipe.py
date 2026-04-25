"""
Research Pipe Audit Logging
JSON trails for full traceability.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from config_research_pipe import get_config


class AuditTrail:
    """Manages audit trail logging for research runs."""
    
    def __init__(self):
        self.config = get_config()
        self.run_id = str(uuid.uuid4())
        self.entries = []
        self.timestamp_start = datetime.utcnow().isoformat()
    
    def log(self, stage: str, data: dict):
        """Append an entry to the audit trail."""
        entry = {
            "stage": stage,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        self.entries.append(entry)
    
    def save(self, question_slug: str = "research"):
        """Write audit trail to JSON file."""
        self.config.OUTPUT_AUDIT_TRAILS.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = self.config.OUTPUT_AUDIT_TRAILS / f"{timestamp}_{question_slug}.json"
        
        output = {
            "run_id": self.run_id,
            "timestamp_start": self.timestamp_start,
            "timestamp_end": datetime.utcnow().isoformat(),
            "entries": self.entries
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        return filename
