# TODO List for Modifying Bayar Button to Show Receipt Modal

- [x] Edit kasir/views.py: Modify proses_bayar to render bayar.html with additional context (transaksi, details, total, informasi_toko, show_modal=True) after saving transaction.
- [x] Edit kasir/templates/bayar.html: Add Bootstrap modal with receipt content, conditional show via JavaScript, update print button for modal only, change back button to close modal and redirect.
- [ ] Test: Run server, perform transaction, verify modal appears, print works for modal, back button closes modal and redirects.
