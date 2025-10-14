# TODO: Fix Cart Reset After Payment

## Steps to Complete:
- [x] Modify halaman_kasir to manage current transaksi in session and show messages
- [x] Add new view: get_keranjang (JSON of current details)
- [x] Update URLs for new view
- [x] Update tambah_ke_keranjang to use session transaksi
- [x] Update update_jumlah to use session transaksi
- [x] Update hapus_item to use session transaksi
- [x] Update halaman_bayar to use session transaksi
- [x] Update proses_bayar to use session transaksi, clear session after success, add message
- [x] Update batalkan_transaksi to use session transaksi
- [x] Update home.html: Add JS to load cart on load, update add/update/hapus
- [x] Test the flow
