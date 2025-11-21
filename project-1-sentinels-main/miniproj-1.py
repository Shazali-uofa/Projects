# Importing the sqlite 3 library
import sqlite3
import re
import hashlib
from datetime import datetime
import getpass as gp



# Creating Registration Page
def Registration(con):

    cur=con.cursor()

    print("\n" + "="*60)
    print("                 📝  USER REGISTRATION  📝")
    print("="*60)

    name = input("👤 Please enter your name: ").strip()
    # This regex pattern is used to validate a email adress
    regex= r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    while True:

        email=input("➡️  Enter your email: ").strip()

        if email.lower()=="q":
            print("↩️ Returning to main menu...")
            return None

        # To validate if email id is correct or not to validate
        if not re.match(regex,email):
            print("❌ Invalid email format. Please try again.")
            continue

        # After this email is valid so we will check if the email does not already exist in the data base
        cur.execute("SELECT * FROM customers WHERE email=? ",(email,))
        exist_email=cur.fetchone()

        # If the email id is found in the database we ask user to enter again
        if exist_email:
            print("⚠️  This email is already registered. Try another one.")
            continue

        else:
            pwd = gp.getpass("➡️  Enter your password: ").strip()

            if pwd.lower()=="q":
                print("↩️ Returning to main menu...")
                return None
            
            # We will reconfirm if the user is entering the current password or does not make any mistake
            while True:
                # Making Sure that the user Enters the correct pwd again
                new_pwd=gp.getpass("➡️  Re-enter your password: ").strip()

                if new_pwd.lower()=="q":
                    print("↩️ Returning to main menu...")
                    return None
                
                if new_pwd==pwd:

                    break

                else:
                    print("❌ Passwords do not match. Try again.")
                    continue

            hashed_pwd = hashlib.sha256(pwd.encode()).hexdigest()
            break


    role="customer"
    # We will add the email password and name in the customer table
    cur.execute("""
        INSERT INTO customers(name,email)
        VALUES(?,?)
        """,(name,email))
    
    uid=cur.lastrowid
    # Now we will add the password and role into the user table
    cur.execute("""
        INSERT INTO users(uid,pwd,role)
        VALUES(?,?,?)
        """,(uid,hashed_pwd,role))
    
    con.commit()

    
    print(f"🎉 Registration Successful, {name}!")
    print(f"✅ Your User ID is: {uid}")
    print("✅ You can now login using your User ID and Password.")
    login_option()


# Created the login option Page
def login_option():

    print("\n====================  💻  OPTIONS  ====================\n")
    print("  🔑  L   Login\n")
    print("  📝  R   Register (First Time User)\n")
    print("  ❌  Q   Quit Program\n")
    print("--------------------------------------------------------")

    # Asking the user to enter their choice
    user = input("👉 Please type one of the above options: ").strip().upper()

    # If the user input is not from the above options we keep on asking again and again
    while user not in ('L','Q','R'):

        print("Please enter a valid option:")

        user=input("Choose again pls: ").strip().upper()


    # If user presses Q then logout from that page
    if user=='Q':
        print("Thank you for visiting us!")
        return "q"
    # If user press L direct them to login page
    elif user=="L":
        return "l"
    # If user press R direct them to registration Page
    elif user=="R":
        return "r"


