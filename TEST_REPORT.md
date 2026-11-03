# Phase 1 code verification

## Automated checks completed
- Python AST parse and bytecode compilation: passed.
- Authenticated artisan app execution using a Streamlit widget stub: passed.
- SQLite schema initialization: passed.
- New `users` and `artisan_profiles` tables: verified.
- Backward-compatible migrations for listing ownership, inquiry ownership and order workflow: verified.
- Salted PBKDF2-HMAC-SHA256 password hashing and constant-time password comparison implemented.
- New listing inserts include authenticated owner ID.
- Listing edit and soft-remove SQL operations constrain by both listing ID and owner ID.
- Inquiry records include buyer and seller account IDs.
- Accepted inquiry conversion creates a linked order with buyer, seller and listing references.
- Buyer order query is scoped to the authenticated buyer.

## Manual tests still required on deployed Streamlit
1. Register an Artisan account and a Buyer account.
2. Sign in/out with both accounts.
3. Confirm Buyer cannot publish, edit or remove artisan listings.
4. Confirm Artisan A cannot edit/remove Artisan B's listings.
5. Submit a buyer inquiry and confirm it appears only for the listing's artisan and the buyer.
6. Accept the inquiry as the artisan and create the order.
7. Confirm the buyer sees the resulting order in My Orders.
8. Confirm records survive a Streamlit restart; if not, configure a managed persistent database.

## Known limitations
This is prototype-grade authentication and authorization, not a production identity service. No email verification, password reset, MFA, rate limiting, account recovery or admin moderation. Streamlit Community Cloud's local filesystem is not guaranteed to persist; external database and object storage are recommended for a real multi-user deployment.
