import sqlite3
from pathlib import Path
from datetime import date, datetime
import pandas as pd
import streamlit as st

DB = Path(__file__).parent / "garment_cluster.db"
st.set_page_config(page_title="Garment Cluster Marketplace", page_icon="🧵", layout="wide")

st.markdown("""
<style>
.stApp{background:linear-gradient(135deg,#edf5f4,#e7eff5)}
.block-container{max-width:1400px;padding-top:1.4rem}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#102a43,#163e5c)}
[data-testid="stSidebar"] *{color:#f4f8fb!important}
.hero{padding:1.3rem 1.5rem;border-radius:18px;background:linear-gradient(115deg,#12344d,#147d79);color:white;margin-bottom:1rem}
.hero h1{color:white;margin:0 0 .3rem}.hero p{color:#e2f4f3;margin:0}
div[data-testid="stMetric"]{background:#e0efed;border:1px solid #b8d8d4;padding:16px;border-radius:15px}
[data-testid="stMetricLabel"],[data-testid="stMetricLabel"] *,[data-testid="stMetricValue"],[data-testid="stMetricValue"] *{color:#18384d!important}
.stButton button[kind="primary"],.stFormSubmitButton button[kind="primary"]{background:#147d79;border-color:#147d79;color:white}
[data-baseweb="tab-list"] button[aria-selected="true"]{border-bottom:2px solid #36c2b4!important}
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
        c.execute("""CREATE TABLE IF NOT EXISTS listings(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,category TEXT NOT NULL,description TEXT DEFAULT '',price REAL NOT NULL,quantity INTEGER NOT NULL,unit TEXT NOT NULL,seller TEXT NOT NULL,location TEXT DEFAULT '',status TEXT NOT NULL DEFAULT 'Available',created_at TEXT NOT NULL)""")
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
            ("Cotton Fabric Roll","Fabric","Demo listing for cotton fabric",185,120,"metres","Demo Fabric Supplier","Nagpur","Available",today),
            ("Bulk Buttons","Accessories","Demo listing for garment making",2.5,250,"pcs","Demo Accessories Shop","Nagpur","Available",today),
            ("Stitching Thread","Thread","Demo listing for thread spools",38,18,"spools","Demo Thread Supplier","Nagpur","Available",today),
            ("Cotton Shirt","Finished Garments","Demo finished garment listing",420,35,"pcs","Demo Garment Unit","Nagpur","Available",today)])
init()

def hero(t,s): st.markdown(f'<div class="hero"><h1>{t}</h1><p>{s}</p></div>',unsafe_allow_html=True)
with st.sidebar:
    st.markdown("## 🧵 Garment Marketplace")
    st.caption("Cluster trade & communication workspace")
    who=st.text_input("Your demo name",value=st.session_state.get("who","Pushpak")).strip() or "Guest"
    st.session_state["who"]=who
    page=st.radio("NAVIGATION",["Marketplace","Messages","Buyer Inquiries","Dashboard","Inventory","Production Orders","Product Catalogue","About Project"])
    st.divider(); st.caption("Student prototype • fictional demo records")
user=st.session_state["who"]

if page=="Marketplace":
    hero("Garment Marketplace","Discover materials and garments, publish offers, and contact sellers.")
    ls=q("SELECT * FROM listings WHERE status='Available' ORDER BY id DESC")
    a,b,c=st.columns(3); a.metric("Available listings",len(ls)); b.metric("Categories",ls.category.nunique() if not ls.empty else 0); c.metric("Locations",ls.location.nunique() if not ls.empty else 0)
    with st.expander("＋ Publish a listing"):
        with st.form("listing_form",clear_on_submit=True):
            a,b=st.columns(2); title=a.text_input("Listing title"); cat=b.selectbox("Category",["Fabric","Thread","Accessories","Finished Garments","Ethnic Wear","Other"])
            desc=st.text_area("Description"); a,b,c=st.columns(3); price=a.number_input("Price per unit (₹)",min_value=0.0,value=100.0); qty=b.number_input("Available quantity",min_value=1,value=1); unit=c.selectbox("Unit",["pcs","metres","kg","spools","rolls","sets"])
            a,b=st.columns(2); seller=a.text_input("Seller / business name",value=user); loc=b.text_input("Location",value="Nagpur")
            submit=st.form_submit_button("Publish listing",type="primary")
        if submit:
            if not title.strip() or not seller.strip(): st.error("Enter a title and seller name.")
            else:
                x("INSERT INTO listings(title,category,description,price,quantity,unit,seller,location,status,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",(title.strip(),cat,desc.strip(),price,int(qty),unit,seller.strip(),loc.strip(),"Available",date.today().isoformat()))
                st.success("Listing published."); st.rerun()
    st.markdown("### Browse listings")
    search=st.text_input("Search marketplace",placeholder="Fabric, buttons, shirts...")
    cats=["All"]+sorted(ls.category.unique().tolist()) if not ls.empty else ["All"]
    catpick=st.selectbox("Category filter",cats)
    shown=ls.copy()
    if search and not shown.empty:
        shown=shown[shown.title.str.contains(search,case=False,na=False)|shown.description.str.contains(search,case=False,na=False)|shown.seller.str.contains(search,case=False,na=False)]
    if catpick!="All" and not shown.empty: shown=shown[shown.category==catpick]
    if shown.empty: st.info("No listings found.")
    for _,r in shown.iterrows():
        with st.container(border=True):
            a,b=st.columns([4,1])
            with a:
                st.markdown(f"### {r.title}"); st.caption(f"{r.category} • {r.seller} • {r.location}")
                st.write(r.description); st.write(f"**₹{r.price:,.2f} / {r.unit}** · Quantity: **{r.quantity} {r.unit}**")
            with b:
                if st.button("Message seller",key=f"msg_{r.id}",type="primary"):
                    st.session_state["recipient"]=r.seller; st.session_state["subject"]=f"Question about {r.title}"; st.session_state["related_listing"]=int(r.id)
                    st.info("Go to Messages in the sidebar to compose your message.")
                if st.button("Send inquiry",key=f"inq_{r.id}"): st.session_state["inq_listing"]=int(r.id)
            if st.session_state.get("inq_listing")==int(r.id):
                with st.form(f"inq_form_{r.id}"):
                    iq=st.number_input("Quantity requested",min_value=1,max_value=max(1,int(r.quantity)),value=1); msg=st.text_area("Requirements or question"); send=st.form_submit_button("Submit inquiry")
                if send:
                    x("INSERT INTO inquiries(listing_id,buyer,quantity,message,status,created_at) VALUES(?,?,?,?,?,?)",(int(r.id),user,int(iq),msg.strip(),"New",datetime.now().isoformat(timespec="minutes")))
                    st.session_state.pop("inq_listing",None); st.success("Inquiry saved."); st.rerun()

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
    st.dataframe(sent,use_container_width=True,hide_index=True) if not sent.empty else st.caption("No sent messages yet.")

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
        st.dataframe(low[["name","quantity","unit","min_stock"]].rename(columns={"name":"Material","quantity":"Quantity","unit":"Unit","min_stock":"Minimum"}),use_container_width=True,hide_index=True) if not low.empty else st.success("No low-stock materials.")
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
    **Marketplace:** browse/search material and garment listings; publish offers with seller, location, price and quantity.

    **Communication:** submit buyer inquiries and use basic in-app text messages stored in SQLite.

    **Technology:** Python, Streamlit, SQLite and Pandas.

    **Scope note:** this is not official SFURTI software. Seed data is fictional. There is no login/verified identity, real-time chat, email/SMS delivery, payments, shipping, dispute resolution, or guaranteed persistent cloud storage. Use demo names and never enter sensitive information.
    """)
