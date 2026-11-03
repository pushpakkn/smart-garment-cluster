import sqlite3
import hashlib, hmac, secrets, re
from pathlib import Path
from datetime import date, datetime
import pandas as pd
import streamlit as st

DB = Path(__file__).parent / "garment_cluster.db"
st.set_page_config(page_title="Artisan Integrated Network & Commerce", page_icon="🧵", layout="wide")

st.markdown("""
<style>
:root{color-scheme:light}
.stApp{background:#f0f2f5!important;color:#1c1e21!important}
.block-container{max-width:1440px;padding-top:1.4rem;padding-bottom:3rem}
[data-testid="stHeader"]{background:#f0f2f5!important}

/* Facebook-inspired clean white sidebar */
[data-testid="stSidebar"]{background:#ffffff!important;border-right:1px solid #dddfe2!important}
[data-testid="stSidebar"] *{color:#1c1e21!important}
[data-testid="stSidebar"] > div:first-child{padding-top:1.15rem}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2{
  color:#1c1e21!important;font-size:1.12rem!important;letter-spacing:-.035em;
  font-weight:780!important;margin-bottom:.12rem!important
}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p{
  color:#65676b!important;font-size:.76rem!important;line-height:1.45
}
.nav-kicker{
  color:#65676b!important;font-size:.65rem!important;font-weight:800!important;
  letter-spacing:.14em!important;text-transform:uppercase!important;margin:1.05rem 0 .22rem!important
}
.nav-hint{color:#65676b!important;font-size:.72rem!important;margin:0 0 .48rem!important}
[data-testid="stSidebar"] [data-testid="stRadio"] > div{gap:.19rem!important}
[data-testid="stSidebar"] [data-testid="stRadio"] label{
  display:flex!important;align-items:center!important;background:transparent!important;
  border:1px solid transparent!important;border-radius:8px!important;
  padding:.39rem .58rem!important;margin:0!important;min-height:2.18rem!important;
  transition:background-color .14s ease,border-color .14s ease!important
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{
  background:#f0f2f5!important;border-color:#e4e6eb!important
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked){
  background:#e7f3ff!important;border-color:#d8eaff!important;
  box-shadow:inset 3px 0 0 #1877f2!important
}
[data-testid="stSidebar"] [data-testid="stRadio"] label p{
  color:#1c1e21!important;font-size:.83rem!important;font-weight:570!important
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p{
  color:#0866ff!important;font-weight:730!important
}
[data-testid="stSidebar"] [data-testid="stRadio"] input{accent-color:#1877f2!important}
[data-testid="stSidebar"] [data-testid="stRadio"] input:focus-visible + div{
  outline:2px solid #1877f2!important;outline-offset:2px!important
}
.sidebar-user-label{color:#1c1e21!important;font-size:.74rem!important;font-weight:750!important;margin:.78rem 0 .28rem!important}
[data-testid="stSidebar"] [data-testid="stTextInput"] input{
  border-radius:8px!important;min-height:2.45rem!important
}
[data-testid="stSidebar"] [data-testid="stTextInput"] input:focus{
  border-color:#1877f2!important;box-shadow:0 0 0 2px rgba(24,119,242,.16)!important
}
.sidebar-foot{
  border-top:1px solid #e4e6eb;padding-top:.78rem;margin-top:1rem;
  color:#65676b!important;font-size:.69rem!important;line-height:1.55;letter-spacing:.025em
}

/* Main canvas, hero and typography */
[data-testid="stMainBlockContainer"]{animation:content-enter .16s ease-out both}
@keyframes content-enter{from{opacity:.92;transform:translateY(2px)}to{opacity:1;transform:translateY(0)}}
@media(prefers-reduced-motion:reduce){
  [data-testid="stMainBlockContainer"]{animation:none!important}
  [data-testid="stSidebar"] [data-testid="stRadio"] label{transition:none!important}
}
.hero{
  padding:1.45rem 1.65rem;border-radius:12px;
  background:linear-gradient(115deg,#1877f2,#0866ff);
  margin-bottom:1.15rem
}
.hero h1,.hero p{color:#ffffff!important}
.hero h1{margin:0 0 .35rem}
.hero p{margin:0;color:#eaf3ff!important}
h1,h2,h3,h4,h5,h6,p,li,label,[data-testid="stMarkdownContainer"],
[data-testid="stWidgetLabel"],[data-testid="stCaptionContainer"]{color:#1c1e21!important}
[data-testid="stCaptionContainer"] p,.stCaption{color:#65676b!important}

/* Inputs */
[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea,[data-baseweb="select"]>div{
  background:#ffffff!important;color:#1c1e21!important;
  -webkit-text-fill-color:#1c1e21!important;border:1px solid #ccd0d5!important;border-radius:8px!important
}
[data-testid="stTextInput"] input::placeholder,[data-testid="stTextArea"] textarea::placeholder{
  color:#65676b!important;-webkit-text-fill-color:#65676b!important;opacity:1!important
}
[data-baseweb="select"] *,[role="option"]{color:#1c1e21!important}
[data-testid="stWidgetLabel"] p{color:#1c1e21!important;font-weight:600!important}

/* Cards, metrics, buttons, tabs and tables */
[data-testid="stMetric"]{
  background:#ffffff!important;border:1px solid #dddfe2!important;
  padding:16px!important;border-radius:10px!important
}
[data-testid="stMetricLabel"],[data-testid="stMetricLabel"] *,
[data-testid="stMetricValue"],[data-testid="stMetricValue"] *{color:#1c1e21!important}
.stButton button[kind="primary"],.stFormSubmitButton button[kind="primary"]{
  background:#1877f2!important;border:1px solid #1877f2!important;color:#ffffff!important;border-radius:7px!important
}
.stButton button[kind="primary"]:hover,.stFormSubmitButton button[kind="primary"]:hover{
  background:#166fe5!important;border-color:#166fe5!important
}
.stButton button:not([kind="primary"]),.stFormSubmitButton button:not([kind="primary"]){
  background:#e4e6eb!important;color:#1c1e21!important;border:1px solid #e4e6eb!important;border-radius:7px!important
}
[data-testid="stExpander"]{
  background:#ffffff!important;border:1px solid #dddfe2!important;border-radius:10px!important
}
[data-testid="stExpander"] summary,[data-testid="stExpander"] summary *{color:#1c1e21!important}
[data-baseweb="tab-list"] button{color:#65676b!important}
[data-baseweb="tab-list"] button[aria-selected="true"]{
  color:#0866ff!important;border-bottom:3px solid #1877f2!important
}
.listing-card{background:#ffffff;border:1px solid #dddfe2;border-radius:10px;padding:1rem;margin:.5rem 0}
.listing-card h3{color:#1c1e21!important}
.listing-price{color:#0866ff!important;font-size:1.08rem;font-weight:750}

/* Floating Messenger-style chat launcher and pop-up */
div[data-testid="stPopover"]{
  position:fixed!important;right:24px!important;bottom:22px!important;
  z-index:99999!important;width:auto!important
}
div[data-testid="stPopover"] > button{
  background:#1877f2!important;color:#fff!important;border:0!important;
  border-radius:999px!important;padding:.72rem 1.15rem!important;
  min-height:3rem!important;font-weight:750!important;
  box-shadow:0 5px 18px rgba(24,119,242,.28)!important
}
div[data-testid="stPopover"] > button:hover{background:#166fe5!important}
div[data-testid="stPopoverBody"]{
  width:min(370px,calc(100vw - 32px))!important;
  max-height:min(620px,75vh)!important;overflow-y:auto!important;
  border:1px solid #dddfe2!important;border-radius:14px!important;
  box-shadow:0 12px 38px rgba(0,0,0,.20)!important;background:#fff!important
}
</style>
""", unsafe_allow_html=True)

