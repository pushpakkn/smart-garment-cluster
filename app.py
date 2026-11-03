import sqlite3
from pathlib import Path
from datetime import date, datetime
import pandas as pd
import streamlit as st

DB = Path(__file__).parent / "garment_cluster.db"
st.set_page_config(page_title="Garment Cluster Marketplace", page_icon="🧵", layout="wide")

st.markdown("""
<style>
:root{color-scheme:light}
.stApp{background:#f3f6fa!important;color:#172b4d!important}
.block-container{max-width:1440px;padding-top:1.4rem;padding-bottom:3rem}
[data-testid="stHeader"]{background:#f3f6fa!important}
[data-testid="stSidebar"]{background:#102f46!important;border-right:1px solid #244b63}
[data-testid="stSidebar"] *{color:#f7fbff!important}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] label{color:#f0f6fb!important}
[data-testid="stSidebar"] input{background:#ffffff!important;color:#172b4d!important;-webkit-text-fill-color:#172b4d!important;border:2px solid #9db7c9!important}
/* Refined sidebar navigation */
[data-testid="stSidebar"] > div:first-child {padding-top:1.25rem}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
  font-size:1.16rem!important; letter-spacing:-.02em; margin-bottom:.15rem!important;
}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
  color:#b9ccda!important; font-size:.78rem!important; line-height:1.45;
}
.nav-kicker {
  color:#8eafc2!important; font-size:.68rem!important; font-weight:800!important;
  letter-spacing:.13em!important; text-transform:uppercase!important;
  margin:1.05rem 0 .35rem!important;
}
.nav-hint {
  color:#b9ccda!important; font-size:.75rem!important; margin:.05rem 0 .55rem!important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
  gap:.22rem!important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
  display:flex!important; align-items:center!important;
  background:rgba(255,255,255,.045)!important;
  border:1px solid rgba(220,238,248,.10)!important;
  border-radius:10px!important;
  padding:.48rem .62rem!important;
  margin:0!important;
  min-height:2.35rem!important;
  transition:background .15s ease,border-color .15s ease!important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
  background:rgba(255,255,255,.11)!important;
  border-color:rgba(185,220,237,.38)!important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
  background:linear-gradient(100deg,rgba(8,127,140,.48),rgba(8,127,140,.20))!important;
  border:1px solid #35b7b1!important;
  box-shadow:inset 3px 0 0 #55d0c6!important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label p {
  color:#eaf3f8!important; font-size:.86rem!important; font-weight:600!important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {
  color:#ffffff!important; font-weight:750!important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] input {
  accent-color:#55d0c6!important;
}
.sidebar-user-label {
  color:#dce9f1!important; font-size:.78rem!important; font-weight:700!important;
  margin:.8rem 0 .25rem!important;
}
.sidebar-foot {
  border-top:1px solid rgba(220,238,248,.16); padding-top:.9rem; margin-top:1.1rem;
  color:#9fb8c9!important; font-size:.72rem!important; line-height:1.5;
}

.hero{padding:1.45rem 1.65rem;border-radius:18px;background:linear-gradient(115deg,#12344d,#087f8c);margin-bottom:1.15rem}
.hero h1,.hero p{color:#fff!important}.hero h1{margin:0 0 .35rem}.hero p{margin:0;color:#e7f5f5!important}
h1,h2,h3,h4,h5,h6,p,li,label,[data-testid="stMarkdownContainer"],
[data-testid="stWidgetLabel"],[data-testid="stCaptionContainer"]{color:#172b4d!important}
[data-testid="stCaptionContainer"] p,.stCaption{color:#526579!important}
[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea,[data-baseweb="select"]>div{
 background:#fff!important;color:#172b4d!important;-webkit-text-fill-color:#172b4d!important;
 border:1px solid #aebfce!important;border-radius:9px!important
}
[data-testid="stTextInput"] input::placeholder,[data-testid="stTextArea"] textarea::placeholder{color:#65788a!important;-webkit-text-fill-color:#65788a!important;opacity:1!important}
[data-baseweb="select"] *,[role="option"]{color:#172b4d!important}
[data-testid="stWidgetLabel"] p{color:#263f56!important;font-weight:600!important}
[data-testid="stMetric"]{background:#fff!important;border:1px solid #d5e0e9!important;padding:16px!important;border-radius:14px!important}
[data-testid="stMetricLabel"],[data-testid="stMetricLabel"] *,
[data-testid="stMetricValue"],[data-testid="stMetricValue"] *{color:#173b53!important}
.stButton button[kind="primary"],.stFormSubmitButton button[kind="primary"]{background:#087f8c!important;border:1px solid #087f8c!important;color:#fff!important}
.stButton button:not([kind="primary"]),.stFormSubmitButton button:not([kind="primary"]){background:#fff!important;color:#173b53!important;border:1px solid #aebfce!important}
[data-testid="stExpander"]{background:#fff!important;border:1px solid #d5e0e9!important;border-radius:12px!important}
[data-testid="stExpander"] summary,[data-testid="stExpander"] summary *{color:#173b53!important}
[data-baseweb="tab-list"] button{color:#344e63!important}
[data-baseweb="tab-list"] button[aria-selected="true"]{color:#087f8c!important;border-bottom:3px solid #087f8c!important}
.listing-card{background:#fff;border:1px solid #d5e0e9;border-radius:14px;padding:1rem;margin:.5rem 0}
.listing-card h3{color:#173b53!important}.listing-price{color:#087f8c!important;font-size:1.08rem;font-weight:750}
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
        today=date.today().isoformat()
        if c.execute("SELECT COUNT(*) FROM materials").fetchone()[0]==0:
            c.executemany("INSERT INTO materials(name,category,quantity,unit,min_stock,supplier,updated_at) VALUES(?,?,?,?,?,?,?)",[
            ("Cotton Fabric","Fabric",120,"metres",30,"Sample supplier",today),("Black Thread","Thread",18,"spools",10,"Sample supplier",today),("Buttons","Accessories",250,"pcs",80,"Sample supplier",today),("Zippers","Accessories",22,"pcs",25,"Sample supplier",today)])
        if c.execute("SELECT COUNT(*) FROM products").fetchone()[0]==0:
            c.executemany("INSERT INTO products(name,category,price,description,created_at) VALUES(?,?,?,?,?)",[
            ("Classic Cotton Shirt","Shirts",699,"Demo product",today),("Festive Kurta","Ethnic Wear",1199,"Demo product",today)])
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

# Seed fictional back-and-forth messages once for a populated classroom demonstration.
with db() as conn:
    if conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0] == 0:
        demo_pairs = [
            ("Demo Fabric Supplier","Pushpak","Fabric sample request","Hello! We have cotton fabric swatches in natural, white and indigo. Would you like to see the options?",None,"2026-11-02T10:15"),
            ("Pushpak","Demo Fabric Supplier","Re: Fabric sample request","Yes, please. I am particularly interested in indigo and natural cotton. What is the minimum order quantity?",None,"2026-11-02T10:22"),
            ("Demo Fabric Supplier","Pushpak","Re: Fabric sample request","The minimum order is 10 metres. We can keep a sample ready for collection in Nagpur.",None,"2026-11-02T10:31"),
            ("Pushpak","Studio Rangrekha","Artwork customisation","Can the Madhubani-inspired motif colours be adjusted to match a festive kurta collection?",None,"2026-11-02T11:05"),
            ("Studio Rangrekha","Pushpak","Re: Artwork customisation","Absolutely. We can prepare a customised colour palette and a placement preview for the front panel.",None,"2026-11-02T11:18"),
            ("Sakhi Embroidery Unit","Pushpak","Mirror-work samples","We can prepare a sample set of mirror-work patches. Do you prefer a floral or geometric pattern?",None,"2026-11-02T12:02"),
            ("Pushpak","Sakhi Embroidery Unit","Re: Mirror-work samples","A floral pattern would be great. Please share the sample price and expected preparation time.",None,"2026-11-02T12:16"),
            ("Demo Garment Unit","Pushpak","Small batch collaboration","We are interested in collaborating on a small batch of printed cotton shirts. Can you share the artwork details?",None,"2026-11-02T13:40"),
            ("Pushpak","Demo Garment Unit","Re: Small batch collaboration","I can share a few design options. Let's begin with a small sample batch and review the print quality.",None,"2026-11-02T13:52")
        ]
        conn.executemany("INSERT INTO messages(sender,recipient,subject,body,listing_id,sent_at,read_status) VALUES(?,?,?,?,?,?,0)",demo_pairs)
        conn.commit()

def hero(t,s): st.markdown(f'<div class="hero"><h1>{t}</h1><p>{s}</p></div>',unsafe_allow_html=True)
def _select_market_nav():
    st.session_state["active_page"] = st.session_state["market_nav"]

def _select_operations_nav():
    st.session_state["active_page"] = st.session_state["operations_nav"]

with st.sidebar:
    st.markdown("## 🧵 Garment Marketplace")
    st.caption("Cluster trade & communication workspace")

    st.markdown('<div class="sidebar-user-label">YOUR DEMO PROFILE</div>', unsafe_allow_html=True)
    who=st.text_input(
        "Your demo name",
        value=st.session_state.get("who","Pushpak"),
        label_visibility="collapsed",
        placeholder="Enter demo name"
    ).strip() or "Guest"
    st.session_state["who"]=who

    st.markdown('<div class="nav-kicker">Marketplace & community</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-hint">Discover work and connect with artisans</div>', unsafe_allow_html=True)
    market_options = ["Artisan Marketplace", "Raw Materials Marketplace", "Messages", "Buyer Inquiries"]
    st.session_state.setdefault("market_nav", st.session_state.get("active_page", "Artisan Marketplace"))
    st.radio(
        "Marketplace navigation",
        market_options,
        key="market_nav",
        on_change=_select_market_nav,
        label_visibility="collapsed",
        format_func=lambda x: {
            "Artisan Marketplace":"🎨  Artisan Marketplace",
            "Raw Materials Marketplace":"🧵  Raw Materials",
            "Messages":"✉️  Messages",
            "Buyer Inquiries":"🤝  Buyer Inquiries"
        }[x]
    )

    st.markdown('<div class="nav-kicker">Cluster management</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-hint">Manage operations and project data</div>', unsafe_allow_html=True)
    operations_options = ["Dashboard", "Inventory", "Production Orders", "Product Catalogue", "About Project"]
    st.session_state.setdefault("operations_nav", st.session_state.get("active_page", "Dashboard"))
    st.radio(
        "Management navigation",
        operations_options,
        key="operations_nav",
        on_change=_select_operations_nav,
        label_visibility="collapsed",
        format_func=lambda x: {
            "Dashboard":"▦  Dashboard",
            "Inventory":"📦  Inventory",
            "Production Orders":"🧾  Production Orders",
            "Product Catalogue":"🛍️  Product Catalogue",
            "About Project":"ⓘ  About Project"
        }[x]
    )
    page = st.session_state.get("active_page", "Artisan Marketplace")
    st.markdown(
        '<div class="sidebar-foot">STUDENT PROTOTYPE<br>Fictional demonstration records</div>',
        unsafe_allow_html=True
    )
user=st.session_state["who"]

def render_marketplace(kind):
    artisan = kind == "artisan"
    if artisan:
        hero("Artisan & Artwork Marketplace","Discover original artwork, handcrafted details and designs created by local artisans.")
        allowed = ["Artwork","Embroidery","Handcrafted Accessories","Print Designs","Textile Art"]
        heading = "Browse artisan creations"
        form_key = "artisan_listing"
        categories = allowed
        empty_msg = "No artisan creations found yet. Be the first to publish an artwork listing."
    else:
        hero("Raw Materials Marketplace","A separate sourcing space for fabrics, threads, trims and garment-making supplies.")
        allowed = ["Fabric","Thread","Accessories","Packaging","Other"]
        heading = "Browse raw materials"
        form_key = "raw_listing"
        categories = allowed
        empty_msg = "No raw-material listings found. Publish a supply offer to get started."

    existing = q("SELECT * FROM listings WHERE status='Available' ORDER BY id DESC")
    filtered = existing[existing.category.isin(allowed)] if not existing.empty else existing
    a,b,c=st.columns(3)
    a.metric("Available offers",len(filtered))
    b.metric("Categories",filtered.category.nunique() if not filtered.empty else 0)
    c.metric("Artisans / suppliers",filtered.seller.nunique() if not filtered.empty else 0)

    with st.expander("＋ Upload and publish a new listing",expanded=False):
        st.write("Add a clear photo of the artwork or product. JPG, JPEG and PNG images are supported.")
        with st.form(form_key,clear_on_submit=True):
            col1,col2=st.columns(2)
            title=col1.text_input("Title")
            category=col2.selectbox("Category",categories)
            description=st.text_area("Description",placeholder="Describe the technique, materials, size, customisation options or story behind the work.")
            col1,col2,col3=st.columns(3)
            price=col1.number_input("Price (₹)",min_value=0.0,value=250.0,step=10.0)
            qty=col2.number_input("Available quantity",min_value=1,value=1)
            unit=col3.selectbox("Unit",["piece","design","set","pcs","metres","kg","spools","rolls"])
            col1,col2=st.columns(2)
            seller=col1.text_input("Artisan / seller name",value=user)
            location=col2.text_input("Location",value="Nagpur")
            upload=st.file_uploader("Upload artwork / product image",type=["png","jpg","jpeg"],key=f"image_{kind}")
            publish=st.form_submit_button("Publish listing",type="primary")
        if publish:
            if not title.strip() or not seller.strip():
                st.error("Please enter a title and artisan / seller name.")
            else:
                image_bytes=upload.getvalue() if upload is not None else None
                x("INSERT INTO listings(title,category,description,price,quantity,unit,seller,location,status,created_at,image) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                  (title.strip(),category,description.strip(),float(price),int(qty),unit,seller.strip(),location.strip(),"Available",date.today().isoformat(),image_bytes))
                st.success("Your listing has been published.")
                st.rerun()

    st.markdown(f"### {heading}")
    search=st.text_input("Search listings",placeholder="Search by title, description or artisan...")
    catpick=st.selectbox("Category",["All"]+categories,key=f"category_{kind}")
    shown=filtered.copy()
    if search and not shown.empty:
        mask=(shown.title.str.contains(search,case=False,na=False) |
              shown.description.str.contains(search,case=False,na=False) |
              shown.seller.str.contains(search,case=False,na=False))
        shown=shown[mask]
    if catpick!="All" and not shown.empty:
        shown=shown[shown.category==catpick]
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
                st.caption(f"{r.category}  ·  {r.seller}  ·  {r.location}")
                st.write(r.description)
                st.markdown(f'<div class="listing-price">₹{r.price:,.2f} / {r.unit}</div>',unsafe_allow_html=True)
                st.caption(f"Available quantity: {r.quantity} {r.unit}")
            with actions:
                if st.button("Message seller",key=f"msg_{kind}_{r.id}",type="primary"):
                    st.session_state["recipient"]=r.seller
                    st.session_state["subject"]=f"Enquiry about {r.title}"
                    st.session_state["related_listing"]=int(r.id)
                    st.session_state["page_jump"]="Messages"
                    st.info("Open Messages in the sidebar to contact this seller.")
                if st.button("Send inquiry",key=f"inq_{kind}_{r.id}"):
                    st.session_state["inq_listing"]=int(r.id)
            if st.session_state.get("inq_listing")==int(r.id):
                with st.form(f"inq_form_{kind}_{r.id}"):
                    iq=st.number_input("Quantity requested",min_value=1,max_value=max(1,int(r.quantity)),value=1)
                    msg=st.text_area("Requirements or question")
                    send=st.form_submit_button("Submit inquiry")
                if send:
                    x("INSERT INTO inquiries(listing_id,buyer,quantity,message,status,created_at) VALUES(?,?,?,?,?,?)",
                      (int(r.id),user,int(iq),msg.strip(),"New",datetime.now().isoformat(timespec="minutes")))
                    st.session_state.pop("inq_listing",None)
                    st.success("Inquiry saved.")
                    st.rerun()

if page=="Artisan Marketplace":
    render_marketplace("artisan")
elif page=="Raw Materials Marketplace":
    render_marketplace("raw")

elif page=="Messages":
    hero("Messages","Basic in-app text messaging between marketplace participants.")
    st.warning("Prototype only: messages are saved in SQLite, not delivered by email/SMS or live push chat. Use demo names and do not enter sensitive information.")
    ls=q("SELECT id,title FROM listings ORDER BY id DESC")
    with st.form("send_message",clear_on_submit=True):
        a,b=st.columns(2); sender=a.text_input("From",value=user); recipient=b.text_input("To",value=st.session_state.get("recipient",""))
        subject=st.text_input("Subject",value=st.session_state.get("subject","")); body=st.text_area("Message")
        opts=["None"]+[f"{r.id} — {r.title}" for _,r in ls.iterrows()]
        related=st.selectbox("Related listing",opts)
        send=st.form_submit_button("Send message",type="primary")
    if send:
        if not sender.strip() or not recipient.strip() or not subject.strip() or not body.strip(): st.error("Complete all message fields.")
        elif sender.strip().casefold()==recipient.strip().casefold(): st.error("Recipient must be different from sender.")
        else:
            lid=int(related.split(" — ",1)[0]) if related!="None" else st.session_state.get("related_listing")
            x("INSERT INTO messages(sender,recipient,subject,body,listing_id,sent_at,read_status) VALUES(?,?,?,?,?,?,0)",(sender.strip(),recipient.strip(),subject.strip(),body.strip(),lid,datetime.now().isoformat(timespec="minutes")))
            st.success("Message saved."); st.session_state.pop("recipient",None); st.session_state.pop("subject",None); st.session_state.pop("related_listing",None); st.rerun()
    st.markdown("### Inbox")
    inbox=q("SELECT * FROM messages WHERE lower(recipient)=lower(?) ORDER BY id DESC",(user,))
    if inbox.empty: st.info(f"No messages addressed to {user}. For a demo, send a message to this name from another participant name.")
    for _,m in inbox.iterrows():
        with st.container(border=True):
            st.markdown(f"**{m.subject}**"); st.caption(f"From {m.sender} • {m.sent_at}"); st.write(m.body)
            if not m.read_status and st.button("Mark read",key=f"read_{m.id}"): x("UPDATE messages SET read_status=1 WHERE id=?",(int(m.id),)); st.rerun()
    st.markdown("### Sent messages")
    sent=q("SELECT sent_at,recipient,subject,body FROM messages WHERE lower(sender)=lower(?) ORDER BY id DESC",(user,))
    if not sent.empty:
        st.dataframe(sent, use_container_width=True, hide_index=True)
    else:
        st.caption("No sent messages yet.")

elif page=="Buyer Inquiries":
    hero("Buyer Inquiries","Review and update inquiries submitted against marketplace listings.")
    iq=q("""SELECT i.id,i.created_at,i.buyer,l.title AS listing,i.quantity,i.message,i.status,l.seller
             FROM inquiries i JOIN listings l ON l.id=i.listing_id ORDER BY i.id DESC""")
    if iq.empty: st.info("No inquiries yet. Buyers can use Send inquiry on a listing.")
    else:
        st.dataframe(iq,use_container_width=True,hide_index=True)
        choices={f"#{r.id} — {r.listing} — {r.buyer}":int(r.id) for _,r in iq.iterrows()}
        pick=st.selectbox("Choose inquiry",list(choices.keys())); rec=iq[iq.id==choices[pick]].iloc[0]
        with st.form("update_iq"):
            status=st.selectbox("Status",["New","Responded","In discussion","Closed"],index=["New","Responded","In discussion","Closed"].index(rec.status))
            save=st.form_submit_button("Update inquiry",type="primary")
        if save: x("UPDATE inquiries SET status=? WHERE id=?",(status,int(rec.id))); st.rerun()

elif page=="Dashboard":
    hero("Marketplace & Cluster Overview","A combined view of inventory, production and marketplace activity.")
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
    hero("Inventory Management","Maintain material quantities and low-stock thresholds.")
    df=q("SELECT * FROM materials ORDER BY name")
    st.dataframe(df,use_container_width=True,hide_index=True)
    with st.expander("Add material"):
        with st.form("add_material"):
            a,b=st.columns(2); name=a.text_input("Name"); cat=b.selectbox("Category",["Fabric","Thread","Accessories","Packaging","Other"])
            a,b,c=st.columns(3); qty=a.number_input("Quantity",min_value=0); unit=b.selectbox("Unit",["pcs","metres","kg","spools","rolls","sets"]); minimum=c.number_input("Minimum stock",min_value=0,value=5)
            supplier=st.text_input("Supplier"); submit=st.form_submit_button("Add",type="primary")
        if submit:
            if not name.strip(): st.error("Enter a material name.")
            else: x("INSERT INTO materials(name,category,quantity,unit,min_stock,supplier,updated_at) VALUES(?,?,?,?,?,?,?)",(name.strip(),cat,int(qty),unit,int(minimum),supplier.strip(),date.today().isoformat())); st.success("Added."); st.rerun()

elif page=="Production Orders":
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
    hero("Product Catalogue","Maintain the simple product catalogue.")
    df=q("SELECT * FROM products ORDER BY name"); st.dataframe(df,use_container_width=True,hide_index=True)
    with st.expander("Add product"):
        with st.form("new_product"):
            name=st.text_input("Product name"); cat=st.selectbox("Category",["Shirts","Ethnic Wear","Accessories","Gift Items","Other"]); price=st.number_input("Price (₹)",min_value=0.0); desc=st.text_area("Description"); submit=st.form_submit_button("Add",type="primary")
        if submit:
            if not name.strip(): st.error("Enter product name.")
            else: x("INSERT INTO products(name,category,price,description,created_at) VALUES(?,?,?,?,?)",(name.strip(),cat,float(price),desc.strip(),date.today().isoformat())); st.success("Added."); st.rerun()

else:
    hero("About Project","A student prototype inspired by the Nagpur Readymade Garment Cluster case-study context.")
    st.markdown("""
    **Artisan Marketplace:** discover and publish artwork, original designs, embroidery, handcrafted accessories and textile art by artisans. Listings support image uploads.

    **Raw Materials Marketplace:** a separate space for fabrics, threads, trims, packaging and other garment-making supplies.

    **Communication:** submit buyer inquiries and use basic in-app text messages stored in SQLite.

    **Technology:** Python, Streamlit, SQLite and Pandas.

    **Scope note:** this is not official SFURTI software. Seed data is fictional. There is no login/verified identity, real-time chat, email/SMS delivery, payments, shipping, dispute resolution, or guaranteed persistent cloud storage. Use demo names and never enter sensitive information.
    """)
