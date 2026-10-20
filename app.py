import sqlite3
from pathlib import Path
from datetime import date
import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "garment_cluster.db"

st.set_page_config(
    page_title="Garment Cluster Manager",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded",
)
CUSTOM_CSS = """
<style>
/* Main page background */
.stApp {
    background: linear-gradient(135deg, #20645b 0%, #e7eff5 100%);
}

/* Main content spacing */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #102a43 0%, #163e5c 100%);
}

[data-testid="stSidebar"] * {
    color: #f4f8fb !important;
}

/* Header banner */
.hero {
    padding: 1.35rem 1.5rem;
    border-radius: 18px;
    background: linear-gradient(115deg, #12344d, #147d79);
    color: #ffffff;
    margin-bottom: 1.1rem;
    box-shadow: 0 5px 18px rgba(18, 52, 77, 0.12);
}

.hero h1 {
    font-size: 2rem;
    margin: 0 0 .35rem 0;
    color: #ffffff;
}

.hero p {
    margin: 0;
    color: #e2f4f3;
    font-size: 1rem;
}

/* Dashboard metric cards */
div[data-testid="stMetric"] {
    background: #e0efed !important;
    border: 1px solid #b8d8d4;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 4px 14px rgba(18, 52, 77, 0.07);
}

/* Metric labels */
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] *,
div[data-testid="stMetricLabel"] p,
div[data-testid="stMetricLabel"] label {
    color: #020629 !important;
    opacity: 1 !important;
    font-weight: 600 !important;
}/* Metric labels */
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] *,
div[data-testid="stMetricLabel"] p,
div[data-testid="stMetricLabel"] label {
    color: #263E50 !important;
    opacity: 1 !important;
    font-weight: 600 !important;
}

/* Metric numbers */
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] * {
    color: #12344d !important;
    opacity: 1 !important;
    font-weight: 750 !important;
}

/* Supporting text */
.metric-card {
    background: #e0efed;
    border: 1px solid #b8d8d4;
    border-radius: 15px;
    padding: 1rem 1.1rem;
    box-shadow: 0 3px 12px rgba(15, 40, 60, .05);
}

.metric-label {
    font-size: .88rem;
    color: #40596b;
    margin-bottom: .3rem;
}

.metric-value {
    font-size: 1.8rem;
    font-weight: 750;
    color: #12344d;
}

.section-note {
    color: #526477;
    font-size: .92rem;
}

/* Buttons */
.stButton button[kind="primary"],
.stFormSubmitButton button[kind="primary"] {
    background: #147d79;
    border-color: #147d79;
    color: #ffffff;
    border-radius: 10px;
}

.stButton button[kind="primary"]:hover,
.stFormSubmitButton button[kind="primary"]:hover {
    background: #10645f;
    border-color: #10645f;
    color: #ffffff;
}

/* Tables and data containers */
div[data-testid="stDataFrame"],
div[data-testid="stTable"] {
    border: 1px solid #d4e2e8;
    border-radius: 12px;
    overflow: hidden;
}

/* Input fields */
.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 9px;
}

/* Headings */
h1, h2, h3, h4 {
    color: #12344d;
}
/* Force metric labels to use a dark, readable color */
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p,
[data-testid="stMetricLabel"] label,
[data-testid="stMetricLabel"] span {
    color: #1B3347 !important;
    -webkit-text-fill-color: #1B3347 !important;
    opacity: 1 !important;
    font-weight: 600 !important;
}
/* Inventory tabs: replace red accents with teal */
.stApp [data-baseweb="tab-list"] button {
    color: #D8E7EA !important;
    border-bottom-color: transparent !important;
}

.stApp [data-baseweb="tab-list"] button p,
.stApp [data-baseweb="tab-list"] button span {
    color: #D8E7EA !important;
}

/* Active tab */
.stApp [data-baseweb="tab-list"] button[aria-selected="true"] {
    color: #FFFFFF !important;
    border-bottom: 2px solid #36C2B4 !important;
}

.stApp [data-baseweb="tab-list"] button[aria-selected="true"] p,
.stApp [data-baseweb="tab-list"] button[aria-selected="true"] span {
    color: #FFFFFF !important;
}

/* Remove red hover effects */
.stApp [data-baseweb="tab-list"] button:hover {
    color: #FFFFFF !important;
    background-color: rgba(54, 194, 180, 0.12) !important;
}

.stApp [data-baseweb="tab-list"] button:hover p,
.stApp [data-baseweb="tab-list"] button:hover span {
    color: #FFFFFF !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, category TEXT NOT NULL, quantity INTEGER NOT NULL DEFAULT 0,
            unit TEXT NOT NULL DEFAULT 'pcs', min_stock INTEGER NOT NULL DEFAULT 5,
            supplier TEXT DEFAULT '', updated_at TEXT NOT NULL)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, category TEXT NOT NULL, price REAL NOT NULL DEFAULT 0,
            description TEXT DEFAULT '', created_at TEXT NOT NULL)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_code TEXT NOT NULL, product_name TEXT NOT NULL, quantity INTEGER NOT NULL,
            due_date TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'Pending',
            notes TEXT DEFAULT '', created_at TEXT NOT NULL)""")
        count = conn.execute("SELECT COUNT(*) FROM materials").fetchone()[0]
        if count == 0:
            today = date.today().isoformat()
            conn.executemany("""INSERT INTO materials(name,category,quantity,unit,min_stock,supplier,updated_at)
                VALUES(?,?,?,?,?,?,?)""", [
                ("Cotton Fabric","Fabric",120,"metres",30,"Sample supplier",today),
                ("Black Thread","Thread",18,"spools",10,"Sample supplier",today),
                ("Buttons","Accessories",250,"pcs",80,"Sample supplier",today),
                ("Zippers","Accessories",22,"pcs",25,"Sample supplier",today),
                ("Lining Fabric","Fabric",45,"metres",15,"Sample supplier",today),
            ])
        if conn.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
            today = date.today().isoformat()
            conn.executemany("""INSERT INTO products(name,category,price,description,created_at)
                VALUES(?,?,?,?,?)""", [
                ("Classic Cotton Shirt","Shirts",699,"Everyday cotton shirt",today),
                ("Festive Kurta","Ethnic Wear",1199,"Sample festive kurta",today),
                ("Printed Scarf","Accessories",349,"Lightweight printed scarf",today),
                ("Kids Gift Set","Gift Items",499,"Sample gift set",today),
            ])
        if conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0:
            today = date.today().isoformat()
            conn.executemany("""INSERT INTO orders(order_code,product_name,quantity,due_date,status,notes,created_at)
                VALUES(?,?,?,?,?,?,?)""", [
                ("ORD-1001","Classic Cotton Shirt",40,today,"In Progress","Sample order",today),
                ("ORD-1002","Festive Kurta",25,today,"Pending","Sample order",today),
                ("ORD-1003","Printed Scarf",60,today,"Completed","Sample order",today),
            ])

