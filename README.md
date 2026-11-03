# Garment Cluster Artisan Marketplace — Phase 1

Python + Streamlit + SQLite prototype.

## Main behaviour
- Public browsing: Artisan Marketplace and Raw Materials Marketplace listings are visible without signing in.
- Registration/login: create Buyer or Artisan accounts. Passwords are stored as salted PBKDF2-HMAC-SHA256 hashes, not plaintext.
- Buyer: browse public listings, start a chat with registered artisans, and submit inquiries.
- Artisan: maintain profile, publish image listings, edit/pause/delete owned listings, review inquiries and accept/reject them.
- Inquiry-to-order: accepting a buyer inquiry creates a linked production order.
- Chat Box: account-based direct conversations replace the old Messages navigation item.
- Raw materials remain in their own marketplace section.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy
Upload all project files and folders to the GitHub repository connected to Streamlit Community Cloud.

## Database
The app automatically adds the new columns and users table to an older SQLite database without deleting existing listings. For real multi-user production use, move SQLite to a managed PostgreSQL database and use persistent image/object storage.

## Limitations
This is a student prototype. It does not yet include email verification, password reset, external identity provider, payment processing, shipping, real-time push notifications, or guaranteed persistence of the local SQLite file on hosted infrastructure. Chat is stored in SQLite and refreshes when the page reruns. Existing pre-account demo listings remain public but do not have an account owner, so account-based chat/inquiry actions are only available for listings published by a registered artisan.
