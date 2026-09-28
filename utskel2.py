import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pathlib import Path

# =========================================================
# MATPLOTLIB
# =========================================================
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


# =========================================================
# WARNA
# =========================================================
PINK = "#ff69b4"
DARK_PINK = "#d63384"
LIGHT_PINK = "#ffe6f2"
WHITE = "#ffffff"
TEXT = "#333333"
GRAY = "#777777"
RED = "#dc3545"
GREEN = "#198754"


# =========================================================
# DATA BARANG
# =========================================================
products = {
    "Indomie Goreng": {
        "harga": 3500,
        "stok": 30
    },
    "Indomie Kuah": {
        "harga": 3500,
        "stok": 30
    },
    "Beras 5 Kg": {
        "harga": 75000,
        "stok": 10
    },
    "Minyak Goreng 1L": {
        "harga": 18000,
        "stok": 20
    },
    "Gula 1 Kg": {
        "harga": 17000,
        "stok": 20
    },
    "Telur 1 Kg": {
        "harga": 30000,
        "stok": 15
    },
    "Aqua 600ml": {
        "harga": 4000,
        "stok": 40
    },
    "Teh Botol": {
        "harga": 5000,
        "stok": 30
    },
    "Kopi Sachet": {
        "harga": 2500,
        "stok": 40
    },
    "Rokok": {
        "harga": 25000,
        "stok": 20
    }
}


# =========================================================
# DATA TRANSAKSI
# =========================================================
cart = {}
sales_history = []

current_user = ""


# =========================================================
# FORMAT RUPIAH
# =========================================================
def rupiah(angka):
    return "Rp{:,.0f}".format(angka).replace(",", ".")


# =========================================================
# BERSIHKAN WINDOW
# =========================================================
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


# =========================================================
# HEADER
# =========================================================
def header(parent, title):
    frame = tk.Frame(
        parent,
        bg=PINK,
        height=70
    )
    frame.pack(fill="x")
    frame.pack_propagate(False)

    tk.Label(
        frame,
        text=title,
        font=("Arial", 22, "bold"),
        bg=PINK,
        fg=WHITE
    ).pack(side="left", padx=20)

    tk.Button(
        frame,
        text="Logout",
        command=logout,
        bg=WHITE,
        fg=DARK_PINK,
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=15
    ).pack(side="right", padx=20)


# =========================================================
# LOGIN
# =========================================================
def login():
    global current_user

    username = username_entry.get().strip()
    password = password_entry.get().strip()

    # LOGIN SESUAI KODE SEBELUMNYA
    if username == "admin" and password == "5678":
        current_user = "admin"
        show_admin()

    elif username == "kasir" and password == "1234":
        current_user = "kasir"
        show_cashier()

    else:
        messagebox.showerror(
            "Login Gagal",
            "Username atau password salah!"
        )


# =========================================================
# LOGOUT
# =========================================================
def logout():
    global cart
    cart = {}

    show_login()


# =========================================================
# HALAMAN LOGIN
# =========================================================
def show_login():
    clear_window()

    root.configure(bg=LIGHT_PINK)

    container = tk.Frame(
        root,
        bg=WHITE,
        padx=40,
        pady=40
    )
    container.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    tk.Label(
        container,
        text="WARUNG MADURA",
        font=("Arial", 25, "bold"),
        bg=WHITE,
        fg=DARK_PINK
    ).pack(pady=(0, 5))

    tk.Label(
        container,
        text="Sistem Kasir",
        font=("Arial", 12),
        bg=WHITE,
        fg=GRAY
    ).pack(pady=(0, 25))

    tk.Label(
        container,
        text="Username",
        bg=WHITE,
        fg=TEXT,
        font=("Arial", 10, "bold")
    ).pack(anchor="w")

    global username_entry
    username_entry = tk.Entry(
        container,
        width=30,
        font=("Arial", 12)
    )
    username_entry.pack(pady=(5, 15))

    tk.Label(
        container,
        text="Password",
        bg=WHITE,
        fg=TEXT,
        font=("Arial", 10, "bold")
    ).pack(anchor="w")

    global password_entry
    password_entry = tk.Entry(
        container,
        width=30,
        font=("Arial", 12),
        show="*"
    )
    password_entry.pack(pady=(5, 20))

    tk.Button(
        container,
        text="LOGIN",
        command=login,
        bg=PINK,
        fg=WHITE,
        font=("Arial", 12, "bold"),
        relief="flat",
        width=25,
        pady=8
    ).pack()

    tk.Label(
        container,
        text="Admin : admin / 5678\nKasir : kasir / 1234",
        bg=WHITE,
        fg=GRAY,
        font=("Arial", 9)
    ).pack(pady=(20, 0))


