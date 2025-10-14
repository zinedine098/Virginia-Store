# TODO: Fix Cashier App Issues

## Issue 1: Product Image Not Showing in Modal for Barcode Input
- [x] Add image element to modal in home.html
- [x] Modify bukaDetail function to accept and display image URL
- [x] Update cariProdukByBarcode to pass image URL to bukaDetail

## Issue 2: Cart Updates Require Reload in Both Modes
- [x] Make cart functions mode-aware (detect current visible table: #tabelKeranjang or #tabelKeranjangBarcode)
- [x] Update tambahKeranjang to update correct table
- [x] Update updateJumlah to update correct table
- [x] Update hapusItem to update correct table
- [x] Update loadKeranjang to be mode-aware or unify with loadKeranjangBarcode
- [x] Ensure calculateTotal and calculateTotalBarcode are called correctly

## Testing
- [ ] Test card mode: add/update/remove items, check immediate updates
- [ ] Test barcode mode: input barcode, check image in modal, add/update/remove items, check immediate updates
