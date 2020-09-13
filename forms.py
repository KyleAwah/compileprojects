from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DecimalField, DateField, FileField, Form, FormField, SelectField, FieldList
from wtforms.validators import InputRequired, Email, EqualTo
from flask_wtf.file import FileField
from wtforms.widgets import TextArea

class product_fields(Form):
    product_name = StringField('Product Name', render_kw={"placeholder": "Product Name"})
    product_QTY = IntegerField('Product QTY', render_kw={"placeholder": " 12 "})
    product_cost_per = DecimalField('Cost Per Product', render_kw={"placeholder": " 15.99 "})

class invoice_fields(FlaskForm):
    invoice_date = DateField('Transaction Date', format='%d-%m-%Y', render_kw={"placeholder": "Day - Month - Year"})
    invoice_number = StringField('Invoice Number', render_kw={"placeholder": "10"})
    currency = SelectField('Currency', choices=[('TTD', '$ TTD'), ('USD', '$ USD'), ('CAD', '$ CAD'), ('GBP', '£ GBP'), ('EURO', '€ EURO')], default=('TTD', '$ TTD'))
    vat = DecimalField('VAT %', render_kw={"placeholder": " 12.5 "}, default= 0.0)
    invoice_policy = StringField('Transaction Policy', render_kw={"placeholder": "Our Policy is that any purchases made through our buisness is subjected to a 10% discount"}, widget=TextArea())
    logo = FileField('logo')
    buisness_name = StringField('Buisness Name', render_kw={"placeholder": "Buisness Name"})
    buisness_address = StringField('Buisness Address', render_kw={"placeholder": "34 X Street Port-of-Spain, Trinidad"})
    buisness_email = StringField('Buisness Email', render_kw={"placeholder": "buisnessemail@gmail.com"})
    client_name = StringField('Client Name', render_kw={"placeholder": "Client Name"})
    client_address = StringField('Client Address', render_kw={"placeholder": "34 X Street Port-of-Spain, Trinidad"})
    client_email = StringField('Client Email', render_kw={"placeholder": "clientemail@gmail.com"})
    product = FieldList(FormField(product_fields), min_entries = 1)
    submit_main = SubmitField('DOWNLOAD INVOICE', render_kw={'class': 'submit_btn'})

class bill_fields(FlaskForm):
    invoice_date = DateField('Transaction Date', format='%d-%m-%Y', render_kw={"placeholder": "Day - Month - Year"})
    invoice_number = StringField('Social Media / Promotional Link', render_kw={"placeholder": "www.yourwebsite.com"})
    currency = SelectField('Currency', choices=[('TTD', '$ TTD'), ('USD', '$ USD'), ('CAD', '$ CAD'), ('GBP', '£ GBP'), ('EURO', '€ EURO')], default=('TTD', '$ TTD'))
    vat = DecimalField('VAT %', render_kw={"placeholder": " 12.5 "}, default= 0.0)
    invoice_policy = StringField('Promotional Paragraph', render_kw={"placeholder": "Enter details about your latest company promotion going on"}, widget=TextArea())
    logo = FileField('logo')
    buisness_name = StringField('Buisness Name', render_kw={"placeholder": "Buisness Name"})
    buisness_address = StringField('Buisness Address', render_kw={"placeholder": "34 X Street Port-of-Spain, Trinidad"})
    product = FieldList(FormField(product_fields), min_entries = 1)
    submit_main = SubmitField('DOWNLOAD RECEIPT', render_kw={'class': 'submit_btn'})

class SignUp(FlaskForm):
    username = StringField('Username', render_kw={'class': 'login_fields'}, validators=[InputRequired('A password is required')])
    first_name = StringField('First Name', render_kw={'class': 'login_fields'}, validators=[InputRequired('A first name is required')])
    last_name = StringField('Last Name', render_kw={'class': 'login_fields'}, validators=[InputRequired('A last name is required')])
    email = StringField('Email', render_kw={'class': 'login_fields'}, validators=[Email(), InputRequired('An email is required')])
    phone = StringField('Whatsapp Phone Number (Optional)', render_kw={'class': 'login_fields'})
    password = PasswordField('Password', render_kw={'class': 'login_fields'}, validators=[InputRequired('A password is required')])
    submit = SubmitField('SIGN UP', render_kw={'class': 'login_btn'})
    re = RecaptchaField()

class LogIn(FlaskForm):
    email = StringField('Email', render_kw={'class': 'login_fields'}, validators=[Email(), InputRequired('Email missing')])
    password = PasswordField('Password', render_kw={'class': 'login_fields'}, validators=[InputRequired('Password missing')])
    re = RecaptchaField()
    submit = SubmitField('LOGIN', render_kw={'class': 'login_btn'})

class EditEmail(FlaskForm):
    email = StringField('New Email', render_kw={'class': 'login_fields'}, validators=[Email(), InputRequired('A new email missing')])
    submit = SubmitField('SAVE CHANGES', render_kw={'class': 'SAVE'})

class EditUsername(FlaskForm):
    username = StringField('New Username', render_kw={'class': 'login_fields'}, validators=[InputRequired('A new username is missing')])
    submit = SubmitField('SAVE CHANGES', render_kw={'class': 'SAVE'})

class EditName(FlaskForm):
    first_name = StringField('New First Name', render_kw={'class': 'login_fields'}, validators=[InputRequired('A new first name is missing')])
    last_name = StringField('New Last Name', render_kw={'class': 'login_fields'}, validators=[InputRequired('A new last name is missing')])
    submit = SubmitField('SAVE CHANGES', render_kw={'class': 'SAVE'})

class EditPassword(FlaskForm):
    old_password = PasswordField('Old Password', render_kw={'class': 'login_fields'}, validators=[InputRequired('Your old password is required')])
    new_password = PasswordField('New Password', render_kw={'class': 'login_fields'}, validators=[InputRequired('A password is required'), EqualTo('new_2_password', message='Passwords must match')])
    new_2_password = PasswordField('Repeat New Password', render_kw={'class': 'login_fields'})
    submit = SubmitField('SAVE CHANGES', render_kw={'class': 'SAVE'})

class SendLostPasswordLink(FlaskForm):
    email = StringField('Please enter the email for your account', render_kw={'class': 'login_fields'}, validators=[Email(), InputRequired('Please enter the email for your account')])
    re = RecaptchaField()
    submit = SubmitField('SEND LINK', render_kw={'class': 'login_btn'})

class EditPassword_reset(FlaskForm):
    new_password = PasswordField('New Password', render_kw={'class': 'login_fields'}, validators=[InputRequired('A password is required'), EqualTo('new_2_password', message='Passwords must match')])
    new_2_password = PasswordField('Repeat New Password', render_kw={'class': 'login_fields'})
    submit = SubmitField('SAVE CHANGES', render_kw={'class': 'login_btn'})

class EmailSend(FlaskForm):
    email = StringField("Receiver's Email address", render_kw={'class': 'login_fields'}, validators=[Email(), InputRequired('Email missing')])
    email_subject = StringField('Subject of Email', render_kw={'class': 'login_fields'}, validators=[InputRequired('Subject of Email Missing')])
    email_body = StringField('Body of Email', render_kw={'class': 'login_fields'}, validators=[InputRequired('Body of Email Missing')], widget=TextArea())
    email_bottom = StringField('Top Label of Email', render_kw={'class': 'login_fields'}, validators=[InputRequired('Top Label  of Email Missing')], widget=TextArea())
    submit = SubmitField('SEND EMAIL', render_kw={'class': 'SAVE'})