# =========================================================
# HALAMAN KASIR
# =========================================================
def show_cashier():
    clear_window()

    root.configure(bg=LIGHT_PINK)

    header(
        root,
        "WARUNG MADURA - KASIR"
    )

    # =====================================================
    # FRAME UTAMA
    # =====================================================
    main = tk.Frame(
        root,
        bg=LIGHT_PINK
    )
    main.pack(fill="both", expand=True, padx=15, pady=15)

    # =====================================================
    # FRAME KIRI
    # =====================================================
    left = tk.Frame(
        main,
        bg=WHITE,
        bd=1,
        relief="solid"
    )
    left.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 10)
    )

    tk.Label(
        left,
        text="DAFTAR BARANG",
        font=("Arial", 16, "bold"),
        bg=WHITE,
        fg=DARK_PINK
    ).pack(pady=10)

    # TABLE BARANG
    columns = ("nama", "harga", "stok")

    global product_tree

    product_tree = ttk.Treeview(
        left,
        columns=columns,
        show="headings",
        height=15
    )

    product_tree.heading(
        "nama",
        text="Nama Barang"
    )

    product_tree.heading(
        "harga",
        text="Harga"
    )

    product_tree.heading(
        "stok",
        text="Stok"
    )

    product_tree.column(
        "nama",
        width=180
    )

    product_tree.column(
        "harga",
        width=120
    )

    product_tree.column(
        "stok",
        width=80
    )

    product_tree.pack(
        fill="both",
        expand=True,
        padx=10
    )

    refresh_product_tree()

    # =====================================================
    # BUTTON TRANSAKSI
    # =====================================================
    transaction_frame = tk.Frame(
        left,
        bg=WHITE
    )
    transaction_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )

    tk.Button(
        transaction_frame,
        text="Tambah ke Keranjang",
        command=add_to_cart,
        bg=PINK,
        fg=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=10,
        pady=8
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        transaction_frame,
        text="Hapus dari Keranjang",
        command=remove_cart_item,
        bg=RED,
        fg=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=10,
        pady=8
    ).pack(
        side="left",
        padx=5
    )

    # =====================================================
    # FRAME KANAN
    # =====================================================
    right = tk.Frame(
        main,
        bg=WHITE,
        bd=1,
        relief="solid",
        width=400
    )
    right.pack(
        side="right",
        fill="both",
        padx=(10, 0)
    )

    tk.Label(
        right,
        text="KERANJANG",
        font=("Arial", 16, "bold"),
        bg=WHITE,
        fg=DARK_PINK
    ).pack(pady=10)

    global cart_tree

    cart_tree = ttk.Treeview(
        right,
        columns=("nama", "qty", "subtotal"),
        show="headings",
        height=10
    )

    cart_tree.heading(
        "nama",
        text="Barang"
    )

    cart_tree.heading(
        "qty",
        text="Qty"
    )

    cart_tree.heading(
        "subtotal",
        text="Subtotal"
    )

    cart_tree.column(
        "nama",
        width=150
    )

    cart_tree.column(
        "qty",
        width=50
    )

    cart_tree.column(
        "subtotal",
        width=110
    )

    cart_tree.pack(
        fill="both",
        expand=True,
        padx=10
    )

    # TOTAL
    global total_label

    total_label = tk.Label(
        right,
        text="Total: Rp0",
        font=("Arial", 18, "bold"),
        bg=WHITE,
        fg=DARK_PINK
    )
    total_label.pack(pady=10)

    # =====================================================
    # PEMBAYARAN
    # =====================================================
    payment_frame = tk.Frame(
        right,
        bg=WHITE
    )
    payment_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )

    tk.Label(
        payment_frame,
        text="Uang Bayar",
        bg=WHITE,
        font=("Arial", 10, "bold")
    ).pack(anchor="w")

    global payment_entry

    payment_entry = tk.Entry(
        payment_frame,
        font=("Arial", 13)
    )
    payment_entry.pack(
        fill="x",
        pady=5
    )

    tk.Button(
        payment_frame,
        text="BAYAR & CETAK STRUK",
        command=checkout,
        bg=GREEN,
        fg=WHITE,
        font=("Arial", 11, "bold"),
        relief="flat",
        pady=10
    ).pack(
        fill="x",
        pady=5
    )

    # =====================================================
    # FITUR KELOLA BARANG
    # SEKARANG KASIR JUGA BISA
    # =====================================================
    manage_frame = tk.LabelFrame(
        right,
        text="Kelola Barang",
        bg=WHITE,
        fg=DARK_PINK,
        font=("Arial", 11, "bold")
    )
    manage_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )

    tk.Button(
        manage_frame,
        text="➕ Tambah Barang",
        command=add_product,
        bg=PINK,
        fg=WHITE,
        font=("Arial", 9, "bold"),
        relief="flat"
    ).grid(
        row=0,
        column=0,
        padx=5,
        pady=5,
        sticky="ew"
    )

    tk.Button(
        manage_frame,
        text="✏ Edit Harga",
        command=edit_price,
        bg=DARK_PINK,
        fg=WHITE,
        font=("Arial", 9, "bold"),
        relief="flat"
    ).grid(
        row=0,
        column=1,
        padx=5,
        pady=5,
        sticky="ew"
    )

    tk.Button(
        manage_frame,
        text="📦 Edit Stok",
        command=edit_stock,
        bg=GREEN,
        fg=WHITE,
        font=("Arial", 9, "bold"),
        relief="flat"
    ).grid(
        row=1,
        column=0,
        padx=5,
        pady=5,
        sticky="ew"
    )

    tk.Button(
        manage_frame,
        text="🗑 Hapus Barang",
        command=delete_product,
        bg=RED,
        fg=WHITE,
        font=("Arial", 9, "bold"),
        relief="flat"
    ).grid(
        row=1,
        column=1,
        padx=5,
        pady=5,
        sticky="ew"
    )

    manage_frame.columnconfigure(0, weight=1)
    manage_frame.columnconfigure(1, weight=1)

    refresh_cart()


