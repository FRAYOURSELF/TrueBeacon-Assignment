# **Project Setup Guide**

## **Prerequisites**
Ensure you have the following installed on your system:
- **Python 3.x**
- **PostgreSQL**
- **Node.js & npm**
- **Git**

---

## **Backend Setup**

### **1. Clone the Repository**
```sh
git clone <repository_url>
cd financial-data-app/backend
```

### **2. Create a Virtual Environment & Install Dependencies**
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

### **3. Set Up PostgreSQL Database**
```sh
sudo -u postgres psql
```
Run the following SQL commands inside the PostgreSQL shell:
```sql
CREATE DATABASE financial_data;
CREATE USER financial_user WITH ENCRYPTED PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE financial_data TO financial_user;
```
Update **backend/database.py** with your database credentials if needed.

### **4. Ensure Data Folder Exists & Add Zip Files**
**Important:** Create a `data` folder in the backend directory and place the required zip files inside it before running the app.
```sh
mkdir -p data
mv /path/to/ticks_data.zip data/
mv /path/to/bhavcopy_eodsnapshot_data.zip data/
```

### **5. Run the Backend Server**
```sh
uvicorn main:app --reload
```
The backend API will be available at **[http://localhost:8000](http://localhost:8000)**.

---

## **Frontend Setup**

### **1. Navigate to the Frontend Directory & Install Dependencies**
```sh
cd ../frontend
npm install
```

### **2. Start the Frontend**
```sh
npm start
```
The frontend will be available at **[http://localhost:3000](http://localhost:3000)**.

---

## **Data Ingestion Process**
When the backend starts, it will automatically:
- Extract `ticks_data.zip` and `bhavcopy_eodsnapshot_data.zip` inside the `data/extracted` folder.
- Process one zip file from `extracted_bhavcopy/`, then process a CSV from within it.
- Insert the first 100 rows of the CSV into the PostgreSQL database.

---

## **Troubleshooting**

### **Module Not Found:**
Ensure you activated the virtual environment:
```sh
source venv/bin/activate
```

### **Database Connection Issues:**
Verify your PostgreSQL credentials in `database.py`.

### **Empty Database:**
Ensure zip files are correctly placed inside `data/`.

---
