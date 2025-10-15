# TODO List for Informasi Toko Implementation

## Step 1: Add InformasiToko Model
- [x] Add InformasiToko model to kasir/models.py with fields: address, factory, phone, mobile, email

## Step 2: Run Migrations
- [x] Run `python manage.py makemigrations`
- [x] Run `python manage.py migrate`

## Step 3: Update Views
- [x] Update halaman_struk in kasir/views.py to fetch InformasiToko and pass to context
- [x] Update cetak_pdf in nota/views.py to fetch InformasiToko and pass to context

## Step 4: Update Templates
- [x] Update kasir/templates/struk.html to use {{ informasi_toko.address }} etc. instead of hardcoded values
- [x] Update nota/templates/nota_struk.html to use {{ informasi_toko.address }} etc. instead of hardcoded values

## Step 5: Create Initial Data
- [x] Create an instance of InformasiToko with the existing data via Django admin or shell

## Step 6: Test
- [x] Test the display in struk.html
- [x] Test the display in nota_struk.html
