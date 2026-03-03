# ShopifyWebhookPOC

A FastAPI app that receives and verifies Shopify webhooks, deployable to Render.

## Project Structure

```
ShopifyWebhookPOC/
├── main.py           ← FastAPI app with webhook handler + HMAC verification
├── requirements.txt  ← Python dependencies
├── .env              ← Local environment variables (gitignored)
└── .gitignore
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check (used by Render) |
| POST | `/webhooks/shopify` | Shopify webhook receiver |

## Local Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your webhook secret in .env
echo "SHOPIFY_WEBHOOK_SECRET=your_secret_here" > .env

# 3. Run the server
uvicorn main:app --reload
```

App runs at `http://localhost:8000`. Docs available at `http://localhost:8000/docs`.

## Local Testing with ngrok

To test webhooks locally before deploying:

```bash
# In terminal 1 — start the app
uvicorn main:app --reload

# In terminal 2 — expose it publicly
ngrok http 8000
```

Copy the `https://xxxx.ngrok.io` URL and use it as your Shopify webhook URL.

## Deploy to Render

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → **New Web Service** → connect your repo
3. Configure:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variable in Render dashboard:
   - Key: `SHOPIFY_WEBHOOK_SECRET`
   - Value: *(from Shopify — see below)*
5. Deploy — note your public URL: `https://your-app.onrender.com`

## Register Webhook in Shopify

1. Go to **Shopify Admin → Settings → Notifications → Webhooks**
2. Click **Create webhook**
   - Event: e.g. `Order creation`
   - Format: `JSON`
   - URL: `https://your-app.onrender.com/webhooks/shopify`
   - API version: latest
3. Copy the **Signing secret** shown → paste it as `SHOPIFY_WEBHOOK_SECRET` in Render
4. Click **Send test notification** to verify the integration

## Supported Webhook Topics

| Topic | Handler |
|-------|---------|
| `orders/create` | Logs order ID, email, total |
| `orders/updated` | Logs order ID, financial status |
| `products/create` | Logs product ID, title |

Add more topics by adding `elif x_shopify_topic == "..."` blocks in `main.py`.

## How HMAC Verification Works

Shopify signs every webhook with a shared secret using HMAC-SHA256.
The app rejects any request that fails verification, protecting against spoofed payloads.

```
HMAC = base64( SHA256( secret + raw_body ) )
```