# =========================================================
# REFRESH DAFTAR BARANG
# =========================================================
def refresh_product_tree():
    if "product_tree" not in globals():
        return

    for item in product_tree.get_children():
        product_tree.delete(item)

    for nama, data in products.items():
        product_tree.insert(
            "",
            "end",
            values=(
                nama,
                rupiah(data["harga"]),
                data["stok"]
            )
        )


# =========================================================
# TAMBAH KE KERANJANG
# =========================================================
def add_to_cart():
    selected = product_tree.selection()

    if not selected:
        messagebox.showwarning(
            "Peringatan",
            "Pilih barang terlebih dahulu!"
        )
        return

    item = product_tree.item(selected[0])
    nama = item["values"][0]

    if products[nama]["stok"] <= 0:
        messagebox.showerror(
            "Stok Habis",
            f"Stok {nama} sudah habis!"
        )
        return

    if nama in cart:
        if cart[nama] < products[nama]["stok"]:
            cart[nama] += 1
        else:
            messagebox.showwarning(
                "Stok",
                "Jumlah melebihi stok!"
            )
    else:
        cart[nama] = 1

    refresh_cart()


# =========================================================
# REFRESH KERANJANG
# =========================================================
def refresh_cart():
    if "cart_tree" not in globals():
        return

    for item in cart_tree.get_children():
        cart_tree.delete(item)

    total = 0

    for nama, qty in cart.items():

        harga = products[nama]["harga"]

        subtotal = harga * qty

        total += subtotal

        cart_tree.insert(
            "",
            "end",
            values=(
                nama,
                qty,
                rupiah(subtotal)
            )
        )

    total_label.config(
        text=f"Total: {rupiah(total)}"
    )


