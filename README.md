# Karthik's Cart — Full-Stack E-Commerce Platform

Karthik's Cart is a complete, modern, multi-category e-commerce web platform engineered with **React (TypeScript + Vite + Tailwind CSS)** on the frontend, **Python (Flask REST API + SQLAlchemy)** on the backend, **PostgreSQL** relational database, and **Razorpay** payment gateway integration (online payment with cryptographic HMAC-SHA256 signature verification and Cash on Delivery).

---

## 🌟 Key Features

1. **Multi-Category Catalog (100+ Authentic Products)**
   - 10 distinct categories with 10 unique, non-duplicated products each:
     - Men's Pants
     - Women's Pants
     - T-Shirts
     - Shirts
     - Smartphones
     - Laptops
     - Electronics
     - Headphones
     - Watches
     - Shoes
   - Rich product models with multiple high-definition images, brand specifications, variant sizes, color swatches, stock counts, and verified ratings.

2. **Search & Multi-Dimensional Filtering**
   - Real-time instant autocomplete search suggestions bar.
   - Dynamic filtering by category, brand checklist, price range slider/inputs, customer star rating (4★+, 3★+), and sizes.
   - Dynamic sorting: Price Low-to-High, High-to-Low, Popularity & Rating, Newest Arrivals, Highest Discount.
   - Clean active filter tags with one-click removal and full pagination.

3. **Cart & Wishlist Engine**
   - Persistent user cart with real-time quantity controls (+ / -).
   - Instant move-to-wishlist and move-to-cart operations.
   - Promotional coupon code engine (`SHOPORA10`, `WELCOME200`, `FESTIVE500`).
   - Free shipping calculation threshold (Orders above ₹999).

4. **Secure Checkout & Razorpay Integration**
   - Multi-step address selection and creation with full validation.
   - Razorpay Online Checkout (UPI, Cards, NetBanking) & Cash on Delivery.
   - **Critical Backend Payment Security**:
     - Payment orders created server-side via Razorpay API.
     - Strict cryptographic HMAC-SHA256 signature verification on backend.
     - Orders marked paid ONLY after successful verification.
     - Safe inventory deduction upon verified purchase or confirmed COD.
     - Inventory restoration upon order cancellation.

5. **Customer Orders & Account Management**
   - Order history tracking with live status progression: `Placed` → `Confirmed` → `Processing` → `Shipped` → `Delivered`.
   - Cancellation of eligible orders with automated stock replenishment.
   - Order invoice details and shipping breakdown.

6. **Executive Admin Dashboard**
   - Role-protected admin portal (`role === 'admin'`).
   - Live KPI overview: Total Sales (₹), Total Orders, Live Products, Active Customers, Low Stock Alert.
   - Orders pipeline with instant status updates.
   - Product Management: Add new products with multiple images, edit, delete, stock updates.
   - Category Management: Create new departments with slug generation.
   - User Management: List registered shoppers and toggle active/suspended status.

---

## 🏗️ Architecture & Project Structure

```
E-Commerce/
├── backend/
│   ├── app/
│   │   ├── models/           # SQLAlchemy Models (users, addresses, categories, products, orders, payments, etc.)
│   │   ├── routes/           # REST Blueprints (auth, products, categories, cart, wishlist, orders, payments, admin)
│   │   ├── services/         # Razorpay cryptographic service & utilities
│   │   ├── utils/            # JWT authentication & admin decorators
│   │   ├── config.py         # App configuration & environment variables
│   │   └── __init__.py       # Application factory & CORS
│   ├── seed/
│   │   ├── sample_products.py# 100 uniquely curated realistic products across 10 categories
│   │   └── seed_data.py      # Database initialization & automated seeding script
│   ├── run.py                # Server entrypoint (Port 5000)
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example          # Environment variables template
│   └── .env                  # Active environment settings
├── frontend/
│   ├── src/
│   │   ├── components/       # Navbar, Footer, ProductCard, SkeletonCard, AuthModal
│   │   ├── pages/            # Home, ProductListing, ProductDetails, Cart, Checkout, OrderSuccess, MyOrders, Wishlist, AdminDashboard
│   │   ├── context/          # AuthContext, CartContext, WishlistContext
│   │   ├── services/         # Axios API client
│   │   ├── types/            # TypeScript interfaces
│   │   ├── App.tsx           # Route layout & providers
│   │   └── main.tsx          # React 18 bootstrap
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
└── README.md
```

---

## 🗄️ Database Design (PostgreSQL Relational Schema)

The database consists of 13 normalized relational tables:
1. `users` — Customer & admin accounts with bcrypt password hashes.
2. `addresses` — Shipping destinations with user foreign key.
3. `categories` — Product categories with unique indexed slugs.
4. `products` — Core inventory with pricing, discounts, stock, specs (JSON), and timestamps.
5. `product_images` — Multiple image gallery per product with primary flag.
6. `product_variants` — Sizes, colors, SKUs, and stock per variant.
7. `cart_items` — Shopping cart lines per user with variant FK.
8. `wishlists` — Saved items per user with unique composite constraint.
9. `orders` — Finalized customer orders with shipping snapshot, financial totals, and statuses.
10. `order_items` — Line items per order with snapshot pricing.
11. `payments` — Transaction records with Razorpay order/payment IDs and HMAC signatures.
12. `reviews` — Verified customer ratings & reviews.
13. `coupons` — Promotional discount rules and minimum order thresholds.

---

## 🚀 Getting Started & Running the Application

### 1. Backend Setup

```bash
cd backend

# Windows PowerShell: create the private environment file if it does not exist
if (!(Test-Path .env)) { Copy-Item .env.example .env }

# Install dependencies
python -m pip install -r requirements.txt

# Start the API (http://localhost:5000)
python run.py
```