def query_df(sql, params=()):
    with connect() as conn:
        return pd.read_sql_query(sql, conn, params=params)

def execute(sql, params=()):
    with connect() as conn:
        conn.execute(sql, params)
        conn.commit()

init_db()

with st.sidebar:
    st.markdown("## 🧵 Garment Cluster")
    st.caption("Management workspace")
    page = st.radio("NAVIGATION", [
        "Dashboard", "Inventory", "Production Orders", "Product Catalogue", "About Project"
    ], label_visibility="visible")
    st.divider()
    st.caption("Student prototype • Sample data")
    st.caption("Nagpur Readymade Garment Cluster case study")

def hero(title, subtitle):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

if page == "Dashboard":
    hero("Cluster Overview", "A simple workspace to monitor materials, production and garment products.")
    materials = query_df("SELECT * FROM materials")
    products = query_df("SELECT * FROM products")
    orders = query_df("SELECT * FROM orders")
    low = materials[materials["quantity"] <= materials["min_stock"]] if not materials.empty else materials
    pending = int(orders["status"].isin(["Pending","In Progress"]).sum()) if not orders.empty else 0
    completed = int((orders["status"] == "Completed").sum()) if not orders.empty else 0
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Material types", f"{len(materials)}", help="Different materials recorded")
    c2.metric("Products listed", f"{len(products)}")
    c3.metric("Open production orders", f"{pending}")
    c4.metric("Low-stock alerts", f"{len(low)}", delta="Needs attention" if len(low) else "Stock looks okay", delta_color="inverse" if len(low) else "normal")
    st.markdown("### Production at a glance")
    left,right = st.columns([1.15,1])
    with left:
        st.markdown("#### Order status")
        if not orders.empty:
            status_counts = orders["status"].value_counts().reindex(["Pending","In Progress","Completed"], fill_value=0)
            chart_data = status_counts.rename_axis("Order Status").reset_index(name="Orders")
            st.bar_chart(
                chart_data,
                x="Order Status",
                y="Orders",
                color="#147d79",
                height=300,
            )
        else:
            st.info("No production orders yet.")
    with right:
        st.markdown("#### Inventory requiring attention")
        if low.empty:
            st.success("No materials are below their minimum stock level.")
        else:
            st.dataframe(low[["name","quantity","unit","min_stock"]].rename(columns={
                "name":"Material","quantity":"Available","unit":"Unit","min_stock":"Minimum level"
            }), use_container_width=True, hide_index=True)
    st.markdown("#### Recent production orders")
    if orders.empty:
        st.info("Add a production order from the Production Orders page.")
    else:
        st.dataframe(orders.sort_values("id", ascending=False)[["order_code","product_name","quantity","due_date","status"]].head(6).rename(columns={
            "order_code":"Order ID","product_name":"Product","quantity":"Qty","due_date":"Due date","status":"Status"
        }), use_container_width=True, hide_index=True)