# =========================================================
# HAPUS DARI KERANJANG
# =========================================================
def remove_cart_item():
    selected = cart_tree.selection()

    if not selected:
        messagebox.showwarning(
            "Peringatan",
            "Pilih barang di keranjang!"
        )
        return

    item = cart_tree.item(selected[0])

    nama = item["values"][0]

    if nama in cart:
        del cart[nama]

    refresh_cart()


# =========================================================
# TAMBAH BARANG
# =========================================================
def add_product():
    window = tk.Toplevel(root)

    window.title("Tambah Barang")

    window.geometry("350x300")

    window.configure(bg=WHITE)

    tk.Label(
        window,
        text="TAMBAH BARANG",
        font=("Arial", 16, "bold"),
        bg=WHITE,
        fg=DARK_PINK
    ).pack(pady=15)

    tk.Label(
        window,
        text="Nama Barang",
        bg=WHITE
    ).pack()

    nama_entry = tk.Entry(
        window,
        width=30
    )
    nama_entry.pack(pady=5)

    tk.Label(
        window,
        text="Harga",
        bg=WHITE
    ).pack()

    harga_entry = tk.Entry(
        window,
        width=30
    )
    harga_entry.pack(pady=5)

    tk.Label(
        window,
        text="Stok",
        bg=WHITE
    ).pack()

    stok_entry = tk.Entry(
        window,
        width=30
    )
    stok_entry.pack(pady=5)

    def save_product():

        nama = nama_entry.get().strip()

        if not nama:
            messagebox.showerror(
                "Error",
                "Nama barang harus diisi!"
            )
            return

        if nama in products:
            messagebox.showerror(
                "Error",
                "Barang sudah ada!"
            )
            return

        try:
            harga = int(harga_entry.get())
            stok = int(stok_entry.get())

            if harga < 0 or stok < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Error",
                "Harga dan stok harus berupa angka!"
            )
            return

        products[nama] = {
            "harga": harga,
            "stok": stok
        }

        refresh_product_tree()

        messagebox.showinfo(
            "Berhasil",
            "Barang berhasil ditambahkan!"
        )

        window.destroy()

    tk.Button(
        window,
        text="SIMPAN",
        command=save_product,
        bg=PINK,
        fg=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=30,
        pady=8
    ).pack(pady=15)


# =========================================================
# EDIT HARGA
# =========================================================
def edit_price():
    selected = product_tree.selection()

    if not selected:
        messagebox.showwarning(
            "Peringatan",
            "Pilih barang terlebih dahulu!"
        )
        return

    item = product_tree.item(selected[0])

    nama = item["values"][0]

    window = tk.Toplevel(root)

    window.title("Edit Harga")

    window.geometry("350x220")

    window.configure(bg=WHITE)

    tk.Label(
        window,
        text=f"Edit Harga\n{nama}",
        font=("Arial", 15, "bold"),
        bg=WHITE,
        fg=DARK_PINK
    ).pack(pady=15)

    entry = tk.Entry(
        window,
        width=30
    )
    entry.pack(pady=10)

    entry.insert(
        0,
        str(products[nama]["harga"])
    )

    def save():

        try:
            harga = int(entry.get())

            if harga < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Error",
                "Harga harus berupa angka!"
            )
            return

        products[nama]["harga"] = harga

        refresh_product_tree()

        messagebox.showinfo(
            "Berhasil",
            "Harga berhasil diubah!"
        )

        window.destroy()

    tk.Button(
        window,
        text="SIMPAN",
        command=save,
        bg=PINK,
        fg=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=30,
        pady=8
    ).pack()


