# COMPILE PROJECTS 2020
# KYLE HALO

# IMPORT FILES #
import os
import os.path as op
import json
import datetime
from functools import wraps
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask import Flask, request, render_template, redirect, flash, url_for, make_response, session, Markup, flash, Response, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from models import db, user, product, orders, wish_list
from forms import invoice_fields, product_fields, bill_fields, SignUp, LogIn, EditEmail, EditUsername, EditName, EditPassword, SendLostPasswordLink, EditPassword_reset, EmailSend
from flask_weasyprint import HTML, render_pdf
from flask_uploads import UploadSet, configure_uploads, IMAGES
import qrcode
from flask_qrcode import QRcode
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

# Login Manager #
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
 return user.query.get(user_id)

# Admin Manager Custom Decorator #
def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin:					
           return func(*args, **kwargs)
        else:
          flash('Account does not have Administrator Privileges')
          return redirect(url_for('index'))
    return decorated_function

# Default User Manager Custom Decorator #
def default_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_premium:					
           return func(*args, **kwargs)
        else:
          flash('Account is already Premium')
          return redirect(url_for('index'))
    return decorated_function

# Premium User Manager Custom Decorator #
def premium_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_premium:					
           return func(*args, **kwargs)
        else:
          flash('Account does not have Premium')
          return redirect(url_for('premium'))
    return decorated_function

# Server Init #
def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CP_DATABASE.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = os.getenv("APP_KEY")
  app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv("RE_SITE_KEY")
  app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv("RE_SITE_SECRET_KEY")
  app.config['UPLOADED_IMAGES_DEST'] = 'uploads/images'
  app.config['MAIL_SERVER'] = 'smtp.gmail.com'
  app.config['MAIL_PORT'] = 465
  app.config['MAIL_USE_TLS'] = False
  app.config['MAIL_USE_SSL'] = True
  app.config['MAIL_USERNAME'] = os.getenv("EMAIL_USER")
  app.config['MAIL_PASSWORD'] = os.getenv("EMAIL_PASS")
  app.config['MAIL_DEFAULT_SENDER'] = ('Compile Projects Support', os.getenv("EMAIL_USER"))
  app.config['MAIL_MAX_EMAILS'] = None
  app.config['MAIL_ASCII_ATTACHMENTS'] = False
  CORS(app)
  QRcode(app)
  login_manager.init_app(app)
  db.init_app(app)
  return app
app = create_app()
app.app_context().push()
images = UploadSet('images', IMAGES)
configure_uploads(app, images)
mail = Mail(app)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

# Flask Admin Setup #
class MyModelView(ModelView):
  column_display_pk = True

  def is_accessible(self):
    return current_user.is_authenticated and current_user.is_admin

  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('login'))

class MyAdminIndexView(AdminIndexView):
  def is_accessible(self):
    return current_user.is_authenticated and current_user.is_admin

  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('login'))

# First Setup Admin View Pages#
#admin = Admin(app)
#admin.add_view(ModelView(user, db.session))

# Normal Admin View Pages #
admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(MyModelView(user, db.session))
admin.add_view(MyModelView(product, db.session))
admin.add_view(MyModelView(orders, db.session))
admin.add_view(MyModelView(wish_list, db.session))
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Folder'))

# Email Confirmation Links Setup #
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Merge Items In Session Function #
def MergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        list1 = list(dict1.items())
        list2 = list(dict2.items())
        return dict (list1 + list2)
    return False


# ALL SERVER ROUTES #

# Main Routes #
@app.route('/', methods=['GET'])
def index():
  agreement = request.cookies.get ('cookie-policy')
  if agreement == None:
      resp = 'no'
  if agreement == 'AGREE':
      resp = 'yes'
  return render_template('main.html', agreement=resp)

@app.route('/products', methods=['GET'])
def products():
  agreement = request.cookies.get ('cookie-policy')
  if agreement == None:
      resp = 'no'
  if agreement == 'AGREE':
      resp = 'yes'
  return render_template('main_products.html', agreement=resp)

@app.route('/aboutus', methods=['GET'])
def aboutus():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    return render_template('main_about_us.html', agreement=resp)

@app.route('/websites', methods=['GET'])
def websites():
  agreement = request.cookies.get ('cookie-policy')
  if agreement == None:
      resp = 'no'
  if agreement == 'AGREE':
      resp = 'yes'
  web_prod = product.query.filter_by(catagory="WEBSITES")
  return render_template('main_websites.html', products = web_prod, agreement=resp)

@app.route('/premium', methods=['GET'])
@login_required
@default_required
def premium():
  agreement = request.cookies.get ('cookie-policy')
  if agreement == None:
      resp = 'no'
  if agreement == 'AGREE':
      resp = 'yes'
  return render_template('main_premium.html', agreement=resp)

