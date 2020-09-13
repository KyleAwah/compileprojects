from main import db, app, user, product
db.create_all(app=app)

prod_to_add = product(price=200, name="COLOR INSTAGRAM", monthly=False, desc="This package offers an augmented reality filter that adjusts the colors of the scene depicted through the user's camera", catagory="FILTERS", sub_catagory="INSTA", img_url="ig_3_hot.jpg", feature_1="1 Augmented Reality Filter", feature_2="Color Effect", feature_3="Filter Icon", feature_4="Demo Video", feature_5="Instagram Upload")
db.session.add(prod_to_add)
db.session.commit()

prod_to_add = product(price=350, name="GRAPHIC INSTAGRAM", monthly=False, desc="This package offers an augmented reality filter that can have any graphic overlay or design applied to the scene depicted through the user's camera", catagory="FILTERS", sub_catagory="INSTA", img_url="ig_2_hot.jpg", feature_1="1 Augmented Reality Filter", feature_2="Color Effect", feature_3="Graphics", feature_4="Filter Icon", feature_5="Demo Video", feature_6="Instagram Upload")
db.session.add(prod_to_add)
db.session.commit()

prod_to_add = product(price=500, name="LOGIC INSTAGRAM", monthly=False, desc="This package offers an augmented filter that has logic processing in it, this can include random generators for example", catagory="FILTERS", sub_catagory="INSTA", img_url="ig_1.jpg", feature_1="1 Augmented Reality Filter", feature_2="Color Effect", feature_3="Graphics", feature_4="Logic Programming", feature_5="Filter Icon", feature_6="Demo Video", feature_7="Instagram Upload")
db.session.add(prod_to_add)
db.session.commit()

prod_to_add = product(price=200, name="COLOR SNAPCHAT", monthly=False, desc="This package offers an augmented reality filter that adjusts the colors of the scene depicted through the user's camera", catagory="FILTERS", sub_catagory="SNAP", img_url="snap_3.jpg", feature_1="1 Augmented Reality Filter", feature_2="Color Effect", feature_3="Filter Icon", feature_4="Demo Video", feature_5="Snapchat Upload")
db.session.add(prod_to_add)
db.session.commit()

prod_to_add = product(price=350, name="GRAPHIC SNAPCHAT", monthly=False, desc="This package offers an augmented reality filter that can have any graphic overlay or design applied to the scene depicted through the user's camera", catagory="FILTERS", sub_catagory="SNAP", img_url="snap_2.jpg", feature_1="1 Augmented Reality Filter", feature_2="Color Effect", feature_3="Graphics", feature_4="Filter Icon", feature_5="Demo Video", feature_6="Snapchat Upload")
db.session.add(prod_to_add)
db.session.commit()

prod_to_add = product(price=500, name="LOGIC SNAPCHAT", monthly=False, desc="This package offers an augmented filter that has logic processing in it, this can include random generators for example", catagory="FILTERS", sub_catagory="SNAP", img_url="snap_1.jpg", feature_1="1 Augmented Reality Filter", feature_2="Color Effect", feature_3="Graphics", feature_4="Logic Programming", feature_5="Filter Icon", feature_6="Demo Video", feature_7="Snapchat Upload")
db.session.add(prod_to_add)
db.session.commit()

prod_to_add = product(price=200, name="COLOR FACEBOOK", monthly=False, desc="This package offers an augmented reality filter that adjusts the colors of the scene depicted through the user's camera", catagory="FILTERS", sub_catagory="FB", img_url="fb_3.jpg", feature_1="1 Augmented Reality Filter", feature_2="Color Effect", feature_3="Filter Icon", feature_4="Demo Video", feature_5="Facebook Upload")
db.session.add(prod_to_add)
db.session.commit()

prod_to_add = product(price=350, name="GRAPHIC FACEBOOK", monthly=False, desc="This package offers an augmented reality filter that can have any graphic overlay or design applied to the scene depicted through the user's camera", catagory="FILTERS", sub_catagory="FB", img_url="fb_2.jpg", feature_1="1 Augmented Reality Filter", feature_2="Color Effect", feature_3="Graphics", feature_4="Filter Icon", feature_5="Demo Video", feature_6="Facebook Upload")
db.session.add(prod_to_add)
db.session.commit()

prod_to_add = product(price=500, name="LOGIC FACEBOOK", monthly=False, desc="This package offers an augmented filter that has logic processing in it, this can include random generators for example", catagory="FILTERS", sub_catagory="FB", img_url="fb_1.jpg", feature_1="1 Augmented Reality Filter", feature_2="Color Effect", feature_3="Graphics", feature_4="Logic Programming", feature_5="Filter Icon", feature_6="Demo Video", feature_7="Facebook Upload")
db.session.add(prod_to_add)
db.session.commit()

prod_to_add = product(price=500, name="SMALL", monthly=False, desc="Simplicity meets functionality, in this good package your website will have all the essentials of a modern digital presence. This package is best suited for small about us websites.", catagory="WEBSITES", img_url="good.jpg", feature_1="2 Pages", feature_2="Mobile Scaling", feature_3="Server Side Programming", feature_4="www.yourname.herokuapp.com")
db.session.add(prod_to_add)
db.session.commit()

prod_to_add = product(price=1000, name="MEDIUM", monthly=True, desc="Step up to the great package and enjoy amazing poweruser features such as a custom url. This package is best suited to blogs and non-profit websites", catagory="WEBSITES", img_url="great_hot.jpg", feature_1="5 Pages", feature_2="Mobile Scaling", feature_3="Server Side Programming", feature_4="www.yourname.com", feature_5="SSL Certificate (Security)")
db.session.add(prod_to_add)
db.session.commit()

prod_to_add = product(price=2000, name="LARGE", monthly=True, desc="Go all out with the awesome package. This package incoperates all of our high end features into a package that wont break the bank. This package is best suited to buisnesses", catagory="WEBSITES", img_url="awe.jpg", feature_1="Unlimited Pages", feature_2="Mobile Scaling", feature_3="Server Side Programming", feature_4="www.yourname.com", feature_5="SSL Certificate (Security)", feature_6="Local Database")
db.session.add(prod_to_add)
db.session.commit()