def db():
    c=sqlite3.connect(DB, check_same_thread=False)
    c.row_factory=sqlite3.Row
    return c
def q(sql, p=()):
    with db() as c: return pd.read_sql_query(sql,c,params=p)
def x(sql,p=()):
    with db() as c: c.execute(sql,p); c.commit()

def password_hash(password,salt):
    return hashlib.pbkdf2_hmac("sha256",password.encode(),salt.encode(),240000).hex()

def get_user():
    uid=st.session_state.get("auth_user_id")
    if not uid: return None
    rows=q("SELECT id,username,email,role,full_name,location,craft,bio FROM users WHERE id=?",(uid,))
    return None if rows.empty else rows.iloc[0].to_dict()

def register_user(username,email,password,role,full_name,location,craft,bio):
    username,email=username.strip(),email.strip().lower()
    if len(username)<3 or not re.fullmatch(r"[A-Za-z0-9_.-]+",username): return False,"Username must be at least 3 characters."
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+",email): return False,"Enter a valid email."
    if len(password)<8: return False,"Password must contain at least 8 characters."
    salt=secrets.token_hex(16)
    try:
        x("INSERT INTO users(username,email,password_hash,salt,role,full_name,location,craft,bio,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
          (username,email,password_hash(password,salt),salt,role,full_name.strip(),location.strip(),craft.strip(),bio.strip(),datetime.now().isoformat(timespec="seconds")))
        return True,"Account created. Sign in to continue."
    except sqlite3.IntegrityError: return False,"Username or email already exists."

def login_user(identifier,password):
    rows=q("SELECT * FROM users WHERE lower(username)=lower(?) OR lower(email)=lower(?)",(identifier.strip(),identifier.strip()))
    if rows.empty: return None
    r=rows.iloc[0]
    if hmac.compare_digest(password_hash(password,str(r.salt)),str(r.password_hash)): return int(r.id)
    return None