# =========================================================
# EDIT STOK
# =========================================================
def edit_stock():
    selected = product_tree.selection()

    if not selected:
        messagebox.showwarning(
            "Peringatan",
            "Pilih barang terlebih dahulu!"
        )
        return

    item = product_tree.item(selected[0])

    nama = item["values"][0]

    window = tk.Toplevel(root)

    window.title("Edit Stok")

    window.geometry("350x220")

    window.configure(bg=WHITE)

    tk.Label(
        window,
        text=f"Edit Stok\n{nama}",
        font=("Arial", 15, "bold"),
        bg=WHITE,
        fg=DARK_PINK
    ).pack(pady=15)

    entry = tk.Entry(
        window,
        width=30
    )
    entry.pack(pady=10)

    entry.insert(
        0,
        str(products[nama]["stok"])
    )

    def save():

        try:
            stok = int(entry.get())

            if stok < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Error",
                "Stok harus berupa angka!"
            )
            return

        products[nama]["stok"] = stok

        refresh_product_tree()

        messagebox.showinfo(
            "Berhasil",
            "Stok berhasil diubah!"
        )

        window.destroy()

    tk.Button(
        window,
        text="SIMPAN",
        command=save,
        bg=GREEN,
        fg=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=30,
        pady=8
    ).pack()


# =========================================================
# HAPUS BARANG
# =========================================================
def delete_product():
    selected = product_tree.selection()

    if not selected:
        messagebox.showwarning(
            "Peringatan",
            "Pilih barang terlebih dahulu!"
        )
        return

    item = product_tree.item(selected[0])

    nama = item["values"][0]

    confirm = messagebox.askyesno(
        "Konfirmasi",
        f"Apakah kamu yakin ingin menghapus {nama}?"
    )

    if confirm:

        if nama in cart:
            del cart[nama]

        del products[nama]

        refresh_product_tree()

        refresh_cart()

        messagebox.showinfo(
            "Berhasil",
            "Barang berhasil dihapus!" 
        )


# =========================================================
# CHECKOUT
# =========================================================
def checkout():

    if not cart:
        messagebox.showwarning(
            "Keranjang Kosong",
            "Belum ada barang di keranjang!"
        )
        return

    try:
        bayar = int(payment_entry.get())

    except ValueError:
        messagebox.showerror(
            "Error",
            "Masukkan jumlah uang yang benar!"
        )
        return

    total = 0

    for nama, qty in cart.items():

        total += products[nama]["harga"] * qty

    if bayar < total:

        messagebox.showerror(
            "Pembayaran Kurang",
            f"Total: {rupiah(total)}\n"
            f"Bayar: {rupiah(bayar)}\n\n"
            f"Uang masih kurang {rupiah(total - bayar)}"
        )

        return

    kembalian = bayar - total

    # Kurangi stok
    for nama, qty in cart.items():

        products[nama]["stok"] -= qty

    # Simpan transaksi
    sales_history.append({
        "tanggal": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        ),
        "kasir": current_user,
        "total": total,
        "bayar": bayar,
        "kembalian": kembalian
    })

    receipt = make_receipt(
        total,
        bayar,
        kembalian
    )

    # Simpan struk
    filename = (
        "struk_"
        + datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
        + ".txt"
    )

    Path(filename).write_text(
        receipt,
        encoding="utf-8"
    )

    show_receipt(receipt)

    cart.clear()

    refresh_product_tree()

    refresh_cart()

    payment_entry.delete(
        0,
        tk.END
    )


# =========================================================
# BUAT STRUK
# =========================================================
def make_receipt(
    total,
    bayar,
    kembalian
):

    lines = []

    lines.append(
        "================================"
    )

    lines.append(
        "        WARUNG MADURA"
    )

    lines.append(
        "================================"
    )

    lines.append(
        datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )
    )

    lines.append(
        f"Kasir : {current_user}"
    )

    lines.append(
        "--------------------------------"
    )

    for nama, qty in cart.items():

        harga = products[nama]["harga"]

        subtotal = harga * qty

        lines.append(
            f"{nama}"
        )

        lines.append(
            f"{qty} x {rupiah(harga)} = {rupiah(subtotal)}"
        )

    lines.append(
        "--------------------------------"
    )

    lines.append(
        f"TOTAL     : {rupiah(total)}"
    )

    lines.append(
        f"BAYAR     : {rupiah(bayar)}"
    )

    lines.append(
        f"KEMBALIAN : {rupiah(kembalian)}"
    )

    lines.append(
        "================================"
    )

    lines.append(
        "      TERIMA KASIH"
    )

    lines.append(
        "================================"
    )

    return "\n".join(lines)


