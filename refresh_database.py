#!/usr/bin/env python3
"""
Script to force refresh the ChromaDB knowledge base with info.txt content
Run this after making changes to info.txt to immediately update the database
"""

import chromadb
import os
from dotenv import load_dotenv

load_dotenv()

def refresh_database():
    print("🔄 Starting database refresh...")
    
    # Initialize ChromaDB
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    try:
        # Delete existing collection
        print("🗑️  Deleting existing collection...")
        try:
            chroma_client.delete_collection("palms_knowledge")
            print("✅ Existing collection deleted")
        except Exception as e:
            print(f"ℹ️  No existing collection to delete: {e}")
        
        # Create new collection
        print("📦 Creating new collection...")
        collection = chroma_client.create_collection("palms_knowledge")
        print("✅ New collection created")
        
        # Load info.txt
        print("📄 Loading info.txt...")
        with open('info.txt', 'r', encoding='utf-8') as file:
            content = file.read()
        print(f"✅ Loaded {len(content)} characters from info.txt")
        
        # Split into chunks
        print("✂️  Splitting content into chunks...")
        sections = content.split('\n##')
        chunks = []
        
        for section in sections:
            if not section.strip():
                continue
            
            # Keep sections intact for better context
            words = section.split()
            chunk_size = 2000
            overlap = 200
            
            if len(words) > chunk_size:
                for i in range(0, len(words), chunk_size - overlap):
                    chunk = ' '.join(words[i:i + chunk_size])
                    if chunk.strip():
                        chunks.append('##' + chunk if i == 0 else chunk)
            else:
                chunks.append('##' + section if not section.startswith('##') else section)
        
        print(f"✅ Created {len(chunks)} chunks")
        
        # Import OpenAI for embeddings
        print("🔌 Connecting to OpenAI...")
        from openai import OpenAI
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            print("❌ OpenAI API key not found in .env file!")
            print("⚠️  Cannot generate embeddings without API key")
            return False
        
        client = OpenAI(api_key=api_key)
        print("✅ Connected to OpenAI")
        
        # Generate embeddings and store
        print("🧮 Generating embeddings and storing in database...")
        embeddings = []
        documents = []
        metadatas = []
        ids = []
        
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) > 50:
                # Generate embedding
                response = client.embeddings.create(
                    input=chunk,
                    model="text-embedding-3-small"
                )
                embedding = response.data[0].embedding
                
                embeddings.append(embedding)
                documents.append(chunk)
                metadatas.append({"chunk_id": i, "type": "product_info"})
                ids.append(f"chunk_{i}")
                
                if (i + 1) % 10 == 0:
                    print(f"   Processed {i + 1}/{len(chunks)} chunks...")
        
        # Add to collection
        if embeddings:
            collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✅ Successfully stored {len(embeddings)} chunks in database")
        else:
            print("❌ No valid chunks to store")
            return False
        
        print("\n🎉 Database refresh complete!")
        print(f"📊 Total chunks in database: {collection.count()}")
        
        # Test query to verify
        print("\n🔍 Testing database with sample query...")
        test_query = "tell me about all PALMS products"
        test_embedding = client.embeddings.create(
            input=test_query,
            model="text-embedding-3-small"
        ).data[0].embedding
        
        results = collection.query(
            query_embeddings=[test_embedding],
            n_results=5
        )
        
        print(f"✅ Test query returned {len(results['documents'][0])} results")
        print(f"   Preview: {results['documents'][0][0][:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during refresh: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("PALMS™ Database Refresh Utility")
    print("=" * 60)
    success = refresh_database()
    print("=" * 60)
    if success:
        print("✅ SUCCESS: Database has been refreshed!")
        print("💡 You can now restart app.py to use the updated database")
    else:
        print("❌ FAILED: Database refresh encountered errors")
    print("=" * 60)