@app.route('/premium/buy', methods=['GET'])
@login_required
@default_required
def premium_buy():
  agreement = request.cookies.get ('cookie-policy')
  if agreement == None:
      resp = 'no'
  if agreement == 'AGREE':
      resp = 'yes'
  prem_user = user.query.get(current_user.id)
  prem_user.is_premium = True
  db.session.commit()
  absolute_total = 500
  absolute_total = "{:.2f}".format(absolute_total)
  new_item = orders(user_id = current_user.id, prod_id = 13, is_completed = True, AMT = 1, total_cost = 500, total_monthly = 0, total_downpayment = 0, monthly_due = False, downpayment_due = False, final_due = False)
  db.session.add(new_item)
  db.session.commit()
  msg = Message(subject = "Hey " + current_user.first_name + " we've Recieved Your Order!", recipients=[current_user.email])
  about_us_link = url_for('aboutus', _external = True)
  contact_us_link = url_for('message_us', _external = True)
  privacy_link = url_for('legal', _external = True)
  FAQ_link = url_for('legal', _external = True)
  FB_link = url_for('FB_compile', _external = True)
  Twit_link = url_for('Twitter_compile', _external = True)
  IG_link = url_for('IG_compile', _external = True)
  GIT_link = url_for('GIT_compile', _external = True)
  icons_8_link = url_for('icons_8', _external = True)
  msg.html = render_template('mail_prem_bill.html', name = current_user.first_name, absolute_total = absolute_total, monthly_total = 0, down = 0,about_us_link = about_us_link, contact_us_link = contact_us_link, privacy_link = privacy_link, FAQ_link = FAQ_link, FB_link = FB_link, Twit_link = Twit_link, IG_link = IG_link, GIT_link = GIT_link,icons_8_link=icons_8_link)
  mail.send(msg)
  msg_2 = Message(subject = current_user.first_name + " welcome to Premium!", recipients=[current_user.email])
  link = url_for('profile_page', _external = True)
  msg_2.html = render_template('mail_prem.html', name = current_user.first_name, absolute_total = absolute_total, monthly_total = 0, down = 0,about_us_link = about_us_link, contact_us_link = contact_us_link, privacy_link = privacy_link, FAQ_link = FAQ_link, FB_link = FB_link, Twit_link = Twit_link, IG_link = IG_link, GIT_link = GIT_link,icons_8_link=icons_8_link, link = link)
  mail.send(msg_2)
  msg_ky = Message(subject= current_user.first_name + " Made An Order!", recipients=[os.getenv("EMAIL_USER")])
  msg_ky.html = render_template('mail_kyle_prem.html', name = current_user.first_name, email = current_user.email,number = current_user.phone_number , absolute_total = absolute_total, monthly_total = 0, down = 0, about_us_link = about_us_link, contact_us_link = contact_us_link, privacy_link = privacy_link, FAQ_link = FAQ_link, FB_link = FB_link, Twit_link = Twit_link, IG_link = IG_link, GIT_link = GIT_link,icons_8_link = icons_8_link)
  mail.send(msg_ky)
  message = Markup("<strong> ACCOUNT UPGRADE SUCCESSFULL! </strong>")
  flash(message + 'Your account has been upgraded to Premium!!')
  return redirect(url_for('profile_page_orders_done'))

@app.route('/invoice', methods=['GET'])
def invoice():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    return render_template('main_invoice.html', agreement=resp)

@app.route('/bill', methods=['GET'])
def bill():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    return render_template('main_bill.html', agreement=resp)

@app.route('/order', methods=['GET'])
def order():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    return render_template('main_order.html', agreement=resp)

@app.route('/filters', methods=['GET'])
def filters():
  agreement = request.cookies.get ('cookie-policy')
  if agreement == None:
      resp = 'no'
  if agreement == 'AGREE':
      resp = 'yes'
  filter_prod = product.query.filter_by(catagory="FILTERS")
  return render_template('main_filters.html', products = filter_prod, agreement=resp)

@app.route('/legal', methods=['GET'])
def legal():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    return render_template('main_privacy.html', agreement=resp)

@app.route('/legal/purchase', methods=['GET'])
def legal_purchase():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    return render_template('main_legal_purchasing.html', agreement=resp)

@app.route('/legal/refund', methods=['GET'])
def legal_refund():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    return render_template('main_legal_refund.html', agreement=resp)

@app.route('/legal/free_app', methods=['GET'])
def legal_free_app():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    return render_template('main_legal_free_app.html', agreement=resp)

@app.route('/faq', methods=['GET'])
def FAQ():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    return render_template('main_FAQ.html', agreement=resp)

@app.route('/FAQ', methods=['GET'])
def FAQ_2():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    return render_template('main_FAQ.html', agreement=resp)

@app.route('/offline', methods=['GET'])
def offline():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    return render_template('main_offline.html', agreement=resp)

@app.route('/commingsoon', methods=['GET'])
def comming_soon():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    return render_template('main_comming_soon.html', agreement=resp)

@app.route('/message_us')
def message_us():
    return redirect("https://m.me/compileprojects")

@app.route('/FB_compile')
def FB_compile():
    return redirect("https://www.facebook.com/compileprojects")

@app.route('/Twitter_compile')
def Twitter_compile():
    return redirect("https://twitter.com/compileproject")

@app.route('/IG_compile')
def IG_compile():
    return redirect("https://www.instagram.com/compileprojects")

@app.route('/GIT_compile')
def GIT_compile():
    return redirect("https://github.com/CompileProjects")

@app.route('/icons_8')
def icons_8():
    return redirect("https://icons8.com")

