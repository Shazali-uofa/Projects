import sqlite3
import bcrypt



# Connect (this creates a new database file)
con = sqlite3.connect("personaltest.db")
cur = con.cursor()

# Create tables (executed as a script)
cur.executescript("""
-- Let's drop the tables in case they exist from previous runs

DROP TABLE IF EXISTS orderlines;
DROP TABLE IF EXISTS cart;
DROP TABLE IF EXISTS search;
DROP TABLE IF EXISTS viewedProduct;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS users;


CREATE TABLE users (
  uid		INTEGER PRIMARY KEY,
  pwd		TEXT,
  role		TEXT
);
CREATE TABLE customers (
  cid		INTEGER PRIMARY KEY,
  name		TEXT, 
  email		TEXT,
  FOREIGN KEY (cid) REFERENCES users
);
CREATE TABLE products (
  pid		INTEGER PRIMARY KEY, 
  name		TEXT, 
  category	TEXT, 
  price		FLOAT, 
  stock_count	INT, 
  descr		TEXT
);
CREATE TABLE sessions (
  cid		INT,
  sessionNo	INT, 
  start_time	DATETIME, 
  end_time	DATETIME,
  PRIMARY KEY (cid, sessionNo),
  FOREIGN KEY (cid) REFERENCES customers ON DELETE CASCADE
);
CREATE TABLE viewedProduct (
  cid		INT, 
  sessionNo	INT, 
  ts		TIMESTAMP, 
  pid		INT,
  PRIMARY KEY (cid, sessionNo, ts),
  FOREIGN KEY (cid, sessionNo) REFERENCES sessions,
  FOREIGN KEY (pid) REFERENCES products
);
CREATE TABLE search (
  cid		INT, 
  sessionNo	INT, 
  ts		TIMESTAMP, 
  query		TEXT,
  PRIMARY KEY (cid, sessionNo, ts),
  FOREIGN KEY (cid, sessionNo) REFERENCES sessions
);
CREATE TABLE cart (
  cid		INT, 
  sessionNo	INT, 
  pid		INT,
  qty		INT,
  PRIMARY KEY (cid, sessionNo, pid),
  FOREIGN KEY (cid, sessionNo) REFERENCES sessions,
  FOREIGN KEY (pid) REFERENCES products
);
CREATE TABLE orders (
  ono INTEGER PRIMARY KEY,
  cid INTEGER,
  sessionNo INTEGER,
  odate DATE,
  shipping_address TEXT,
  FOREIGN KEY (cid, sessionNo) REFERENCES sessions
);

CREATE TABLE orderlines (
  ono		INT, 
  lineNo	INT, 
  pid		INT, 
  qty		INT, 
  uprice	FLOAT, 
  PRIMARY KEY (ono, lineNo),
  FOREIGN KEY (ono) REFERENCES orders ON DELETE CASCADE
);
""")



# Users For now we are just doing this shit

cur.executemany(
    "INSERT INTO users VALUES (?, ?, ?)",
    [
        (1, bcrypt.hashpw(b"abc123", bcrypt.gensalt()), "customer"),
        (2, bcrypt.hashpw(b"xyz789", bcrypt.gensalt()), "customer"),
        (3, bcrypt.hashpw(b"sales123", bcrypt.gensalt()), "sales")
    ]
)
con.commit()

# Customers
cur.executemany("INSERT INTO customers VALUES (?, ?, ?)", [
    (1, 'Henil Patel', 'henil@gmail.com'),
    (2, 'Joyce Smith', 'joyce@gmail.com'),
    (3, 'Shaz Ali', 'shaz@gmail.com')
])

# Products
cur.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)", [
    (1, 'iPhone 15', 'Smartphone', 1399.99, 10, 'Apple iPhone 15 with A17 Bionic chip'),
    (2, 'iPhone 14', 'Smartphone', 1199.99, 8, 'Apple iPhone 14 with A16 chip'),
    (3, 'iPhone 13', 'Smartphone', 999.99, 15, 'Apple iPhone 13 with A15 chip'),
    (4, 'iPhone 13 Mini', 'Smartphone', 899.99, 20, 'Compact iPhone 13 Mini'),
    (5, 'iPhone 12', 'Smartphone', 799.99, 5, 'Apple iPhone 12 with OLED display'),
    (6, 'iPhone SE', 'Smartphone', 599.99, 25, 'Budget iPhone SE 2022 model'),
    (7, 'Samsung Galaxy S23', 'Smartphone', 1099.99, 12, 'Samsung flagship phone'),
    (8, 'Samsung Galaxy S22', 'Smartphone', 999.99, 10, 'Samsung Galaxy S22 powerful performance'),
    (9, 'Google Pixel 8', 'Smartphone', 1099.99, 9, 'Google Pixel 8 with AI camera'),
    (10, 'Google Pixel 7', 'Smartphone', 899.99, 7, 'Google Pixel 7 great night mode'),
    (11, 'OnePlus 11', 'Smartphone', 849.99, 18, 'Fast and smooth OnePlus 11'),
    (12, 'OnePlus Nord 3', 'Smartphone', 499.99, 30, 'Affordable OnePlus Nord 3'),
    (13, 'MacBook Air M2', 'Laptop', 1699.99, 6, 'Lightweight MacBook Air with M2 chip'),
    (14, 'Sony WH-1000XM5', 'Headphones', 549.99, 14, 'Noise-cancelling headphones'),
    (15, 'Nike Backpack', 'Accessories', 89.99, 22, 'Durable everyday backpack')
])

con.commit()
print("✅ Sample data added successfully!")
con.close()
