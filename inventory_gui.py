import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from functools import partial

# =================== DATABASE CONNECTION ===================
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Himavarshini@2006",
            database="InventoryManagementSystem"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Connection failed: {err}")
        return None

# ------------------- Shared DB helpers -------------------
def safe_query(query, params=(), fetch=False):
    con = connect_db()
    if con is None:
        return None
    try:
        cur = con.cursor()
        cur.execute(query, params)
        if fetch:
            return cur.fetchall()
        con.commit()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return None
    finally:
        con.close()

# =================== LOGIN & REGISTRATION ===================
def login_user():
    username = username_var.get().strip()
    password = password_var.get().strip()

    if not (username and password):
        messagebox.showwarning("Input Error", "Enter both username and password!")
        return

    con = connect_db()
    if con is None:
        return
    try:
        cur = con.cursor()
        cur.execute("SELECT Role FROM Users WHERE Username=%s AND Password=%s", (username, password))
        result = cur.fetchone()
        if result:
            role = result[0]
            login_window.destroy()
            open_main_window(username, role)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        con.close()

def register_user():
    username = reg_user_var.get().strip()
    password = reg_pass_var.get().strip()
    role = reg_role_var.get()
    if not (username and password):
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return
    try:
        con = connect_db()
        cur = con.cursor()
        cur.execute("INSERT INTO Users (Username, Password, Role) VALUES (%s, %s, %s)", (username, password, role))
        con.commit()
        messagebox.showinfo("Success", f"User '{username}' registered as {role}!")
        register_window.destroy()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        con.close()

def open_register_window():
    global register_window, reg_user_var, reg_pass_var, reg_role_var
    register_window = tk.Toplevel(login_window)
    register_window.title("Register New User")
    register_window.geometry("420x320")
    register_window.configure(bg="#f6fbff")

    tk.Label(register_window, text="Register New User", font=("Helvetica", 14, "bold"), bg="#f6fbff").pack(pady=10)
    frm = tk.Frame(register_window, bg="#f6fbff")
    frm.pack(padx=10, pady=10, fill="x")

    tk.Label(frm, text="Username:", bg="#f6fbff").grid(row=0, column=0, sticky="w", pady=6)
    reg_user_var = tk.StringVar()
    tk.Entry(frm, textvariable=reg_user_var).grid(row=0, column=1, pady=6, sticky="ew")

    tk.Label(frm, text="Password:", bg="#f6fbff").grid(row=1, column=0, sticky="w", pady=6)
    reg_pass_var = tk.StringVar()
    tk.Entry(frm, textvariable=reg_pass_var, show="*").grid(row=1, column=1, pady=6, sticky="ew")

    tk.Label(frm, text="Role:", bg="#f6fbff").grid(row=2, column=0, sticky="w", pady=6)
    reg_role_var = tk.StringVar(value="Staff")
    ttk.Combobox(frm, textvariable=reg_role_var, values=["Admin", "Manager", "Staff"], state="readonly").grid(row=2, column=1, pady=6, sticky="ew")

    frm.columnconfigure(1, weight=1)
    tk.Button(register_window, text="Register", command=register_user, bg="#0366d6", fg="white", width=16).pack(pady=12)

# =================== PRODUCT MANAGEMENT ===================
def load_products_into_tree(tree):
    """Load products into provided Treeview (tree)."""
    if tree is None:
        return
    try:
        if not tree.winfo_exists():
            return
    except Exception:
        return

    for row in tree.get_children():
        tree.delete(row)
    con = connect_db()
    if con is None:
        return
    try:
        cur = con.cursor()
        cur.execute("SELECT ProductID, Name, Category, CostPrice, SellingPrice, Quantity FROM Products")
        for r in cur.fetchall():
            tree.insert("", "end", values=r)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        con.close()

def add_product_from_vars(name_var, category_var, cost_var, sell_var, qty_var, supplier_var, tree):
    name = name_var.get().strip()
    cat = category_var.get().strip()
    try:
        cost = float(cost_var.get())
        sell = float(sell_var.get())
        qty = int(qty_var.get())
        supplier = int(supplier_var.get()) if supplier_var.get() else None
    except Exception:
        messagebox.showwarning("Input Error", "Please ensure numeric fields are numbers.")
        return

    if not (name and cat):
        messagebox.showwarning("Input Error", "Fill name and category!")
        return

    try:
        con = connect_db()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO Products (Name, Category, CostPrice, SellingPrice, Quantity, SupplierID)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (name, cat, cost, sell, qty, supplier))
        con.commit()
        messagebox.showinfo("Success", "Product added successfully!")
        load_products_into_tree(tree)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        con.close()