# User / Login Server Paths #
@app.route('/login', methods=['GET', 'POST'])
def login():
  agreement = request.cookies.get ('cookie-policy')
  if agreement == None:
      resp = 'no'
  if agreement == 'AGREE':
      resp = 'yes'
  form = LogIn()
  if form.validate_on_submit():
    data = request.form
    User = user.query.filter_by(email = data['email']).first()
    if User and User.check_password(data['password']):
      login_user(User)
      if current_user.login_counter == 0:
        flash('Welcome to your new Compile Projects account ' + current_user.first_name + " we hope you'll enjoy your stay. Please confirm your email address via the email in your inbox")
        token = s.dumps(data['email'], salt='email-confirm')
        msg = Message(subject = "Hey " + current_user.first_name + " please take a few seconds to confirm your Compile Projects account!", recipients=[current_user.email])
        link = url_for ('confirm_email', token = token, _external = True)
        about_us_link = url_for('aboutus', _external = True)
        contact_us_link = url_for('message_us', _external = True)
        privacy_link = url_for('legal', _external = True)
        FAQ_link = url_for('legal', _external = True)
        FB_link = url_for('FB_compile', _external = True)
        Twit_link = url_for('Twitter_compile', _external = True)
        IG_link = url_for('IG_compile', _external = True)
        GIT_link = url_for('GIT_compile', _external = True)
        icons_8_link = url_for('icons_8', _external = True)
        msg.html = render_template('mail_email_confirm_send.html', name = current_user.first_name, link = link,about_us_link = about_us_link, contact_us_link = contact_us_link, privacy_link = privacy_link, FAQ_link = FAQ_link, FB_link = FB_link, Twit_link = Twit_link, IG_link = IG_link, GIT_link = GIT_link, icons_8_link = icons_8_link)
        mail.send(msg)
      elif current_user.login_counter != 0:
        flash('Welcome Back ' + current_user.first_name)
      return redirect(url_for('profile_page'))
    else:
      flash('Invalid Username or Password for Account, Please try again')
      return redirect(url_for('login'))
  return render_template('main_login.html', form=form, agreement=resp)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    form = SignUp()
    if form.validate_on_submit():
        data = request.form
        newuser = user(username=data['username'], first_name=data['first_name'], last_name=data['last_name'] , email=data['email'], phone_number=data['phone'], login_counter = 0, is_admin = False, is_premium = False, email_confirmed = False)
        newuser.set_password(data['password'])
        db.session.add(newuser)
        db.session.commit()
        flash('Account Succesfully Created!')
        return redirect(url_for('login'))
    return render_template('main_signup.html', form=form, agreement=resp)

@app.route('/confirm_email/send', methods=['GET', 'POST'])
@login_required
def confirm_email_send():
  token = s.dumps(current_user.email, salt='email-confirm')
  msg = Message(subject = "Hey " + current_user.first_name + " please take a few seconds to confirm your Compile Projects account!", recipients=[current_user.email])
  link = url_for ('confirm_email', token = token, _external = True)
  about_us_link = url_for('aboutus', _external = True)
  contact_us_link = url_for('message_us', _external = True)
  privacy_link = url_for('legal', _external = True)
  FAQ_link = url_for('legal', _external = True)
  FB_link = url_for('FB_compile', _external = True)
  Twit_link = url_for('Twitter_compile', _external = True)
  IG_link = url_for('IG_compile', _external = True)
  GIT_link = url_for('GIT_compile', _external = True)
  icons_8_link = url_for('icons_8', _external = True)
  msg.html = render_template('mail_email_confirm_send.html', name = current_user.first_name, link = link,about_us_link = about_us_link, contact_us_link = contact_us_link, privacy_link = privacy_link, FAQ_link = FAQ_link, FB_link = FB_link, Twit_link = Twit_link, IG_link = IG_link, GIT_link = GIT_link, icons_8_link=icons_8_link)
  mail.send(msg)
  flash('Confirmation Email sent to '+current_user.email)
  return redirect(request.referrer)

@app.route('/confirm_email/<token>', methods=['GET', 'POST'])
@login_required
def confirm_email(token):
  try:
    email = s.loads(token, salt='email-confirm')
  except SignatureExpired:
    flash('&#x26A0; Conformation Link Expired')
    return redirect(url_for('profile_page'))
  except BadTimeSignature:
    flash('&#x26A0; Incorrect Conformation Link')
    return redirect(url_for('profile_page'))
  update_user = user.query.get(current_user.id)
  update_user.email_confirmed = True
  db.session.commit()
  flash('Email Confirmed!')
  msg = Message(subject = "The email address for your Compile Projects account has been confirmed!", recipients=[current_user.email])
  about_us_link = url_for('aboutus', _external = True)
  contact_us_link = url_for('message_us', _external = True)
  privacy_link = url_for('legal', _external = True)
  FAQ_link = url_for('legal', _external = True)
  FB_link = url_for('FB_compile', _external = True)
  Twit_link = url_for('Twitter_compile', _external = True)
  IG_link = url_for('IG_compile', _external = True)
  GIT_link = url_for('GIT_compile', _external = True)
  icons_8_link = url_for('icons_8', _external = True)
  msg.html = render_template('mail_email_confirm.html', name = current_user.first_name,about_us_link = about_us_link, contact_us_link = contact_us_link, privacy_link = privacy_link, FAQ_link = FAQ_link, FB_link = FB_link, Twit_link = Twit_link, IG_link = IG_link, GIT_link = GIT_link, icons_8_link = icons_8_link)
  mail.send(msg)
  return redirect(url_for('profile_page'))