# =========================================================
# TAMPILKAN STRUK
# =========================================================
def show_receipt(receipt):

    window = tk.Toplevel(root)

    window.title("Struk Pembayaran")

    window.geometry(
        "450x600"
    )

    text = tk.Text(
        window,
        font=("Courier New", 10)
    )

    text.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    text.insert(
        "1.0",
        receipt
    )

    text.config(
        state="disabled"
    )

    tk.Button(
        window,
        text="Tutup",
        command=window.destroy,
        bg=PINK,
        fg=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=30,
        pady=8
    ).pack(pady=10)


# =========================================================
# HALAMAN ADMIN
# =========================================================
def show_admin():

    clear_window()

    root.configure(
        bg=LIGHT_PINK
    )

    header(
        root,
        "WARUNG MADURA - ADMIN"
    )

    main = tk.Frame(
        root,
        bg=LIGHT_PINK
    )

    main.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    # DASHBOARD
    tk.Label(
        main,
        text="Dashboard Admin",
        font=("Arial", 24, "bold"),
        bg=LIGHT_PINK,
        fg=DARK_PINK
    ).pack(pady=15)

    # Statistik
    stat_frame = tk.Frame(
        main,
        bg=LIGHT_PINK
    )

    stat_frame.pack(
        fill="x",
        pady=10
    )

    create_stat(
        stat_frame,
        "Jumlah Barang",
        len(products)
    ).pack(
        side="left",
        fill="x",
        expand=True,
        padx=5
    )

    create_stat(
        stat_frame,
        "Total Stok",
        sum(
            item["stok"]
            for item in products.values()
        )
    ).pack(
        side="left",
        fill="x",
        expand=True,
        padx=5
    )

    create_stat(
        stat_frame,
        "Transaksi",
        len(sales_history)
    ).pack(
        side="left",
        fill="x",
        expand=True,
        padx=5
    )

    # TOMBOL
    button_frame = tk.Frame(
        main,
        bg=LIGHT_PINK
    )

    button_frame.pack(
        pady=30
    )

    tk.Button(
        button_frame,
        text="📦 Kelola Barang",
        command=admin_products,
        bg=PINK,
        fg=WHITE,
        font=("Arial", 12, "bold"),
        relief="flat",
        padx=25,
        pady=15
    ).grid(
        row=0,
        column=0,
        padx=10
    )

    tk.Button(
        button_frame,
        text="📊 Grafik Penjualan",
        command=show_sales_graph,
        bg=DARK_PINK,
        fg=WHITE,
        font=("Arial", 12, "bold"),
        relief="flat",
        padx=25,
        pady=15
    ).grid(
        row=0,
        column=1,
        padx=10
    )

    tk.Button(
        button_frame,
        text="📋 Data Penjualan",
        command=show_sales_data,
        bg=GREEN,
        fg=WHITE,
        font=("Arial", 12, "bold"),
        relief="flat",
        padx=25,
        pady=15
    ).grid(
        row=0,
        column=2,
        padx=10
    )


# =========================================================
# STATISTIK
# =========================================================
def create_stat(
    parent,
    title,
    value
):

    frame = tk.Frame(
        parent,
        bg=WHITE,
        bd=1,
        relief="solid",
        padx=20,
        pady=15
    )

    tk.Label(
        frame,
        text=title,
        bg=WHITE,
        fg=GRAY,
        font=("Arial", 10)
    ).pack()

    tk.Label(
        frame,
        text=value,
        bg=WHITE,
        fg=DARK_PINK,
        font=("Arial", 22, "bold")
    ).pack()

    return frame


