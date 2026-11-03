# Artisan & Garment Cluster Marketplace

Student demonstration prototype built with Python, Streamlit, SQLite and Pandas.

## Marketplace structure
- **Artisan Marketplace** is the main creative marketplace. It contains only artisan work: original artwork, embroidery, handcrafted accessories, print designs and textile art.
- **Raw Materials Marketplace** is separate and contains fabric, thread, trims, packaging and garment-making supplies.
- Both marketplaces include a publish form with image upload (PNG/JPG/JPEG), description, price, quantity, seller and location.
- Sample artisan artwork thumbnails are included in `artwork_samples/`. Listings can also display images uploaded by the user.

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## GitHub / Streamlit deployment
Upload `app.py`, `requirements.txt`, `README.md`, the `.streamlit/config.toml` file, and the `artwork_samples` folder to the repository root. GitHub web upload may require uploading the image files individually or using GitHub Desktop.

## Demo communication
The app seeds fictional sample messages once if the messages table is empty. Change the sidebar demo name to `Pushpak`, `Demo Fabric Supplier`, `Studio Rangrekha`, `Sakhi Embroidery Unit`, or `Demo Garment Unit` to view both sides of the sample conversation.

All listings, people and messages are fictional. This is not official SFURTI software. Messages are stored in SQLite and are not live chat, email or SMS. No authentication, payment, shipping or verified identity is implemented.
