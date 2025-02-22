test_emails = {
    "phishing": """
    Dear Valued Customer,
    
    Your account security has been compromised. Click here immediately to verify:
    http://fake-bank.com/verify
    
    If you don't respond within 24 hours, your account will be suspended.
    
    Best regards,
    Bank Security Team
    """,
    
    "legitimate": """
    Hi John,
    
    Just following up on our meeting from yesterday. I've attached the project timeline 
    we discussed. Let me know if you need any changes.
    
    Thanks,
    Sarah Johnson
    Marketing Director
    """,
    
    "suspicious": """
    URGENT: Your PayPal account needs attention!
    
    We've noticed unusual activity. Verify your information here:
    www.paypa1-secure.com
    
    Your account will be limited if you don't act now!
    """
}