# =========================================================
# KELOLA BARANG ADMIN
# =========================================================
def admin_products():

    window = tk.Toplevel(root)

    window.title(
        "Kelola Barang"
    )

    window.geometry(
        "700x500"
    )

    window.configure(
        bg=LIGHT_PINK
    )

    tk.Label(
        window,
        text="KELOLA BARANG",
        font=("Arial", 20, "bold"),
        bg=LIGHT_PINK,
        fg=DARK_PINK
    ).pack(pady=15)

    columns = (
        "nama",
        "harga",
        "stok"
    )

    tree = ttk.Treeview(
        window,
        columns=columns,
        show="headings"
    )

    tree.heading(
        "nama",
        text="Nama Barang"
    )

    tree.heading(
        "harga",
        text="Harga"
    )

    tree.heading(
        "stok",
        text="Stok"
    )

    tree.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    def refresh():

        for item in tree.get_children():
            tree.delete(item)

        for nama, data in products.items():

            tree.insert(
                "",
                "end",
                values=(
                    nama,
                    rupiah(data["harga"]),
                    data["stok"]
                )
            )

    refresh()

    button_frame = tk.Frame(
        window,
        bg=LIGHT_PINK
    )

    button_frame.pack(
        pady=10
    )

    tk.Button(
        button_frame,
        text="Tambah",
        command=add_product,
        bg=PINK,
        fg=WHITE,
        relief="flat",
        padx=20,
        pady=8
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        button_frame,
        text="Edit Harga",
        command=edit_price,
        bg=DARK_PINK,
        fg=WHITE,
        relief="flat",
        padx=20,
        pady=8
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        button_frame,
        text="Edit Stok",
        command=edit_stock,
        bg=GREEN,
        fg=WHITE,
        relief="flat",
        padx=20,
        pady=8
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        button_frame,
        text="Hapus",
        command=delete_product,
        bg=RED,
        fg=WHITE,
        relief="flat",
        padx=20,
        pady=8
    ).pack(
        side="left",
        padx=5
    )


# =========================================================
# GRAFIK PENJUALAN
# =========================================================
def show_sales_graph():

    if not MATPLOTLIB_AVAILABLE:

        messagebox.showerror(
            "Error",
            "Matplotlib belum terinstall.\n\n"
            "Install dengan:\n"
            "pip install matplotlib"
        )

        return

    if not sales_history:

        messagebox.showinfo(
            "Grafik",
            "Belum ada data transaksi."
        )

        return

    totals = []

    labels = []

    for sale in sales_history:

        labels.append(
            sale["tanggal"]
        )

        totals.append(
            sale["total"]
        )

    plt.figure(
        figsize=(10, 5)
    )

    plt.plot(
        range(
            1,
            len(totals) + 1
        ),
        totals,
        marker="o"
    )

    plt.title(
        "Grafik Penjualan Warung Madura"
    )

    plt.xlabel(
        "Transaksi"
    )

    plt.ylabel(
        "Total Penjualan"
    )

    plt.xticks(
        range(
            1,
            len(totals) + 1
        ),
        labels,
        rotation=45
    )

    plt.tight_layout()

    plt.show()


# =========================================================
# DATA PENJUALAN
# =========================================================
def show_sales_data():

    window = tk.Toplevel(root)

    window.title(
        "Data Penjualan"
    )

    window.geometry(
        "800x450"
    )

    window.configure(
        bg=WHITE
    )

    tk.Label(
        window,
        text="DATA PENJUALAN",
        font=("Arial", 20, "bold"),
        bg=WHITE,
        fg=DARK_PINK
    ).pack(pady=15)

    columns = (
        "tanggal",
        "kasir",
        "total",
        "bayar",
        "kembalian"
    )

    tree = ttk.Treeview(
        window,
        columns=columns,
        show="headings"
    )

    tree.heading(
        "tanggal",
        text="Tanggal"
    )

    tree.heading(
        "kasir",
        text="Kasir"
    )

    tree.heading(
        "total",
        text="Total"
    )

    tree.heading(
        "bayar",
        text="Bayar"
    )

    tree.heading(
        "kembalian",
        text="Kembalian"
    )

    for sale in sales_history:

        tree.insert(
            "",
            "end",
            values=(
                sale["tanggal"],
                sale["kasir"],
                rupiah(sale["total"]),
                rupiah(sale["bayar"]),
                rupiah(sale["kembalian"])
            )
        )

    tree.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )


# =========================================================
# WINDOW UTAMA
# =========================================================
root = tk.Tk()

root.title(
    "Warung Madura - Sistem Kasir"
)

root.geometry(
    "1100x700"
)

root.minsize(
    900,
    600
)

show_login()

root.mainloop()