On first startup, the backend creates the SQLite file `backend/shopora.db`, creates missing tables, and inserts any missing sample categories and products (100 items). Initialization is transactional and never drops existing tables or deletes existing catalog records. If you already have a private `backend/.env`, keep it and set its local `DATABASE_URL` to `sqlite:///shopora.db` to use SQLite.

To seed local coupons, run this once from `backend/`:

```bash
python -m seed.seed_data
```

Demo accounts are disabled by default. To seed them locally, set `SEED_DEMO_USERS=true` and provide `SEED_ADMIN_EMAIL`, `SEED_ADMIN_PASSWORD`, `SEED_CUSTOMER_EMAIL`, and `SEED_CUSTOMER_PASSWORD` in your private `backend/.env` before running the seeder. Render keeps `SEED_DEMO_USERS=false`.

Development-only SQLite reset (permanently deletes the local database contents):

```bash
flask --app run reset-db
```

This command refuses to reset PostgreSQL or a production environment.

### 2. Frontend Setup & Launch

```bash
cd frontend

# 1. Install dependencies
npm install

# 2. Start Vite development server (http://localhost:3000)
npm run dev
```

Visit **`http://localhost:3000`**. The frontend defaults to `/api`; Vite proxies that path to the local Flask server. For a separate API origin, set `VITE_API_BASE_URL` in `frontend/.env.local`. The Render deployment serves the API and frontend from the same origin, so the default `/api` also works in production.

### 3. Product and Search API checks

The existing category API remains available at `/api/categories`; `/api/products/categories` is also available for clients that expect it. Product listing supports search and pagination:

```powershell
Invoke-RestMethod "http://localhost:5000/api/health"
Invoke-RestMethod "http://localhost:5000/api/products?page=1&limit=12"
Invoke-RestMethod "http://localhost:5000/api/products/search?q=iPhone"
Invoke-RestMethod "http://localhost:5000/api/products/search/suggestions?q=Samsung"
```

Search is case-insensitive and covers product name, brand, description, category name, and category slug. Empty suggestions return an empty array; a search with no matches returns HTTP 200 with an empty product list and pagination metadata. Invalid pagination returns HTTP 400, and database failures return HTTP 503.

---

## 🔑 Accounts

Create a customer account through the registration page. For local admin/demo accounts, set `SEED_DEMO_USERS=true` and provide `SEED_ADMIN_EMAIL`, `SEED_ADMIN_PASSWORD`, `SEED_CUSTOMER_EMAIL`, and `SEED_CUSTOMER_PASSWORD` in the private `backend/.env`, then run `python -m seed.seed_data` from `backend/`. No default demo passwords are included in the application or frontend.

---

## 🎟️ Active Discount Coupons

- `SHOPORA10` — Flat 10% instant discount on all orders above ₹500.
- `WELCOME200` — Flat ₹200 off on your first order above ₹1,000.
- `FESTIVE500` — Special festive ₹500 off on orders above ₹2,500.

---

## 💳 Razorpay Configuration

In `backend/.env`:
```env
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
```
- In development/test mode, standard test credentials can be generated at [https://dashboard.razorpay.com/app/keys](https://dashboard.razorpay.com/app/keys).
- With no API keys, simulated checkout is available only in development and still validates an HMAC signature. Production requires Razorpay credentials for online payments.

---

## ☁️ Deploying to Render

1. Push this repository to GitHub and sign in to [Render](https://render.com).
2. Select **New → Blueprint**, connect this repository, and deploy the `render.yaml` Blueprint.
   It creates a Flask web service, a PostgreSQL database, and builds/serves the React app from that service.
3. In the web service's **Environment** settings, add `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` to enable Razorpay. Use your own keys; never publish them in this repository. Without them, production online payments are unavailable; simulated checkout is development-only.
4. Open the service's `onrender.com` URL. App startup creates missing tables and inserts missing catalog records without dropping tables or deleting existing records. The initial deploy hook does not create the public demo admin/customer accounts.

The Blueprint uses Render's free plans, which have usage limits; Render's free PostgreSQL database is temporary. Upgrade the database plan in Render before relying on it for persistent production data. Register accounts through the deployed site; real payment processing requires valid Razorpay credentials.

Production requires `DATABASE_URL`, `SECRET_KEY`, and `JWT_SECRET_KEY`. The Blueprint links `DATABASE_URL` to Render Postgres and generates the two secret keys. If you created the service manually, connect the Postgres database and set those variables in the web service's **Environment** settings. Never use a local SQLite file for Render's ephemeral filesystem.

### Environment variables

| Variable | Local development | Render production |
|---|---|---|
| `DATABASE_URL` | Optional; defaults to `backend/shopora.db` SQLite | Required; Blueprint maps it to Postgres |
| `SECRET_KEY` | Optional; generated locally when omitted | Required, generated by Blueprint |
| `JWT_SECRET_KEY` | Optional; generated locally when omitted | Required, generated by Blueprint |
| `FLASK_ENV` | `development` | `production` |
| `SEED_DEMO_USERS` | `false` by default; only enable with private seed credentials | `false` |
| `SEED_ADMIN_EMAIL` / `SEED_ADMIN_PASSWORD` | Required only when opting into a local demo admin | Not used |
| `SEED_CUSTOMER_EMAIL` / `SEED_CUSTOMER_PASSWORD` | Required only when opting into a local demo customer | Not used |
| `RAZORPAY_KEY_ID` / `RAZORPAY_KEY_SECRET` | Optional test keys | Optional; required for real payments |
| `VITE_API_BASE_URL` | Defaults to `/api` and uses the Vite proxy | Defaults to same-origin `/api` |