# Created the login page for the user
def login(con):
    
    # Creating a cursor
    cur=con.cursor()
    # Printing the login Page
    print("\n" + "="*55)
    print("                🔐  LOGIN PAGE  🔐")
    print("="*55)
    

    # Asking the user for the input 
    while True:
        uid = input("\n👤 Enter User ID (Q to return) : ").strip()

        # Quit Option

        if uid.lower()=="q":
            print("↩️ Returning to main menu...")
            return None
        
        if not uid.isdigit():
            print("❌ User ID must be a number.")
            continue

        uid=int(uid)

        break
    # Got a valid uid and now we want password
    pwd = gp.getpass("\n🔑 Enter your Password (Q to return) : ").strip()
    
    if pwd.lower()=="q":
        print("↩️ Returning to main menu...")
        return None
    
    # Convert password to hashed value
    entered_hash=hashlib.sha256(pwd.encode()).hexdigest()

    # to check if the user exists or not in our database
    cur.execute("SELECT uid,pwd,role FROM users WHERE uid=?", (uid,))
    user = cur.fetchone()

    # The user does not exist in our database
    if not user:
        print("❌ User not found in the system.")
        return None
    
    # The user exists in our database
    stored_hash=user[1]

    while True:
        
        if entered_hash == stored_hash:
            break
        
        print("❌ Password does not match!")

        pwd=gp.getpass("\n🔑 Enter password again (or Q to cancel): ").strip()

        if pwd.lower()=="q":
            print("↩️ Returning to main menu...")
            return None
        
        entered_hash=hashlib.sha256(pwd.encode()).hexdigest()

    # User Successful Login
    print("\n✅ Login Successful! Welcome,", user[0])
        
        
    # We will add the session No of the user to make it even more correct
    # The idea is really cool to get the last sessionNo u use the Max funtion
    cur.execute("SELECT MAX(sessionNo) FROM sessions WHERE cid=?",(uid,))
    session_check=cur.fetchone()[0]

    # If there was no Session No found we will give them a new session No which is 1
    if session_check is None:

        new_session=1

    # If there is a returning customer the user will get the new sessionNo
    else:
        new_session=session_check+1

    # Now we will insert the value into the sessions Table

    cur.execute("""

            INSERT INTO sessions(cid,sessionNo,start_time,end_time)
            VALUES(?,?,CURRENT_TIMESTAMP,NULL)


            """,(uid,new_session))
        
    con.commit()

    # This will print like which session has been started for the user!!

    print(f"\n🆕 Session {new_session} started for user {uid}")
    print("-------------------------------------------------------")
    role=user[2]

    if role=="customer":
        customer_page(con,uid,new_session)

        
    elif role=="salesperson":
        SalesPerson(con)

    return uid,new_session

# We will create Functions for the Sales Person Now
def SalesPerson(con):


    print("\n" + "="*60)
    print("                   🛒  SALESPERSON PAGE  🛒")
    print("="*60)
    
    print("\nPlease choose an option:")
    print("──────────────────────────────────────────────")
    print("  C  Check & Update Products")
    print("  G  View Sales Report")
    print("  S  View Top-Selling Products")
    print("──────────────────────────────────────────────")


    while True:
        # Asking salesperson to enter one of the choice
        option = input("➡️  Enter your choice (C/G/S): ").strip().upper()

        # If the option is not with the provided the salesperson needs to try again!
        if option not in ('C','G','S','Q'):
            print("❌ Invalid choice. Please try again.")
            continue
        
        print("\n" + "-"*60) 
        
        if option=="C":
            print("🔧  Opening *Product Update* section...")
            Check_Update(con)

        elif option=="G":
            print("📊  Opening *Sales Report*...")
            GetSales(con)

        elif option=="S":
            
            TopSelling(con)
        
        elif option=="Q":
            break

        print("-"*60 + "\n")

        

# Giving the Salesperson to Check and Update the products

def Check_Update(con):

    cur=con.cursor()

    
    print("\n" + "="*55)
    print("             🔧  CHECK & UPDATE PRODUCTS  🔧")
    print("="*55)

    update=input("➡️  Enter the Product ID you want to view: ").strip()

    # Detail info of the product
    cur.execute("""

        SELECT *
        FROM products
        WHERE pid=?
        
        """,(update,))
    
    results=cur.fetchone()

    if not results:
        print("❌ No product found with this ID!")

        return
    
    pid,name,category,price,stock_count,descr=results
    print("\n" + "="*55)
    print(f"🆔 ID: {pid}")
    print(f"🏷️ Name: {name}")
    print(f"📁 Category: {category}")
    print(f"💲 Price: {price}")
    print(f"📦 Stock: {stock_count}")
    print("\n" + "="*55)



    print("Press U to update Price or S to update the stock_count")

    option=input("Please Enter your selection:").strip().upper()

    if option=="U":
        update_price=float(input("Enter the price you would like to set?"))
        cur.execute("""
        UPDATE products
        SET price = ?
        WHERE pid = ?
        """,(update_price,update))

        con.commit()

        print("✅ Price updated successfully!")

    elif option=="S":
        update_stock=int(input("Enter the stock count u will like to update"))
        cur.execute("""
        UPDATE products
        SET stock_count=?
        WHERE pid=?
        """,(update_stock,update))

        con.commit()

        print("✅ Stock count updated successfully!")


    elif option=="Q":
        print("✅ Exiting...")
        return
    

# We will get the SalesReport Now

