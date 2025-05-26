
# 💊 Pharmacy Management System

A comprehensive, Django-based Pharmacy Management System designed to streamline and automate pharmacy operations. This platform integrates medicine inventory management, a point of sale (POS) system, sales tracking, return handling, and administrative reporting—all in a single application.

---

## 🚀 Features

### 🏥 1. Inventory Management
- Maintain detailed records for each medicine:
  - Brand & generic names
  - Batch number
  - Dosage (amount & unit)
  - Expiry date & PAR level
  - Stock quantity
  - Unit & box pricing
  - Dosage form
- Automatic stock tracking & adjustments
- Low stock alerts & expiry notifications

### 💳 2. Point of Sale (POS)
- Real-time sales transactions
- Multiple payment methods (cash, card)
- Auto stock deduction on sale
- Customer data recording
- 10% tax calculation
- Change amount calculation
- Printable invoices
- **🚫 Shows only non-expired medicines**
- **✅ Automatically filters out expired medicines from the POS view**

### 📦 3. Order & Return Management
- Unique order ID generation
- Multiple items per order
- Real-time stock validation
- Comprehensive order history
- Easy return processing:
  - Auto stock replenishment
  - Return tracking by date & customer
  - Return log maintenance

### 📊 4. Dashboard & Reporting
- Central dashboard with real-time metrics:
  - Recent sales
  - Expiring medications
  - Low stock indicators
  - Pending & zero-stock orders
- **⚠️ Alerts include medications expiring within the next 3 months**
- Date-based sales filter
- Sales and return analytics

---

## 🧩 Models & Database Design

### 🧪 Medicine Model
- Tracks all essential drug info
- Manages stock level and expiry
- Fields: `brand`, `generic`, `batch_no`, `dosage`, `price`, `stock`, etc.

### 🧾 Order Model
- Handles customer orders
- Links multiple items per order
- Manages order status and metadata

### 💰 Sale Model
- Stores transaction details:
  - Amount paid, tax, change, date, payment method
- Auto calculates tax & grand total

### 🔁 Return Model
- Connects to original orders
- Records returned quantities
- Restores stock accordingly

---

## ⚙️ Core Logic Highlights

### 📉 Stock Reduction on Sale

### ✅ Stock Validation Before Sale

### 💵 Payment Processing

### 🔄 Return Stock Update

---

## 🔍 Search & Filter Capabilities

* Live medicine search with suggestions
* Date-based sales filtering
* Return history access
* Search by customer name, phone, or order ID

---

## 🔐 Validation
* Validation for:

  * Stock levels
  * Payment accuracy
  * Expired medicines
  * Order quantity

---

## 🖥️ User Interface

* Clean design
* TailwindCSS-powered frontend
* Real-time search UX
* Accessible layout on desktop

---

## 📂 Tech Stack

* **Backend**: Django (Python)
* **Frontend**: HTML, TailwindCSS, JavaScript
* **Database**: MySql, easy to switch to PostgreSQL
* **Templating**: Django Templates

---


## 🔧 Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/omernaseem12/Pharmacy-Management-System.git
cd pharmacy-management-system
```

2. **Create and activate a virtual environment**

```bash
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run migrations**

```bash
python3 manage.py migrate
```

5. **Start the development server**

```bash
python3 manage.py runserver
```

6. **Access the app**

* Open `http://127.0.0.1:8000/inventory` in your browser.

---

## 🤝 Contributing

Pull requests are welcome! If you find bugs or want to suggest features, feel free to open an issue or submit a PR.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

* Django Project
* Tailwind CSS
* Your team / contributors (add names if applicable)

---

