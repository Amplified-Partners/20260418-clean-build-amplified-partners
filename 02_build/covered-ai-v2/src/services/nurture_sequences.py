"""
Lead Nurture Email Sequences (Tier 3)

Automated email sequences for leads who aren't ready to sign up yet.
"""

import os
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from enum import Enum

try:
    import resend
    RESEND_AVAILABLE = True
except ImportError:
    RESEND_AVAILABLE = False


RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "Ewan from Covered AI <ewan@covered.ai>")


class SequenceType(str, Enum):
    DEMO_FOLLOWUP = "demo_followup"  # After they've had a demo
    COLD_INTRO = "cold_intro"        # Cold outreach
    REENGAGEMENT = "reengagement"    # Went quiet


# Email sequences - day offset and template
SEQUENCES = {
    SequenceType.DEMO_FOLLOWUP: [
        {"day": 0, "template": "demo_thanks"},
        {"day": 2, "template": "demo_value_reminder"},
        {"day": 5, "template": "demo_social_proof"},
        {"day": 10, "template": "demo_last_chance"},
    ],
    SequenceType.COLD_INTRO: [
        {"day": 0, "template": "cold_intro"},
        {"day": 3, "template": "cold_pain_point"},
        {"day": 7, "template": "cold_social_proof"},
        {"day": 14, "template": "cold_final"},
    ],
    SequenceType.REENGAGEMENT: [
        {"day": 0, "template": "reengage_check_in"},
        {"day": 7, "template": "reengage_new_feature"},
        {"day": 21, "template": "reengage_last_try"},
    ],
}


# Email templates
TEMPLATES = {
    # Demo followup sequence
    "demo_thanks": {
        "subject": "Good chatting, {first_name}",
        "body": """
Hi {first_name},

Thanks for taking the time to chat with me about Covered AI.

Quick recap: Gemma answers your phone 24/7, captures every lead, and triages emergencies — so you never miss a job again.

Ready to get started? Just reply to this email and I'll set you up in 10 minutes.

Cheers,
Ewan

P.S. You can call 0800 COVERED anytime to hear Gemma in action.
"""
    },
    
    "demo_value_reminder": {
        "subject": "Quick question",
        "body": """
{first_name},

Just wondering — how many calls do you reckon you miss each week?

Most {vertical}s I talk to say it's somewhere between 5-10. At an average job value of £{avg_job_value}, that's potentially £{missed_revenue} walking out the door.

Gemma catches those calls. Every single one.

Worth a quick 10-minute setup? Reply and I'll sort it.

Ewan
"""
    },
    
    "demo_social_proof": {
        "subject": "How Ralph's plumbing business changed",
        "body": """
{first_name},

Quick story:

Ralph runs a plumbing business in Newcastle. Before Covered, he was missing calls while on jobs, losing maybe £2-3k a month in work he never even knew about.

Three weeks with Gemma:
- 47 calls answered
- 12 emergency jobs he would have missed
- £4,200 in extra revenue

His words: "I actually sleep now. Knowing Gemma's got the phone."

Want the same? Reply and we'll get you set up today.

Ewan
"""
    },
    
    "demo_last_chance": {
        "subject": "Final check-in",
        "body": """
{first_name},

I'll keep this short.

If Covered AI isn't right for you, no worries at all. I won't keep emailing.

But if there's anything holding you back — questions, concerns, "I'm just busy" — just reply and let me know. Happy to help.

Either way, best of luck with the business.

Ewan

P.S. If you ever want to pick this up again, just call 0800 COVERED. We'll be here.
"""
    },
    
    # Cold intro sequence
    "cold_intro": {
        "subject": "Missed calls = missed money",
        "body": """
Hi {first_name},

I'm Ewan. I built an AI receptionist called Gemma specifically for {vertical}s like you.

She answers your phone 24/7, captures every caller's details, and forwards emergencies to you immediately.

No more missed calls. No more voicemails. No more "sorry, we tried calling but..."

Call 0800 COVERED right now and she'll answer. It's a demo that takes 30 seconds.

Ewan
Covered AI
"""
    },
    
    "cold_pain_point": {
        "subject": "What happens to the calls you miss?",
        "body": """
{first_name},

Here's a question that might sting a bit:

When a customer calls and you can't answer — while you're on a job, at dinner, asleep — where does that call go?

Voicemail? They hang up and call your competitor.
Ring out? Same thing.

Every missed call is someone who needed you, couldn't reach you, and went elsewhere.

Gemma catches those calls. All of them. 24/7.

£297/month. One missed job pays for it.

Reply if you want to see how it works.

Ewan
"""
    },
    
    "cold_social_proof": {
        "subject": "12 emergency jobs in 3 weeks",
        "body": """
{first_name},

Ralph's a plumber in Newcastle. Started using Gemma three weeks ago.

In that time:
- 47 calls answered
- 12 emergency jobs captured (that he would have missed)
- £4,200 in extra revenue

His quote: "I was losing jobs I didn't even know existed."

You're probably in the same boat. We all are.

Want to plug the leak? Call 0800 COVERED to hear Gemma, or reply and I'll set you up.

Ewan
"""
    },
    
    "cold_final": {
        "subject": "Last one from me",
        "body": """
{first_name},

Last email, I promise.

If now's not the right time, I get it. Running a {vertical} business is busy.

But if you ever want an AI to answer your phone — professional, 24/7, never misses a call — Covered AI will be here.

Call 0800 COVERED anytime to hear Gemma in action.

Good luck with everything.

Ewan
"""
    },
    
    # Reengagement sequence
    "reengage_check_in": {
        "subject": "Been a while, {first_name}",
        "body": """
{first_name},

Hope business is going well!

You looked at Covered AI a while back. Just checking in — still struggling with missed calls?

We've made some improvements since then:
- Faster setup (now takes 5 minutes)
- Better emergency detection
- SMS notifications

If you want to give it another look, just reply. Happy to walk you through what's new.

Ewan
"""
    },
    
    "reengage_new_feature": {
        "subject": "New feature you might like",
        "body": """
{first_name},

Quick update: we just added automatic Google review requests.

After Gemma handles a call and you complete the job, she can automatically send the customer a review request. Hands-free 5-star reviews.

Thought you might find that useful.

Reply if you want to see how it works.

Ewan
"""
    },
    
    "reengage_last_try": {
        "subject": "Still there?",
        "body": """
{first_name},

Just a final check-in.

If Covered AI isn't for you, no problem at all. I'll stop emailing.

But if there's anything I can help with — questions, concerns, whatever — just reply.

Either way, wishing you all the best with the business.

Ewan
"""
    },
}