def GetSales(con):
    cur=con.cursor()

    # Using the orders table to count the number of distinct orders
    cur.execute("""
    SELECT COUNT(DISTINCT o.ono)
    FROM orders o
    WHERE o.odate >= DATE('NOW','-7 days');

    """)
    # This will print the number of distinct orders in the past 7 days
    number=cur.fetchone()[0]
    

    # To find the number of disttinct products sold
    cur.execute("""
    SELECT COUNT(DISTINCT ol.pid)
    FROM orderlines ol
    JOIN orders o ON o.ono=ol.ono
    WHERE o.odate>= DATE('NOW','-7 days');
    """)

    product_number=cur.fetchone()[0]
    

    # To find the distinct customers
    cur.execute("""
    SELECT COUNT(DISTINCT o.cid)
    FROM orders o
    WHERE o.odate>=DATE('NOW','-7 days');
    """)

    customer_count=cur.fetchone()[0]
    

    # To find the average spent by each customer

    cur.execute("""
    SELECT AVG(customer_total)
    FROM (
    SELECT o.cid, SUM(ol.uprice * ol.qty) AS customer_total
    FROM orderlines ol
    JOIN orders o ON o.ono = ol.ono
    WHERE o.odate >= DATE('now', '-7 days')
    GROUP BY o.cid
    
    );
    """)

    spending=cur.fetchone()[0]

    # To get the total Sales of the past 7 days
    cur.execute("""
    SELECT SUM(ol.uprice * ol.qty)
    FROM orderlines ol 
    JOIN orders o ON ol.ono=o.ono
    WHERE o.odate >= DATE('NOW','-7 days');


    """)

    total_sales=cur.fetchone()[0]

    print("\n📊 WEEKLY SALES REPORT (Last 7 Days)")
    print("─────────────────────────────────────────")
    print(f"📦 Distinct Orders:              {number}")
    print(f"🛒 Distinct Products Sold:       {product_number}")
    print(f"👥 Distinct Customers:           {customer_count}")
    print(f"💰 Avg Spending per Customer:    ${spending:.2f}")
    print(f"💰 Total Sales Amount:           ${total_sales:.2f}")
    print("─────────────────────────────────────────")


# We will create a function to see top-selling products

def TopSelling(con):

    cur=con.cursor()
    print("\n" + "="*70)
    print("                         🔥  TOP-SELLING PRODUCTS          ")
    print("="*70)

    # To View a list of top three products based on the number of distinct order

    cur.execute("""
    SELECT ol.pid,p.name,COUNT(DISTINCT ol.ono) AS max_order
    FROM orderlines ol
    JOIN products p ON p.pid=ol.pid
    GROUP BY ol.pid
    ORDER BY max_order DESC
    LIMIT 3;
    

    """)
    order_max=cur.fetchall()

    if not order_max:
        print("❌ No order data found.")

    else:
        
        print("\n🏆 TOP 3 PRODUCTS (By Number of Distinct Orders)")
        print("┌────────────┬──────────────────────────────┬──────────────┐")
        print("│ Product ID │ Name                         │ Order Count  │")
        print("├────────────┼──────────────────────────────┼──────────────┤")

        for pid, name, count in order_max:
            print(f"│ {pid:<10} │ {name:<28} │ {count:<12} │")

        print("└────────────┴──────────────────────────────┴──────────────┘")

        
    print("======================================================================")
    # To see the top 3 products viewed

    cur.execute("""
    SELECT vp.pid,p.name,COUNT(vp.pid) AS max_count 
    FROM viewedProduct vp
    JOIN products p ON vp.pid=p.pid
    GROUP BY vp.pid
    ORDER BY max_count DESC
    LIMIT 3;
    

    """)

    results=cur.fetchall()

    if not results:
        print("❌ No products found.")

    else:
        print("\n🏆 TOP 3 PRODUCTS (By Total Views)")
        print("┌────────────┬──────────────────────────────┬──────────────┐")
        print("│ Product ID │ Name                         │ Views        │")
        print("├────────────┼──────────────────────────────┼──────────────┤")

        for pid, name, count in results:
            print(f"│ {pid:<10} │ {name:<28} │ {count:<12} │")

        print("└────────────┴──────────────────────────────┴──────────────┘")




