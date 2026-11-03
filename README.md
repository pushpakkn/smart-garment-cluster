# Artisan Integrated Network & Commerce

Phase 1 student prototype built with Python, Streamlit, SQLite and Pandas.

## Main behaviour
- Public browsing: Artisan Marketplace and Raw Materials Marketplace listings are visible without signing in.
- Registration/login: create Buyer or Artisan accounts. Passwords are stored as salted PBKDF2-HMAC-SHA256 hashes, not plaintext.
- Buyer: browse public listings, start a chat with registered artisans, and submit inquiries.
- Artisan: maintain profile, publish image listings, edit/pause/delete owned listings, review inquiries and accept/reject them.
- Inquiry-to-order: accepting a buyer inquiry creates a production order.
- Chat Box: account-based direct conversations with preloaded fictional conversations for classroom demonstrations.
- Management workspace: seeded inventory, production orders, product catalogue and marketplace listings so the dashboard and management pages are populated on first run.

## Demo accounts
The sidebar includes one-click **Buyer demo** and **Artisan demo** access. You can also sign in manually:

| Role | Username | Password |
|---|---|---|
| Buyer | `buyer` | `demo1234` |
| Artisan | `artisan` | `demo1234` |
| Artisan | `artisan2` | `demo1234` |

All demo identities, conversations, products, materials, orders and listings are fictional sample data. Do not use these credentials for a public production system. Demo conversations are visible when signed in as the corresponding demo user; use Sign out and switch demo role to show both sides of the conversation.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy
Upload all project files and folders to the GitHub repository connected to Streamlit Community Cloud.

## Database
The app adds missing columns to an older SQLite database and preserves existing records. Seed records are inserted only when their identifying username, title, product name or order code is not already present. For real multi-user production use, move SQLite to a managed PostgreSQL database and use persistent image/object storage.

## Limitations
This is a student prototype. It does not include email verification, password reset, an external identity provider, payment processing, shipping, real-time push notifications, or guaranteed persistence of the local SQLite file on hosted infrastructure. Chat is stored in SQLite and refreshes when the page reruns. Demo data is fictional and is intended for presentation/testing only.
