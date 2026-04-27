"""
TickTick Integration
====================
Create tasks via TickTick API.

API Docs: https://developer.ticktick.com/api
"""

import os
import httpx
from datetime import datetime, timedelta
from typing import Optional
import re


class TickTickClient:
    """
    TickTick API client for task management.
    """
    
    BASE_URL = "https://api.ticktick.com/open/v1"
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        self._projects = None
    
    async def get_projects(self) -> list:
        """Get all projects/lists."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/project",
                headers=self.headers
            )
            response.raise_for_status()
            self._projects = response.json()
            return self._projects
    
    async def get_default_project_id(self) -> str:
        """Get the Inbox project ID."""
        if not self._projects:
            await self.get_projects()
        
        # Find inbox or first project
        for project in self._projects:
            if project.get("name", "").lower() == "inbox":
                return project["id"]
        
        # Fallback to first project
        if self._projects:
            return self._projects[0]["id"]
        
        return None
    
    async def create_task(
        self,
        title: str,
        due_date: Optional[datetime] = None,
        priority: int = 0,  # 0=none, 1=low, 3=medium, 5=high
        project_id: Optional[str] = None,
        content: Optional[str] = None
    ) -> dict:
        """
        Create a new task in TickTick.
        
        Args:
            title: Task title
            due_date: Optional due date
            priority: 0 (none), 1 (low), 3 (medium), 5 (high)
            project_id: Project/list ID (defaults to Inbox)
            content: Optional task description
        
        Returns:
            Created task data
        """
        if not project_id:
            project_id = await self.get_default_project_id()
        
        task_data = {
            "title": title,
            "projectId": project_id,
            "priority": priority
        }
        
        if due_date:
            task_data["dueDate"] = due_date.strftime("%Y-%m-%dT%H:%M:%S+0000")
        
        if content:
            task_data["content"] = content
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/task",
                headers=self.headers,
                json=task_data
            )
            response.raise_for_status()
            return response.json()


def parse_due_date(text: str) -> Optional[datetime]:
    """
    Parse natural language due dates.
    
    Handles:
    - today, tomorrow
    - monday, tuesday, etc.
    - in X days/hours
    - next week
    """
    text = text.lower().strip()
    now = datetime.now()
    
    # Today/tomorrow
    if "today" in text:
        return now.replace(hour=17, minute=0, second=0, microsecond=0)
    if "tomorrow" in text:
        return (now + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
    
    # Day of week
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for i, day in enumerate(days):
        if day in text:
            days_ahead = i - now.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return (now + timedelta(days=days_ahead)).replace(hour=9, minute=0, second=0, microsecond=0)
    
    # In X days
    match = re.search(r"in (\d+) day", text)
    if match:
        days = int(match.group(1))
        return (now + timedelta(days=days)).replace(hour=9, minute=0, second=0, microsecond=0)
    
    # In X hours
    match = re.search(r"in (\d+) hour", text)
    if match:
        hours = int(match.group(1))
        return now + timedelta(hours=hours)
    
    # Next week
    if "next week" in text:
        days_until_monday = (7 - now.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        return (now + timedelta(days=days_until_monday)).replace(hour=9, minute=0, second=0, microsecond=0)
    
    return None


def parse_priority(text: str) -> int:
    """Parse priority from text. Returns 0, 1, 3, or 5."""
    text = text.lower()
    
    if any(word in text for word in ["urgent", "asap", "critical", "high priority"]):
        return 5
    if any(word in text for word in ["important", "medium priority"]):
        return 3
    if any(word in text for word in ["low priority", "whenever", "eventually"]):
        return 1
    
    return 0