# Creating Customer Page
def customer_page(con,uid,new_session):
    # This is printing the design of the customer page

    while True:
        
        print("\n" + "="*60)
        print("\n             🛍️  CUSTOMER MAIN MENU  🛍️")
        print("="*60)
        print("\n [S] 🔎  Search for Products")
        print("\n [C] 🛒  Cart Management & Checkout")
        print("\n [V] 📦  View Past Orders")
        print("\n [Q] ❌  Exit to Main Menu\n")
        print("="*60)


        # Checking for the menu is true or not 
        while True:
           
            menu = input("\n👉 Please select an option: ").strip().upper()
            
            if menu in ('S','C','V','Q'):
                break

            print("\n❌ Invalid option. Please try again.")

        # Customer wants to select
        if menu=="S":
            print("\n🔍 Opening Product Search Page...\n")
            search(con,uid,new_session)
            print("\n🔚 Closing the search page...")
        # Customer Cart Managment
        elif menu=="C":
            CartManagment(con,uid,new_session)

        elif menu=="V":
            past_Order(con,uid)
        elif menu=="Q":
            print("\n👋 Returning to Main Menu...")
<<<<<<< HEAD

            login_option()
=======
            break
            # login_option()
>>>>>>> 617c72e489f89cf2cc1cccbc822bd566c7be845c


# Searching for a product
def search(con,uid,cur_session):

    cur=con.cursor()
    # User input
    user_input=input("👉 Please enter the name of the product or the key word u want to search: ").strip().lower()
    
    # If user types in q we direct to the customer page
    if user_input.lower()=="q":
        print("\n↩️ Returning to customer page menu...")
        return

    # Prevent from the empty input
    if not user_input:
        print("\n❌ You must enter at least one keyword.\n")
        return search(con,uid,cur_session)
    
    # Saving the user search history in the search table
    cur.execute("""
        
        INSERT INTO search(cid,sessionNo,ts,query) 
        VALUES(?,?,CURRENT_TIMESTAMP,?)
    """,(uid,cur_session,user_input))
    
    con.commit()

    # Split the input into the words
    keywords=user_input.split()

    # Base query
    query= " FROM products WHERE 1=1 "
    conditions=""
    param=[]
    
    for words in keywords:
        # Removes spaces from input 
        cleaned = words.replace(" ", "")
        conditions+=" AND (REPLACE(LOWER(name), ' ', '') LIKE ? OR REPLACE(LOWER(descr), ' ', '') LIKE ?)"

        param.extend([f"%{cleaned}%",f"%{cleaned}%"])

    count_query="SELECT COUNT(*) " + query+ conditions
    cur.execute(count_query,param)
    total=cur.fetchone()[0]

    if total==0:
        print("\n❌ No matching products found!")

        while True:
            print("-"*65)
            print("Would you like to: \n")
            print("  1️  Search again\n")

            print("  2️  Return to Customer Menu")

            print("-"*65)
            choice = input("\nEnter 1 or 2: ").strip()

            if choice=="1":
                # print("\n")
                return search(con,uid,cur_session)
            
            elif choice=="2":
                print("\n↩️ Returning to customer page menu...")
                return
            
            else:
                print("\n⚠️ Invalid input. Please enter 1 or 2.")
    
    # Pagination Setup and values
    
    page=0
    per_page=5

    while True:
       
        offset = page * per_page
        # This is used to combine the different queries
        final_sql="SELECT * " + query + conditions + " LIMIT ? OFFSET ?"
        
        # To run the the combined query
        cur.execute(final_sql,param + [per_page,offset])

        # This will only bring Max 5 pages perpage
        results=cur.fetchall()

        # If the query returns no rows we print and break the loop
        if not results:
            print("\n❌ No more products.")
            return
        
        # To print the start of the page to make it more user friendly
        print("\n" + "="*70)
        print(f"📄  PAGE {page + 1}")
        print("="*70)

        # If the results were found then we print out pid,name and price
        for row in results:
            pid, name, category, price, stock, descr = row
            print(f"🆔 {pid:<4} | 📦 {name:<25} | 💲 ${price:>7.2f}")
        print("\n" + "─"*70)



        # To print the end of the page to make it user friendly
        print("="*70)
        print(f"📄  END OF PAGE {page + 1}")
        print("="*70)

        # Different options given so the user can choose any one
        print("\n" + "-"*70)
        print(" 👉  [N]  Next   |   [P]  Prev   |   [S]  Select   |   [Q]  Quit")
        print("-"*70)

        choice=input("\nPlease enter your choice: ").strip().upper()

        # If the customer wish to go on the next page
        if choice=="N":
            if (page + 1) * per_page >= total:
                print("❌ No more pages.")

            else:
                page+=1

        # If the customer wishes to go on the previous page
        elif choice=="P":
            if page > 0:
                page-=1
            
            else:
                print("You are already on the first Page")

        # If the customer wants to select the item
        elif choice=="S":

            while True:
                product_id = input("\nEnter product ID (or Q to cancel): ").strip()

                # When the user is 
                if product_id.lower()=="q":
                    print("\n↩️ Returning to product list...")
                    break

                if not product_id.isdigit():
                    print("\n❌ Invalid product ID.")
                    continue
                product_id=int(product_id)



                if product_id <=0:
                    print("\nProduct id must be greater than 0")
                    continue
                
                # We will also check if the pid is in our database!

                cur.execute("""
                SELECT *
                FROM products
                WHERE pid = ?

                """,(product_id,))

                output=cur.fetchone()
                if not output:
                    print("\n❌ Product ID does not exist.")

                    continue

                # If its a valid product id break it
                customer_select(con,uid,product_id,cur_session)
                break


        # If the customer wants to just see and wants go back to the main menu
        elif choice=="Q":
            print("\n↩️ Returning to customer page menu...")
            return
        
        # If neither of the option is there raise an error
        else:
            print("\n❌ Invalid option. Please try again.")


