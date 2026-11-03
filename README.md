# Artisan Integrated Network & Commerce

Student prototype built with Python, Streamlit, SQLite and Pandas.

## Management workspace
- **Inventory:** compact stock table showing material, category, available quantity, unit, reorder level, stock status, supplier and last-updated date. Guests can view the table; Artisan accounts can add materials.
- **Production Orders:** review orders and update their status.
- **Product Catalogue:** public product showcase with detailed descriptions, category filters, search, prices, product IDs, date added and a complete table view. Artisan accounts can add products.
- Dashboard metrics and charts summarize management data.

## Demo accounts
| Role | Username | Password |
|---|---|---|
| Buyer | `buyer` | `demo1234` |
| Artisan | `artisan` | `demo1234` |
| Artisan | `artisan2` | `demo1234` |

All demo identities, conversations, products, materials, orders and listings are fictional.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

Replace the files in the GitHub repository connected to Streamlit Community Cloud with the contents of this ZIP, then allow the app to redeploy.

Existing database records are retained. The app adds missing demonstration products and materials without duplicating matching names. This is a student prototype; chat refreshes on Streamlit reruns and SQLite persistence on hosted infrastructure is not guaranteed.


## Accessibility and QA
The latest build includes contrast-focused styling for text, inputs, menus, buttons, tables, metrics, tabs, chat and alerts. See `TEST_REPORT.md` for automated checks and representative WCAG contrast calculations. A deployed-browser visual check is still required.
