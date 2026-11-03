# Garment Cluster Marketplace — Phase 1

A student prototype built with Python, Streamlit, SQLite and Pandas.

## Implemented in Phase 1
- **Authentication:** account registration and sign-in for Buyer and Artisan roles. Passwords are stored as salted PBKDF2-HMAC-SHA256 hashes.
- **Role-aware access:** Buyers browse, send inquiries and view their orders. Artisans manage their profile, publish/manage listings, review inquiries and manage production.
- **Artisan profiles:** studio name, location, craft specialisation, biography and public business contact.
- **Listing ownership:** new listings are tied to the authenticated artisan. Artisans can edit, pause/unpause or remove only their own listings. Removed listings are soft-removed to preserve order history.
- **Inquiry-to-order workflow:** buyer inquiries are tied to buyer and seller accounts. Artisans can respond, accept or reject. Accepted inquiries can be converted into confirmed orders. Buyers can view their orders.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## GitHub / Streamlit deployment
Upload `app.py`, `requirements.txt`, `README.md`, `TEST_REPORT.md`, `.streamlit/config.toml`, and the complete `artwork_samples/` folder.

## Important limitations
This is a college demonstration prototype, not a production commerce platform. It does not include email verification, password reset, MFA, rate limiting, account recovery, administrator moderation, payments, shipping, refunds or dispute resolution. SQLite and local image BLOB storage are acceptable for a small demo, but Streamlit Community Cloud local filesystem persistence is not guaranteed across restarts/rebuilds. Use managed PostgreSQL and object storage before relying on real multi-user data. Legacy demo listings may have no owner account; newly published listings are owner-linked.