elif page == "Inventory":
    hero("Inventory Management", "Record fabric and other supplies, update quantities, and spot low stock early.")
    tab1,tab2 = st.tabs(["📦 View inventory","➕ Add material"])
    with tab1:
        df = query_df("SELECT * FROM materials ORDER BY name")
        if not df.empty:
            search = st.text_input("Search materials", placeholder="Type a material name or category")
            if search:
                df = df[df["name"].str.contains(search, case=False, na=False) | df["category"].str.contains(search, case=False, na=False)]
            df["Stock status"] = df.apply(lambda r: "⚠️ Low stock" if r["quantity"] <= r["min_stock"] else "In stock", axis=1)
            st.dataframe(df[["id","name","category","quantity","unit","min_stock","supplier","Stock status"]].rename(columns={
                "id":"ID","name":"Material","category":"Category","quantity":"Quantity","unit":"Unit",
                "min_stock":"Minimum stock","supplier":"Supplier"
            }), use_container_width=True, hide_index=True)
            st.markdown("#### Update or remove a material")
            options = {f'{r["name"]} (ID {r["id"]})': int(r["id"]) for _,r in df.iterrows()}
            if options:
                chosen = st.selectbox("Choose material", list(options.keys()), key="edit_material")
                record = query_df("SELECT * FROM materials WHERE id=?", (options[chosen],)).iloc[0]
                with st.form("update_material_form"):
                    a,b,c = st.columns(3)
                    qty = a.number_input("Current quantity", min_value=0, value=int(record["quantity"]))
                    min_stock = b.number_input("Minimum stock alert", min_value=0, value=int(record["min_stock"]))
                    supplier = c.text_input("Supplier", value=str(record["supplier"] or ""))
                    save = st.form_submit_button("Save changes", type="primary")
                if save:
                    execute("UPDATE materials SET quantity=?,min_stock=?,supplier=?,updated_at=? WHERE id=?",
                            (int(qty),int(min_stock),supplier,date.today().isoformat(),int(record["id"])))
                    st.success("Inventory updated.")
                    st.rerun()
                if st.button("Delete selected material", type="secondary"):
                    execute("DELETE FROM materials WHERE id=?", (int(record["id"]),))
                    st.success("Material deleted.")
                    st.rerun()
        else:
            st.info("No materials found. Add one in the next tab.")
    with tab2:
        with st.form("add_material_form", clear_on_submit=True):
            a,b = st.columns(2)
            name = a.text_input("Material name", placeholder="e.g. Cotton fabric")
            category = b.selectbox("Category", ["Fabric","Thread","Accessories","Packaging","Other"])
            c,d,e = st.columns(3)
            quantity = c.number_input("Available quantity", min_value=0, value=0)
            unit = d.selectbox("Unit", ["pcs","metres","kg","spools","rolls","sets"])
            min_stock = e.number_input("Alert when stock reaches", min_value=0, value=5)
            supplier = st.text_input("Supplier (optional)")
            submit = st.form_submit_button("Add material", type="primary")
        if submit:
            if not name.strip():
                st.error("Please enter a material name.")
            else:
                execute("INSERT INTO materials(name,category,quantity,unit,min_stock,supplier,updated_at) VALUES(?,?,?,?,?,?,?)",
                        (name.strip(),category,int(quantity),unit,int(min_stock),supplier.strip(),date.today().isoformat()))
                st.success(f"{name} added to inventory.")
                st.rerun()

