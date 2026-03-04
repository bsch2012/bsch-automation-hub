"""
WhatsApp Business Auto-Reply Template
Generic customer service automation for UMKM & freelancers
"""

import os
from datetime import datetime

class WhatsAppAutoReply:
    """
    Simple auto-reply system for WhatsApp Business API
    Handles common customer inquiries with template responses
    """
    
    def __init__(self):
        self.business_name = "Your Business Name"
        self.business_hours = "09:00-18:00"
        self.response_templates = self._load_templates()
    
    def _load_templates(self):
        """Load predefined response templates"""
        return {
            "greeting": {
                "triggers": ["hi", "hello", "halo", "hai"],
                "response": f"Hi! Welcome to {self.business_name}. How can we help you today?"
            },
            "hours": {
                "triggers": ["jam berapa", "buka kapan", "hours", "open"],
                "response": f"We're open {self.business_hours} daily. Outside these hours, send us a message and we'll respond ASAP!"
            },
            "pricing": {
                "triggers": ["harga", "price", "berapa", "cost"],
                "response": "Please share what you're interested in, and I'll send you our price list!"
            },
            "order_status": {
                "triggers": ["order", "pesanan", "status"],
                "response": "To check your order status, please share your order number (e.g., #12345)"
            },
            "contact": {
                "triggers": ["contact", "hubungi", "email", "phone"],
                "response": "You can reach us at:\n📧 Email: contact@yourbusiness.com\n📱 WhatsApp: This number\n🌐 Website: yourbusiness.com"
            },
            "thanks": {
                "triggers": ["thanks", "terima kasih", "thank you"],
                "response": "You're welcome! Let us know if you need anything else 😊"
            }
        }
    
    def detect_intent(self, message):
        """
        Detect customer intent from message
        Returns matching template or None
        """
        message_lower = message.lower()
        
        for intent, data in self.response_templates.items():
            for trigger in data["triggers"]:
                if trigger in message_lower:
                    return data["response"]
        
        return None
    
    def generate_response(self, incoming_message):
        """
        Generate appropriate response based on message
        """
        # Check for template match
        template_response = self.detect_intent(incoming_message)
        
        if template_response:
            return template_response
        
        # Default response if no match
        return self._default_response()
    
    def _default_response(self):
        """Fallback response when no template matches"""
        return (
            f"Thanks for your message! Our team will respond within 1 hour during business hours ({self.business_hours}).\n\n"
            "Common questions:\n"
            "• Business hours\n"
            "• Pricing info\n"
            "• Order status\n\n"
            "Type your question and we'll help you out!"
        )
    
    def log_interaction(self, phone_number, message, response):
        """Log customer interactions for analytics"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {phone_number}: {message} -> {response}\n"
        
        # In production: save to database or file
        print(log_entry)
        return log_entry


# Example Usage
if __name__ == "__main__":
    # Initialize bot
    bot = WhatsAppAutoReply()
    
    # Test scenarios
    test_messages = [
        "Hi there!",
        "Berapa harga produknya?",
        "Jam berapa buka?",
        "I want to check my order status",
        "Thank you!"
    ]
    
    print("=== WhatsApp Auto-Reply Test ===\n")
    for msg in test_messages:
        response = bot.generate_response(msg)
        print(f"Customer: {msg}")
        print(f"Bot: {response}\n")
