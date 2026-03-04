"""
WhatsApp Broadcast Message Template
Send bulk messages to customer segments with personalization

IMPORTANT: Always comply with WhatsApp Business API terms
- Get opt-in consent before sending
- Respect message frequency limits
- Provide opt-out option
"""

import time
from datetime import datetime
import csv

class BroadcastManager:
    """
    Manage broadcast campaigns to customer segments
    """
    
    def __init__(self, customer_file='customers.csv'):
        self.customer_file = customer_file
        self.customers = self._load_customers()
        self.sent_count = 0
        self.failed_count = 0
    
    def _load_customers(self):
        """Load customer list from CSV"""
        customers = []
        
        try:
            with open(self.customer_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    customers.append(row)
        except FileNotFoundError:
            print(f"Customer file not found: {self.customer_file}")
        
        return customers
    
    def segment_customers(self, segment_type):
        """
        Filter customers by segment
        
        segment_type options:
        - 'all': All customers
        - 'vip': High-value customers
        - 'active': Recently engaged
        - 'inactive': No contact in 60+ days
        - 'new': First purchase within 30 days
        """
        
        if segment_type == 'all':
            return self.customers
        
        elif segment_type == 'vip':
            # Example: LTV > 10000000
            return [c for c in self.customers 
                   if float(c.get('ltv', 0)) > 10000000]
        
        elif segment_type == 'active':
            # Example: Contacted within 30 days
            return [c for c in self.customers 
                   if c.get('status') == 'active']
        
        elif segment_type == 'inactive':
            # Example: No contact in 60+ days
            return [c for c in self.customers 
                   if c.get('status') == 'inactive']
        
        elif segment_type == 'new':
            # Example: Customer type = 'new'
            return [c for c in self.customers 
                   if c.get('type') == 'new']
        
        else:
            return []
    
    def personalize_message(self, template, customer):
        """
        Replace placeholders with customer data
        
        Placeholders:
        {name}, {phone}, {last_purchase}, {ltv}
        """
        message = template
        
        replacements = {
            '{name}': customer.get('name', 'Customer'),
            '{phone}': customer.get('phone', ''),
            '{last_purchase}': customer.get('last_purchase', 'N/A'),
            '{ltv}': customer.get('ltv', '0')
        }
        
        for placeholder, value in replacements.items():
            message = message.replace(placeholder, str(value))
        
        return message
    
    def send_broadcast(self, segment, template, delay=2):
        """
        Send broadcast message to segment
        
        Args:
            segment: Customer segment to target
            template: Message template with {placeholders}
            delay: Seconds between messages (avoid spam detection)
        """
        
        target_customers = self.segment_customers(segment)
        
        print(f"\n=== Broadcast Campaign ===")
        print(f"Segment: {segment}")
        print(f"Target: {len(target_customers)} customers")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        for customer in target_customers:
            try:
                # Personalize message
                message = self.personalize_message(template, customer)
                
                # Send message (replace with actual WhatsApp API call)
                success = self._send_message(
                    customer.get('phone'), 
                    message
                )
                
                if success:
                    self.sent_count += 1
                    print(f"✅ Sent to {customer.get('name')} ({customer.get('phone')})")
                else:
                    self.failed_count += 1
                    print(f"❌ Failed: {customer.get('name')}")
                
                # Delay between messages
                time.sleep(delay)
                
            except Exception as e:
                self.failed_count += 1
                print(f"❌ Error sending to {customer.get('name')}: {e}")
        
        # Campaign summary
        self._print_summary()
    
    def _send_message(self, phone, message):
        """
        Placeholder for actual WhatsApp API call
        
        Replace this with your WhatsApp Business API implementation
        Example using official API or services like Twilio, MessageBird
        """
        
        # DEMO MODE - Just print message
        print(f"\n--- Message to {phone} ---")
        print(message)
        print("--- End Message ---\n")
        
        # In production, implement actual API call:
        # response = whatsapp_api.send_message(phone, message)
        # return response.success
        
        return True  # Simulate success for demo
    
    def _print_summary(self):
        """Print campaign summary"""
        print("\n=== Campaign Summary ===")
        print(f"Total Sent: {self.sent_count}")
        print(f"Failed: {self.failed_count}")
        print(f"Success Rate: {(self.sent_count/(self.sent_count+self.failed_count)*100):.1f}%")
        print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# Message Templates

TEMPLATES = {
    'promotional': """
Hi {name}!

Special offer just for you! 🎉

Get 20% OFF all products this weekend only.
Use code: WEEKEND20

Shop now: [your-link]

Reply STOP to unsubscribe.
""",
    
    'reactivation': """
Hey {name},

We miss you! It's been a while since your last visit.

Here's 15% off to welcome you back.
Code: COMEBACK15

Valid for 7 days. Looking forward to serving you again!

Reply STOP to unsubscribe.
""",
    
    'product_launch': """
Hi {name}!

Exciting news! We just launched [New Product]

As a valued customer, you get early access + 10% discount.

Check it out: [your-link]

Limited stock available!

Reply STOP to unsubscribe.
""",
    
    'feedback': """
Hi {name},

How was your recent experience with us?

We'd love to hear your feedback! It takes just 1 minute:
[feedback-link]

Thank you for helping us improve!

Reply STOP to unsubscribe.
""",
    
    'event': """
Hi {name}!

You're invited to our [Event Name]!

📅 Date: [Date]
🕒 Time: [Time]
📍 Location: [Location]

RSVP: [link] or reply to this message

See you there!

Reply STOP to unsubscribe.
"""
}


# Example Usage

if __name__ == "__main__":
    # Initialize broadcast manager
    manager = BroadcastManager('customers.csv')
    
    # Example 1: Send promotional message to active customers
    print("\n### Campaign 1: Weekend Promotion ###")
    manager.send_broadcast(
        segment='active',
        template=TEMPLATES['promotional'],
        delay=2
    )
    
    # Example 2: Reactivation campaign for inactive customers
    print("\n### Campaign 2: Reactivation ###")
    manager.send_broadcast(
        segment='inactive',
        template=TEMPLATES['reactivation'],
        delay=3
    )
    
    # Example 3: Custom template
    print("\n### Campaign 3: Custom Message ###")
    custom_template = """
Hi {name}!

Just checking in. How can we serve you better?

Your feedback matters to us.

Reply to this message anytime!
"""
    
    manager.send_broadcast(
        segment='vip',
        template=custom_template,
        delay=2
    )


# IMPORTANT NOTES:
"""
1. Always get customer consent before broadcasting
2. Respect WhatsApp's message rate limits
3. Provide clear opt-out instructions
4. Track opt-outs and respect them
5. Personalize messages for better engagement
6. Test on small segment first
7. Monitor delivery rates and adjust
8. Comply with local data privacy laws (GDPR, etc.)
"""
