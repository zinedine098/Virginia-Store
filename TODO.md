# TODO: Change nota_suplayer app from Customer to Suplayer

- [x] Edit nota_suplayer/models.py: Change import to Suplayer, field to suplayer, update __str__
- [x] Edit nota_suplayer/forms.py: Change model to Suplayer, rename CustomerForm to SuplayerForm, update fields and widgets
- [x] Edit nota_suplayer/views.py: Change import to Suplayer, CustomerForm to SuplayerForm, add_customer to add_suplayer, update field accesses and JSON keys
- [x] Edit nota_suplayer/urls.py: Change path to 'add_suplayer/', name to 'add_suplayer'
- [x] Edit nota_suplayer/templates/nota_struk.html: Replace 'customer' with 'suplayer', update labels
- [x] Edit nota_suplayer/templates/nota_struk_modal.html: Replace 'customer' with 'suplayer', update labels
- [x] Edit nota_suplayer/templates/nota_kosong.html: Replace 'customer' with 'suplayer', update labels
- [x] Edit nota_suplayer/templates/edit_nota.html: Replace 'customer' with 'suplayer', update labels
- [x] Edit nota_suplayer/templates/cetak_nota_kosong.html: Replace 'customer' with 'suplayer', update labels
- [ ] Run python manage.py makemigrations nota_suplayer
- [ ] Run python manage.py migrate
- [ ] Test the app