def init():
    with db() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS materials(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,category TEXT NOT NULL,quantity INTEGER NOT NULL DEFAULT 0,unit TEXT NOT NULL DEFAULT 'pcs',min_stock INTEGER NOT NULL DEFAULT 5,supplier TEXT DEFAULT '',updated_at TEXT NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,category TEXT NOT NULL,price REAL NOT NULL DEFAULT 0,description TEXT DEFAULT '',created_at TEXT NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT,order_code TEXT NOT NULL,product_name TEXT NOT NULL,quantity INTEGER NOT NULL,due_date TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'Pending',notes TEXT DEFAULT '',created_at TEXT NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS listings(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,category TEXT NOT NULL,description TEXT DEFAULT '',price REAL NOT NULL,quantity INTEGER NOT NULL,unit TEXT NOT NULL,seller TEXT NOT NULL,location TEXT DEFAULT '',status TEXT NOT NULL DEFAULT 'Available',created_at TEXT NOT NULL, image BLOB)""")
        # Backward-compatible migration for existing hosted/local databases.
        cols = [r[1] for r in c.execute("PRAGMA table_info(listings)").fetchall()]
        if "image" not in cols:
            c.execute("ALTER TABLE listings ADD COLUMN image BLOB")
        c.execute("""CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT,sender TEXT NOT NULL,recipient TEXT NOT NULL,subject TEXT NOT NULL,body TEXT NOT NULL,listing_id INTEGER,sent_at TEXT NOT NULL,read_status INTEGER NOT NULL DEFAULT 0)""")
        c.execute("""CREATE TABLE IF NOT EXISTS inquiries(id INTEGER PRIMARY KEY AUTOINCREMENT,listing_id INTEGER NOT NULL,buyer TEXT NOT NULL,quantity INTEGER NOT NULL,message TEXT DEFAULT '',status TEXT NOT NULL DEFAULT 'New',created_at TEXT NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL,email TEXT UNIQUE NOT NULL,password_hash TEXT NOT NULL,salt TEXT NOT NULL,role TEXT NOT NULL,full_name TEXT NOT NULL,location TEXT DEFAULT '',craft TEXT DEFAULT '',bio TEXT DEFAULT '',created_at TEXT NOT NULL)""")
        # Migrate older hosted databases: CREATE TABLE IF NOT EXISTS does not add
        # columns to an existing users table. Add newer profile fields safely.
        user_cols = [r[1] for r in c.execute("PRAGMA table_info(users)").fetchall()]
        user_migrations = [
            ("email", "TEXT NOT NULL DEFAULT ''"),
            ("password_hash", "TEXT NOT NULL DEFAULT ''"),
            ("salt", "TEXT NOT NULL DEFAULT ''"),
            ("role", "TEXT NOT NULL DEFAULT 'Buyer'"),
            ("full_name", "TEXT NOT NULL DEFAULT ''"),
            ("location", "TEXT DEFAULT ''"),
            ("craft", "TEXT DEFAULT ''"),
            ("bio", "TEXT DEFAULT ''"),
            ("created_at", "TEXT NOT NULL DEFAULT ''"),
        ]
        for col, definition in user_migrations:
            if col not in user_cols:
                c.execute(f"ALTER TABLE users ADD COLUMN {col} {definition}")
        listing_cols=[r[1] for r in c.execute("PRAGMA table_info(listings)").fetchall()]
        if "owner_user_id" not in listing_cols: c.execute("ALTER TABLE listings ADD COLUMN owner_user_id INTEGER")
        inquiry_cols=[r[1] for r in c.execute("PRAGMA table_info(inquiries)").fetchall()]
        for col,definition in [("buyer_user_id","INTEGER"),("artisan_user_id","INTEGER"),("order_id","INTEGER")]:
            if col not in inquiry_cols: c.execute(f"ALTER TABLE inquiries ADD COLUMN {col} {definition}")
        order_cols=[r[1] for r in c.execute("PRAGMA table_info(orders)").fetchall()]
        for col,definition in [("listing_id","INTEGER"),("buyer_user_id","INTEGER"),("artisan_user_id","INTEGER"),("inquiry_id","INTEGER")]:
            if col not in order_cols: c.execute(f"ALTER TABLE orders ADD COLUMN {col} {definition}")
        today=date.today().isoformat()
        if c.execute("SELECT COUNT(*) FROM materials").fetchone()[0]==0:
            c.executemany("INSERT INTO materials(name,category,quantity,unit,min_stock,supplier,updated_at) VALUES(?,?,?,?,?,?,?)",[
            ("Cotton Fabric","Fabric",120,"metres",30,"Sample supplier",today),("Black Thread","Thread",18,"spools",10,"Sample supplier",today),("Buttons","Accessories",250,"pcs",80,"Sample supplier",today),("Zippers","Accessories",22,"pcs",25,"Sample supplier",today)])
        if c.execute("SELECT COUNT(*) FROM products").fetchone()[0]==0:
            c.executemany("INSERT INTO products(name,category,price,description,created_at) VALUES(?,?,?,?,?)",[
            ("Classic Cotton Shirt","Shirts",699,"Demo product",today),("Festive Kurta","Ethnic Wear",1199,"Demo product",today)])
        # Add a consistent catalogue set for presentations, including upgrades of older databases.
        catalogue_demo = [
            ("Classic Cotton Shirt", "Shirts", 699, "Breathable everyday cotton shirt with a regular fit, reinforced seams and a clean button-down finish.", today),
            ("Festive Zari Kurta", "Ethnic Wear", 1499, "Festive kurta featuring subtle zari detailing, a comfortable lining and a straight silhouette.", today),
            ("Indigo Printed Dupatta", "Accessories", 549, "Lightweight cotton dupatta with an indigo-inspired repeating print and finished edges.", today),
            ("Handcrafted Tote Bag", "Bags", 799, "Reusable fabric tote with reinforced handles and a handcrafted decorative panel.", today),
            ("Kids Occasion Waistcoat", "Kids Wear", 899, "Lightweight occasion waistcoat designed for comfortable layering and easy movement.", today),
            ("Block Print Cushion Cover", "Home Textiles", 399, "Decorative cushion cover with a repeat block-print pattern and concealed closure.", today),
            ("Embroidered Stole", "Accessories", 999, "Soft woven stole finished with hand-embroidered floral accents along the border.", today),
            ("Cotton Lounge Set", "Loungewear", 1299, "Two-piece cotton lounge set designed for relaxed everyday comfort.", today),
            ("Decorative Fabric Gift Set", "Gift Items", 599, "Curated set of decorative fabric pieces suitable for gifting and craft projects.", today),
            ("Printed Kids Frock", "Kids Wear", 749, "Printed cotton frock with a comfortable fit and neatly finished seams.", today),
        ]
        for product in catalogue_demo:
            if not c.execute("SELECT 1 FROM products WHERE name=?", (product[0],)).fetchone():
                c.execute("INSERT INTO products(name,category,price,description,created_at) VALUES(?,?,?,?,?)", product)
        # Expand the materials table for a useful but compact stock-control demonstration.
        material_demo = [
            ("Cotton Fabric", "Fabric", 120, "metres", 30, "Demo Fabric Supply", today),
            ("Silk Blend Fabric", "Fabric", 42, "metres", 15, "Demo Textile House", today),
            ("Black Stitching Thread", "Thread", 18, "spools", 10, "Demo Thread Supply", today),
            ("Embroidery Thread Set", "Thread", 24, "sets", 8, "Demo Thread Supply", today),
            ("Metal Buttons", "Accessories", 250, "pcs", 80, "Demo Trim Supply", today),
            ("Concealed Zippers", "Accessories", 22, "pcs", 25, "Demo Trim Supply", today),
            ("Lining Fabric", "Fabric", 45, "metres", 15, "Demo Fabric Supply", today),
            ("Packaging Covers", "Packaging", 90, "pcs", 30, "Demo Packaging Co.", today),
        ]
        for material in material_demo:
            if not c.execute("SELECT 1 FROM materials WHERE name=?", (material[0],)).fetchone():
                c.execute("INSERT INTO materials(name,category,quantity,unit,min_stock,supplier,updated_at) VALUES(?,?,?,?,?,?,?)", material)
        if c.execute("SELECT COUNT(*) FROM orders").fetchone()[0]==0:
            c.execute("INSERT INTO orders(order_code,product_name,quantity,due_date,status,notes,created_at) VALUES(?,?,?,?,?,?,?)",("ORD-1001","Classic Cotton Shirt",40,today,"In Progress","Sample order",today))
        if c.execute("SELECT COUNT(*) FROM listings").fetchone()[0]==0:
            c.executemany("INSERT INTO listings(title,category,description,price,quantity,unit,seller,location,status,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",[
            ("Madhubani Floral Motif Set","Artwork","Original Madhubani-inspired motif collection for kurta panels and dupattas.",650,12,"designs","Studio Rangrekha","Nagpur","Available",today),
            ("Warli Border Illustration","Artwork","Hand-drawn Warli-inspired border artwork for stoles, shirts and home textiles.",480,18,"designs","Adivasi Art Collective","Nagpur","Available",today),
            ("Mirror-Work Embroidery Patches","Embroidery","Handcrafted mirror-work patches for jackets, bags and festive garments.",55,100,"pcs","Sakhi Embroidery Unit","Nagpur","Available",today),
            ("Block-Print Floral Artwork","Print Designs","Repeat floral artwork suitable for cotton fabric printing.",720,8,"designs","PrintCraft Studio","Nagpur","Available",today),
            ("Cotton Fabric Roll","Fabric","Demo raw material listing for cotton fabric.",185,120,"metres","Demo Fabric Supplier","Nagpur","Available",today),
            ("Bulk Buttons","Accessories","Demo raw material listing for garment making.",2.5,250,"pcs","Demo Accessories Shop","Nagpur","Available",today),
            ("Stitching Thread","Thread","Demo raw material listing for thread spools.",38,18,"spools","Demo Thread Supplier","Nagpur","Available",today)])
init()


# Ensure the artisan marketplace has demo artwork even when upgrading an older database.
art_demo = [
    ("Madhubani Floral Motif Set","Artwork","Original Madhubani-inspired motif collection for kurta panels and dupattas.",650,12,"designs","Studio Rangrekha","Nagpur","Available",date.today().isoformat()),
    ("Warli Border Illustration","Artwork","Hand-drawn Warli-inspired border artwork for stoles, shirts and home textiles.",480,18,"designs","Adivasi Art Collective","Nagpur","Available",date.today().isoformat()),
    ("Mirror-Work Embroidery Patches","Embroidery","Handcrafted mirror-work patches for jackets, bags and festive garments.",55,100,"pcs","Sakhi Embroidery Unit","Nagpur","Available",date.today().isoformat()),
    ("Block-Print Floral Artwork","Print Designs","Repeat floral artwork suitable for cotton fabric printing.",720,8,"designs","PrintCraft Studio","Nagpur","Available",date.today().isoformat())
]
with db() as conn:
    for item in art_demo:
        if not conn.execute("SELECT 1 FROM listings WHERE title=?", (item[0],)).fetchone():
            conn.execute("INSERT INTO listings(title,category,description,price,quantity,unit,seller,location,status,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",item)
    conn.commit()

# Attach included sample artwork images to the matching demo listings.
sample_images = {
    "Madhubani Floral Motif Set": "madhubani_motifs.png",
    "Warli Border Illustration": "warli_art.png",
    "Mirror-Work Embroidery Patches": "mirror_embroidery.png",
    "Block-Print Floral Artwork": "textile_print.png"
}
with db() as conn:
    for title, filename in sample_images.items():
        image_path = Path(__file__).parent / "artwork_samples" / filename
        if image_path.exists():
            conn.execute("UPDATE listings SET image=? WHERE title=? AND image IS NULL",
                         (image_path.read_bytes(), title))
    conn.commit()

# Seed repeatable classroom demo accounts, listings and chat conversations.
# These accounts contain fictional data and are intended only for demonstrations.
demo_accounts = [
    ("buyer", "buyer.demo@artisync.example", "Buyer", "Aarav Mehta", "Nagpur", "", "Demo buyer account for testing enquiries and chats."),
    ("artisan", "artisan.demo@artisync.example", "Artisan", "Meera Kulkarni", "Nagpur", "Madhubani & textile art", "Demo artisan account showcasing artwork listings."),
    ("artisan2", "artisan2.demo@artisync.example", "Artisan", "Riya Sharma", "Nagpur", "Embroidery & handcrafted work", "Second demo artisan for multi-contact conversations."),
]
with db() as conn:
    for username,email,role,full_name,location,craft,bio in demo_accounts:
        if not conn.execute("SELECT 1 FROM users WHERE username=?", (username,)).fetchone():
            salt=secrets.token_hex(16)
            conn.execute(
                "INSERT INTO users(username,email,password_hash,salt,role,full_name,location,craft,bio,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
                (username,email,password_hash("demo1234",salt),salt,role,full_name,location,craft,bio,datetime.now().isoformat(timespec="seconds"))
            )
    demo_user_ids={r["username"]:r["id"] for r in conn.execute(
        "SELECT id,username FROM users WHERE username IN ('buyer','artisan','artisan2')"
    ).fetchall()}
    # Attach existing public sample listings to demo artisan accounts so chat and inquiries work.
    conn.execute("UPDATE listings SET owner_user_id=? WHERE seller IN ('Studio Rangrekha','Adivasi Art Collective','PrintCraft Studio') AND owner_user_id IS NULL",
                 (demo_user_ids["artisan"],))
    conn.execute("UPDATE listings SET owner_user_id=? WHERE seller='Sakhi Embroidery Unit' AND owner_user_id IS NULL",
                 (demo_user_ids["artisan2"],))
    # Additional public sample listings to make both marketplaces feel populated.
    extra_listings = [
        ("Festive Peacock Motif","Artwork","Decorative peacock composition for festive apparel and dupatta panels.",890,6,"designs","Meera Kulkarni","Nagpur","Available","artisan"),
        ("Geometric Warli Border","Artwork","Repeatable border design for stoles, cushion covers and apparel.",520,15,"designs","Meera Kulkarni","Nagpur","Available","artisan"),
        ("Hand Embroidered Floral Patches","Embroidery","Small-batch floral patches for jackets, bags and accessories.",85,60,"pcs","Riya Sharma","Nagpur","Available","artisan2"),
        ("Decorative Thread Tassels","Handcrafted Accessories","Hand-finished tassels for dupattas, bags and home décor.",35,80,"pcs","Riya Sharma","Nagpur","Available","artisan2"),
        ("Indigo Cotton Fabric","Fabric","Pre-cut indigo cotton fabric suitable for sampling and small production runs.",210,75,"metres","Demo Fabric Supply","Nagpur","Available",None),
        ("Embroidery Thread Set","Thread","Assorted colour thread set for hand embroidery work.",160,24,"sets","Demo Thread Supply","Nagpur","Available",None),
        ("Metal Button Assortment","Accessories","Assorted decorative buttons for sample garment production.",4,300,"pcs","Demo Trim Supply","Nagpur","Available",None),
    ]
    for title,category,description,price,quantity,unit,seller,location,status,owner in extra_listings:
        if not conn.execute("SELECT 1 FROM listings WHERE title=?", (title,)).fetchone():
            owner_id=demo_user_ids.get(owner) if owner else None
            conn.execute("""INSERT INTO listings(title,category,description,price,quantity,unit,seller,location,status,created_at,owner_user_id)
                            VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                         (title,category,description,price,quantity,unit,seller,location,status,date.today().isoformat(),owner_id))
    # Link legacy demo artwork records to the artisan account for functional chat/inquiry buttons.
    conn.execute("UPDATE listings SET owner_user_id=? WHERE seller='Studio Rangrekha' AND owner_user_id IS NULL",
                 (demo_user_ids["artisan"],))
    # Populate management tables without duplicating records on later reruns.
    materials = [
        ("Silk Blend Fabric","Fabric",42,"metres",20,"Demo Textile Supplier"),
        ("Embroidery Thread","Thread",9,"spools",12,"Demo Thread Supplier"),
        ("Decorative Buttons","Accessories",180,"pcs",50,"Demo Trim Supplier"),
        ("Packaging Pouches","Packaging",65,"pcs",25,"Demo Packaging Supplier"),
        ("Lining Material","Fabric",28,"metres",15,"Demo Textile Supplier"),
    ]
    for name,category,qty,unit,minimum,supplier in materials:
        if not conn.execute("SELECT 1 FROM materials WHERE name=?", (name,)).fetchone():
            conn.execute("INSERT INTO materials(name,category,quantity,unit,min_stock,supplier,updated_at) VALUES(?,?,?,?,?,?,?)",
                         (name,category,qty,unit,minimum,supplier,date.today().isoformat()))
    products = [
        ("Indigo Printed Kurta","Ethnic Wear",1499,"Demo catalogue item with block-print detailing."),
        ("Handcrafted Tote Bag","Accessories",799,"Demo artisan-made cotton tote bag."),
        ("Embroidered Cushion Cover","Gift Items",599,"Demo cushion cover with hand embroidery."),
        ("Printed Cotton Stole","Accessories",449,"Demo lightweight printed stole."),
        ("Kids Festive Set","Gift Items",999,"Demo festive clothing set."),
        ("Classic Cotton Shirt - Blue","Shirts",849,"Demo cotton shirt in indigo blue."),
    ]
    for name,category,price,description in products:
        if not conn.execute("SELECT 1 FROM products WHERE name=?", (name,)).fetchone():
            conn.execute("INSERT INTO products(name,category,price,description,created_at) VALUES(?,?,?,?,?)",
                         (name,category,price,description,date.today().isoformat()))
    orders = [
        ("ORD-DEMO-1002","Festive Kurta",18,"Pending","Awaiting material confirmation."),
        ("ORD-DEMO-1003","Printed Cotton Stole",35,"In Progress","Printing completed; finishing underway."),
        ("ORD-DEMO-1004","Handcrafted Tote Bag",20,"Completed","Ready for quality check."),
        ("ORD-DEMO-1005","Indigo Printed Kurta",12,"In Progress","Stitching in progress."),
        ("ORD-DEMO-1006","Embroidered Cushion Cover",24,"Pending","Scheduled for next production slot."),
        ("ORD-DEMO-1007","Kids Festive Set",10,"Completed","Demo order completed."),
    ]
    for code,product,qty,status,notes in orders:
        if not conn.execute("SELECT 1 FROM orders WHERE order_code=?", (code,)).fetchone():
            conn.execute("INSERT INTO orders(order_code,product_name,quantity,due_date,status,notes,created_at) VALUES(?,?,?,?,?,?,?)",
                         (code,product,qty,date.today().isoformat(),status,notes,date.today().isoformat()))
    # Seed buyer-to-artisan chats. Existing user conversations are never overwritten.
    chat_examples = [
        ("buyer","artisan","Madhubani artwork enquiry","Hello Meera, can the peacock motif be customised to use teal and gold colours?"),
        ("artisan","buyer","Madhubani artwork enquiry","Yes! I can prepare a colour variation. The usual turnaround for a custom design is 3–4 days."),
        ("buyer","artisan","Madhubani artwork enquiry","That works. Could you also share a preview before confirming the quantity?"),
        ("artisan","buyer","Madhubani artwork enquiry","Of course. I will share a digital preview first."),
        ("buyer","artisan2","Embroidery sample request","Hi Riya, are the floral patches available in a set of 20?"),
        ("artisan2","buyer","Embroidery sample request","Hello! Yes, I can prepare a set of 20. Would you prefer pastel or bright colours?"),
        ("buyer","artisan2","Embroidery sample request","Pastel colours would be ideal. Please share the estimated price."),
    ]
    for sender,recipient,subject,body in chat_examples:
        if not conn.execute("SELECT 1 FROM messages WHERE sender=? AND recipient=? AND body=?",
                            (sender,recipient,body)).fetchone():
            conn.execute("INSERT INTO messages(sender,recipient,subject,body,listing_id,sent_at,read_status) VALUES(?,?,?,?,NULL,?,0)",
                         (sender,recipient,subject,body,datetime.now().isoformat(timespec="minutes")))
    conn.commit()