# This function is when the customer selects a products
def customer_select(con,uid,pid,select_session):

    cur=con.cursor()
    
    # Record to update the viewed product
    cur.execute("INSERT INTO viewedProduct(cid,sessionNo,ts,pid) VALUES(?,?,CURRENT_TIMESTAMP,?)",(uid,select_session,pid))
    con.commit()

    # When the person enters the pid we get all the details of the product
    cur.execute("SELECT * FROM products WHERE pid=?",(pid,))
    product_row=cur.fetchone()

    # If no product is found 
    if not product_row:
        print("❌ Product not found.")
        return
    # We give all the details related to that product
    if product_row:
        pid, name, category, price, stock, descr = product_row
        print("─"*70)
        print(f"🆔  Product ID : {pid}")
        print(f"📦  Name       : {name}")
        print(f"🏷️  Category   : {category}")
        print(f"💲  Price      : ${price:.2f}")
        print(f"📉  Stock Left : {stock}")
        print(f"📝  Description: {descr}")
        print("─"*70)

            
        # We will allow the user to add2cart the product if there is enough stock present
        if stock > 0:

            add = input("🛒 Add to cart? (Y/N or Q to cancel): ").strip().lower()

            if add=="q":

                print("\n↩️ Returning to search list...")

                return
            
            if add=="y":
                # We will check for if the user enters a proper number or not for the products to be added in the cart
                while True:

                    quantity = input("\n🧮 Please enter how many items you'd like to add to your cart: ").strip()

                    
                    if quantity.lower()=="q":
                        print("\n↩️ Returning to product page...")
                        return
                    
                    if not quantity.isdigit():
                        print("\n❌ Quantity must be a number!")
                        continue
                    
                    quantity=int(quantity)

                    if quantity<=0:
                        print("\n❌ Must be greater than 0.")
                        continue

                    if quantity > stock:
                        print(f"\n📦 Current stock available: {stock}")
                        print("🚫 Not enough stock. Try again.")
                        continue
                    
                    # Valid Quantity
                    break
                    
                
                # Updating the stock count in the product table
                cur.execute("""
                UPDATE products
                SET stock_count = stock_count - ?
                WHERE pid = ?;

                """,(quantity,pid))

                con.commit()
                
                # We will check if the item is alredy added into the cart or not
                cur.execute("""
                    SELECT * 
                    FROM cart 
                    WHERE cid=? AND pid=? AND sessionNo=?
                    """,(uid,pid,select_session))
                
                
                item=cur.fetchone()
                # It means that item is already added in the cart
                if item:
                    cur.execute("""

                                UPDATE cart 
                                SET qty=qty+?
                                WHERE cid=? AND pid=? 
                                AND sessionNo=?                    


                                """,(quantity,uid,pid,select_session))

                    print(f"\n 🔁 Product {pid} quantity increased in your cart!")

                # The product was not in the cart so we will add it according to the user need
                else:
                    cur.execute("""

                            INSERT INTO cart(cid,sessionNo,pid,qty) VALUES(?,?,?,?)

                            """,(uid,select_session,pid,quantity))

                    print(f"\n✅ Product {pid} was successfully added to your cart!")

                    con.commit()

                print(f"\n📦 Current Stock Now: {stock - quantity}")

            # If the customer chooses No he did not wanted to added the product to the cart
            else:
                print("\n❌ Product not added to the cart.\n")


        else:
            print("\n⚠️ Sorry! This product is currently out of stock.\n")
            return


