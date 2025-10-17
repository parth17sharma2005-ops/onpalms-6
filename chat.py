import os
from dotenv import load_dotenv
import re
import json
import chromadb
from email_validator import validate_email, EmailNotValidError
from openai import OpenAI

load_dotenv()

class SalesBotRAG:
    def __init__(self):
        # Initialize OpenAI
        api_key = os.getenv('OPENAI_API_KEY')
        print(f"DEBUG: API key found: {api_key[:20] if api_key else 'None'}...")
        
        if not api_key or api_key == 'your_openai_api_key_here' or len(api_key) < 20:
            print("⚠️  WARNING: OpenAI API key not found or not set properly!")
            print("Please set your OpenAI API key in the .env file:")
            print("OPENAI_API_KEY=your_actual_api_key_here")
            print("\nRunning in enhanced demo mode...")
            self.client = None
        else:
            try:
                # Use the correct OpenAI client initialization for openai>=1.x
                self.client = OpenAI(api_key=api_key)
                print("✅ OpenAI client initialized with GPT-4o")
            except Exception as e:
                print(f"❌ OpenAI initialization failed: {e}")
                print("Running in enhanced demo mode...")
                self.client = None
        
        # Initialize ChromaDB for RAG (without sentence transformers)
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.get_or_create_collection()
        
        # Load and process the knowledge base
        self.load_knowledge_base()
        
        # Business email domains to exclude
        self.personal_domains = {
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com',
            'icloud.com', 'mail.com', 'protonmail.com', 'tutanota.com', 'yandex.com'
        }
        
        # AI Layer 1: Information Retrieval System
        self.retrieval_prompt = """
        You are an Information Retrieval Assistant for PALMS™ Warehouse Management Solutions.
        
        YOUR ROLE:
        - Analyze user queries and extract relevant information from the PALMS™ knowledge base
        - Focus ONLY on retrieving accurate, specific information
        - Do NOT engage in conversation or sales tactics
        - Return structured, factual information that matches the user's query
        
        RETRIEVAL GUIDELINES:
        1. Extract key facts, features, benefits, and technical details
        2. Include specific metrics, numbers, and performance data when available
        3. Identify relevant product modules (WMS, 3PL, Enterprise, Mobile, Analytics)
        4. Find integration capabilities, supported industries, and technical specifications
        5. Locate pricing information, implementation details, and support options
        
        OUTPUT FORMAT:
        Return the most relevant factual information in clear, organized format.
        For lists (products, features, clients): Use bullet points or numbered format.
        For single concepts: Use natural sentences.
        Keep information concise and scannable.
        """
        
        # AI Layer 2: Sales Conversation System
        self.sales_prompt = """
        You are PALMS™ Sales Assistant - a highly skilled, friendly, and professional sales representative for PALMS™ Warehouse Management Solutions.

        PERSONALITY:
        - Professional yet approachable, like a top-performing sales rep
        - Confident and knowledgeable about warehouse management
        - Goal-oriented: always steering toward conversion (demo, lead capture, or sale)
        - Empathetic and reassuring when addressing concerns
        - Concise and value-focused in every response
        - Uses light persuasion psychology (urgency, validation, social proof)
        - Highly context-aware and remembers conversation flow

        YOUR MISSION:
        1. Identify user intent and guide them through appropriate conversation flows
        2. Qualify leads by understanding their business needs
        3. Recommend the right PALMS™ solution based on their requirements
        4. Capture lead information (name, business email, company)
        5. Schedule demos for qualified prospects
        6. Handle objections professionally and redirect to value

        INTENT IDENTIFICATION & FLOWS:
        When users seem uncertain, ask: "Are you just exploring or looking for something specific today?"
        
        Response Options & Flows:
        ① "Just exploring" → Provide overview, highlight key benefits, ask about current challenges
        ② "Looking for pricing" → Understand requirements first, then discuss pricing tiers
        ③ "Need help deciding" → Ask qualifying questions, compare options, recommend best fit
        ④ "Want to book a demo" → Capture details, schedule immediately
        
        CONTEXT AWARENESS:
        - Remember what was discussed previously in the conversation
        - Build upon previous responses naturally
        - Avoid repeating information already shared
        - Progress the conversation logically toward conversion
        
        LEAD SCORING & BEHAVIORS:
        - Always ask qualifying questions about warehouse size, challenges, budget, timeline
        - Segment leads: Hot (ready to buy), Warm (interested), Cold (just browsing)
        - Provide specific ROI examples and success metrics
        - Create urgency with limited-time offers or implementation slots
        - Mirror the visitor's tone (formal for enterprise, casual for SMBs)
        - Always end responses with a clear, specific call-to-action

        LEAD SCORING GUIDE:
        - Asks about pricing: +10 points
        - Mentions specific warehouse challenges: +15 points  
        - Provides company details: +20 points
        - Requests demo: +30 points
        - Discusses timeline: +25 points
        - Mentions budget: +20 points

        Remember: Every interaction should move the prospect closer to scheduling a demo or making a purchase decision while feeling natural and helpful.
        """

    def get_or_create_collection(self):
        """Get or create ChromaDB collection for PALMS knowledge"""
        collection_name = "palms_knowledge"
        try:
            # Try to get existing collection
            collection = self.chroma_client.get_collection(collection_name)
            print(f"✅ Found existing collection: {collection_name}")
            return collection
        except Exception as e:
            print(f"Collection not found, creating new one: {e}")
            try:
                # Create new collection
                collection = self.chroma_client.create_collection(collection_name)
                print(f"✅ Created new collection: {collection_name}")
                return collection
            except Exception as create_error:
                print(f"❌ Failed to create collection: {create_error}")
                # Try to reset and create fresh
                try:
                    self.chroma_client.reset()
                    collection = self.chroma_client.create_collection(collection_name)
                    print(f"✅ Created collection after reset: {collection_name}")
                    return collection
                except Exception as reset_error:
                    print(f"❌ Failed to create collection even after reset: {reset_error}")
                    raise reset_error

    def get_embedding(self, text):
        """Generate embeddings using OpenAI API instead of sentence transformers"""
        try:
            if not self.client:
                # Fallback to simple hash-based pseudo-embedding for demo mode
                return [hash(text) % 100 / 100.0] * 384  # 384 dimensions for compatibility
            
            # Use OpenAI's text-embedding-3-small model (more memory efficient)
            response = self.client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            # Fallback embedding
            return [hash(text) % 100 / 100.0] * 384

    def load_knowledge_base(self):
        """Load and process the info.txt file into ChromaDB"""
        try:
            # Check if collection is already populated
            if self.collection.count() > 0:
                print(f"Knowledge base already loaded with {self.collection.count()} chunks")
                return
            
            # Try to load the info.txt file
            info_file_path = 'info.txt'
            if not os.path.exists(info_file_path):
                print(f"Warning: {info_file_path} not found. Creating basic knowledge base...")
                content = self.get_basic_palms_info()
            else:
                try:
                    with open(info_file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        print(f"Loaded knowledge base from {info_file_path} ({len(content)} characters)")
                        
                    # If file is empty or too small, use basic info
                    if len(content.strip()) < 100:
                        print("Info.txt file appears empty, using basic knowledge base")
                        content = self.get_basic_palms_info()
                except Exception as e:
                    print(f"Error reading {info_file_path}: {e}")
                    content = self.get_basic_palms_info()
            
            # Split content into chunks for better retrieval
            chunks = self.split_content_into_chunks(content)
            print(f"Created {len(chunks)} knowledge chunks")
            
            if not chunks:
                print("No content to process")
                return
            
            # Generate embeddings and store in ChromaDB
            embeddings = []
            documents = []
            metadatas = []
            ids = []
            
            for i, chunk in enumerate(chunks):
                if len(chunk.strip()) > 50:  # Only process meaningful chunks
                    embedding = self.get_embedding(chunk)
                    embeddings.append(embedding)
                    documents.append(chunk)
                    metadatas.append({"chunk_id": i, "type": "product_info"})
                    ids.append(f"chunk_{i}")
            
            # Only add if we have embeddings
            if embeddings:
                self.collection.add(
                    embeddings=embeddings,
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                print(f"Successfully added {len(embeddings)} chunks to knowledge base")
            else:
                print("No valid content chunks found to add to knowledge base")
            
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
            
    def get_basic_palms_info(self):
        """Fallback basic PALMS info if info.txt is not found"""
        return """
        PALMS™ is a comprehensive warehouse management solution designed for modern supply chain operations.
        
        Core Features:
        - Real-time inventory tracking with 99.9% accuracy
        - Automated order processing with smart queue management
        - AI-driven warehouse space optimization
        - Dynamic stock movement tracking with path optimization
        - Multi-warehouse management with centralized control
        - Advanced barcode and RFID integration
        - Mobile operations with handheld devices
        - Real-time analytics with predictive insights
        
        Performance Benefits:
        - 40% reduction in picking time
        - 60% improvement in space utilization
        - 45% reduction in processing errors
        - 30% increase in throughput
        
        Solutions:
        - PALMS™ WMS (Standard warehouse management)
        - PALMS™ 3PL (Third-party logistics solution)
        - PALMS™ Enterprise (Large-scale operations)
        - PALMS™ Mobile (Mobile warehouse operations)
        - PALMS™ Analytics (Business intelligence platform)
        
        Integration:
        - ERP system integration (SAP, Oracle, Microsoft Dynamics)
        - Hardware integration (RFID, HHT, AGV)
        - API-based integration
        - EDI capabilities
        - Real-time data sync
        
        Industries Served:
        - Manufacturing
        - Retail and E-commerce
        - Cold Storage and Agriculture
        - Automotive
        - Electronics and High-Tech
        - FMCG and Consumer Goods
        
        Contact: sales@onpalms.com, Phone: +91 79755 52867
        """

    def split_content_into_chunks(self, content, chunk_size=500, overlap=50):
        """Split content into overlapping chunks for better retrieval"""
        words = content.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks

    def retrieve_relevant_context(self, query, n_results=3):
        """Retrieve relevant context from the knowledge base"""
        try:
            if self.collection.count() == 0:
                print("Knowledge base is empty")
                return ""
                
            query_embedding = self.get_embedding(query)
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            if results and 'documents' in results and results['documents']:
                relevant_text = ' '.join(results['documents'][0])
                print(f"Retrieved {len(relevant_text)} characters of context for query: {query[:50]}...")
                return relevant_text
            return ""
            
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return ""

    def validate_business_email(self, email):
        """Validate if email is a business email (not personal)"""
        try:
            # Basic email validation
            validate_email(email)
            
            # Extract domain
            domain = email.split('@')[1].lower()
            
            # Check if it's a personal domain
            return domain not in self.personal_domains
            
        except (EmailNotValidError, IndexError):
            return False

    def analyze_message_intent(self, message, session):
        """Analyze user message for intent and update lead scoring"""
        message_lower = message.lower()
        
        # Advanced intent scoring with context awareness
        previous_score = session.get('lead_score', 0)
        
        # Pricing interest (high buying intent)
        if any(word in message_lower for word in ['price', 'cost', 'pricing', 'how much', 'budget', 'expensive', 'affordable']):
            session['lead_score'] += 10
            session['interests'] = session.get('interests', [])
            if 'pricing' not in session['interests']:
                session['interests'].append('pricing')
            
        # Demo/trial interest (very high buying intent) - but respect decline status
        demo_positive_words = ['demo', 'demonstration', 'show me', 'try', 'test', 'trial', 'see it']
        demo_negative_words = ['no demo', 'not interested', 'do not want', "don't want", 'no thanks', 'not now', 'decline']
        
        has_demo_positive = any(word in message_lower for word in demo_positive_words)
        has_demo_negative = any(word in message_lower for word in demo_negative_words)
        
        if has_demo_positive and not has_demo_negative:
            session['lead_score'] += 30
            session['interests'] = session.get('interests', [])
            if 'demo' not in session['interests']:
                session['interests'].append('demo')
        elif has_demo_negative:
            session['demo_declined'] = True
            
        # Technical/feature interest (moderate buying intent)
        if any(word in message_lower for word in ['warehouse', 'inventory', 'wms', 'problems', 'challenges', 'features', 'capabilities']):
            session['lead_score'] += 15
            session['interests'] = session.get('interests', [])
            if 'features' not in session['interests']:
                session['interests'].append('features')
            
        # Timeline/urgency (high buying intent)
        if any(word in message_lower for word in ['timeline', 'when', 'implementation', 'go live', 'urgent', 'asap', 'soon']):
            session['lead_score'] += 25
            session['interests'] = session.get('interests', [])
            if 'timeline' not in session['interests']:
                session['interests'].append('timeline')
        
        # Company/business details (qualification signal)
        if any(word in message_lower for word in ['company', 'business', 'we are', 'our warehouse', 'my company', 'organization']):
            session['lead_score'] += 20
            session['qualification_level'] = session.get('qualification_level', 0) + 1
            
        # Comparison shopping (buying intent)
        if any(word in message_lower for word in ['compare', 'versus', 'vs', 'alternative', 'better than', 'difference']):
            session['lead_score'] += 15
            session['interests'] = session.get('interests', [])
            if 'comparison' not in session['interests']:
                session['interests'].append('comparison')
        
        # Industry-specific mentions (qualification signal)
        industries = ['manufacturing', 'retail', 'ecommerce', '3pl', 'logistics', 'distribution', 'automotive', 'pharmaceutical']
        if any(industry in message_lower for industry in industries):
            session['lead_score'] += 10
            session['industry'] = next((industry for industry in industries if industry in message_lower), None)
        
        # Size indicators (qualification signal)
        size_indicators = ['warehouse', 'warehouses', 'facility', 'facilities', 'sqft', 'square feet', 'employees', 'staff']
        if any(indicator in message_lower for indicator in size_indicators):
            session['qualification_level'] = session.get('qualification_level', 0) + 1
        
        # Determine lead temperature with more nuanced scoring
        current_score = session['lead_score']
        qualification = session.get('qualification_level', 0)
        
        if current_score >= 60 or (current_score >= 40 and qualification >= 2):
            session['stage'] = 'hot_lead'
        elif current_score >= 30 or (current_score >= 20 and qualification >= 1):
            session['stage'] = 'warm_lead'
        elif current_score >= 15:
            session['stage'] = 'interested'
        else:
            session['stage'] = 'cold_lead'
        
        # Track conversation progression
        session['message_count'] = session.get('message_count', 0) + 1
        
        # Detect if user needs intent clarification (early in conversation, low engagement)
        if (session['message_count'] <= 3 and 
            current_score <= 15 and 
            not any(word in message_lower for word in ['hello', 'hi', 'hey', 'what is palms', 'about palms'])):
            session['needs_intent_clarification'] = True

    def get_enhanced_demo_response(self, message, relevant_context, lead_score, stage, session):
        """Generate intelligent demo responses when OpenAI API is not available"""
        message_lower = message.lower()
        conversation_history = session.get('conversation_history', [])
        
        # Extract specific information from context for more targeted responses
        def extract_context_info(context, keywords):
            """Extract specific information from context based on keywords"""
            if not context:
                return ""
            context_lower = context.lower()
            relevant_parts = []
            for keyword in keywords:
                if keyword in context_lower:
                    # Find sentences containing the keyword
                    sentences = context.split('.')
                    for sentence in sentences:
                        if keyword in sentence.lower():
                            relevant_parts.append(sentence.strip())
            return ' '.join(relevant_parts[:2])  # Return first 2 relevant sentences
        
        # Products and solutions inquiries
        if any(word in message_lower for word in ['products', 'solutions', 'all products', 'what do you offer', 'modules', 'editions']):
            products_info = extract_context_info(relevant_context, ['wms', '3pl', 'enterprise', 'mobile', 'analytics'])
            return f"""PALMS™ offers a complete suite of warehouse management solutions:

• **PALMS™ WMS** - Core warehouse management with 99.9% inventory accuracy
• **PALMS™ 3PL** - Third-party logistics with multi-client management  
• **PALMS™ Enterprise** - Large-scale operations with advanced customization
• **PALMS™ Mobile** - Mobile operations and barcode scanning
• **PALMS™ Analytics** - Business intelligence and reporting platform

Each solution delivers 40% faster picking and dramatically improves warehouse efficiency. {products_info}

What's your warehouse size and industry so I can recommend the perfect fit for your operation?"""
        
        # Greeting responses with context awareness
        elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            if len(conversation_history) == 0:
                return "Hello! I'm here to help with PALMS™ warehouse management solutions.\nAre you exploring options or need something specific?"
            else:
                return "Hello again! How can I help you with PALMS™ today?"
            
        # Product information with context
        elif any(word in message_lower for word in ['what is palms', 'about palms', 'palms wms', 'what does palms do']):
            return "PALMS™ is a warehouse management system with 99.9% inventory accuracy and automated order processing.\nWhat's your warehouse size? I can show you specific benefits for your operation."
            
        # Pricing inquiries with context
        elif any(word in message_lower for word in ['price', 'cost', 'pricing', 'how much', 'budget']):
            return "PALMS™ pricing depends on warehouse size and features needed - typically ROI in 6-12 months.\nWhat's your warehouse size and daily order volume for accurate pricing?"
            
        # Handle demo decline responses
        elif any(phrase in message_lower for phrase in ['no demo', 'not interested', 'do not want', "don't want", 'no thanks', 'not now', 'decline', 'pass']):
            session['demo_declined'] = True
            return "No problem at all! I'm happy to answer any questions about PALMS™ features and benefits.\nWhat specific warehouse challenges are you facing?"
            
        # Demo requests - check if declined before
        elif any(word in message_lower for word in ['demo', 'demonstration', 'show me', 'see it']):
            if session.get('demo_declined'):
                return "I can answer any questions about PALMS™ features and benefits.\nWhat specific warehouse challenges are you trying to solve?"
            else:
                return "Great! I can schedule a personalized PALMS™ demo with real-time tracking and ROI calculator.\nWhat industry are you in so I can tailor it for your needs?"
            
        # Features and benefits with context
        elif any(word in message_lower for word in ['features', 'capabilities', 'what does', 'benefits', 'functionality']):
            features_info = extract_context_info(relevant_context, ['features', 'capabilities', 'tracking', 'automation', 'integration'])
            return f"""PALMS™ offers comprehensive warehouse management capabilities:

• **Real-time Inventory Tracking** - 99.9% accuracy eliminates stock discrepancies
• **Automated Order Processing** - Smart queuing speeds up fulfillment  
• **AI-Driven Space Optimization** - Up to 60% better storage efficiency
• **Mobile Picking & Scanning** - Seamless handheld device integration
• **Advanced Analytics** - Insights and reporting you never had before
• **Multi-Warehouse Management** - Centralized control across locations
• **ERP Integration** - Works with 50+ systems including SAP and Oracle

{features_info}

Which of these areas is causing the biggest headache in your current operation?"""
            
        # Integration questions with specific details
        elif any(word in message_lower for word in ['integration', 'erp', 'systems', 'connect', 'api']):
            integration_info = extract_context_info(relevant_context, ['integration', 'erp', 'sap', 'oracle', 'api', 'edi'])
            return f"Excellent question! PALMS™ plays very well with others. We integrate seamlessly with all major ERP systems including SAP, Oracle, Microsoft Dynamics, and over 50 other platforms. {integration_info} Whether you need EDI connections, REST APIs, or real-time data synchronization, our integration team has you covered. We actually achieve 99% successful go-lives within just 4-8 weeks, which is pretty impressive in this industry. What ERP or software systems are you currently using?"
            
        # Mobile and technology with context
        elif any(word in message_lower for word in ['mobile', 'handheld', 'scanning', 'app', 'technology']):
            mobile_info = extract_context_info(relevant_context, ['mobile', 'scanning', 'handheld', 'barcode', 'rfid'])
            return f"Yes! PALMS™ Mobile is a game-changer. {mobile_info} It enables barcode/RFID scanning, real-time updates, mobile picking with optimized paths, worker tracking, and task management. Works on any Android/iOS device with offline capability. Many clients report 30% productivity improvements. Are you currently using handheld devices or looking to implement them?"
            
        # Industry-specific responses
        elif any(word in message_lower for word in ['manufacturing', 'retail', 'ecommerce', '3pl', 'cold storage', 'automotive']):
            industry = next((word for word in ['manufacturing', 'retail', 'ecommerce', '3pl', 'cold storage', 'automotive'] if word in message_lower), 'your industry')
            industry_info = extract_context_info(relevant_context, [industry, 'industry'])
            return f"""Perfect! PALMS™ has extensive experience in {industry}. We offer specialized features:

• **Industry-Specific Workflows** - Tailored processes for {industry} operations
• **Compliance Tracking** - FDA, GMP, and regulatory requirements
• **Lot/Batch Control** - Complete traceability and quality management
• **Optimized Processes** - Best practices from {industry} leaders

{industry_info}

Our {industry} clients typically see 35-50% efficiency improvements. What are your biggest operational challenges right now?"""
            
        # Problems and challenges with solutions
        elif any(word in message_lower for word in ['problem', 'challenge', 'issue', 'difficulty', 'inefficient']):
            problems_info = extract_context_info(relevant_context, ['accuracy', 'errors', 'efficiency', 'problems'])
            return f"I understand - warehouse challenges directly impact your bottom line. {problems_info} PALMS™ addresses common issues: inventory inaccuracy → 99.9% accuracy, slow picking → 40% faster, space waste → 60% optimization, manual errors → 45% reduction, poor visibility → real-time tracking. What specific challenges are costing you the most right now?"
            
        # Client/case studies inquiries
        elif any(word in message_lower for word in ['clients', 'customers', 'case studies', 'success stories', 'who uses']):
            return f"""PALMS™ serves diverse industries with impressive results:

• **Manufacturing** - 40% faster picking, 60% space optimization
• **Retail & E-commerce** - 99.9% inventory accuracy, faster order fulfillment  
• **3PL & Logistics** - Multi-client management, automated billing
• **Cold Storage** - Temperature monitoring, compliance tracking
• **Automotive** - Serial number tracking, JIT delivery
• **Electronics** - Component management, quality control

Key client achievements:
• Reduced picking errors by 45%
• Increased throughput by 30% 
• ROI achieved within 6-12 months
• 99% successful implementations

What industry are you in? I can share specific success stories relevant to your business."""
        
        # Comparison questions
        elif any(word in message_lower for word in ['compared to', 'versus', 'vs', 'better than', 'difference']):
            return f"""Great question! Here's how PALMS™ stands out:

• **99.9% Inventory Accuracy** - Industry average is only 63%
• **4-8 Week Implementation** - Others take 6+ months
• **Mobile-First Design** - Comprehensive handheld integration
• **Flexible Deployment** - Cloud, on-premise, or hybrid options  
• **Superior ROI** - 6-12 month payback period
• **Exceptional Support** - 24/7 technical assistance

{extract_context_info(relevant_context, ['advantage', 'performance', 'roi'])}

Are you currently evaluating other WMS solutions? I can do a detailed comparison."""
        
        # Intent clarification for uncertain users
        elif (session.get('message_count', 0) <= 2 and 
              lead_score <= 15 and 
              not any(word in message_lower for word in ['hello', 'hi', 'what is palms'])):
            return "I'd love to help you find the right warehouse solution! Are you: ① Just exploring WMS options ② Looking for specific pricing ③ Need help deciding between solutions ④ Ready to book a demo? This helps me provide the most relevant information for your situation."
        
        # Context-aware default responses based on conversation stage
        else:
            if stage == 'hot_lead':
                return "Based on our conversation, PALMS™ seems like a perfect fit for your needs. With your level of interest and requirements, I'd recommend scheduling a personalized demo to see exactly how we can solve your warehouse challenges and calculate your specific ROI. When would be a good time for a 30-minute demo?"
            elif stage == 'warm_lead':
                return f"Thanks for your continued interest! {extract_context_info(relevant_context, ['benefits', 'roi', 'efficiency'])} PALMS™ has helped businesses like yours achieve dramatic warehouse improvements. What's the most important factor in your WMS decision - ROI timeline, ease of implementation, or specific functionality?"
            elif len(conversation_history) >= 4:
                return "I've shared quite a bit about PALMS™ capabilities. What questions do you still have? I'm here to help you understand exactly how we can solve your warehouse challenges and improve your operations."
            else:
                responses = [
                    f"I'm here to help you discover how PALMS™ can optimize your warehouse operations. {extract_context_info(relevant_context, ['accuracy', 'efficiency'])} What brings you here today - inventory accuracy issues, slow order processing, or other warehouse challenges?",
                    f"Welcome to PALMS™! {extract_context_info(relevant_context, ['benefits', 'performance'])} We help businesses achieve 99.9% inventory accuracy and dramatically faster operations. What aspect of warehouse management is your biggest priority right now?",
                    f"Great to connect! {extract_context_info(relevant_context, ['solutions', 'clients'])} PALMS™ specializes in turning warehouse challenges into competitive advantages. Whether it's inventory accuracy, order speed, or space optimization - what matters most to your operation?"
                ]
                import random
                return random.choice(responses)

    def get_information_layer_response(self, message, relevant_context):
        """Layer 1: Information Retrieval - Extract relevant facts from knowledge base"""
        if not self.client:
            return relevant_context[:500]  # Fallback for demo mode
            
        try:
            prompt = f"""
            {self.retrieval_prompt}
            
            KNOWLEDGE BASE CONTEXT:
            {relevant_context}
            
            USER QUERY: {message}
            
            Extract and return only the most relevant factual information that answers the user's query.
            Focus on specific features, benefits, metrics, and technical details.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using GPT-4o for better accuracy
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=400,
                temperature=0.2  # Lower temperature for factual accuracy
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error in information layer: {e}")
            return relevant_context[:500]

    def get_sales_layer_response(self, message, extracted_info, session):
        """Layer 2: Sales Conversation - Context-aware sales interaction"""
        conversation_history = session.get('conversation_history', [])[-8:]  # Last 4 exchanges
        lead_score = session.get('lead_score', 0)
        stage = session.get('stage', 'greeting')
        
        # Build conversation context
        context_summary = ""
        if len(conversation_history) >= 2:
            context_summary = "Previous conversation topics: "
            for i in range(0, len(conversation_history)-1, 2):
                if i+1 < len(conversation_history):
                    context_summary += f"User asked about: {conversation_history[i]['content'][:50]}... "
        
        if not self.client:
            return self.get_enhanced_demo_response(message, extracted_info, lead_score, stage, session)
            
        try:
            prompt = f"""
            {self.sales_prompt}
            
            EXTRACTED PALMS™ INFORMATION:
            {extracted_info}
            
            CONVERSATION CONTEXT:
            - Lead Score: {lead_score}/100
            - Lead Stage: {stage}
            - {context_summary}
            - Full conversation: {json.dumps(conversation_history[-6:]) if conversation_history else 'First interaction'}
            
            CURRENT USER MESSAGE: {message}
            
            RESPONSE GUIDELINES:
            1. Keep responses to 2 lines maximum unless user asks for detailed explanation
            2. Be direct and answer their specific question first
            3. Respect demo decline status - don't push if they said no to demos
            4. Use extracted information to be accurate and helpful
            5. Add one brief follow-up question or next step if relevant
            6. Be context-aware - don't repeat previous information
            7. Demo declined status: {session.get('demo_declined', False)}
            
            FORMATTING REQUIREMENTS:
            - Maximum 2 lines unless user specifically asks for more details
            - Line 1: Direct answer to their question with key facts
            - Line 2: Brief follow-up or next step (if appropriate)
            - Use bullet points only if they ask about multiple items
            - Be conversational but concise
            
            INTENT IDENTIFICATION (use when appropriate):
            If user seems uncertain or new, offer: "Are you just exploring or looking for something specific today?"
            ① Just exploring → Overview + key benefits + ask about challenges
            ② Looking for pricing → Understand requirements + discuss pricing
            ③Need help deciding → Qualifying questions + recommendations  
            ④Want to book demo → Capture details + schedule
            
            Generate a compelling, context-aware sales response:
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using GPT-4o for better context understanding
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error in sales layer: {e}")
            return self.get_demo_response(message, extracted_info, lead_score, stage)

    def get_response(self, message, session):
        """Main response method using enhanced TOFU two-layer AI system"""
        
        # TOFU Enhancement: Advanced lead qualification
        session = self.enhanced_lead_qualification(message, session)
        
        # Analyze intent and update scoring (existing logic)
        self.analyze_message_intent(message, session)
        
        # TOFU Enhancement: Determine engagement strategy
        engagement_strategy = self.get_tofu_engagement_strategy(session)
        
        # Check if user is asking for human handoff
        if any(phrase in message.lower() for phrase in ['human', 'person', 'agent', 'representative', 'speak to someone']):
            return {
                'message': "I'd be happy to connect you with our sales team! Please fill out the demo form below and our experts will reach out within 24 hours to provide personalized assistance.",
                'show_demo_form': True
            }
        
        try:
            # Layer 1: Retrieve relevant context from knowledge base
            relevant_context = self.retrieve_relevant_context(message)
            
            # Layer 1: Extract specific information using AI
            extracted_info = self.get_information_layer_response(message, relevant_context)
            
            # Layer 2: Generate context-aware sales response
            bot_message = self.get_sales_layer_response(message, extracted_info, session)
            
            # TOFU Enhancement: Only add conversation flow for next-step questions, not content questions
            # Don't override when user is asking about features, company info, pricing details, etc.
            is_content_question = any(keyword in message.lower() for keyword in [
                'what', 'how', 'why', 'tell me', 'explain', 'about', 'feature', 'price', 
                'cost', 'company', 'product', 'integration', 'works', 'does', 'can it',
                'mobile', 'industry', 'clients', 'case', 'benefit', 'problem', 'challenge'
            ])
            
            if not is_content_question:
                tofu_response = self.get_tofu_conversation_flow(message, session, engagement_strategy)
                if tofu_response and engagement_strategy in ['direct_sales', 'nurture_warm']:
                    # Only enhance with TOFU for next-step conversations
                    bot_message = tofu_response
            
            # Only show demo form if user explicitly requests a demo or call
            demo_request_phrases = [
                'demo', 'schedule demo', 'book demo', 'show me demo', 'see demo', 'want demo', 
                'i want a demo', 'i would like a demo', 'can i get a demo', 'request demo', 
                'try demo', 'demo please', 'demonstration', 'book a demo', 'schedule a demo',
                'sign up for demo', 'get a demo', 'demo session', 'product demo', 'live demo',
                # Call-related phrases that should also trigger demo form
                'book a call', 'schedule a call', 'book call', 'schedule call', 'want a call',
                'request a call', 'call me', 'phone call', 'sales call', 'consultation call',
                'speak with someone', 'talk to sales', 'contact sales', 'sales consultation',
                'schedule consultation', 'book consultation', 'arrange a call', 'set up a call'
            ]
            message_lower = message.lower()
            
            # Check for explicit demo requests (more specific matching)
            show_demo_form = False
            for phrase in demo_request_phrases:
                if phrase in message_lower:
                    show_demo_form = True
                    break
            
            # Also check for "yes" responses only if the bot recently asked about demo
            if not show_demo_form and 'yes' in message_lower:
                # Check if the conversation context suggests this is a demo response
                recent_context = ' '.join([msg['content'] for msg in session.get('conversation_history', [])[-3:]])
                if 'demo' in recent_context.lower() or 'demonstration' in recent_context.lower():
                    show_demo_form = True
            
            # Track negative demo responses to avoid future prompts
            negative_demo_words = ['no demo', 'not interested', 'do not want', "don't want", 'no thanks', 
                                 'not now', 'maybe later', 'not ready', 'just browsing', 'just looking',
                                 'decline', 'pass', 'skip demo', 'no need', 'not necessary']
            has_negative_intent = any(phrase in message_lower for phrase in negative_demo_words)
            if has_negative_intent:
                session['demo_declined'] = True
                show_demo_form = False
            
            return {
                'message': bot_message,
                'show_demo_form': show_demo_form,
                'tofu_data': {
                    'engagement_strategy': engagement_strategy,
                    'lead_score': session.get('lead_score', 0),
                    'qualification_signals': session.get('qualification_signals', []),
                    'touch_count': session.get('touch_count', 0)
                }
            }
            
        except Exception as e:
            print(f"Error in get_response: {e}")
            return {
                'message': "I'm experiencing a technical issue right now. Please try asking your question again, or feel free to contact our sales team directly at sales@onpalms.com for immediate assistance.",
                'show_demo_form': False
            }
    
    # TOFU Enhancement Methods
    def enhanced_lead_qualification(self, message, session):
        """Enhanced TOFU-based lead qualification"""
        message_lower = message.lower()
        
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
                            session['lead_score'] = session.get('lead_score', 0) + 25
                            session['qualification_signals'] = session.get('qualification_signals', [])
                            session['qualification_signals'].append(f"{category}_{level}")
                        elif level == 'medium' or level == 'near_term' or level == 'exploring':
                            session['lead_score'] = session.get('lead_score', 0) + 15
                        else:
                            session['lead_score'] = session.get('lead_score', 0) + 5
        
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

    def get_tofu_conversation_flow(self, message, session, engagement_strategy):
        """TOFU-based conversation flow management - only for next-step guidance"""
        
        # Only provide TOFU responses for general inquiries or next-step questions
        # Not for specific content questions
        message_lower = message.lower()
        
        # Check if this is a next-step type question
        is_next_step_question = any(phrase in message_lower for phrase in [
            'what now', 'next step', 'what should', 'how do i proceed', 
            'what do you recommend', 'ready to move', 'lets go', "let's proceed"
        ])
        
        if not is_next_step_question:
            return None  # Let the main AI response handle content questions
        
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
                'touch_3': "Great! I can connect you with our sales team who can provide detailed pricing and create a customized implementation plan for your business."
            }
        }
        
        touch_count = session.get('touch_count', 0) + 1
        session['touch_count'] = touch_count
        
        # Select appropriate response based on engagement strategy and touch count
        if engagement_strategy in flows:
            touch_key = f'touch_{min(touch_count, 3)}'
            return flows[engagement_strategy].get(touch_key, None)
        
        return None

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