def hero(t,s): st.markdown(f'<div class="hero"><h1>{t}</h1><p>{s}</p></div>',unsafe_allow_html=True)
def _select_market_nav():
    st.session_state["active_page"]=st.session_state["market_nav"]
def _select_operations_nav():
    st.session_state["active_page"]=st.session_state["operations_nav"]

signed_in=get_user()
with st.sidebar:
    st.markdown("## Artisan Integrated Network & Commerce")
    st.caption("A digital workspace for artisans and garment businesses")
    if signed_in:
        st.markdown(f"**{signed_in['full_name']}**")
        st.caption(f"{signed_in['role']} · {signed_in['location'] or 'Location not set'}")
        if st.button("Sign out",use_container_width=True):
            st.session_state.pop("auth_user_id",None)
            st.session_state.pop("active_page",None)
            st.rerun()
    else:
        st.markdown('<div class="nav-kicker">Guest access</div>',unsafe_allow_html=True)
        st.caption("Browse all listings without an account.")
        with st.expander("Sign in / Create account"):
            login_tab,register_tab=st.tabs(["Sign in","Register"])
            with login_tab:
                with st.form("login_form"):
                    login_id=st.text_input("Username or email")
                    login_pw=st.text_input("Password",type="password")
                    login_submit=st.form_submit_button("Sign in",type="primary")
                if login_submit:
                    uid=login_user(login_id,login_pw)
                    if uid:
                        st.session_state["auth_user_id"]=uid
                        st.rerun()
                    else: st.error("Incorrect username/email or password.")
            with register_tab:
                with st.form("register_form"):
                    full_name=st.text_input("Full name")
                    username=st.text_input("Username")
                    email=st.text_input("Email")
                    role=st.selectbox("Account type",["Buyer","Artisan"])
                    location=st.text_input("Location",value="Nagpur")
                    craft=st.text_input("Craft / specialisation",disabled=(role!="Artisan"))
                    bio=st.text_area("Short profile description")
                    pw=st.text_input("Password (8+ characters)",type="password")
                    pw2=st.text_input("Confirm password",type="password")
                    reg=st.form_submit_button("Create account",type="primary")
                if reg:
                    if not full_name.strip(): st.error("Enter your full name.")
                    elif pw!=pw2: st.error("Passwords do not match.")
                    else:
                        ok,msg=register_user(username,email,pw,role,full_name,location,craft,bio)
                        (st.success if ok else st.error)(msg)

        st.markdown("**Quick demo access**")
        demo_left,demo_right=st.columns(2)
        if demo_left.button("Buyer demo",use_container_width=True):
            demo_uid=q("SELECT id FROM users WHERE username='buyer'")
            if not demo_uid.empty:
                st.session_state["auth_user_id"]=int(demo_uid.iloc[0]["id"])
                st.session_state["active_page"]="Chat Box"
                st.session_state["market_nav"]="Chat Box"
                st.rerun()
        if demo_right.button("Artisan demo",use_container_width=True):
            demo_uid=q("SELECT id FROM users WHERE username='artisan'")
            if not demo_uid.empty:
                st.session_state["auth_user_id"]=int(demo_uid.iloc[0]["id"])
                st.session_state["active_page"]="Chat Box"
                st.session_state["market_nav"]="Chat Box"
                st.rerun()
        st.caption("Demo password for manual sign-in: demo1234")
    st.markdown('<div class="nav-kicker">Marketplace</div>',unsafe_allow_html=True)
    market_options=["Artisan Marketplace","Raw Materials Marketplace"]
    if signed_in: market_options += ["Chat Box","Buyer Inquiries","My Profile"]
    st.session_state.setdefault("market_nav","Artisan Marketplace")
    if st.session_state["market_nav"] not in market_options: st.session_state["market_nav"]="Artisan Marketplace"
    st.radio("Marketplace navigation",market_options,key="market_nav",on_change=_select_market_nav,
             label_visibility="collapsed",
             format_func=lambda x:{"Artisan Marketplace":"🎨  Artisan Marketplace","Raw Materials Marketplace":"🧵  Raw Materials",
             "Chat Box":"💬  Chat Box","Buyer Inquiries":"🤝  Buyer Inquiries","My Profile":"👤  My Profile"}[x])
    st.markdown('<div class="nav-kicker">Cluster management</div>',unsafe_allow_html=True)
    ops=["Dashboard","Inventory","Production Orders","Product Catalogue","About Project"]
    if signed_in and signed_in["role"]=="Artisan": ops.append("My Listings")
    st.session_state.setdefault("operations_nav","Dashboard")
    if st.session_state["operations_nav"] not in ops: st.session_state["operations_nav"]="Dashboard"
    st.radio("Management navigation",ops,key="operations_nav",on_change=_select_operations_nav,
             label_visibility="collapsed",
             format_func=lambda x:{"Dashboard":"▦  Dashboard","Inventory":"📦  Inventory","Production Orders":"🧾  Production Orders",
             "Product Catalogue":"🛍️  Product Catalogue","About Project":"ⓘ  About Project","My Listings":"🗂️  My Listings"}[x])
    page=st.session_state.get("active_page","Artisan Marketplace")
    if page not in market_options+ops: page="Artisan Marketplace"
    st.markdown('<div class="sidebar-foot">PUBLIC LISTINGS · ACCOUNT REQUIRED TO PARTICIPATE</div>',unsafe_allow_html=True)