def update_product_quantity_from_vars(tree, qty_var):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Product", "Select a product to update!")
        return
    try:
        pid = tree.item(selected[0])['values'][0]
        new_qty = int(qty_var.get())
    except Exception:
        messagebox.showwarning("Input Error", "Enter a valid integer quantity.")
        return
    try:
        con = connect_db()
        cur = con.cursor()
        cur.execute("UPDATE Products SET Quantity=%s WHERE ProductID=%s", (new_qty, pid))
        con.commit()
        messagebox.showinfo("Updated", "Product quantity updated successfully!")
        load_products_into_tree(tree)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        con.close()

def delete_selected_product(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Product", "Select a product to delete!")
        return
    pid = tree.item(selected[0])['values'][0]
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this product?")
    if not confirm:
        return
    try:
        con = connect_db()
        cur = con.cursor()
        cur.execute("DELETE FROM Products WHERE ProductID=%s", (pid,))
        con.commit()
        messagebox.showinfo("Deleted", "Product deleted successfully!")
        load_products_into_tree(tree)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        con.close()

def delete_product_by_name(name_entry, tree):
    name = name_entry.get().strip()
    if not name:
        messagebox.showwarning("Input Error", "Enter product name to delete.")
        return
    con = connect_db()
    if con is None:
        return
    try:
        cur = con.cursor()
        cur.execute("SELECT ProductID, Name, Quantity FROM Products WHERE Name=%s", (name,))
        rows = cur.fetchall()
        if not rows:
            messagebox.showinfo("Not Found", f"No product found with name '{name}'.")
            return
        if len(rows) > 1:
            sel_win = tk.Toplevel()
            sel_win.title("Select Product to Delete")
            sel_tree = ttk.Treeview(sel_win, columns=("ID","Name","Qty"), show="headings")
            for c in ("ID","Name","Qty"):
                sel_tree.heading(c, text=c)
                sel_tree.column(c, anchor="center")
            for r in rows:
                sel_tree.insert("", "end", values=r)
            sel_tree.pack(fill="both", expand=True, padx=10, pady=10)
            def confirm_del():
                sel = sel_tree.selection()
                if not sel:
                    messagebox.showwarning("Select", "Select the exact product to delete.")
                    return
                pid = sel_tree.item(sel[0])['values'][0]
                try:
                    cur.execute("DELETE FROM Products WHERE ProductID=%s", (pid,))
                    con.commit()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                    return
                sel_win.destroy()
                messagebox.showinfo("Deleted", "Product deleted.")
                load_products_into_tree(tree)
            tk.Button(sel_win, text="Delete Selected", command=confirm_del, bg="#e63946", fg="white").pack(pady=8)
        else:
            pid = rows[0][0]
            confirm = messagebox.askyesno("Confirm", f"Delete '{name}' (ID {pid}) ?")
            if confirm:
                cur.execute("DELETE FROM Products WHERE ProductID=%s", (pid,))
                con.commit()
                messagebox.showinfo("Deleted", f"Product '{name}' deleted.")
                load_products_into_tree(tree)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        con.close()

# =================== TRIGGERS / FUNCTIONS / LOGS ===================
def get_total_stock_value():
    try:
        con = connect_db()
        cur = con.cursor()
        cur.execute("SELECT GetTotalStockValue()")
        res = cur.fetchone()
        con.close()
        if res and res[0] is not None:
            messagebox.showinfo("Total Stock Value", f"₹ {res[0]:.2f}")
        else:
            messagebox.showinfo("Total Stock Value", "No value returned.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def check_stock_status_for_selected(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Product", "Select a product to check stock!")
        return
    pid = tree.item(selected[0])['values'][0]
    try:
        con = connect_db()
        cur = con.cursor()
        cur.execute("SELECT CheckStockLevel(%s)", (pid,))
        status = cur.fetchone()
        con.close()
        if status:
            messagebox.showinfo("Stock Level", f"Product ID {pid}: {status[0]}")
        else:
            messagebox.showinfo("Stock Level", "No result returned.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_sales_log():
    con = connect_db()
    if con is None:
        return
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM SalesLog ORDER BY ActionTime DESC")
        rows = cur.fetchall()
        log_window = tk.Toplevel(root)
        log_window.title("Sales Log (Trigger Output)")
        tree = ttk.Treeview(log_window, columns=("LogID", "ProductID", "Quantity", "ActionTime", "Message"), show="headings")
        for col in ("LogID", "ProductID", "Quantity", "ActionTime", "Message"):
            tree.heading(col, text=col)
            tree.column(col, width=140)
        for r in rows:
            tree.insert("", "end", values=r)
        tree.pack(fill="both", expand=True, padx=10, pady=10)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        con.close()

# =================== QUERIES ===================
def view_products_with_suppliers():
    con = connect_db()
    if con is None:
        return
    try:
        cur = con.cursor()
        cur.execute("""
            SELECT p.ProductID, p.Name, s.SupplierName, p.Quantity
            FROM Products p
            JOIN Suppliers s ON p.SupplierID = s.SupplierID;
        """)
        rows = cur.fetchall()
        win = tk.Toplevel(root)
        win.title("Products with Suppliers (JOIN Query)")
        tree = ttk.Treeview(win, columns=("ProductID", "ProductName", "SupplierName", "Quantity"), show="headings")
        for col in ("ProductID", "ProductName", "SupplierName", "Quantity"):
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        for row in rows:
            tree.insert("", "end", values=row)
        tree.pack(fill="both", expand=True, padx=10, pady=10)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        con.close()

def view_low_stock():
    con = connect_db()
    if con is None:
        return
    try:
        cur = con.cursor()
        cur.execute("""
            SELECT Name, Quantity FROM Products
            WHERE Quantity < (SELECT AVG(Quantity) FROM Products);
        """)
        rows = cur.fetchall()
        win = tk.Toplevel(root)
        win.title("Low Stock Products (Nested Query)")
        tree = ttk.Treeview(win, columns=("Name", "Quantity"), show="headings")
        for col in ("Name", "Quantity"):
            tree.heading(col, text=col)
        for row in rows:
            tree.insert("", "end", values=row)
        tree.pack(fill="both", expand=True, padx=10, pady=10)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        con.close()

# =================== STORED PROCEDURES (ORDERS) ===================
def add_sales_order():
    win = tk.Toplevel(root)
    win.title("Add Sales Order")
    win.geometry("450x350")
    win.configure(bg="#fffdf6")

    # --- Fetch Customers from Database ---
    customers = []
    con = connect_db()
    if con:
        try:
            cur = con.cursor()
            cur.execute("SELECT CustomerID, Name FROM Customers")
            customers = cur.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load customers: {e}")
        finally:
            con.close()

    # --- Create mapping for Customer Name -> ID ---
    customer_names = [c[1] for c in customers]
    customer_map = {c[1]: c[0] for c in customers}

    # --- Form Fields ---
    frm = tk.Frame(win, bg="#fffdf6")
    frm.pack(padx=20, pady=12, fill="x")

    tk.Label(frm, text="Customer Name:", bg="#fffdf6").grid(row=0, column=0, sticky="w", pady=8)
    cust_name_var = tk.StringVar()
    cust_combo = ttk.Combobox(frm, textvariable=cust_name_var, values=customer_names, state="readonly", width=28)
    cust_combo.grid(row=0, column=1, pady=8, sticky="ew")

    tk.Label(frm, text="Product ID:", bg="#fffdf6").grid(row=1, column=0, sticky="w", pady=8)
    prod = tk.IntVar()
    tk.Entry(frm, textvariable=prod, width=30).grid(row=1, column=1, pady=8, sticky="ew")

    tk.Label(frm, text="Quantity:", bg="#fffdf6").grid(row=2, column=0, sticky="w", pady=8)
    qty = tk.IntVar()
    tk.Entry(frm, textvariable=qty, width=30).grid(row=2, column=1, pady=8, sticky="ew")

    frm.columnconfigure(1, weight=1)

    # --- Confirm button handler ---
    def confirm():
        cust_name = cust_name_var.get()
        if not cust_name:
            messagebox.showwarning("Input Error", "Please select a customer!")
            return
        cust_id = customer_map.get(cust_name)
        try:
            con = connect_db()
            cur = con.cursor()
            emp_id = 2  
            cur.callproc('AddSalesOrder', (cust_id, emp_id, prod.get(), qty.get()))
            con.commit()
            messagebox.showinfo("Success", f"Sales order for {cust_name} added successfully! (EmployeeID=2)")
            win.destroy()
            safe_reload_products()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add order: {e}")
        finally:
            con.close()

    tk.Button(win, text="Submit", command=confirm, bg="#2a9d8f", fg="white", width=15).pack(pady=20)




def add_purchase_order():
    win = tk.Toplevel(root)
    win.title("Add Purchase Order")
    win.geometry("420x360")
    win.configure(bg="#fffdf6")

    frm = tk.Frame(win, bg="#fffdf6")
    frm.pack(padx=12, pady=12, fill="x")
    tk.Label(frm, text="Supplier ID:", bg="#fffdf6").grid(row=0, column=0, sticky="w", pady=6)
    supp = tk.IntVar(); tk.Entry(frm, textvariable=supp).grid(row=0, column=1, sticky="ew", pady=6)
    tk.Label(frm, text="Employee ID:", bg="#fffdf6").grid(row=1, column=0, sticky="w", pady=6)
    emp = tk.IntVar(); tk.Entry(frm, textvariable=emp).grid(row=1, column=1, sticky="ew", pady=6)
    tk.Label(frm, text="Product ID:", bg="#fffdf6").grid(row=2, column=0, sticky="w", pady=6)
    prod = tk.IntVar(); tk.Entry(frm, textvariable=prod).grid(row=2, column=1, sticky="ew", pady=6)
    tk.Label(frm, text="Quantity:", bg="#fffdf6").grid(row=3, column=0, sticky="w", pady=6)
    qty = tk.IntVar(); tk.Entry(frm, textvariable=qty).grid(row=3, column=1, sticky="ew", pady=6)
    frm.columnconfigure(1, weight=1)

    def confirm():
        try:
            con = connect_db()
            cur = con.cursor()
            cur.callproc('AddPurchaseOrder', (supp.get(), emp.get(), prod.get(), qty.get()))
            con.commit()
            messagebox.showinfo("Success", "Purchase order added and stock updated!")
            win.destroy()
            safe_reload_products()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            con.close()

    tk.Button(win, text="Submit", command=confirm, bg="#2a9d8f", fg="white").pack(pady=10)

# =================== AGGREGATE & CUSTOMER REPORTS ===================
def view_aggregate_reports():
    con = connect_db()
    if con is None:
        return
    try:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM Products;")
        total = cur.fetchone()[0]
        cur.execute("SELECT SUM(Quantity) FROM Products;")
        stock = cur.fetchone()[0] or 0
        cur.execute("SELECT AVG(SellingPrice) FROM Products;")
        avg = cur.fetchone()[0] or 0
        # may fail if SalesOrderDetails missing; safe fallback used
        try:
            cur.execute("SELECT SUM(Quantity * UnitPrice) FROM SalesOrderDetails;")
            revenue = cur.fetchone()[0] or 0
        except Exception:
            revenue = 0

        win = tk.Toplevel(root)
        win.title("Aggregate Reports")
        win.geometry("700x500")
        win.configure(bg="#fffdf6")

        tk.Label(win, text="📊 Inventory & Sales Reports", font=("Helvetica", 14, "bold"), bg="#fffdf6").pack(pady=8)
        text = tk.Text(win, width=80, height=25, font=("Courier New", 10))
        text.pack(padx=10, pady=10)
        text.insert(tk.END, f"Total Products: {total}\nTotal Quantity: {stock}\nAverage Selling Price: ₹ {avg:.2f}\nTotal Revenue: ₹ {revenue:.2f}\n\nCategory-wise Stock Value:\n")
        cur.execute("SELECT Category, SUM(Quantity * CostPrice) FROM Products GROUP BY Category;")
        for cat, val in cur.fetchall():
            text.insert(tk.END, f"{cat:<20} ₹ {val:.2f}\n")
        text.config(state="disabled")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        con.close()

def view_customer_purchases():
    con = connect_db()
    if con is None:
        return
    try:
        cur = con.cursor()
        cur.execute("""
            SELECT c.Name, SUM(sod.Quantity) AS Items, SUM(sod.Quantity * sod.UnitPrice) AS Total
            FROM Customers c
            JOIN SalesOrders so ON c.CustomerID = so.CustomerID
            JOIN SalesOrderDetails sod ON so.SOID = sod.SOID
            GROUP BY c.CustomerID;
        """)
        rows = cur.fetchall()
        win = tk.Toplevel(root)
        win.title("Customer Purchase Summary")
        win.geometry("720x420")
        tree = ttk.Treeview(win, columns=("Customer", "Items", "Total"), show="headings")
        for col in ("Customer","Items","Total"):
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor="center")
        for r in rows:
            tree.insert("", "end", values=r)
        tree.pack(fill="both", expand=True, padx=10, pady=10)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        con.close()

# =================== DASHBOARD CARDS ===================
def build_dashboard_cards(frame):
    con = connect_db()
    counts = {}
    if con:
        try:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM Products;")
            counts['products'] = cur.fetchone()[0]

            try:
                cur.execute("SELECT COUNT(*) FROM Suppliers;")
                counts['suppliers'] = cur.fetchone()[0]
            except Exception:
                counts['suppliers'] = 0

            try:
                cur.execute("SELECT COUNT(*) FROM SalesOrders;")
                counts['sales'] = cur.fetchone()[0]
            except Exception:
                counts['sales'] = 0

            try:
                cur.execute("SELECT COUNT(*) FROM PurchaseOrders;")
                counts['purchases'] = cur.fetchone()[0]
            except Exception:
                counts['purchases'] = 0

            try:
                cur.execute("SELECT COUNT(*) FROM Customers;")
                counts['customers'] = cur.fetchone()[0]
            except Exception:
                counts['customers'] = 0

        except Exception:
            counts = {'products':0,'suppliers':0,'sales':0,'purchases':0,'customers':0}
        finally:
            con.close()
    else:
        counts = {'products':0,'suppliers':0,'sales':0,'purchases':0,'customers':0}

    
    card_specs = [
        ("Products", counts['products'], "#219ebc"),
        ("Suppliers", counts['suppliers'], "#8ac926"),
        ("Sales Orders", counts['sales'], "#fb5607"),
        ("Purchase Orders", counts['purchases'], "#8338ec"),
        ("Customers", counts['customers'], "#ff006e"),
    ]

    for i, (title, value, color) in enumerate(card_specs):
        card = tk.Frame(frame, bg=color, width=160, height=90, relief="raised", bd=1)
        card.grid(row=i//3, column=i%3, padx=12, pady=12, sticky="nsew")
        card.grid_propagate(False)
        tk.Label(card, text=title, bg=color, fg="white", font=("Helvetica", 12, "bold")).pack(anchor="w", padx=8, pady=(8,0))
        tk.Label(card, text=value, bg=color, fg="white", font=("Helvetica", 22, "bold")).pack(anchor="w", padx=8, pady=(0,8))


# =================== NAVIGATION PAGES -------------------
def show_dashboard(content_frame):
    for w in content_frame.winfo_children(): w.destroy()
    header = tk.Label(content_frame, text="Dashboard", font=("Helvetica", 18, "bold"), bg="#ffffff")
    header.pack(anchor="w", padx=12, pady=8)
    cards_frame = tk.Frame(content_frame, bg="#ffffff")
    cards_frame.pack(fill="x", padx=12)
    build_dashboard_cards(cards_frame)

def show_products_page(content_frame, username, role):
    for w in content_frame.winfo_children(): w.destroy()
    header = tk.Label(content_frame, text="Products", font=("Helvetica", 18, "bold"), bg="#ffffff")
    header.pack(anchor="w", padx=12, pady=8)

    top_fr = tk.Frame(content_frame, bg="#ffffff")
    top_fr.pack(fill="x", padx=12)

    # form inputs
    form = tk.LabelFrame(top_fr, text="Add / Update Product", bg="#ffffff")
    form.pack(side="left", padx=6, pady=6, fill="both", expand=False)

    name_v = tk.StringVar(); cat_v = tk.StringVar(); cost_v = tk.StringVar(); sell_v = tk.StringVar(); qty_v = tk.StringVar(); supp_v = tk.StringVar()
    tk.Label(form, text="Name:", bg="#ffffff").grid(row=0,column=0, sticky="w", padx=6, pady=4)
    tk.Entry(form, textvariable=name_v, width=18).grid(row=0,column=1, padx=6, pady=4)
    tk.Label(form, text="Category:", bg="#ffffff").grid(row=1,column=0, sticky="w", padx=6, pady=4)
    tk.Entry(form, textvariable=cat_v, width=18).grid(row=1,column=1, padx=6, pady=4)
    tk.Label(form, text="Cost:", bg="#ffffff").grid(row=0,column=2, sticky="w", padx=6, pady=4)
    tk.Entry(form, textvariable=cost_v, width=12).grid(row=0,column=3, padx=6, pady=4)
    tk.Label(form, text="Sell:", bg="#ffffff").grid(row=1,column=2, sticky="w", padx=6, pady=4)
    tk.Entry(form, textvariable=sell_v, width=12).grid(row=1,column=3, padx=6, pady=4)
    tk.Label(form, text="Qty:", bg="#ffffff").grid(row=2,column=0, sticky="w", padx=6, pady=4)
    tk.Entry(form, textvariable=qty_v, width=12).grid(row=2,column=1, padx=6, pady=4)
    tk.Label(form, text="Supplier ID:", bg="#ffffff").grid(row=2,column=2, sticky="w", padx=6, pady=4)
    tk.Entry(form, textvariable=supp_v, width=12).grid(row=2,column=3, padx=6, pady=4)

    # product tree
    tree_fr = tk.Frame(content_frame, bg="#ffffff")
    tree_fr.pack(fill="both", expand=True, padx=12, pady=8)

    global product_tree
    product_tree = ttk.Treeview(tree_fr, columns=("ID","Name","Category","Cost","Sell","Qty"), show="headings")
    for c in ("ID","Name","Category","Cost","Sell","Qty"):
        product_tree.heading(c, text=c)
        product_tree.column(c, width=120, anchor="center")
    vsb = ttk.Scrollbar(tree_fr, orient="vertical", command=product_tree.yview)
    product_tree.configure(yscroll=vsb.set)
    vsb.pack(side="right", fill="y")
    product_tree.pack(fill="both", expand=True)

    # right side controls
    ctrl_fr = tk.Frame(top_fr, bg="#ffffff")
    ctrl_fr.pack(side="left", padx=8, pady=6, fill="y")

    # Buttons with role checks
    def safe_add():
        add_product_from_vars(name_v, cat_v, cost_v, sell_v, qty_v, supp_v, product_tree)

    def safe_update():
        update_product_quantity_from_vars(product_tree, qty_v)

    btn_add = tk.Button(ctrl_fr, text="Add Product", command=safe_add, bg="#2a9d8f", fg="white", width=14)
    btn_update = tk.Button(ctrl_fr, text="Update Quantity", command=safe_update, bg="#ffb703", fg="black", width=14)
    btn_delete_sel = tk.Button(ctrl_fr, text="Delete Selected", command=partial(delete_selected_product, product_tree), bg="#e63946", fg="white", width=14)
    btn_check_stock = tk.Button(ctrl_fr, text="Check Stock", command=lambda: check_stock_status_for_selected(product_tree), bg="#06d6a0", fg="white", width=14)
    btn_total_value = tk.Button(ctrl_fr, text="Total Stock Value", command=get_total_stock_value, bg="#ffb703", fg="black", width=14)

    btn_add.pack(pady=6)
    btn_update.pack(pady=6)
    btn_delete_sel.pack(pady=6)
    btn_check_stock.pack(pady=6)
    btn_total_value.pack(pady=6)

    # Delete by name
    tk.Label(ctrl_fr, text="Delete by Name:", bg="#ffffff").pack(pady=(10,2))
    del_name_entry = tk.Entry(ctrl_fr)
    del_name_entry.pack(pady=4)
    btn_delete_name = tk.Button(ctrl_fr, text="Delete Name", command=partial(delete_product_by_name, del_name_entry, product_tree), bg="#d62828", fg="white", width=14)
    btn_delete_name.pack(pady=4)

    # Search box
    search_fr = tk.Frame(content_frame, bg="#ffffff")
    search_fr.pack(fill="x", padx=12)
    tk.Label(search_fr, text="Search (by name):", bg="#ffffff").pack(side="left", padx=6)
    search_var = tk.StringVar()
    search_e = tk.Entry(search_fr, textvariable=search_var, width=30)
    search_e.pack(side="left", padx=4)
    def search_action():
        q = search_var.get().strip()
        for r in product_tree.get_children(): product_tree.delete(r)
        con = connect_db()
        if con is None:
            return
        try:
            cur = con.cursor()
            if q:
                cur.execute("SELECT ProductID, Name, Category, CostPrice, SellingPrice, Quantity FROM Products WHERE Name LIKE %s", (f"%{q}%",))
            else:
                cur.execute("SELECT ProductID, Name, Category, CostPrice, SellingPrice, Quantity FROM Products")
            for r in cur.fetchall():
                product_tree.insert("", "end", values=r)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            con.close()
    tk.Button(search_fr, text="Search", command=search_action, bg="#0366d6", fg="white").pack(side="left", padx=6)
    tk.Button(search_fr, text="Reload All", command=lambda: load_products_into_tree(product_tree), bg="#6c757d", fg="white").pack(side="left", padx=6)

    # role-based UI adjustments (granular)
    if role == "Manager":
        # Manager can do most but not delete
        btn_delete_sel.config(state="disabled")
        btn_delete_name.config(state="disabled")
    elif role == "Staff":
        # Staff: disable add/update/delete controls but allow check stock, total stock, search/reload & view logs/reports
        btn_add.config(state="disabled")
        btn_update.config(state="disabled")
        btn_delete_sel.config(state="disabled")
        btn_delete_name.config(state="disabled")
    # else Admin: full access

    load_products_into_tree(product_tree)

def show_orders_page(content_frame, role):
    for w in content_frame.winfo_children(): w.destroy()
    header = tk.Label(content_frame, text="Orders", font=("Helvetica", 18, "bold"), bg="#ffffff")
    header.pack(anchor="w", padx=12, pady=8)

    frm = tk.Frame(content_frame, bg="#ffffff")
    frm.pack(padx=12, pady=10, fill="x")

    btn_add_sales = tk.Button(frm, text="Add Sales Order", command=add_sales_order, bg="#06d6a0", fg="white", width=18)
    btn_add_purchase = tk.Button(frm, text="Add Purchase Order", command=add_purchase_order, bg="#ffd166", fg="black", width=18)
    btn_view_sales_log = tk.Button(frm, text="View Sales Log (Trigger)", command=view_sales_log, bg="#ff8fab", fg="black", width=22)

    btn_add_sales.grid(row=0, column=0, padx=6, pady=6)
    btn_add_purchase.grid(row=0, column=1, padx=6, pady=6)
    btn_view_sales_log.grid(row=0, column=2, padx=6, pady=6)

    # Role restrictions:
    if role == "Manager":
        # Manager: can add sales and purchase, but you can adjust if needed
        pass
    elif role == "Staff":
        # staff should be blocked from adding orders
        btn_add_sales.config(state="disabled")
        btn_add_purchase.config(state="disabled")

def show_reports_page(content_frame):
    for w in content_frame.winfo_children(): w.destroy()
    header = tk.Label(content_frame, text="Reports & Queries", font=("Helvetica", 18, "bold"), bg="#ffffff")
    header.pack(anchor="w", padx=12, pady=8)
    frm = tk.Frame(content_frame, bg="#ffffff")
    frm.pack(padx=12, pady=10, fill="both", expand=True)
    tk.Button(frm, text="Aggregate Reports", command=view_aggregate_reports, bg="#f94144", fg="white", width=20).pack(pady=6)
    tk.Button(frm, text="Customer Purchase Summary", command=view_customer_purchases, bg="#577590", fg="white", width=24).pack(pady=6)
    tk.Button(frm, text="Products + Suppliers (JOIN)", command=view_products_with_suppliers, bg="#2a9d8f", fg="white", width=26).pack(pady=6)
    tk.Button(frm, text="Low Stock (Nested)", command=view_low_stock, bg="#ffb703", fg="black", width=24).pack(pady=6)

# =================== MAIN DASHBOARD / NAVIGATION ===================
def open_main_window(username, role):
    global root, product_tree
    root = tk.Tk()
    root.title(f"Inventory Management System - {role}")
    root.geometry("1200x760")
    root.configure(bg="#e9f5f8")

    # top bar
    top = tk.Frame(root, bg="#023047", height=60)
    top.pack(side="top", fill="x")
    tk.Label(top, text="📦 Inventory Management System", font=("Helvetica", 18, "bold"), bg="#023047", fg="white").pack(side="left", padx=18)
    tk.Label(top, text=f"Logged in as: {username} ({role})", bg="#ffb703", fg="#023047", padx=10, pady=6, font=("Helvetica",11,"bold"), relief="raised").pack(side="right", padx=12)

    # left sidebar
    sidebar = tk.Frame(root, bg="#0b132b", width=220)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # center content area
    content_frame = tk.Frame(root, bg="#ffffff")
    content_frame.pack(side="left", fill="both", expand=True)

    nav_buttons = [
        ("Dashboard", lambda: show_dashboard(content_frame)),
        ("Products", lambda: show_products_page(content_frame, username, role)),
        ("Orders", lambda: show_orders_page(content_frame, role)),
        ("Reports", lambda: show_reports_page(content_frame)),
        ("Customers", lambda: view_customer_purchases()),
        ("Logout", lambda: (root.destroy(), main()))
    ]

    tk.Label(sidebar, text="Menu", bg="#0b132b", fg="#ffffff", font=("Helvetica", 12, "bold")).pack(pady=(12,6))
    for (txt, cmd) in nav_buttons:
        b = tk.Button(sidebar, text=txt, command=cmd, bg="#14213d", fg="white", relief="flat", anchor="w")
        b.pack(fill="x", padx=12, pady=6)

    # default page
    show_dashboard(content_frame)

    # product_tree will be created inside products page (so define it here as placeholder)
    product_tree = None

    root.mainloop()

# =================== Safe reload helper - prevents invalid command name error ===========
def safe_reload_products():
    """Reload the product tree only if it exists and is a live widget."""
    global product_tree
    try:
        if product_tree is not None and product_tree.winfo_exists():
            load_products_into_tree(product_tree)
    except Exception:
        # swallow safely — protects against destroyed widgets
        pass

# =================== LOGIN WINDOW ENTRY POINT ===================
def main():
    global login_window, username_var, password_var
    login_window = tk.Tk()
    login_window.title("Login - Inventory System")
    login_window.geometry("420x320")
    login_window.configure(bg="#edf6f9")

    tk.Label(login_window, text="Inventory Management Login", font=("Helvetica", 16, "bold"), bg="#edf6f9", fg="#023047").pack(pady=14)
    frm = tk.Frame(login_window, bg="#edf6f9")
    frm.pack(padx=18, pady=6, fill="x")

    tk.Label(frm, text="Username:", bg="#edf6f9").grid(row=0, column=0, sticky="w", pady=6)
    username_var = tk.StringVar()
    tk.Entry(frm, textvariable=username_var).grid(row=0, column=1, pady=6, sticky="ew")

    tk.Label(frm, text="Password:", bg="#edf6f9").grid(row=1, column=0, sticky="w", pady=6)
    password_var = tk.StringVar()
    tk.Entry(frm, textvariable=password_var, show="*").grid(row=1, column=1, pady=6, sticky="ew")

    frm.columnconfigure(1, weight=1)
    btn_fr = tk.Frame(login_window, bg="#edf6f9")
    btn_fr.pack(pady=10)
    tk.Button(btn_fr, text="Login", command=login_user, bg="#023047", fg="white", width=14).grid(row=0, column=0, padx=6)
    tk.Button(btn_fr, text="Register", command=open_register_window, bg="#8ecae6", fg="black", width=14).grid(row=0, column=1, padx=6)

    login_window.mainloop()

if __name__ == "__main__":
    main()
