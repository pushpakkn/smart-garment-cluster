# Phase 1 + Demonstration Data Verification Report

## Automated checks
- Python syntax compilation: PASS.
- Existing Phase 1 navigation and account flows retained in source.
- Demo Buyer and two Demo Artisan accounts are seeded idempotently.
- Demo accounts use salted PBKDF2-HMAC-SHA256 password hashes.
- Buyer-to-artisan sample conversations are seeded without overwriting existing user messages.
- Sample listings are attached to demo artisan owners so chat and inquiry actions can be demonstrated.
- Additional fictional materials, products and production orders populate the management workspace.
- Seed logic checks unique usernames, listing titles, product names and order codes before inserting records.

## Demo scenarios
1. Use **Buyer demo** in the sidebar and open Chat Box to show existing conversations with two artisans.
2. Send a new message and sign out.
3. Use **Artisan demo** to open Chat Box and show the buyer's message in the corresponding conversation.
4. Open Artisan Marketplace and Raw Materials Marketplace as a guest to demonstrate public listing visibility.
5. Sign in as Artisan and open My Listings to edit, pause or delete listings owned by that demo account.
6. Open Dashboard, Inventory, Production Orders and Product Catalogue to demonstrate populated management records.
7. As Buyer, open a demo-owned listing, start a chat or submit an inquiry; as Artisan, review it in Buyer Inquiries.

## Demo credentials
- Buyer: `buyer` / `demo1234`
- Artisan: `artisan` / `demo1234`
- Second Artisan: `artisan2` / `demo1234`

## Limitations
Streamlit browser-level visual testing must still be performed after deployment. Chat is stored in SQLite and refreshes on page rerun; it is not a real-time push messaging service. Demo records are fictional. Do not use the demo credentials in a public production deployment.