user=signed_in["username"] if signed_in else "Guest"

def render_marketplace(kind):
    artisan = kind == "artisan"
    if artisan:
        hero("Artisan & Artwork Marketplace","Discover original artwork, handcrafted details and designs created by local artisans.")
        allowed=["Artwork","Embroidery","Handcrafted Accessories","Print Designs","Textile Art"]
        heading="Browse artisan creations"
        empty_msg="No artisan creations found yet."
    else:
        hero("Raw Materials Marketplace","A separate sourcing space for fabrics, threads, trims and garment-making supplies.")
        allowed=["Fabric","Thread","Accessories","Packaging","Other"]
        heading="Browse raw materials"
        empty_msg="No raw-material listings found."
    existing=q("SELECT * FROM listings WHERE status='Available' ORDER BY id DESC")
    filtered=existing[existing.category.isin(allowed)] if not existing.empty else existing
    c1,c2,c3=st.columns(3)
    c1.metric("Available offers",len(filtered))
    c2.metric("Categories",filtered.category.nunique() if not filtered.empty else 0)
    c3.metric("Creators / suppliers",filtered.seller.nunique() if not filtered.empty else 0)

    if not signed_in:
        st.info("Guest browsing is enabled. Listings are public. Sign in as an Artisan to publish, or as a Buyer to chat and send inquiries.")
    elif signed_in["role"]=="Buyer":
        st.info("You are signed in as a Buyer. Browse listings and contact artisans.")
    else:
        with st.expander("＋ Upload and publish a new listing"):
            st.write("Add a clear photo. JPG, JPEG and PNG images are supported.")
            with st.form(f"publish_{kind}",clear_on_submit=True):
                c1,c2=st.columns(2)
                title=c1.text_input("Title")
                category=c2.selectbox("Category",allowed)
                description=st.text_area("Description")
                c1,c2,c3=st.columns(3)
                price=c1.number_input("Price (₹)",min_value=0.0,value=250.0,step=10.0)
                qty=c2.number_input("Available quantity",min_value=1,value=1)
                unit=c3.selectbox("Unit",["piece","design","set","pcs","metres","kg","spools","rolls"])
                c1,c2=st.columns(2)
                seller=c1.text_input("Artisan / seller name",value=signed_in["full_name"])
                location=c2.text_input("Location",value=signed_in["location"] or "Nagpur")
                upload=st.file_uploader("Upload image",type=["png","jpg","jpeg"],key=f"image_{kind}")
                publish=st.form_submit_button("Publish listing",type="primary")
            if publish:
                if not title.strip():
                    st.error("Enter a listing title.")
                else:
                    image_bytes=upload.getvalue() if upload else None
                    x("""INSERT INTO listings(title,category,description,price,quantity,unit,seller,location,status,created_at,image,owner_user_id)
                         VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                      (title.strip(),category,description.strip(),float(price),int(qty),unit,seller.strip(),location.strip(),
                       "Available",date.today().isoformat(),image_bytes,int(signed_in["id"])))
                    st.success("Listing published.")
                    st.rerun()

    st.markdown(f"### {heading}")
    search=st.text_input("Search listings",placeholder="Search by title, description or creator...")
    cat=st.selectbox("Category",["All"]+allowed,key=f"category_{kind}")
    shown=filtered.copy()
    if search and not shown.empty:
        mask=(shown.title.str.contains(search,case=False,na=False) |
              shown.description.str.contains(search,case=False,na=False) |
              shown.seller.str.contains(search,case=False,na=False))
        shown=shown[mask]
    if cat!="All" and not shown.empty:
        shown=shown[shown.category==cat]
    if shown.empty:
        st.info(empty_msg)
    for _,r in shown.iterrows():
        with st.container(border=True):
            pic,details,actions=st.columns([1.05,3.2,1.05])
            with pic:
                if r.get("image") is not None and not pd.isna(r.get("image")):
                    st.image(bytes(r["image"]),use_container_width=True)
                else:
                    st.markdown(f"""<div style="height:150px;border-radius:12px;background:linear-gradient(135deg,#e8f3f2,#dce8f1);display:flex;align-items:center;justify-content:center;font-size:48px">{"🎨" if artisan else "🧵"}</div>""",unsafe_allow_html=True)
            with details:
                st.markdown(f"### {r.title}")
                st.caption(f"{r.category} · {r.seller} · {r.location}")
                st.write(r.description)
                st.markdown(f'<div class="listing-price">₹{r.price:,.2f} / {r.unit}</div>',unsafe_allow_html=True)
                st.caption(f"Available: {r.quantity} {r.unit}")
            with actions:
                if signed_in and signed_in["role"]=="Buyer" and pd.notna(r.get("owner_user_id")):
                    if st.button("Chat with artisan",key=f"chat_{kind}_{r.id}",type="primary"):
                        st.session_state["chat_partner"]=int(r.owner_user_id)
                        st.session_state["chat_listing_title"]=r.title
                        st.session_state["active_page"]="Chat Box"
                        st.session_state["market_nav"]="Chat Box"
                        st.rerun()
                elif not signed_in:
                    st.caption("Sign in to contact")
                if signed_in and signed_in["role"]=="Buyer":
                    if st.button("Send inquiry",key=f"inq_{kind}_{r.id}"):
                        st.session_state["inq_listing"]=int(r.id)
            if st.session_state.get("inq_listing")==int(r.id) and signed_in and signed_in["role"]=="Buyer":
                with st.form(f"inq_form_{kind}_{r.id}"):
                    requested=st.number_input("Quantity requested",min_value=1,max_value=max(1,int(r.quantity)),value=1)
                    note=st.text_area("Requirements or question")
                    send=st.form_submit_button("Submit inquiry")
                if send:
                    x("""INSERT INTO inquiries(listing_id,buyer,quantity,message,status,created_at,buyer_user_id,artisan_user_id)
                         VALUES(?,?,?,?,?,?,?,?)""",
                      (int(r.id),signed_in["full_name"],int(requested),note.strip(),"New",
                       datetime.now().isoformat(timespec="minutes"),int(signed_in["id"]),
                       int(r.owner_user_id) if pd.notna(r.get("owner_user_id")) else None))
                    st.session_state.pop("inq_listing",None)
                    st.success("Inquiry submitted.")
                    st.rerun()

if page=="Artisan Marketplace":
    render_marketplace("artisan")
elif page=="Raw Materials Marketplace":
    render_marketplace("raw")

elif page=="Chat Box":
    hero("Chat Box","Your conversations, in a compact Messenger-style pop-up.")
    if not signed_in:
        st.info("Sign in to chat. All public marketplace listings remain visible without an account.")
    else:
        contacts=q("SELECT id,username,full_name,role FROM users WHERE id<>? ORDER BY full_name",(int(signed_in["id"]),))
        if contacts.empty:
            st.info("No other registered users yet. Create a second account to test buyer–artisan conversations.")
        else:
            st.markdown("### Your conversations")
            st.caption("Open the blue **Chats** button at the bottom-right of the app to bring up a floating conversation window. It stays available while you browse other sections.")
            for _, contact in contacts.iterrows():
                preview=q("""SELECT body,sent_at,sender FROM messages
                    WHERE (lower(sender)=lower(?) AND lower(recipient)=lower(?))
                       OR (lower(sender)=lower(?) AND lower(recipient)=lower(?))
                    ORDER BY id DESC LIMIT 1""",(signed_in["username"],contact.username,contact.username,signed_in["username"]))
                left,right=st.columns([4,1])
                with left:
                    st.markdown(f"**{contact.full_name}** · {contact.role}")
                    if not preview.empty:
                        p=preview.iloc[0]
                        st.caption(f"{'You: ' if str(p.sender).lower()==signed_in['username'].lower() else ''}{p.body} · {p.sent_at}")
                    else:
                        st.caption("No messages yet")
                with right:
                    if st.button("Open chat",key=f"open_chat_{int(contact.id)}",type="primary"):
                        st.session_state["chat_partner"]=int(contact.id)
                        st.session_state["chat_popup_open"]=True
                        st.rerun()
                st.divider()

elif page=="Buyer Inquiries":
    hero("Buyer Inquiries","Review requests and convert accepted inquiries into production orders.")
    if not signed_in:
        st.info("Sign in to view and manage inquiries.")
    else:
        if signed_in["role"]=="Artisan":
            iq=q("""SELECT i.id,i.created_at,i.buyer,l.title AS listing,i.quantity,i.message,i.status,i.order_id,i.buyer_user_id
                    FROM inquiries i JOIN listings l ON l.id=i.listing_id
                    WHERE i.artisan_user_id=? ORDER BY i.id DESC""",(int(signed_in["id"]),))
        else:
            iq=q("""SELECT i.id,i.created_at,i.buyer,l.title AS listing,i.quantity,i.message,i.status,i.order_id,i.buyer_user_id
                    FROM inquiries i JOIN listings l ON l.id=i.listing_id
                    WHERE i.buyer_user_id=? ORDER BY i.id DESC""",(int(signed_in["id"]),))
        if iq.empty:
            st.info("No inquiries yet.")
        else:
            st.dataframe(iq.drop(columns=["order_id"]),use_container_width=True,hide_index=True)
            options={f"#{r.id} · {r.listing} · {r.buyer}":int(r.id) for _,r in iq.iterrows()}
            chosen=st.selectbox("Select inquiry",list(options))
            row=iq[iq.id==options[chosen]].iloc[0]
            st.write("**Buyer requirements:** "+str(row.message or "No additional message"))
            if signed_in["role"]=="Artisan" and row.status=="New":
                left,right=st.columns(2)
                if left.button("Accept & create production order",type="primary"):
                    code="ORD-"+datetime.now().strftime("%y%m%d%H%M%S")
                    x("INSERT INTO orders(order_code,product_name,quantity,due_date,status,notes,created_at,listing_id,buyer_user_id,artisan_user_id,inquiry_id) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                      (code,str(row.listing),int(row.quantity),date.today().isoformat(),"Pending",str(row.message or ""),date.today().isoformat(),None,int(row.buyer_user_id) if pd.notna(row.buyer_user_id) else None,int(signed_in["id"]),int(row.id)))
                    oid=int(q("SELECT id FROM orders WHERE order_code=?",(code,)).iloc[0]["id"])
                    x("UPDATE inquiries SET status='Accepted',order_id=? WHERE id=?",(oid,int(row.id)))
                    st.success("Accepted. A linked production order has been created.")
                    st.rerun()
                if right.button("Reject inquiry"):
                    x("UPDATE inquiries SET status='Rejected' WHERE id=?",(int(row.id),))
                    st.rerun()
            elif row.status=="Accepted":
                st.success("This inquiry has been converted into a production order.")
            else:
                st.info("Request status: "+str(row.status))


elif page=="My Profile":
    hero("My Profile","Manage your public artisan or buyer profile.")
    if not signed_in:
        st.info("Sign in to manage your profile.")
    else:
        with st.form("profile_update"):
            full_name=st.text_input("Full name",value=signed_in["full_name"])
            location=st.text_input("Location",value=signed_in["location"] or "")
            craft=st.text_input("Craft / specialisation",value=signed_in["craft"] or "",disabled=signed_in["role"]!="Artisan")
            bio=st.text_area("About you",value=signed_in["bio"] or "")
            save=st.form_submit_button("Save profile",type="primary")
        if save:
            x("UPDATE users SET full_name=?,location=?,craft=?,bio=? WHERE id=?",
              (full_name.strip(),location.strip(),craft.strip(),bio.strip(),int(signed_in["id"])))
            st.success("Profile updated.")
            st.rerun()

elif page=="My Listings":
    hero("My Listings","Edit, pause or remove listings published by your artisan account.")
    if not signed_in or signed_in["role"]!="Artisan":
        st.info("An Artisan account is required.")
    else:
        mine=q("SELECT * FROM listings WHERE owner_user_id=? ORDER BY id DESC",(int(signed_in["id"]),))
        if mine.empty:
            st.info("You have not published any listings yet.")
        for _,r in mine.iterrows():
            with st.container(border=True):
                st.markdown(f"### {r.title}")
                st.caption(f"{r.category} · {r.status} · ₹{r.price:,.2f}")
                with st.expander("Edit listing"):
                    with st.form(f"edit_listing_{r.id}"):
                        title=st.text_input("Title",value=r.title)
                        description=st.text_area("Description",value=r.description or "")
                        price=st.number_input("Price",min_value=0.0,value=float(r.price))
                        quantity=st.number_input("Quantity",min_value=0,value=int(r.quantity))
                        status=st.selectbox("Status",["Available","Unavailable"],index=0 if r.status=="Available" else 1)
                        save=st.form_submit_button("Save changes",type="primary")
                    if save:
                        x("UPDATE listings SET title=?,description=?,price=?,quantity=?,status=? WHERE id=? AND owner_user_id=?",
                          (title.strip(),description.strip(),float(price),int(quantity),status,int(r.id),int(signed_in["id"])))
                        st.rerun()
                if st.button("Delete listing",key=f"delete_{r.id}"):
                    x("DELETE FROM listings WHERE id=? AND owner_user_id=?",(int(r.id),int(signed_in["id"])))
                    st.rerun()

elif page=="Dashboard":
    hero("Management Overview","A combined view of inventory, production, catalogue and marketplace activity.")
    m=q("SELECT * FROM materials"); p=q("SELECT * FROM products"); o=q("SELECT * FROM orders"); l=q("SELECT * FROM listings"); i=q("SELECT * FROM inquiries"); ms=q("SELECT * FROM messages")
    low=m[m.quantity<=m.min_stock] if not m.empty else m
    a,b,c,d,e=st.columns(5); a.metric("Materials",len(m)); b.metric("Catalogue products",len(p)); c.metric("Open orders",int(o.status.isin(["Pending","In Progress"]).sum()) if not o.empty else 0); d.metric("Available listings",int((l.status=="Available").sum()) if not l.empty else 0); e.metric("Buyer inquiries",len(i))
    a,b=st.columns(2)
    with a:
        st.markdown("### Order status")
        if not o.empty: st.bar_chart(o.status.value_counts().reindex(["Pending","In Progress","Completed"],fill_value=0))
        else: st.info("No orders.")
    with b:
        st.markdown("### Low-stock materials")
        if not low.empty:
            low_display = low[["name", "quantity", "unit", "min_stock"]].rename(
                columns={"name": "Material", "quantity": "Quantity", "unit": "Unit", "min_stock": "Minimum"}
            )
            st.dataframe(low_display, use_container_width=True, hide_index=True)
        else:
            st.success("No low-stock materials.")
    st.caption(f"Messages stored: {len(ms)} • Inquiries: {len(i)}. Counts are from this app database.")

elif page=="Inventory":
    hero("Inventory Management", "A clear stock register for materials used across production.")
    df=q("SELECT name,category,quantity,unit,min_stock,supplier,updated_at FROM materials ORDER BY category,name")
    if not df.empty:
        df["Stock status"] = df.apply(lambda r: "Low stock" if r.quantity <= r.min_stock else "In stock", axis=1)
        view=df.rename(columns={"name":"Material","category":"Category","quantity":"Available","unit":"Unit","min_stock":"Reorder level","supplier":"Supplier","updated_at":"Last updated"})
        st.dataframe(view[["Material","Category","Available","Unit","Reorder level","Stock status","Supplier","Last updated"]], use_container_width=True, hide_index=True,
                     column_config={"Available":st.column_config.NumberColumn(format="%d"),"Reorder level":st.column_config.NumberColumn(format="%d")})
        low=int((df.quantity<=df.min_stock).sum())
        st.caption(f"{len(df)} material records • {low} at or below reorder level. Demo supplier details are fictional.")
    else:
        st.info("No inventory records yet.")
    if signed_in and signed_in.get("role")=="Artisan":
        with st.expander("Add inventory item"):
            with st.form("add_material"):
                a,b=st.columns(2); name=a.text_input("Material name"); cat=b.selectbox("Category",["Fabric","Thread","Accessories","Packaging","Other"])
                a,b,c=st.columns(3); qty=a.number_input("Available quantity",min_value=0); unit=b.selectbox("Unit",["pcs","metres","kg","spools","rolls","sets"]); minimum=c.number_input("Reorder level",min_value=0,value=5)
                supplier=st.text_input("Supplier"); submit=st.form_submit_button("Add material",type="primary")
            if submit:
                if not name.strip(): st.error("Enter a material name.")
                else: x("INSERT INTO materials(name,category,quantity,unit,min_stock,supplier,updated_at) VALUES(?,?,?,?,?,?,?)",(name.strip(),cat,int(qty),unit,int(minimum),supplier.strip(),date.today().isoformat())); st.success("Material added."); st.rerun()
    else:
        st.caption("Inventory is shown in read-only demo mode. Sign in with an Artisan account to add records.")
elif page=="Production Orders":
    if not signed_in:
        st.info("Sign in to access this section.")
    else:
        hero("Production Orders","Review and update production order status.")
        df=q("SELECT * FROM orders ORDER BY id DESC")
        st.dataframe(df,use_container_width=True,hide_index=True)
        if not df.empty:
            labels={f"{r.order_code} — {r.product_name}":int(r.id) for _,r in df.iterrows()}; pick=st.selectbox("Select order",list(labels)); r=df[df.id==labels[pick]].iloc[0]
            with st.form("edit_order"):
                status=st.selectbox("Status",["Pending","In Progress","Completed"],index=["Pending","In Progress","Completed"].index(r.status)); due=st.date_input("Due date",value=date.fromisoformat(r.due_date)); notes=st.text_input("Notes",value=str(r.notes or "")); save=st.form_submit_button("Save",type="primary")
            if save: x("UPDATE orders SET status=?,due_date=?,notes=? WHERE id=?",(status,due.isoformat(),notes,int(r.id))); st.rerun()
        with st.expander("Create production order"):
            prods=q("SELECT name FROM products"); names=prods.name.tolist() if not prods.empty else []
            with st.form("new_order"):
                code=st.text_input("Order ID",value=f"ORD-{1001+len(df)}"); product=st.selectbox("Product",names) if names else st.text_input("Product name"); qty=st.number_input("Quantity",min_value=1,value=10); due=st.date_input("Due date",value=date.today()); status=st.selectbox("Initial status",["Pending","In Progress","Completed"]); notes=st.text_input("Notes"); submit=st.form_submit_button("Create",type="primary")
            if submit:
                if not code.strip() or not product: st.error("Enter order ID and product.")
                else: x("INSERT INTO orders(order_code,product_name,quantity,due_date,status,notes,created_at) VALUES(?,?,?,?,?,?,?)",(code.strip(),product,int(qty),due.isoformat(),status,notes.strip(),date.today().isoformat())); st.success("Created."); st.rerun()
elif page=="Product Catalogue":
    hero("Product Catalogue", "Explore finished products with detailed descriptions, pricing and categories.")
    df=q("SELECT id,name,category,price,description,created_at FROM products ORDER BY category,name")
    if not df.empty:
        a,b,c=st.columns(3)
        a.metric("Products",len(df)); b.metric("Categories",df.category.nunique()); c.metric("Price range",f"₹{df.price.min():,.0f} – ₹{df.price.max():,.0f}")
        st.divider()
        f1,f2=st.columns([1.5,1])
        search=f1.text_input("Search catalogue",placeholder="Search product name or description")
        categories=["All categories"]+sorted(df.category.dropna().unique().tolist())
        category=f2.selectbox("Category",categories)
        filtered=df.copy()
        if search.strip():
            mask=filtered.apply(lambda r: search.lower() in f"{r['name']} {r['description']} {r['category']}".lower(),axis=1)
            filtered=filtered[mask]
        if category!="All categories": filtered=filtered[filtered.category==category]
        st.caption(f"Showing {len(filtered)} of {len(df)} catalogue products • Prices in INR")
        if filtered.empty:
            st.info("No products match your search. Try another term or category.")
        else:
            icons={"Shirts":"👕","Ethnic Wear":"🧵","Accessories":"👜","Bags":"👜","Kids Wear":"🧒","Home Textiles":"🏡","Loungewear":"☁️","Gift Items":"🎁"}
            for offset in range(0,len(filtered),2):
                cols=st.columns(2)
                for col,(_,r) in zip(cols,filtered.iloc[offset:offset+2].iterrows()):
                    with col:
                        st.markdown('<div class="listing-card">',unsafe_allow_html=True)
                        st.markdown(f"### {icons.get(r.category,'✦')}  {r['name']}")
                        st.markdown(f"<span class='listing-price'>₹{float(r.price):,.2f}</span>  ·  <span style='color:#526579'>{r.category}</span>",unsafe_allow_html=True)
                        st.write(str(r.description or "No description provided."))
                        st.caption(f"Product ID: PRD-{int(r.id):04d}  ·  Added: {r.created_at}")
                        st.markdown('</div>',unsafe_allow_html=True)
            with st.expander("View complete catalogue table"):
                table=filtered.rename(columns={"id":"ID","name":"Product","category":"Category","price":"Price (₹)","description":"Description","created_at":"Date added"})
                st.dataframe(table,use_container_width=True,hide_index=True)
    else:
        st.info("No catalogue products are available yet.")
    if signed_in and signed_in.get("role")=="Artisan":
        with st.expander("Add a catalogue product"):
            with st.form("new_product"):
                name=st.text_input("Product name"); cat=st.selectbox("Category",["Shirts","Ethnic Wear","Accessories","Bags","Kids Wear","Home Textiles","Loungewear","Gift Items","Other"]); price=st.number_input("Price (₹)",min_value=0.0); desc=st.text_area("Detailed description",placeholder="Describe the material, design, finish and intended use..."); submit=st.form_submit_button("Add product",type="primary")
            if submit:
                if not name.strip(): st.error("Enter product name.")
                else: x("INSERT INTO products(name,category,price,description,created_at) VALUES(?,?,?,?,?)",(name.strip(),cat,float(price),desc.strip(),date.today().isoformat())); st.success("Product added."); st.rerun()
    else:
        st.caption("Catalogue is publicly viewable. Sign in with an Artisan account to add products.")

else:
    hero("About Project","A student prototype inspired by the Nagpur Readymade Garment Cluster case-study context.")
    st.markdown("""
    **Artisan Marketplace:** discover and publish artwork, original designs, embroidery, handcrafted accessories and textile art by artisans. Listings support image uploads.

    **Raw Materials Marketplace:** a separate space for fabrics, threads, trims, packaging and other garment-making supplies.

    **Communication:** registered buyers and artisans can chat directly; buyers can submit inquiries and artisans can convert accepted requests into production orders.

    **Technology:** Python, Streamlit, SQLite and Pandas.

    **Scope note:** this is not official SFURTI software. Seed data is fictional. Accounts use salted PBKDF2 password hashes. Email verification, password reset, payments, shipping, dispute resolution and guaranteed persistent cloud storage are outside this prototype's scope. Chat is stored in SQLite and does not provide push notifications. Use demo names and never enter sensitive information.
    """)


# Persistent floating chat pop-up (available while browsing any signed-in section).
if signed_in:
    chat_contacts=q("SELECT id,username,full_name,role FROM users WHERE id<>? ORDER BY full_name",(int(signed_in["id"]),))
    unread_count=int(q("SELECT COUNT(*) AS n FROM messages WHERE lower(recipient)=lower(?) AND read_status=0",(signed_in["username"],)).iloc[0]["n"])
    launcher_label=f"💬 Chats  ·  {unread_count}" if unread_count else "💬 Chats"
    with st.popover(launcher_label,help="Open your conversations",use_container_width=False):
        st.markdown("### Messenger")
        st.caption("Private buyer–artisan conversations")
        if chat_contacts.empty:
            st.info("No contacts yet. Create another account to start a conversation.")
        else:
            contact_ids=chat_contacts.id.astype(int).tolist()
            preferred=st.session_state.get("chat_partner")
            if preferred not in contact_ids:
                preferred=contact_ids[0]
            selected=st.selectbox(
                "Chat with",
                contact_ids,
                index=contact_ids.index(preferred),
                key="floating_chat_contact",
                format_func=lambda uid: (
                    chat_contacts[chat_contacts.id==uid].iloc[0]["full_name"]
                    + " · " + chat_contacts[chat_contacts.id==uid].iloc[0]["role"]
                ),
            )
            st.session_state["chat_partner"]=int(selected)
            partner=chat_contacts[chat_contacts.id==selected].iloc[0]
            st.markdown(f"**{partner.full_name}**")
            st.caption(str(partner.role)+" · Active conversation")
            history=q("""SELECT id,sender,recipient,body,sent_at FROM messages
                WHERE (lower(sender)=lower(?) AND lower(recipient)=lower(?))
                   OR (lower(sender)=lower(?) AND lower(recipient)=lower(?))
                ORDER BY id DESC LIMIT 40""",
                (signed_in["username"],partner.username,partner.username,signed_in["username"]))
            history=history.iloc[::-1] if not history.empty else history
            if history.empty:
                st.caption("No messages yet. Say hello!")
            else:
                for _,m in history.iterrows():
                    own=str(m.sender).lower()==signed_in["username"].lower()
                    with st.chat_message("user" if own else "assistant"):
                        st.write(str(m.body))
                        st.caption(("You" if own else str(partner.full_name))+" · "+str(m.sent_at))
                    if not own:
                        x("UPDATE messages SET read_status=1 WHERE id=?",(int(m.id),))
            with st.form("floating_chat_compose",clear_on_submit=True):
                message=st.text_input("Message",placeholder="Write a message…",label_visibility="collapsed")
                send=st.form_submit_button("Send",type="primary",use_container_width=True)
            if send:
                if not message.strip():
                    st.warning("Write a message first.")
                else:
                    x("INSERT INTO messages(sender,recipient,subject,body,listing_id,sent_at,read_status) VALUES(?,?,?,?,?,?,0)",
                      (signed_in["username"],partner.username,"Chat",message.strip(),None,datetime.now().isoformat(timespec="minutes")))
                    st.rerun()
