# ARTISAN INTEGRATED NETWORK & COMMERCE
## QA and Contrast Remediation Report

### Automated checks completed
- Python source compilation: PASS.
- CSS parsing with tinycss2: PASS (92 CSS rules; no parser errors).
- Fresh SQLite schema initialization: PASS.
- Repeated startup/idempotency check: PASS; demo seed rows are guarded against duplicate names/codes.
- Legacy SQLite migration: PASS; missing user profile columns and listing image/owner columns are added while the pre-existing user row is preserved.
- Required database tables: PASS (`materials`, `products`, `orders`, `listings`, `messages`, `inquiries`, `users`).
- Navigation branch coverage: PASS for all explicit pages; About Project is the intentional final fallback page.
- Public catalogue and inventory read-only code paths: present.
- Artisan-only create/edit controls: present for inventory, catalogue products and owned listings.
- Chat history/send and inquiry workflows: present in the application code.

### Contrast remediation
Added explicit high-contrast styles for:
- Main app text, captions and links.
- Sidebar navigation, selected/hover states and sidebar form controls.
- Text inputs, text areas, placeholders, selects, dropdown menus and multiselect tags.
- Primary, secondary and disabled buttons, plus visible keyboard focus.
- Dataframes/tables and column headers.
- Metrics, expanders, tabs, chat messages and alert panels.
- Catalogue listing cards and prices.

Representative WCAG contrast ratios (calculated from the CSS colour pairs):
| Foreground | Background | Ratio |
|---|---|---:|
| `#172b4d` | `#f3f6fa` | 13.01:1 |
| `#526579` | `#ffffff` | 6.01:1 |
| `#c5d5df` | `#102f46` | 9.20:1 |
| `#075e70` | `#ffffff` | 7.38:1 |
| `#ffffff` | `#08727d` | 5.66:1 |
| `#173b53` | `#e8eff4` | 10.12:1 |

These representative pairs exceed WCAG AA contrast thresholds for normal text (4.5:1).

### Manual verification still required
Streamlit is not installed in this build environment, so a real browser/session test could not be performed here. After deploying, check the pages in Chrome at desktop and narrow/mobile widths, especially the Streamlit dataframe grid, dropdown popovers, chat bubbles and alerts. Streamlit can change internal DOM selectors between versions, so browser inspection remains necessary.

### Important scope note
This is a student prototype with fictional sample data. Chat updates on app reruns and does not provide real-time push notifications. SQLite persistence on Streamlit Community Cloud is not guaranteed for production workloads.