# This is used for Cart Managment

def CartManagment(con,uid,cart_session):

    cur=con.cursor()
    
    # We use this query to join the cart and the products table
    cur.execute("""

            SELECT p.pid, p.name, p.price, SUM(c.qty) AS qty, SUM(p.price * c.qty) AS total
            FROM cart c
            JOIN products p ON c.pid=p.pid
            WHERE cid=?
            GROUP BY p.pid;

               """,(uid,))
    # We take all the rows returned by the query
    result=cur.fetchall()

    # If there exist in the cart we print out the whole cart
    if result:
        print(f"{'PID':<6} {'Product Name':<28} {'Price($)':>12} {'Qty':>6} {'Total($)':>12}")
        print("─" * 75)

        total_sum = 0
    # We loop through all the rows given in the result
        for rows in result:
            pid, name, price, qty, total = rows

            print(f"{pid:<6} {name:<28} {price:>12.2f} {qty:>6} {total:>12.2f}")
            total_sum += total

        print("─" * 75)
        grand_total = total_sum
        print(f"{'':<46}{'🎉 Grand Total:':<15}${grand_total:>10.2f}")
        print("═" * 75)
        print("✅  You can [R]emove items, [U]pdate quantity, or [C]heckout\n")

        # We will now ask the customer if he wants to remove from the cart or not
        option=input("WHich option would u like to choose: ").strip().upper()
        
        # If the user chooses to remove product from the cart
        if option=="R":
            print("\n🗑️  Remove Item from Cart")
            print("─" * 40)
            # remove = input("🔢 Enter the Product ID (PID) you wish to remove: ").strip()

            while True:
                # To make sure that the user enters a valid pid and not some random characters
                remove = input("🔢 Enter the Product ID (PID) you wish to remove: ").strip()
                if not remove.isdigit():
                    print("❌ Product ID must be a number.")
                    continue

                remove=int(remove)

                # Check if PID exists in the user cart or not ?
                cur.execute("SELECT qty FROM cart WHERE cid=? AND pid=?",(uid,remove))
                row=cur.fetchone()

                if not row:
                    print("❌ This product is not in your cart. Please enter pid again.")
                    continue

                # Asking the user how mu
                amount=input("How many items would you like to remove from the cart: ").strip()

                # If its not a number ask the user to enter it again
                if not amount.isdigit():
                    print("❌ Please enter a valid positive number.")
                    continue
                
                amount = int(amount)

                if amount<=0:
                    print("❌ Amount must be greater than zero.") 
                    continue

                break
                
            
            # Preventing removing more than available
            current_qty= row[0]
            # If the entered amount is more present in cart it will automatically make it same
            if amount > current_qty:
                amount = current_qty
            
            # When the user enters which item he wants to remove we update the qty removing 1 qty
            cur.execute("UPDATE cart SET qty=qty-? WHERE cid=? AND pid=?",(amount,uid,remove))
            con.commit()

            # If the user removes the product from the cart we will update our product table stock_count
            
            cur.execute("""
            UPDATE products
            SET stock_count = stock_count + ?
            WHERE pid = ?
            """,(amount,remove))

            con.commit()
            
            # If the qty is equal to zero we remove the row from the cart table
            cur.execute("SELECT qty FROM cart WHERE cid=? AND pid=?",(uid,remove))
            row=cur.fetchone()
            
            # row checks for if there is any row returned
            # row[0] checks the first column which is qty
            # If both row and row[0] are less than or equal to 0 then the product will be removed from the cart
            if row and row[0]<=0:
                cur.execute("DELETE FROM cart WHERE cid=? AND pid=?",(uid,remove))
                con.commit()

                print("Product was completely removed from the cart!")

            else:
                print("✅ Cart updated successfully!")

            print(f"🆔 Product {remove} updated/removed.")
        # If the user choose to update the cart
        
        elif option=="U":
            print("\n🔄 Update Item Quantity")
            
            # Get a valid pid from the user Cart
            while True:
                product_pid= input("Enter PID to update: ").strip()

                if not product_pid.isdigit():
                    print("❌ PID must be a number.")
                    continue

                product_pid=int(product_pid)

                # Check if the item is in cart or not?
                cur.execute("""
                SELECT qty
                FROM cart c
                WHERE c.pid=? AND c.cid = ?
                """,(product_pid,uid))

                found=cur.fetchone()

                if not found:
                    print("❌ This PID is NOT in your cart.")
                    continue
                
                # Quantity Currently in the cart
                old_qty = found[0]
                break
            # Get the new Quantity
            while True:

                update_qty = input("Enter NEW quantity: ").strip()

                if not update_qty.isdigit():

                    print("❌ Enter a valid positive number.")

                    continue

                update_qty=int(update_qty)

                if update_qty<=0:

                    print("❌ Quantity must be greater than zero.")
                    
                    continue

                
                break

            # We will check if there is enough stock present or not 
            cur.execute("SELECT stock_count FROM products WHERE pid=?",(product_pid,))

            stock_row=cur.fetchone()
            
            if not stock_row:
                print("❌ Product not found.")
                return
            
            # This gives the actual value of the stock_count
            stock=stock_row[0]

            # Compute difference 
            difference = update_qty - old_qty
            # difference > 0 users wants more 
            # difference < 0 user wants Less or to return items
            
            
            
            # If the requested update quantity is higher than the current stock it will raise an error
            if difference >0 and difference > stock:
                print(f"⚠️ Not enough stock! Only {stock} available.")
                return
            
            # Update the Cart Quantity
            cur.execute("""
            UPDATE cart 
            SET qty = ?
            WHERE pid = ? AND cid = ?    


            """,(update_qty,product_pid,uid))

            # Update the Product Stock also
            cur.execute("""
            UPDATE products
            SET stock_count = stock_count - ?
            WHERE pid = ?
            """,(difference,product_pid))

            con.commit()
            
            print(f"✅ Quantity updated from {old_qty} → {update_qty}")
            print("✅ Cart updated successfully!")
            



        
            
        
        # We will now check for if the customer wants to checkout
        elif option=="C":

            checkout(con,uid,cart_session)
        
    
    else:
        print("Your car is empty Please Add Something in your Cart!")


