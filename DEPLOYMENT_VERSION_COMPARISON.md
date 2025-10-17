# Deployment Version Comparison

## Current Files Ready for Deployment

### ✅ PRODUCTION (Memory-Optimized for Render Free Tier)

**Files:**
- `chat.py` - Uses OpenAI embeddings API
- `requirements.txt` - Optimized dependencies (no sentence-transformers)
- `Procfile` - Gunicorn with PORT binding

**Memory Usage:** ~50-100MB (fits in 512MB limit)

**Pros:**
- ✅ Deploys successfully on Render free tier
- ✅ Better quality embeddings from OpenAI
- ✅ Lower memory footprint
- ✅ No model loading delay at startup

**Cons:**
- ⚠️ API latency ~150ms per query
- ⚠️ Small cost (~$0.20/month)
- ⚠️ Requires OpenAI API key in environment

---

### 🔄 FALLBACK (If Production Fails)

**Files:**
- `chat_FALLBACK_with_sentence_transformers.py` - Local embeddings
- `requirements_FALLBACK_with_sentence_transformers.txt` - Includes sentence-transformers

**Memory Usage:** ~150-200MB (may exceed 512MB with full stack)

**Pros:**
- ✅ Instant local embeddings (<50ms)
- ✅ No API costs
- ✅ Works offline

**Cons:**
- ❌ May exceed Render's 512MB memory limit
- ❌ Slower startup (model loading)
- ❌ Higher CPU usage

---

## Deployment Strategy

### Step 1: Deploy Production Version (Recommended)
```bash
git add chat.py requirements.txt
git commit -m "Replace sentence-transformers with OpenAI embeddings for memory optimization"
git push origin main
```

**Monitor:** Check Render logs for successful deployment under 512MB

### Step 2: If Production Fails, Use Fallback
```bash
cp chat_FALLBACK_with_sentence_transformers.py chat.py
cp requirements_FALLBACK_with_sentence_transformers.txt requirements.txt
git add chat.py requirements.txt
git commit -m "Rollback to sentence-transformers version"
git push origin main
```

### Step 3: Alternative - Upgrade Render Plan
If both fail, consider Render's Starter plan ($7/month) for 512MB → 2GB RAM

---

## Environment Variables Required

Make sure these are set in Render dashboard:

```
OPENAI_API_KEY=sk-proj-bpiwS5JJcqlm...
GOOGLE_SCRIPT_URL=https://script.google.com/macros/s/AKfycbwtkTDW3CjoKgSJrDgj2dWn6oU-ZXYncoGuu6h7zeB5lT14xe_8Q-yjtlwYxHZ61H77/exec
```

---

## Testing Checklist

After deployment, test:

- [ ] Chat interface loads
- [ ] Bot responds to "hello"
- [ ] Bot retrieves info from knowledge base
- [ ] Demo form submission works
- [ ] Google Sheets integration works
- [ ] Memory stays under 512MB (check Render metrics)

---

**Recommendation:** Try production version first. The OpenAI embeddings approach is more reliable for Render's free tier constraints.
