# Customer Tracking & CRM Workflow

Simple customer relationship management for UMKM and freelancers.

## Overview

Track customer interactions, purchase history, and engagement without expensive CRM software.

**Tools Used:**
- Google Sheets (data storage)
- WhatsApp Business (communication)
- Notion (workflow management)
- Python scripts (automation)

## Customer Data Structure

### Essential Fields

**Basic Info:**
- Customer ID (auto-generated)
- Name
- Phone Number (WhatsApp)
- Email
- Location/City

**Engagement:**
- First Contact Date
- Last Contact Date
- Total Interactions
- Response Rate (%)
- Preferred Channel (WhatsApp/Email)

**Business:**
- Customer Type (New/Returning/VIP)
- Total Purchases
- Total Revenue
- Average Order Value
- Last Purchase Date
- Lifetime Value (LTV)

**Status:**
- Active/Inactive
- Tags (Custom labels)
- Notes
- Next Follow-up Date

## Tracking Workflow

### Stage 1: First Contact

**When customer reaches out:**
1. Log basic info (name, phone, inquiry)
2. Assign Customer ID
3. Record inquiry type
4. Set follow-up reminder (24h)

**Template Response:**
```
Hi [Name]! Thanks for reaching out.
I've noted your inquiry about [topic].
Let me get back to you with details shortly!
```

### Stage 2: Qualification

**Determine customer priority:**
- Hot Lead (ready to buy)
- Warm Lead (interested, needs nurturing)
- Cold Lead (just browsing)

**Actions:**
- Hot → Immediate response + proposal
- Warm → Add to nurture sequence
- Cold → Add to newsletter list

### Stage 3: Engagement

**Track all interactions:**
- WhatsApp messages (in/out)
- Calls made
- Emails sent
- Meetings scheduled

**Engagement Score:**
```
Score = (Messages Replied / Messages Sent) × 100
High Engagement: >70%
Medium: 40-70%
Low: <40%
```

### Stage 4: Conversion

**When sale is made:**
1. Update customer type (New → Returning)
2. Log purchase details
3. Calculate LTV
4. Set post-purchase follow-up (7 days)

### Stage 5: Retention

**Keep customers engaged:**
- Monthly check-ins (personalized)
- Special offers (birthdays, anniversaries)
- Feedback requests (after purchase)
- Reactivation campaigns (inactive >60 days)

## Automation Scripts

### Track WhatsApp Interactions
```python
import csv
from datetime import datetime

class CustomerTracker:
    def __init__(self, csv_file='customers.csv'):
        self.csv_file = csv_file
    
    def log_interaction(self, phone, name, message_type, notes=''):
        """Log customer interaction"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        interaction = {
            'timestamp': timestamp,
            'phone': phone,
            'name': name,
            'type': message_type,  # incoming/outgoing
            'notes': notes
        }
        
        # Append to CSV
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=interaction.keys())
            writer.writerow(interaction)
        
        return interaction
    
    def get_customer_history(self, phone):
        """Get all interactions for a customer"""
        history = []
        
        with open(self.csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['phone'] == phone:
                    history.append(row)
        
        return history
    
    def calculate_engagement(self, phone):
        """Calculate customer engagement rate"""
        history = self.get_customer_history(phone)
        
        if not history:
            return 0
        
        outgoing = sum(1 for h in history if h['type'] == 'outgoing')
        incoming = sum(1 for h in history if h['type'] == 'incoming')
        
        if outgoing == 0:
            return 0
        
        engagement_rate = (incoming / outgoing) * 100
        return round(engagement_rate, 2)

# Usage
tracker = CustomerTracker()
tracker.log_interaction('+6281234567890', 'John Doe', 'incoming', 'Inquiry about pricing')
engagement = tracker.calculate_engagement('+6281234567890')
print(f"Engagement Rate: {engagement}%")
```

### Auto Follow-up Reminder
```python
from datetime import datetime, timedelta

def check_followup_due(customers_list):
    """Check which customers need follow-up today"""
    today = datetime.now().date()
    due_followups = []
    
    for customer in customers_list:
        followup_date = customer.get('next_followup')
        
        if followup_date and followup_date <= today:
            due_followups.append({
                'name': customer['name'],
                'phone': customer['phone'],
                'last_contact': customer['last_contact'],
                'notes': customer['notes']
            })
    
    return due_followups

def set_next_followup(days=7):
    """Set next follow-up date"""
    next_date = datetime.now().date() + timedelta(days=days)
    return next_date

# Example usage
customers = [
    {
        'name': 'Jane Smith',
        'phone': '+6281234567891',
        'next_followup': datetime.now().date(),
        'last_contact': '2026-03-01',
        'notes': 'Interested in subscription service'
    }
]

due_today = check_followup_due(customers)
for customer in due_today:
    print(f"📞 Follow-up: {customer['name']} - {customer['notes']}")
```