# We will create function to handle checkout options

def checkout(con,uid,check_session):
    
    cur=con.cursor()

    print("\n🛒 The customer wants to check out!")
    print("──────────────────────────────────────────────")

    cur.execute("""

            SELECT p.pid, p.name, p.price, SUM(c.qty) AS qty, SUM(p.price * c.qty) AS total
            FROM cart c
            JOIN products p ON c.pid=p.pid
            WHERE c.cid=?
            GROUP BY p.pid;

               """,(uid,))
    
    # It gives all the products present in the cart

    checkout_item=cur.fetchall()
    # There were no products in the cart
    if not checkout_item:
        print("⚠️  Your cart is empty. Please add items before checkout.")
        return

    # Printing all the products in the cart
    print("\n📦 Items in your cart:")   
    print("─" * 70)
    print(f"{'PID':<5} {'Name':<20} {'Price':<10} {'Qty':<5} {'Total':<10}")
    print("─" * 70)

    total_sum1 = 0
    for check in checkout_item:
        # ALERT WE HAVE TO TAKE THE PRICE FROM THE CURRENT PRODUCT TABLE
        pid, name, price, qty, total = check
        total_sum1 += total
        print(f"{pid:<5} {name:<20} ${price:<9.2f} {qty:<5} ${total:<9.2f}")

    print("─" * 70)
    print(f"💰 Grand Total: ${total_sum1:.2f}")
    print("─" * 70)
    # We will ask the user if they want to confirm this checkout or not?
    ask=input("Would you like to proceed to checkout? (Y/N): ").strip().upper()

    if ask=="Y":
        print("Yes the customer wants to checkout")
        # Ask for shipping address
        adress=input("Can you please enter your home adress: ").strip()
        # We write down the current date
        today=datetime.now().date()
        today_str=today.isoformat()

        # We update our query to the backend
        cur.execute("""
                    INSERT INTO orders(cid,sessionNo,odate,shipping_address) 
                    VALUES (?,?,?,?)""",(uid,check_session,today_str,adress))
        
        con.commit()

        # We have to update the orderline and also update the stock count
        # We get the the order id 
        ono=cur.lastrowid
        lineNo=1

        for lines in checkout_item:

            pid, name, price, qty, total = lines
            
            # Add each product into the orderline table
            cur.execute("""
                INSERT INTO orderlines(ono,lineNo,pid,qty,uprice)
                VALUES(?,?,?,?,?)
                        """,(ono,lineNo,pid,qty,price))
            
            lineNo+=1

            # Now we also have to update the stock amount in the product tables
            cur.execute("""

                UPDATE products
                SET stock_count=stock_count-?
                WHERE pid=?
                """,(qty,pid))
        
        con.commit()

        
        print("\n✅ Your order has been placed successfully!")
        print(f"🧾 Order Number: {ono}")
        print("📦 Your cart will now be cleared.")

        # After the order is placed we clear the cart NOW

        cur.execute("DELETE FROM cart WHERE cid=?",(uid,))
        
        con.commit()




    else:
        print("Your order was aborted or cancelled!")