def _send_email(to: str, subject: str, body: str) -> bool:
    """Send plain text email via Resend."""
    if not RESEND_AVAILABLE or not RESEND_API_KEY:
        print(f"[EMAIL MOCK] To: {to}, Subject: {subject}")
        return True
    
    try:
        resend.api_key = RESEND_API_KEY
        resend.Emails.send({
            "from": FROM_EMAIL,
            "to": to,
            "subject": subject,
            "text": body,
        })
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def render_template(
    template_key: str,
    first_name: str,
    vertical: str = "business",
    avg_job_value: int = 200,
    **kwargs
) -> tuple[str, str]:
    """Render an email template with variables."""
    template = TEMPLATES.get(template_key)
    if not template:
        raise ValueError(f"Template {template_key} not found")
    
    # Calculate missed revenue (5 calls/week * 4 weeks * avg job value)
    missed_revenue = 5 * 4 * avg_job_value
    
    context = {
        "first_name": first_name,
        "vertical": vertical,
        "avg_job_value": avg_job_value,
        "missed_revenue": f"{missed_revenue:,}",
        **kwargs,
    }
    
    subject = template["subject"].format(**context)
    body = template["body"].strip().format(**context)
    
    return subject, body


def send_sequence_email(
    to_email: str,
    template_key: str,
    first_name: str,
    vertical: str = "business",
    avg_job_value: int = 200,
    **kwargs
) -> bool:
    """Send a specific email from a sequence."""
    subject, body = render_template(
        template_key=template_key,
        first_name=first_name,
        vertical=vertical,
        avg_job_value=avg_job_value,
        **kwargs
    )
    
    return _send_email(to_email, subject, body)


def get_sequence_schedule(
    sequence_type: SequenceType,
    start_date: datetime = None
) -> List[Dict[str, Any]]:
    """Get the email schedule for a sequence."""
    if start_date is None:
        start_date = datetime.utcnow()
    
    sequence = SEQUENCES.get(sequence_type, [])
    schedule = []
    
    for item in sequence:
        send_date = start_date + timedelta(days=item["day"])
        schedule.append({
            "template": item["template"],
            "day": item["day"],
            "send_date": send_date.isoformat(),
            "send_date_display": send_date.strftime("%a %d %b"),
        })
    
    return schedule


# Lead storage (in-memory, replace with database)
_leads: Dict[str, Dict[str, Any]] = {}


def add_to_sequence(
    email: str,
    first_name: str,
    sequence_type: SequenceType,
    vertical: str = "business",
    avg_job_value: int = 200,
    metadata: Dict[str, Any] = None,
) -> str:
    """Add a lead to an email sequence."""
    import uuid
    
    lead_id = str(uuid.uuid4())[:8]
    
    _leads[lead_id] = {
        "id": lead_id,
        "email": email,
        "first_name": first_name,
        "sequence_type": sequence_type.value,
        "vertical": vertical,
        "avg_job_value": avg_job_value,
        "metadata": metadata or {},
        "created_at": datetime.utcnow().isoformat(),
        "current_step": 0,
        "status": "active",
        "emails_sent": [],
    }
    
    # Send first email immediately
    sequence = SEQUENCES.get(sequence_type, [])
    if sequence and sequence[0]["day"] == 0:
        template_key = sequence[0]["template"]
        success = send_sequence_email(
            to_email=email,
            template_key=template_key,
            first_name=first_name,
            vertical=vertical,
            avg_job_value=avg_job_value,
        )
        if success:
            _leads[lead_id]["emails_sent"].append({
                "template": template_key,
                "sent_at": datetime.utcnow().isoformat(),
            })
            _leads[lead_id]["current_step"] = 1
    
    return lead_id


def stop_sequence(lead_id: str, reason: str = "unsubscribed") -> bool:
    """Stop a sequence for a lead."""
    if lead_id in _leads:
        _leads[lead_id]["status"] = "stopped"
        _leads[lead_id]["stopped_reason"] = reason
        _leads[lead_id]["stopped_at"] = datetime.utcnow().isoformat()
        return True
    return False


def get_lead(lead_id: str) -> Optional[Dict[str, Any]]:
    """Get lead by ID."""
    return _leads.get(lead_id)


def list_leads(status: str = None) -> List[Dict[str, Any]]:
    """List all leads, optionally filtered by status."""
    leads = list(_leads.values())
    if status:
        leads = [l for l in leads if l["status"] == status]
    return sorted(leads, key=lambda x: x["created_at"], reverse=True)
