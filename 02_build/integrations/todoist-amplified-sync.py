#!/usr/bin/env python3
"""
Todoist Sync for Amplified Partners
Coordinates 3 Claude instances + Clawd + Ewan

All agents see what everyone's doing. No duplicate work.
"""

import os
import sys
from todoist_api_python.api import TodoistAPI
from datetime import datetime

def load_token():
    """Load Todoist API token"""
    token_file = os.path.expanduser('~/.openclaw/workspace/.todoist-token')
    if not os.path.exists(token_file):
        print(f"❌ Todoist token not found at {token_file}")
        print("Create token at: Settings → Integrations → Developer")
        print(f"Save it to: {token_file}")
        sys.exit(1)

    with open(token_file, 'r') as f:
        return f.read().strip()

def get_or_create_projects(api):
    """Get or create Amplified Partners project structure"""

    all_projects = api.get_projects()

    # Find or create main workspace
    workspace = None
    for proj in all_projects:
        if proj.name == "Amplified Partners":
            workspace = proj
            break

    if not workspace:
        workspace = api.add_project(name="Amplified Partners")
        print(f"✅ Created workspace: Amplified Partners")

    # Agent projects we need
    agent_names = ['Claude-A', 'Claude-B', 'Claude-C', 'Clawd', 'Ewan']
    agent_projects = {}

    for agent_name in agent_names:
        found = False
        for proj in all_projects:
            if proj.name == agent_name and proj.parent_id == workspace.id:
                agent_projects[agent_name] = proj
                found = True
                break

        if not found:
            agent_projects[agent_name] = api.add_project(
                name=agent_name,
                parent_id=workspace.id
            )
            print(f"✅ Created project: {agent_name}")

    return workspace, agent_projects

def display_all_tasks(api, projects):
    """Display all tasks for all agents"""

    print("\n" + "="*80)
    print("AMPLIFIED PARTNERS - COORDINATION BOARD")
    print("="*80 + "\n")

    for agent_name, project in projects.items():
        print(f"\n## {agent_name.upper()}")
        print("-" * 40)

        tasks = api.get_tasks(project_id=project.id)

        if not tasks:
            print("  No tasks")
            continue

        # Group by status
        active = [t for t in tasks if not t.is_completed]
        completed = [t for t in tasks if t.is_completed]

        if active:
            print("  🔥 ACTIVE:")
            for task in active:
                priority_emoji = {4: "‼️", 3: "❗", 2: "❕", 1: ""}
                emoji = priority_emoji.get(task.priority, "")
                print(f"     {emoji} {task.content}")
                if task.description:
                    print(f"        💬 {task.description}")

        if completed:
            print(f"  ✅ COMPLETED TODAY: {len(completed)} tasks")

    print("\n" + "="*80 + "\n")

def add_task(api, projects, agent_name, content, description=None, priority=1):
    """Add a task for a specific agent"""

    if agent_name not in projects:
        print(f"❌ Unknown agent: {agent_name}")
        print(f"Available: {', '.join(projects.keys())}")
        return None

    project = projects[agent_name]

    task = api.add_task(
        content=content,
        project_id=project.id,
        description=description,
        priority=priority
    )

    print(f"✅ Task added for {agent_name}: {content}")
    return task

def complete_task(api, task_id):
    """Mark a task as complete"""
    try:
        api.close_task(task_id=task_id)
        print(f"✅ Task completed: {task_id}")
        return True
    except Exception as e:
        print(f"❌ Error completing task: {e}")
        return False

def sync_status():
    """Main sync - display all tasks"""
    try:
        api = TodoistAPI(load_token())
        workspace, projects = get_or_create_projects(api)
        display_all_tasks(api, projects)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description='Todoist sync for Amplified Partners')
    parser.add_argument('--status', action='store_true', help='Show all tasks')
    parser.add_argument('--add', type=str, help='Add task (format: agent:content)')
    parser.add_argument('--complete', type=str, help='Complete task by ID')
    parser.add_argument('--priority', type=int, default=1, choices=[1,2,3,4],
                       help='Priority (1=low, 4=urgent)')
    parser.add_argument('--description', type=str, help='Task description')

    args = parser.parse_args()

    api = TodoistAPI(load_token())
    workspace, projects = get_or_create_projects(api)

    if args.add:
        if ':' not in args.add:
            print("❌ Format: agent:content (e.g., Claude-A:Build landing page)")
            sys.exit(1)

        agent, content = args.add.split(':', 1)
        add_task(api, projects, agent, content, args.description, args.priority)
        print("\n")
        display_all_tasks(api, projects)

    elif args.complete:
        complete_task(api, args.complete)

    else:
        # Default: show status
        display_all_tasks(api, projects)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No args: show status
        sync_status()
    else:
        main()