# To view the Past Orders for the customer

def past_Order(con,uid):

    print("\n🧾 ORDER HISTORY")
    print("──────────────────────────────────────────────────────────")

    cur=con.cursor()
    # We will get the all order history of user
    page=0
    # We will print 5 orders per page
    per_page=5
    while True:
        start=per_page*page

        cur.execute("""

        SELECT o.ono,o.odate,o.shipping_address
        FROM orders o
        WHERE o.cid=?
        ORDER BY o.ono DESC
        LIMIT ? OFFSET ?
        """,(uid,per_page,start))
    
        results=cur.fetchall()

        # If there are no results found means that the customer does not have any past orders
        if not results:
            print("❌ You have no past orders.")
            break

        # Printing the Orders Page
        print("\n📦 Your Orders:")
        print("──────────────────────────────────────────────────────────")
        print("\n" + "="*70)
        print(f"📄  PAGE {page + 1}")
        print("="*100)

        for order_row in results:
            ono,date,addr=order_row
            print(f"• Order #{ono:<5} | Date: {date} | Address: {addr}")
        
        print("="*100)
        print(f"📄  END OF PAGE {page + 1}")
        print("="*70)
        print("\n👉 Enter Order Number OR press: [N] Next | [P] Previous | [Q] Quit")

        print("──────────────────────────────────────────────────────────")
        
        while True:

            # Asking the customer if they want to see the order history of particular product
            option=input("Which order would you like to see in detail: ").strip().lower()
            
            if not option.isdigit():
                print("❌ Invalid order number. Try again.")
                continue

            ono=int(option)

            if ono <=0:
                print("Please enter a valid order number !")
                continue
            
            break

        # If the user press navigate to the next page
        if option=="n":
            page+=1
            continue
        elif option=="p":
            # If the user presses p even there are no pages then there will be print statment printed 
            if page==0:
                print("⚠️ You are already on the first page!")
                continue
            # If there are previous pages then its safer to go 1 page above
            page-=1
            continue

        elif option=="q":
            break


        cur.execute("""

        SELECT p.name,p.category,ol.qty,ol.uprice
        FROM orderlines ol
        JOIN products p ON ol.pid=p.pid
        WHERE ol.ono=?
        

        """,(ono,))
    
        # We will store the details of that order
        # It can be more than one product from the order line
        details=cur.fetchall()
        # If no details were found 
        if not details:
            print("No details found for that order")
            continue

        print(f"\n🧾 ORDER DETAILS — Order #{option}")
        print("──────────────────────────────────────────────────────────")
        print(f"{'Product Name':<20} {'Category':<15} {'Qty':<5} {'Unit($)':<8} {'Total($)':<10}")
        print("--------------------------------------------------------------------------")

        grand_total = 0

        for ord_detail in details:
            name,category,qty,price=ord_detail
            line_total = qty * price
            grand_total += line_total
            print(f"{name:<20} {category:<15} {qty:<5} ${price:<8.2f} ${line_total:<10.2f}")
        
        print("--------------------------------------------------------------------------")
        print(f"{'':<45} GRAND TOTAL: ${grand_total:.2f}")
        print("--------------------------------------------------------------------------\n")

        # We will ask the user wants to stay in the page or leave
        next_option=input("Press q to exit the program:").strip().lower()
        
        if next_option=="q":
            break


def main_menu():
    while True:
        # show options page
        choice = login_option()  

        # User Pressed login
        if choice == 'l':        
            result = login(con)
            if result is None:
                continue
        # User Pressed Quit
        elif choice == 'q':      
            print("👋 Goodbye!")
            break
            # return None
        # User Pressed Register
        elif choice=="r":
            value=Registration(con)

            if value is None:
                None
                         


if __name__ == "__main__":
    con = sqlite3.connect("personaltest.db")
    print("Created the connection successfully!")
    main_menu()