@app.route('/admin/send_mail', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_send_mail():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    form = EmailSend()
    if form.validate_on_submit():
      data = request.form
      email = data['email']
      sub =  data['email_subject']
      body =  data['email_body']
      bot =  data['email_bottom']
      admin_name = current_user.first_name
      msg = Message(subject = sub, recipients=[email], sender=[admin_name+' From Compile Projects', os.getenv("EMAIL_USER")])
      about_us_link = url_for('aboutus', _external = True)
      contact_us_link = url_for('message_us', _external = True)
      privacy_link = url_for('legal', _external = True)
      FAQ_link = url_for('legal', _external = True)
      FB_link = url_for('FB_compile', _external = True)
      Twit_link = url_for('Twitter_compile', _external = True)
      IG_link = url_for('IG_compile', _external = True)
      GIT_link = url_for('GIT_compile', _external = True)
      icons_8_link = url_for('icons_8', _external = True)
      msg.html = render_template('mail_admin_send.html',about_us_link = about_us_link, contact_us_link = contact_us_link, privacy_link = privacy_link, FAQ_link = FAQ_link, FB_link = FB_link, Twit_link = Twit_link, IG_link = IG_link, GIT_link = GIT_link, icons_8_link = icons_8_link, admin_name = admin_name, body = body, bot = bot)
      mail.send(msg)
      flash('Email Sent!')
    return render_template('main_profile_mail_send.html', agreement=resp, form = form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    return render_template('main_profile.html', agreement=resp)

@app.route('/profile/orders', methods=['GET', 'POST'])
@login_required
def profile_page_orders_pending():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    test = False
    my_prods = db.session.query(orders, product).outerjoin(product, orders.prod_id == product.id).all()
    test_query = orders.query.filter_by(user_id = current_user.id).first()
    if test_query:
      test = True
    done_counter = 0
    number_of_prods = 0
    all_orders_complete = False
    for key, item in my_prods:
      number_of_prods += 1
      if key.is_completed:
        done_counter += 1
    if done_counter == number_of_prods:
      all_orders_complete = True
    return render_template('main_profile_orders.html', prods = my_prods, test = test, agreement=resp, all_orders_complete = all_orders_complete)

@app.route('/profile/purchased', methods=['GET', 'POST'])
@login_required
def profile_page_orders_done():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    test = False
    my_prods = db.session.query(orders, product).outerjoin(product, orders.prod_id == product.id).all()
    test_query = orders.query.filter_by(user_id = current_user.id).first()
    if test_query:
      test = True
    done_counter = 0
    number_of_prods = 0
    all_orders_complete = False
    for key, item in my_prods:
      number_of_prods += 1
      if key.is_completed:
        done_counter += 1
    if done_counter != number_of_prods:
      all_orders_complete = True
    return render_template('main_profile_orders_done.html', prods = my_prods, test = test, agreement=resp,all_orders_complete = all_orders_complete)

@app.route('/profile/wishlist', methods=['GET', 'POST'])
@login_required
def profile_page_wishlist():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    test = False
    my_wish_list = db.session.query(wish_list, product).filter(wish_list.user_id == current_user.id).filter(wish_list.prod_id == product.id).all()
    test_query = wish_list.query.filter_by(user_id = current_user.id).first()
    if test_query:
      test = True
    return render_template('main_profile_wishlist.html', prods = my_wish_list, test = test, agreement=resp)

@app.route('/wishlist/add/<id>', methods=['GET', 'POST'])
@login_required
def wishlist(id):
  test = db.session.query(wish_list).filter(wish_list.user_id == current_user.id).filter(wish_list.prod_id == id).all()
  prod = product.query.filter_by(id = id).first()
  if test:
    flash(prod.name+' is already in '+current_user.first_name+"'s Wishlist...")
  if not test:
    new_item = wish_list(user_id = current_user.id, prod_id = id)
    db.session.add(new_item)
    db.session.commit()
    flash(prod.name+' added to '+current_user.first_name+"'s Wishlist!...")
  return redirect(request.referrer)

@app.route('/wishlist/remove/<id>', methods=['GET', 'DELETE'])
@login_required
def wishlist_del(id):
  del_item = wish_list.query.get(id)
  del_item_info = product.query.get(id)
  db.session.delete(del_item)
  db.session.commit()
  flash(del_item_info.name+' removed from '+current_user.first_name+"'s Wishlist")
  return redirect(request.referrer)

@app.route('/profile/settings', methods=['GET', 'POST'])
@login_required
def profile_page_settings():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    return render_template('main_profile_settings.html', agreement=resp)

@app.route('/profile/email_reset', methods=['GET', 'POST'])
@login_required
def profile_page_email():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    form = EditEmail()
    if form.validate_on_submit():
        data = request.form
        email = data['email']
        test = user.query.filter_by(email = email).first()
        if test:
          flash('The email address '+ email +' already belongs to another person')
          return redirect(request.referrer)
        if not test:
          update = user.query.get(current_user.id)
          msg = Message(subject = current_user.first_name +" the email address for your Compile Projects account has been changed", recipients=[current_user.email])
          about_us_link = url_for('aboutus', _external = True)
          contact_us_link = url_for('message_us', _external = True)
          privacy_link = url_for('legal', _external = True)
          FAQ_link = url_for('legal', _external = True)
          FB_link = url_for('FB_compile', _external = True)
          Twit_link = url_for('Twitter_compile', _external = True)
          IG_link = url_for('IG_compile', _external = True)
          GIT_link = url_for('GIT_compile', _external = True)
          icons_8_link = url_for('icons_8', _external = True)
          msg.html = render_template('mail_email_change.html', name = current_user.first_name,about_us_link = about_us_link, contact_us_link = contact_us_link, privacy_link = privacy_link, FAQ_link = FAQ_link, FB_link = FB_link, Twit_link = Twit_link, IG_link = IG_link, GIT_link = GIT_link, email = email,icons_8_link=icons_8_link)
          mail.send(msg)
          update.email = email
          update.email_confirmed = False
          db.session.commit()
          token = s.dumps(current_user.email, salt='email-confirm')
          msg = Message(subject = "Hey " + current_user.first_name + " please take a few seconds to confirm your Compile Projects account!", recipients=[current_user.email])
          link = url_for ('confirm_email', token = token, _external = True)
          msg.html = render_template('mail_email_confirm_send.html', name = current_user.first_name, link = link,about_us_link = about_us_link, contact_us_link = contact_us_link, privacy_link = privacy_link, FAQ_link = FAQ_link, FB_link = FB_link, Twit_link = Twit_link, IG_link = IG_link, GIT_link = GIT_link,icons_8_link=icons_8_link)
          mail.send(msg)
          flash('Email Updated! Please verify that '+ email +' is your new email through the mail sent to this address')
          return redirect(url_for('profile_page'))
    return render_template('main_profile_settings_email.html', agreement=resp, form = form)

@app.route('/profile/username_reset', methods=['GET', 'POST'])
@login_required
def profile_page_username():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    form = EditUsername()
    if form.validate_on_submit():
        data = request.form
        username = data['username']
        test = user.query.filter_by(username = username).first()
        if test:
          flash('The username '+ username +' already belongs to another person')
          return redirect(request.referrer)
        if not test:
          update = user.query.get(current_user.id)
          msg = Message(subject = current_user.first_name +" the username for your Compile Projects account has been changed", recipients=[current_user.email])
          about_us_link = url_for('aboutus', _external = True)
          contact_us_link = url_for('message_us', _external = True)
          privacy_link = url_for('legal', _external = True)
          FAQ_link = url_for('legal', _external = True)
          FB_link = url_for('FB_compile', _external = True)
          Twit_link = url_for('Twitter_compile', _external = True)
          IG_link = url_for('IG_compile', _external = True)
          GIT_link = url_for('GIT_compile', _external = True)
          icons_8_link = url_for('icons_8', _external = True)
          msg.html = render_template('mail_username_change.html', name = current_user.first_name,about_us_link = about_us_link, contact_us_link = contact_us_link, privacy_link = privacy_link, FAQ_link = FAQ_link, FB_link = FB_link, Twit_link = Twit_link, IG_link = IG_link, GIT_link = GIT_link, email = username, icons_8_link=icons_8_link)
          mail.send(msg)
          update.username = username
          db.session.commit()
          flash('Username Updated!')
          return redirect(url_for('profile_page'))
    return render_template('main_profile_settings_user_name.html', agreement=resp, form = form)

@app.route('/profile/name_reset', methods=['GET', 'POST'])
@login_required
def profile_page_name():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    form = EditName()
    if form.validate_on_submit():
        data = request.form
        f_name = data['first_name']
        l_name = data['last_name']
        update = user.query.get(current_user.id)
        msg = Message(subject = current_user.first_name +" your name for your Compile Projects account has been changed", recipients=[current_user.email])
        about_us_link = url_for('aboutus', _external = True)
        contact_us_link = url_for('message_us', _external = True)
        privacy_link = url_for('legal', _external = True)
        FAQ_link = url_for('legal', _external = True)
        FB_link = url_for('FB_compile', _external = True)
        Twit_link = url_for('Twitter_compile', _external = True)
        IG_link = url_for('IG_compile', _external = True)
        GIT_link = url_for('GIT_compile', _external = True)
        icons_8_link = url_for('icons_8', _external = True)
        msg.html = render_template('mail_name_change.html', name = current_user.first_name,about_us_link = about_us_link, contact_us_link = contact_us_link, privacy_link = privacy_link, FAQ_link = FAQ_link, FB_link = FB_link, Twit_link = Twit_link, IG_link = IG_link, GIT_link = GIT_link, f_name = f_name, l_name = l_name,icons_8_link=icons_8_link)
        mail.send(msg)
        update.first_name = f_name
        update.last_name = l_name
        db.session.commit()
        flash("Name Updated! We'll call you " + current_user.first_name + " " + current_user.last_name + " from now on!")
        return redirect(url_for('profile_page'))
    return render_template('main_profile_settings_name.html', agreement=resp, form = form)

@app.route('/profile/password_reset', methods=['GET', 'POST'])
@login_required
def profile_page_password():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    form = EditPassword()
    if form.validate_on_submit():
        data = request.form
        old_pass = data['old_password']
        new_pass = data['new_password']
        edit_user = user.query.get(current_user.id)
        if not edit_user.check_password(old_pass):
          flash('Incorrect old Password')
          return redirect(request.referrer)
        if edit_user.check_password(old_pass):
          msg = Message(subject = current_user.first_name +" the password for your Compile Projects account has been changed", recipients=[current_user.email])
          about_us_link = url_for('aboutus', _external = True)
          contact_us_link = url_for('message_us', _external = True)
          privacy_link = url_for('legal', _external = True)
          FAQ_link = url_for('legal', _external = True)
          FB_link = url_for('FB_compile', _external = True)
          Twit_link = url_for('Twitter_compile', _external = True)
          IG_link = url_for('IG_compile', _external = True)
          GIT_link = url_for('GIT_compile', _external = True)
          icons_8_link = url_for('icons_8', _external = True)
          msg.html = render_template('mail_pass_change.html', name = current_user.first_name,about_us_link = about_us_link, contact_us_link = contact_us_link, privacy_link = privacy_link, FAQ_link = FAQ_link, FB_link = FB_link, Twit_link = Twit_link, IG_link = IG_link, GIT_link = GIT_link,icons_8_link=icons_8_link)
          mail.send(msg)
          edit_user.set_password(new_pass)
          db.session.commit()
          flash('Password Updated!')
          return redirect(url_for('profile_page'))
    return render_template('main_profile_settings_pass.html', agreement=resp, form = form)

@app.route('/forgot_pass', methods=['GET', 'POST'])
def forgot_pass():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    form = SendLostPasswordLink()
    if form.validate_on_submit():
        data = request.form
        email = data['email']
        token = s.dumps(email, salt='pass-reset')
        secure_link = url_for ('reset_pass_token', token = token, _external = True)
        msg = Message(subject = " Here is the link to reset the password for your Compile Projects account", recipients=[email])
        about_us_link = url_for('aboutus', _external = True)
        contact_us_link = url_for('message_us', _external = True)
        privacy_link = url_for('legal', _external = True)
        FAQ_link = url_for('legal', _external = True)
        FB_link = url_for('FB_compile', _external = True)
        Twit_link = url_for('Twitter_compile', _external = True)
        IG_link = url_for('IG_compile', _external = True)
        GIT_link = url_for('GIT_compile', _external = True)
        icons_8_link = url_for('icons_8', _external = True)
        msg.html = render_template('mail_password_recovery_link.html',about_us_link = about_us_link, contact_us_link = contact_us_link, privacy_link = privacy_link, FAQ_link = FAQ_link, FB_link = FB_link, Twit_link = Twit_link, IG_link = IG_link, GIT_link = GIT_link,icons_8_link=icons_8_link, secure_link = secure_link)
        mail.send(msg)
        flash('An email was sent to '+email)
        return redirect(request.referrer)
    return render_template('main_password_recovery_send.html', agreement=resp, form = form)

@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset_pass_token(token):
  email = s.loads(token, salt='pass-reset')
  expire_date = datetime.datetime.now()
  expire_date = expire_date + datetime.timedelta(days=1)
  cookie = make_response(redirect(url_for('reset_pass_page')))
  cookie.set_cookie('email_name',email, expires=expire_date)
  return cookie

@app.route('/reset', methods=['GET', 'POST'])
def reset_pass_page():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    email = request.cookies.get('email_name')
    if email == None:
        return redirect(url_for('forgot_pass'))
    form = EditPassword_reset()
    if form.validate_on_submit():
        data = request.form
        new_pass = data['new_password']
        edit_user = user.query.filter_by(email = email).first()
        msg = Message(subject = "Hey "+edit_user.first_name+" The password for your Compile Projects account has been reset", recipients=[edit_user.email])
        about_us_link = url_for('aboutus', _external = True)
        contact_us_link = url_for('message_us', _external = True)
        privacy_link = url_for('legal', _external = True)
        FAQ_link = url_for('legal', _external = True)
        FB_link = url_for('FB_compile', _external = True)
        Twit_link = url_for('Twitter_compile', _external = True)
        IG_link = url_for('IG_compile', _external = True)
        GIT_link = url_for('GIT_compile', _external = True)
        icons_8_link = url_for('icons_8', _external = True)
        msg.html = render_template('mail_pass_change.html', name = edit_user.first_name,about_us_link = about_us_link, contact_us_link = contact_us_link, privacy_link = privacy_link, FAQ_link = FAQ_link, FB_link = FB_link, Twit_link = Twit_link, IG_link = IG_link, GIT_link = GIT_link,icons_8_link=icons_8_link)
        mail.send(msg)
        edit_user.set_password(new_pass)
        db.session.commit()
        flash('Password Reset!')
        return redirect(url_for('login'))
    return render_template('main_password_reset.html', agreement=resp, form = form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    this_user = user.query.get(current_user.id)
    this_user.login_counter += 1
    db.session.commit()
    message = Markup("<strong> LOGGED OUT </strong>")
    flash (message + 'Goodbye ' + current_user.first_name)
    logout_user()
    return redirect(url_for('index'))

@app.route('/delete_account', methods=['GET', 'DELETE'])
@login_required
def delete_account():
    this_user = user.query.get(current_user.id)
    db.session.delete(this_user)
    db.session.commit()
    message = Markup("<strong> ACCOUNT DELETED </strong>")
    flash (message + 'Goodbye ' + current_user.first_name + ' thank you for shopping with us!')
    msg = Message(subject = current_user.first_name + " your account has been deleted", recipients=[current_user.email])
    about_us_link = url_for('aboutus', _external = True)
    contact_us_link = url_for('message_us', _external = True)
    privacy_link = url_for('legal', _external = True)
    FAQ_link = url_for('legal', _external = True)
    FB_link = url_for('FB_compile', _external = True)
    Twit_link = url_for('Twitter_compile', _external = True)
    IG_link = url_for('IG_compile', _external = True)
    GIT_link = url_for('GIT_compile', _external = True)
    signup = url_for('signup', _external = True)
    icons_8_link = url_for('icons_8', _external = True)
    msg.html = render_template('mail_del.html', name = current_user.first_name,about_us_link = about_us_link, contact_us_link = contact_us_link, privacy_link = privacy_link, FAQ_link = FAQ_link, FB_link = FB_link, Twit_link = Twit_link, IG_link = IG_link, GIT_link = GIT_link, signup = signup,icons_8_link=icons_8_link)
    mail.send(msg)
    logout_user()
    return redirect(url_for('index'))

# Shopping Cart Functions #
@app.route('/cart', methods=['GET'])
def cart():
  agreement = request.cookies.get ('cookie-policy')
  if agreement == None:
      resp = 'no'
  if agreement == 'AGREE':
      resp = 'yes'
  absolute_total = 0
  monthly_total = 0
  monthly_counter = 0
  recomend_products = product.query.all()
  if 'ShoppingCart' in session and len(session['ShoppingCart']) > 0:
    for key, item in session['ShoppingCart'].items():
      absolute_total += item["price_total"]
      if item["monthly"] == True:
        monthly_counter += item["AMT_IN_CART"]
  monthly_total = monthly_counter * 200
  return render_template('main_cart.html', recomend_products = recomend_products, absolute_total = absolute_total, monthly_total = monthly_total, agreement=resp)

@app.route('/checkout/menu', methods=['GET', 'POST'])
@login_required
def checkout_menu():
  agreement = request.cookies.get ('cookie-policy')
  if agreement == None:
      resp = 'no'
  if agreement == 'AGREE':
      resp = 'yes'
  absolute_total = 0
  monthly_total = 0
  monthly_counter = 0
  in_cart_counter = 0
  recomend_products = product.query.all()
  for key, item in session['ShoppingCart'].items():
    in_cart_counter += item["AMT_IN_CART"]
    absolute_total += item["price_total"]
    if item["monthly"] == True:
      monthly_counter += item["AMT_IN_CART"]
  US_TOTAL = absolute_total * 0.15
  monthly_total = monthly_counter * 200 
  return render_template('main_check_out.html', recomend_products = recomend_products, absolute_total = absolute_total, monthly_total = monthly_total, agreement=resp, US_TOTAL = US_TOTAL)

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
  absolute_total = 0
  monthly_total = 0
  monthly_counter = 0
  if 'ShoppingCart' in session and len(session['ShoppingCart']) > 0:
    for key, item in session['ShoppingCart'].items():
      absolute_total += item["price_total"]
      if item["monthly"] == True:
        monthly_counter += item["AMT_IN_CART"]
  monthly_total = monthly_counter * 200
  downpayment = absolute_total * 20 / 100
  downpayment = "{:.2f}".format(downpayment)
  absolute_total = "{:.2f}".format(absolute_total)
  monthly_total = "{:.2f}".format(monthly_total)
  list_x = []
  for key, item in session['ShoppingCart'].items():
    new_item = orders(user_id = current_user.id, prod_id = item["id"], is_completed = False, AMT = item["AMT_IN_CART"], total_cost = "{:.2f}".format(item["price_total"]), total_monthly = "{:.2f}".format(item["monthly_price"]), total_downpayment = downpayment, monthly_due = False, downpayment_due = True, final_due = False)
    db.session.add(new_item)
    db.session.commit()
    list_x.append(new_item.id)
    print(new_item.id)
  msg = Message(subject = "Hey " + current_user.first_name + " We've Recieved Your Order!", recipients=[current_user.email])
  about_us_link = url_for('aboutus', _external = True)
  contact_us_link = url_for('message_us', _external = True)
  privacy_link = url_for('legal', _external = True)
  FAQ_link = url_for('legal', _external = True)
  FB_link = url_for('FB_compile', _external = True)
  Twit_link = url_for('Twitter_compile', _external = True)
  IG_link = url_for('IG_compile', _external = True)
  GIT_link = url_for('GIT_compile', _external = True)
  icons_8_link = url_for('icons_8', _external = True)
  msg.html = render_template('mail_layout.html', name = current_user.first_name, absolute_total = absolute_total, monthly_total = monthly_total, down = downpayment,about_us_link = about_us_link, contact_us_link = contact_us_link, privacy_link = privacy_link, FAQ_link = FAQ_link, FB_link = FB_link, Twit_link = Twit_link, IG_link = IG_link, GIT_link = GIT_link,icons_8_link=icons_8_link)
  mail.send(msg)
  msg_ky = Message(subject= current_user.first_name + " Made An Order!", recipients=[os.getenv("EMAIL_USER")])
  msg_ky.html = render_template('mail_kyle.html', name = current_user.first_name, email = current_user.email,number = current_user.phone_number,  absolute_total = absolute_total, monthly_total = monthly_total, down = downpayment,about_us_link = about_us_link, contact_us_link = contact_us_link, privacy_link = privacy_link, FAQ_link = FAQ_link, FB_link = FB_link, Twit_link = Twit_link, IG_link = IG_link, GIT_link = GIT_link,icons_8_link = icons_8_link, list_x = list_x)
  mail.send(msg_ky)
  session['ShoppingCart'].clear()
  message = Markup("<strong> ORDER SUCCESSFULLY PLACED! </strong>")
  flash(message + 'Please check your email, an employee shal contact you soon')
  return redirect(url_for('profile_page_orders_pending'))

@app.route('/shop/<id>', methods=['GET'])
def shop(id):
  agreement = request.cookies.get ('cookie-policy')
  if agreement == None:
      resp = 'no'
  if agreement == 'AGREE':
      resp = 'yes'
  amt_in_cart = 0
  incart = False
  name = "prod_"+id
  if 'ShoppingCart' in session and len(session['ShoppingCart']) > 0:
    for key, item in session['ShoppingCart'].items():
        if key == name:
          incart = True
          for field in item:
             if field == "AMT_IN_CART":
                amt_in_cart = item[field]
  prod = product.query.get(id)
  if prod.in_stock == False:
    return redirect (url_for('offline'))
  if prod.catagory == "FILTERS":
    recomend_products = product.query.filter_by(catagory="FILTERS")
  if prod.catagory == "WEBSITES":
    recomend_products = product.query.filter_by(catagory="WEBSITES")
  return render_template('main_any_prod.html', prod = prod, recomend_products = recomend_products, incart = incart, amt_in_cart = amt_in_cart, agreement=resp)

@app.route('/add_to_cart/<id>/<amt>', methods=['GET'])
def add_to_cart(id, amt):
    amt = int(amt)
    add_prod = product.query.get(id)
    if add_prod.in_stock == False:
       return redirect (url_for('offline'))
    price_total = add_prod.price * amt
    monthly_total = 0
    if add_prod.monthly:
    	monthly_total = 200 * amt
    add_cart_item = {"prod_"+id:{"id":id, "price_total": price_total, "price_per": add_prod.price, "name": add_prod.name, "monthly": add_prod.monthly, "desc": add_prod.desc, "catagory": add_prod.catagory, "sub_catagory": add_prod.sub_catagory, "img_url": add_prod.img_url, "feature_1": add_prod.feature_1, "feature_2": add_prod.feature_2, "feature_3": add_prod.feature_3, "feature_4": add_prod.feature_4, "feature_5": add_prod.feature_5, "feature_6": add_prod.feature_6, "feature_7": add_prod.feature_7, "AMT_IN_CART":amt, "monthly_price": monthly_total}}
    if 'ShoppingCart' in session:
       session['ShoppingCart'] = MergeDicts(session['ShoppingCart'] , add_cart_item)
       return redirect(url_for('cart'))
    else:
       session['ShoppingCart'] = add_cart_item
       return redirect(url_for('cart'))

@app.route('/remove_from_cart/<id>', methods=['GET'])
def remove_from_cart(id):
   del_name = "prod_"+id
   if 'ShoppingCart' not in session and len(session['ShoppingCart']) <= 0:
      return redirect(request.referrer)
   else:
      session.modified = True
      for key, item in session['ShoppingCart'].items():
         if key == del_name:
           session['ShoppingCart'].pop(key, None)
           return redirect(request.referrer)

# Cookie Setting Routes #
@app.route('/setcookie', methods=['GET'])
def setcookie_invoice():
  expire_date = datetime.datetime.now()
  expire_date = expire_date + datetime.timedelta(days=90)
  cookie = make_response(redirect(request.referrer))
  cookie.set_cookie('cookie-policy','AGREE', expires=expire_date)
  return cookie

# Web Application Routes #

# Invoice Maker #
@app.route('/invoice/app', methods=['GET', 'POST'])
def invoice_app():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    form = invoice_fields()
    #session.clear()
    if form.validate_on_submit():
        if form.logo.data == None:
          file_url = '/_uploads/images/white.png'
        if form.logo.data:
          filename = images.save(form.logo.data)
          file_url = images.url(filename)
        data = {}
        all_products = []
        absolute_total = 0
        for field in form.product:
          total_this_item = field.product_cost_per.data * field.product_QTY.data
          absolute_total += total_this_item
          cost_per = str(field.product_cost_per.data)
          total_this = str(total_this_item)
          current_product = {"Name": field.product_name.data, "QTY": field.product_QTY.data, "Cost_Per": cost_per, "Total_This": total_this}
          all_products.append(current_product)
        vat_num = absolute_total * form.vat.data / 100
        absolute_total = absolute_total + vat_num
        absolute_total = "{:.2f}".format(absolute_total)
        data = {"currency": form.currency.data, "invoice_number": form.invoice_number.data,"invoice_date": form.invoice_date.data,"invoice_policy": form.invoice_policy.data,"buisness_name": form.buisness_name.data,"buisness_address": form.buisness_address.data,"buisness_email": form.buisness_email.data, "client_name": form.client_name.data, "client_address": form.client_address.data, "client_email": form.client_email.data, "overall_total": str(absolute_total), "logo": file_url, "vat_per": str(form.vat.data), "vat_num": str(vat_num)}
        data ["all_products"] = all_products
        session['data'] = data
        return redirect(url_for('invoice_render_func'))
    return render_template('invoice_menu.html', form=form, agreement=resp)

@app.route('/invoice/render', methods=['GET'])
def invoice_render_func():
  stat = "YES"
  if session['data']['vat_per'] == "0.00":
     stat = "NO"
  html = render_template('invoice_render.html', stat = stat)
  return render_pdf(HTML(string=html), download_filename = "Invoice.pdf")

@app.route('/invoice/preview', methods=['GET'])
def invoice_preview_func():
  stat = "YES"
  if session['data']['vat_per'] == "0.00":
     stat = "NO"
  html = render_template('invoice_render.html', stat = stat)
  return render_pdf(HTML(string=html))

# Receipt Maker #
@app.route('/bill/app', methods=['GET', 'POST'])
def bill_app():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    form = bill_fields()
    if form.validate_on_submit():
        if form.logo.data == None:
          file_url = '/_uploads/images/white.png'
        if form.logo.data:
          filename = images.save(form.logo.data)
          file_url = images.url(filename)
        data = {}
        all_products = []
        absolute_total = 0
        for field in form.product:
          total_this_item = field.product_cost_per.data * field.product_QTY.data
          absolute_total += total_this_item
          cost_per = str(field.product_cost_per.data)
          total_this = str(total_this_item)
          current_product = {"Name": field.product_name.data, "QTY": field.product_QTY.data, "Cost_Per": cost_per, "Total_This": total_this}
          all_products.append(current_product)
        vat_num = absolute_total * form.vat.data / 100
        absolute_total = absolute_total + vat_num
        absolute_total = "{:.2f}".format(absolute_total)
        data = {"currency": form.currency.data, "promo_link": form.invoice_number.data,"invoice_date": form.invoice_date.data,"invoice_policy": form.invoice_policy.data,"buisness_name": form.buisness_name.data,"buisness_address": form.buisness_address.data, "overall_total": str(absolute_total), "logo": file_url, "vat_per": str(form.vat.data), "vat_num": str(vat_num)}
        data ["all_products"] = all_products
        session['data'] = data
        return redirect(url_for('bill_render_func'))
    return render_template('bill_menu.html', form=form, agreement=resp)

@app.route('/bill/render', methods=['GET'])
def bill_render_func():
  qr_me = session['data']['promo_link']
  stat = "YES"
  if session['data']['vat_per'] == "0.00":
     stat = "NO"
  html = render_template('bill_render.html', stat = stat, qr=qr_me)
  return render_pdf(HTML(string=html), download_filename = "Receipt.pdf")

@app.route('/bill/preview', methods=['GET'])
def bill_preview_func():
  qr_me = session['data']['promo_link']
  stat = "YES"
  if session['data']['vat_per'] == "0.00":
     stat = "NO"
  html = render_template('bill_render.html', stat = stat, qr=qr_me)
  return render_pdf(HTML(string=html))

# Website Configurator#
@app.route('/websites/app', methods=['GET'])
@login_required
@admin_required
def websites_app():
    agreement = request.cookies.get('cookie-policy')
    if agreement == None:
        resp = 'no'
    if agreement == 'AGREE':
        resp = 'yes'
    return render_template('main_websites_app.html', agreement=resp)

# Hosting Routes #
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)