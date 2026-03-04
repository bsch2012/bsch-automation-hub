# Notion Dashboard Automation

Client management & task tracking system for freelancers and UMKM.

## Dashboard Structure

### 1. Client Database

**Properties:**
- Name (Title)
- Status (Select: Active / On-hold / Completed)
- Contact (Email)
- WhatsApp (Phone)
- Project Type (Multi-select)
- Start Date (Date)
- Deadline (Date)
- Budget (Number)
- Notes (Text)

**Views:**
- Active Clients (Filter: Status = Active)
- By Deadline (Sort: Deadline ascending)
- High Priority (Filter: Budget > threshold)

### 2. Task Management

**Properties:**
- Task Name (Title)
- Client (Relation to Client DB)
- Status (Select: To Do / In Progress / Review / Done)
- Priority (Select: Low / Medium / High / Urgent)
- Due Date (Date)
- Assigned To (Person)
- Time Estimate (Number - hours)
- Actual Time (Number - hours)

**Views:**
- My Tasks (Filter: Assigned to Me, Status ≠ Done)
- This Week (Filter: Due Date = This Week)
- Overdue (Filter: Due Date < Today, Status ≠ Done)
- By Client (Group by: Client)

### 3. Revenue Tracking

**Properties:**
- Month (Date)
- Client (Relation)
- Service Type (Select)
- Amount (Number)
- Status (Select: Pending / Paid / Overdue)
- Invoice Number (Text)
- Payment Date (Date)

**Formulas:**
- Monthly Total: `sum(amount) where month = current_month`
- Pending Amount: `sum(amount) where status = Pending`

## Automation Ideas

### Google Sheets Integration

**Sync Flow:**
1. New client added to Notion
2. Auto-create row in Google Sheets
3. Track in spreadsheet for accounting
4. Sync back status updates

**Use Case:**
- Notion = Daily workflow
- Sheets = Financial reporting
- Auto-sync = No manual entry

### WhatsApp Notifications

**Triggers:**
- New client signed → WhatsApp notification
- Task deadline approaching → Reminder
- Payment received → Confirmation

**Implementation:**
- Notion API webhook
- WhatsApp Business API
- Automation script (Python/Node.js)

### Email Automation

**Auto-send:**
- Welcome email (new client)
- Invoice reminders (payment due)
- Project updates (milestone completed)

## Setup Guide

### 1. Create Notion Workspace
```
1. Go to notion.so
2. Create new page: "Business Dashboard"
3. Add database: "Clients"
4. Add database: "Tasks"
5. Add database: "Revenue"
```

### 2. Connect to API

**Get API Key:**
1. Notion Settings → Integrations
2. Create new integration
3. Copy API token

**Share Database:**
1. Open database
2. Share → Add integration
3. Select your integration

### 3. Basic Sync Script (Python)
```python
import requests
import os

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Query database
def get_clients():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers)
    return response.json()

# Add new client
def add_client(name, email, phone):
    url = "https://api.notion.com/v1/pages"
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": name}}]},
            "Contact": {"email": email},
            "WhatsApp": {"phone_number": phone},
            "Status": {"select": {"name": "Active"}}
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
```

## Templates

### Weekly Review Template
```
## Week of [Date]

### Completed This Week
- [ ] Client A - Project X
- [ ] Client B - Task Y

### In Progress
- [ ] Client C - Milestone 1
- [ ] Client D - Design Phase

### Next Week Priorities
1. [High Priority Task]
2. [Medium Priority Task]
3. [Low Priority Task]

### Revenue This Week
- Total Invoiced: Rp X
- Payments Received: Rp Y
- Outstanding: Rp Z
```

### Client Onboarding Checklist
```
## New Client: [Name]

### Setup
- [ ] Add to Client Database
- [ ] Create project folder
- [ ] Send welcome email
- [ ] Schedule kickoff call

### Documentation
- [ ] Contract signed
- [ ] Payment terms agreed
- [ ] Scope documented
- [ ] Timeline confirmed

### First Tasks
- [ ] Create initial task list
- [ ] Assign team members
- [ ] Set up communication channel
- [ ] Share project dashboard
```

## Best Practices

### Daily Workflow
1. **Morning:** Review "My Tasks" view
2. **Throughout day:** Update task status
3. **End of day:** Log time spent
4. **Weekly:** Client check-ins + revenue review

### Maintenance
- Archive completed projects monthly
- Review overdue tasks weekly
- Update client status regularly
- Backup database quarterly

## Resources

- [Notion API Docs](https://developers.notion.com)
- [Python Notion SDK](https://github.com/ramnes/notion-sdk-py)
- [Community Templates](https://notion.so/templates)

## Next Steps

1. Duplicate template to your Notion
2. Customize properties for your business
3. Add first 5 clients
4. Set up basic automation
5. Iterate based on usage

---

**Updated:** March 2026