elif page == "Production Orders":
    hero("Production Orders", "Track each order from pending work to production and completion.")
    tab1,tab2 = st.tabs(["📋 Order list","➕ Create order"])
    with tab1:
        df = query_df("SELECT * FROM orders ORDER BY id DESC")
        if not df.empty:
            filter_status = st.selectbox("Filter by status", ["All","Pending","In Progress","Completed"])
            shown = df if filter_status == "All" else df[df["status"] == filter_status]
            st.dataframe(shown[["id","order_code","product_name","quantity","due_date","status","notes"]].rename(columns={
                "id":"ID","order_code":"Order ID","product_name":"Product","quantity":"Quantity",
                "due_date":"Due date","status":"Status","notes":"Notes"
            }), use_container_width=True, hide_index=True)
            st.markdown("#### Update order status")
            labels = {f'{r["order_code"]} — {r["product_name"]}': int(r["id"]) for _,r in df.iterrows()}
            chosen = st.selectbox("Choose order", list(labels.keys()))
            rec = df[df["id"] == labels[chosen]].iloc[0]
            with st.form("status_form"):
                new_status = st.selectbox("New status", ["Pending","In Progress","Completed"], index=["Pending","In Progress","Completed"].index(rec["status"]))
                new_due = st.date_input("Due date", value=date.fromisoformat(rec["due_date"]))
                new_notes = st.text_input("Notes", value=str(rec["notes"] or ""))
                save_status = st.form_submit_button("Update order", type="primary")
            if save_status:
                execute("UPDATE orders SET status=?,due_date=?,notes=? WHERE id=?",
                        (new_status,new_due.isoformat(),new_notes,int(rec["id"])))
                st.success("Order updated.")
                st.rerun()
            if st.button("Delete selected order"):
                execute("DELETE FROM orders WHERE id=?", (int(rec["id"]),))
                st.success("Order deleted.")
                st.rerun()
        else:
            st.info("No orders yet. Create one in the next tab.")
    with tab2:
        products = query_df("SELECT name FROM products ORDER BY name")
        product_names = products["name"].tolist() if not products.empty else []
        with st.form("new_order_form", clear_on_submit=True):
            order_code = st.text_input("Order ID", value=f"ORD-{1000 + int(query_df('SELECT COUNT(*) AS n FROM orders').iloc[0]['n']) + 1}")
            if product_names:
                product_name = st.selectbox("Product", product_names)
            else:
                product_name = st.text_input("Product name")
            qty = st.number_input("Quantity to produce", min_value=1, value=10)
            due = st.date_input("Due date", value=date.today())
            status = st.selectbox("Initial status", ["Pending","In Progress","Completed"])
            notes = st.text_input("Notes (optional)")
            submit_order = st.form_submit_button("Create production order", type="primary")
        if submit_order:
            if not order_code.strip() or not product_name:
                st.error("Please provide an order ID and product.")
            else:
                execute("INSERT INTO orders(order_code,product_name,quantity,due_date,status,notes,created_at) VALUES(?,?,?,?,?,?,?)",
                        (order_code.strip(),product_name,int(qty),due.isoformat(),status,notes.strip(),date.today().isoformat()))
                st.success("Production order created.")
                st.rerun()

elif page == "Product Catalogue":
    hero("Product Catalogue", "A simple catalogue of garments and related products made by the cluster.")
    products = query_df("SELECT * FROM products ORDER BY name")
    if not products.empty:
        col1,col2 = st.columns([2,1])
        with col1:
            search = st.text_input("Search products", placeholder="Search by product or category")
        with col2:
            categories = ["All"] + sorted(products["category"].dropna().unique().tolist())
            cat = st.selectbox("Category", categories)
        shown = products.copy()
        if search:
            shown = shown[shown["name"].str.contains(search, case=False, na=False) | shown["category"].str.contains(search, case=False, na=False)]
        if cat != "All":
            shown = shown[shown["category"] == cat]
        cards = st.columns(3)
        icons = {"Shirts":"👕","Ethnic Wear":"🪡","Accessories":"🧣","Gift Items":"🎁"}
        for i,(_,p) in enumerate(shown.iterrows()):
            with cards[i % 3]:
                st.markdown(f"### {icons.get(p['category'],'🧵')} {p['name']}")
                st.caption(p["category"])
                st.markdown(f"**₹{p['price']:,.0f}**")
                st.write(p["description"] or "No description added.")
                st.divider()
    else:
        st.info("No products added yet.")
    with st.expander("➕ Add a product"):
        with st.form("add_product_form", clear_on_submit=True):
            name = st.text_input("Product name")
            category = st.selectbox("Category", ["Shirts","Ethnic Wear","Accessories","Gift Items","Other"])
            price = st.number_input("Selling price (₹)", min_value=0.0, value=0.0, step=50.0)
            description = st.text_area("Short description")
            add = st.form_submit_button("Add product", type="primary")
        if add:
            if not name.strip():
                st.error("Please enter a product name.")
            else:
                execute("INSERT INTO products(name,category,price,description,created_at) VALUES(?,?,?,?,?)",
                        (name.strip(),category,float(price),description.strip(),date.today().isoformat()))
                st.success("Product added.")
                st.rerun()

else:
    hero("About This Project", "A student-built prototype inspired by the Nagpur Readymade Garment Cluster case study.")
    st.markdown("""
    ### Project objective
    Provide a simple place to record materials, monitor stock levels, track production orders and display a product catalogue.

    ### Technology used
    - **Python + Streamlit:** application and interface
    - **SQLite:** local database
    - **Pandas:** tables and data handling

    ### Important scope note
    This is a student prototype, not an official SFURTI application. The initial records are fictional sample data for demonstration only; they are not actual cluster business records and have not been verified with cluster members.
    """)
    st.info("Tip: use the Inventory, Production Orders and Product Catalogue pages to add, edit and remove records. Your changes are saved in the local SQLite database.")
