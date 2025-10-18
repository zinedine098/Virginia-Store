# TODO: Ubah Sistem Nota Kosong agar Langsung Simpan ke Database

## Step 1: Tambah Field is_temporary di NotaPayment Model
- Edit nota/models.py untuk menambah field Boolean is_temporary dengan default True.

## Step 2: Modifikasi View nota_kosong
- Jika belum ada temp_nota_id di session, buat NotaPayment temporary dan simpan id di session.
- Saat add_item, simpan langsung NotaKosong ke DB dengan nota_payment_id dari session.
- Load daftar_barang dari DB berdasarkan nota_payment_id temporary.
- Pada submit_payment, update NotaPayment dengan data form dan set is_temporary=False.

## Step 3: Update Fungsi update_quantity
- Pastikan update langsung ke DB untuk item yang ada.

## Step 4: Update Fungsi delete_item
- Pastikan delete langsung dari DB.

## Step 5: Update Template nota_kosong.html
- Pastikan script JavaScript handle db_id untuk setiap item.

## Step 6: Test Perubahan
- Jalankan server dan test add item, update quantity, delete, dan submit payment.