## Google Sheets Integration

### Setup Spreadsheet

**Sheet 1: Customers**
| Customer ID | Name | Phone | Email | Type | Status | LTV | Last Contact | Next Followup |
|------------|------|-------|-------|------|--------|-----|--------------|---------------|

**Sheet 2: Interactions**
| Date | Customer ID | Type | Channel | Notes | Response Time |
|------|-------------|------|---------|-------|---------------|

**Sheet 3: Revenue**
| Date | Customer ID | Product/Service | Amount | Status |
|------|-------------|-----------------|--------|--------|

### Auto-sync Script
```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def sync_to_sheets(customer_data):
    """Sync customer data to Google Sheets"""
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'credentials.json', scope)
    client = gspread.authorize(creds)
    
    # Open spreadsheet
    sheet = client.open('Customer Tracker').sheet1
    
    # Append new row
    row = [
        customer_data['id'],
        customer_data['name'],
        customer_data['phone'],
        customer_data['email'],
        customer_data['type'],
        customer_data['status']
    ]
    
    sheet.append_row(row)
    return True
```

## Segmentation Strategy

### Customer Segments

**VIP Customers:**
- LTV > Rp 10,000,000
- Purchase frequency: Monthly
- Engagement rate: >80%
- Action: Priority support, exclusive offers

**Loyal Customers:**
- 3+ purchases
- Active in last 30 days
- Engagement rate: >60%
- Action: Loyalty rewards, early access

**At-Risk Customers:**
- No purchase in 60+ days
- Declining engagement
- Action: Reactivation campaign, special discount

**New Customers:**
- First purchase within 30 days
- Action: Onboarding sequence, gather feedback

## Metrics to Track

### Key Performance Indicators

**Customer Acquisition:**
- New customers/month
- Cost per acquisition
- Source breakdown (WhatsApp/Email/Referral)

**Engagement:**
- Average response time
- Message open rate
- Interaction frequency

**Revenue:**
- Monthly recurring revenue (MRR)
- Customer lifetime value (LTV)
- Average order value (AOV)
- Repeat purchase rate

**Retention:**
- Churn rate (monthly)
- Customer retention rate
- Reactivation success rate

## Best Practices

### Daily Tasks
- [ ] Check new inquiries (morning)
- [ ] Review follow-up list
- [ ] Log all interactions
- [ ] Respond within 2 hours (business hours)

### Weekly Tasks
- [ ] Update customer statuses
- [ ] Review engagement scores
- [ ] Identify at-risk customers
- [ ] Plan reactivation campaigns

### Monthly Tasks
- [ ] Calculate LTV for all customers
- [ ] Segment review and adjustment
- [ ] Revenue analysis by segment
- [ ] Strategy optimization

## Templates

### Reactivation Message
```
Hi [Name]! 

We haven't heard from you in a while and wanted to check in.

We've added some new [products/services] that might interest you.

As a valued customer, here's a special 15% discount code: WELCOME15

Valid until [date]. Looking forward to serving you again!
```

### Post-Purchase Follow-up
```
Hi [Name]!

Thanks for your recent purchase of [product/service]!

How's everything going? Any questions or feedback?

We're here to help anytime. Reply to this message or call us directly.

PS: Refer a friend and both get 10% off your next order!
```

## Tools & Resources

**Free Tools:**
- Google Sheets (data storage)
- Google Forms (feedback collection)
- WhatsApp Business (communication)

**Automation:**
- Zapier (connect apps)
- IFTTT (simple workflows)
- Python scripts (custom automation)

**Analytics:**
- Google Data Studio (dashboard)
- Excel/Sheets pivot tables
- Customer cohort analysis

## Next Steps

1. Set up tracking spreadsheet
2. Define your customer segments
3. Create automation scripts
4. Implement follow-up system
5. Track metrics monthly
6. Optimize based on data

---

**Updated:** March 2026
```

---

**COMMIT MESSAGE:**
```
Complete customer tracking workflow - add missing sections
