# TOFU Multi-Touch Conversation Strategy
# Progressive engagement based on TOFU principles

def get_tofu_conversation_flow(self, message, session, engagement_strategy):
    """TOFU-based conversation flow management"""
    
    flows = {
        'awareness': {
            'touch_1': "I'd love to help you understand warehouse management solutions! Are you currently facing any specific challenges with inventory accuracy, order processing speed, or warehouse efficiency?",
            'touch_2': "Many businesses struggle with warehouse optimization. PALMS™ helps companies achieve 99.9% inventory accuracy and 40% faster operations. What's your biggest warehouse pain point?",
            'touch_3': "Based on our conversation, it sounds like you're exploring options. Would it be helpful if I shared some success stories from businesses similar to yours?"
        },
        'nurture_cold': {
            'touch_1': "Great questions! Let me share how PALMS™ specifically addresses those challenges with real measurable results...",
            'touch_2': "I can see you're evaluating your options carefully. Here's how we compare to other solutions in the market...",
            'touch_3': "Based on your requirements, I'd like to show you some relevant case studies. What industry are you in?"
        },
        'nurture_warm': {
            'touch_1': "Excellent - you clearly understand the value of a robust WMS. Let me provide specific ROI calculations for businesses like yours...",
            'touch_2': "Your questions show you're serious about implementation. Would you like to see a customized demo showing how PALMS™ handles your specific requirements?",
            'touch_3': "I can tell you're ready to move forward. Let's schedule a personalized consultation to map out your implementation timeline and ROI projections."
        },
        'direct_sales': {
            'touch_1': "Perfect! Based on your needs and timeline, PALMS™ is exactly what you're looking for. I'd like to connect you with our senior solutions consultant for a detailed demo.",
            'touch_2': "Your requirements align perfectly with our enterprise solutions. Let's schedule a technical deep-dive session with our implementation team.",
            'touch_3': "I can see you're ready to make a decision. Let me arrange a call with our sales director to discuss pricing and implementation timeline."
        }
    }
    
    touch_count = session.get('touch_count', 0) + 1
    session['touch_count'] = touch_count
    
    # Select appropriate response based on engagement strategy and touch count
    if engagement_strategy in flows:
        touch_key = f'touch_{min(touch_count, 3)}'
        return flows[engagement_strategy].get(touch_key, flows[engagement_strategy]['touch_3'])
    
    return None

# Enhanced Question Types for Better Qualification
def get_qualifying_questions(self, engagement_strategy, session):
    """Smart qualifying questions based on TOFU stage"""
    
    questions = {
        'awareness': [
            "What brings you to explore warehouse management solutions today?",
            "Are you currently using any WMS or still managing inventory manually?",
            "What's your biggest warehouse challenge right now?"
        ],
        'nurture_cold': [
            "What's your current warehouse size and daily order volume?",
            "How are you handling inventory accuracy issues currently?",
            "What's your timeline for implementing a new system?"
        ],
        'nurture_warm': [
            "Who else is involved in this decision-making process?",
            "What's your budget range for a WMS implementation?",
            "When would you ideally like to go live with a new system?"
        ],
        'direct_sales': [
            "Would you like to schedule a demo for next week?",
            "Who would be the key stakeholders for this decision?",
            "What's your procurement process for software purchases?"
        ]
    }
    
    return questions.get(engagement_strategy, questions['awareness'])
