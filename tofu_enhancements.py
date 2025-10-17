# Enhanced TOFU Lead Qualification System
# Add to chat.py

def enhanced_lead_qualification(self, message, session):
    """Enhanced TOFU-based lead qualification"""
    message_lower = message.lower()
    current_score = session.get('lead_score', 0)
    
    # TOFU Qualification Criteria
    qualification_signals = {
        'intent_signals': {
            'high': ['need solution', 'looking for', 'evaluating', 'budget approved', 'decision maker', 'procurement'],
            'medium': ['interested in', 'want to know', 'considering', 'exploring options'],
            'low': ['just curious', 'browsing', 'maybe later', 'just looking']
        },
        'authority_signals': {
            'high': ['ceo', 'cto', 'warehouse manager', 'operations director', 'procurement manager'],
            'medium': ['supervisor', 'team lead', 'analyst', 'coordinator'],
            'low': ['intern', 'student', 'researcher']
        },
        'timeline_signals': {
            'urgent': ['asap', 'immediately', 'this quarter', 'next month'],
            'near_term': ['in 3 months', 'this year', 'soon'],
            'long_term': ['next year', 'future', 'someday']
        },
        'budget_signals': {
            'confirmed': ['budget approved', 'funds allocated', 'ready to purchase'],
            'exploring': ['budget planning', 'cost analysis', 'roi calculation'],
            'unclear': ['just researching', 'preliminary']
        }
    }
    
    # Calculate enhanced qualification score
    for category, signals in qualification_signals.items():
        for level, keywords in signals.items():
            for keyword in keywords:
                if keyword in message_lower:
                    if level == 'high' or level == 'urgent' or level == 'confirmed':
                        session['lead_score'] += 25
                        session['qualification_signals'] = session.get('qualification_signals', [])
                        session['qualification_signals'].append(f"{category}_{level}")
                    elif level == 'medium' or level == 'near_term' or level == 'exploring':
                        session['lead_score'] += 15
                    else:
                        session['lead_score'] += 5
    
    return session

def get_tofu_engagement_strategy(self, session):
    """Determine engagement strategy based on TOFU principles"""
    lead_score = session.get('lead_score', 0)
    signals = session.get('qualification_signals', [])
    
    if lead_score >= 75 or any('high' in signal for signal in signals):
        return 'direct_sales'  # Ready for demo/sales call
    elif lead_score >= 40:
        return 'nurture_warm'  # Provide detailed info, case studies
    elif lead_score >= 20:
        return 'nurture_cold'  # Educational content, build trust
    else:
        return 'awareness'     # Basic information, qualify further
