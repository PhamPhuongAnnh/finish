
# _______________________________Thêm thư viện___________________________________________________________

from flask import Flask, render_template, Response, request, redirect, flash
import cv2
from flask_login.utils import login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from sqlalchemy.sql import func
from ultralytics import YOLO
import numpy as np
import easyocr
import requests
from datetime import datetime
import pytz
import re
from flask_caching import Cache
from flask_lazyviews import LazyViews
# _______________________________Khai báo__________________________________________________________________

app = Flask(__name__,static_folder='static')
app.config['SECRET_KEY'] = '8sfkahf0-qdqb82hd'
#login
login = LoginManager(app=app)
#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///license.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
user = None
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
# Tạo đối tượng LazyViews
lazyviews = LazyViews(app)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    license_phate = db.Column(db.String(50), nullable=False)

    def __init__(self, name, license_phate):
        self.name = name
        self.license_phate = license_phate

class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
    def is_active(self):
        return True
    def get_id(self):
        return str(self.id)

class Manager(db.Model):
    __tablename__="manager"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    license_phate = db.Column(db.String(50), nullable=False)
    checkin=db.Column(db.DateTime, nullable=True)
    checkout=db.Column(db.DateTime, nullable=True)
    
    def __init__(self, license_phate, checkin=None, checkout=None):
        self.license_phate = license_phate
        self.checkin = checkin
        self.checkout = checkout

# Gọi db.create_all() trong ngữ cảnh ứng dụng
with app.app_context():
    db.create_all()
# ______________________________API_______________________________________________________________________


#Login
@login.user_loader
def user_load(user_id):
    return Admin.query.get(user_id)

@app.route('/login', methods=["POST"])
def login():
    global admin
    username = request.form.get("username")
    password = str(request.form.get("password"))
    remember_me = request.form.get('remember-me')  # Kiểm tra xem ô "Remember Me" có được chọn không

    # Thực hiện xác thực người dùng ở đây (đây chỉ là một ví dụ đơn giản)

    # Nếu ô "Remember Me" được chọn, lưu thông tin người dùng vào session
    if remember_me:
        session['username'] = username
    user = Admin.query.filter_by(username=username, password=password).first()
    if user:
        login_user(user)
        return redirect("api/video")
    else:
        flash('Sai tài khoản hoặc mật khẩu. Vui lòng đăng nhập lại', 'danger')
        return redirect("/")

@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")

@app.route('/admin')
def admin():
    global user
    users = User.query.all()
    return render_template('admin.html', users = users)

# Đăng ký hàm xử lý admin với Lazy Views
# lazyviews.add('/admin', admin)

@app.route('/deleteuser/<int:id>')
def deleteuser(id):
    global user
    User.query.filter_by(id=id).delete()
    db.session.commit()
    users = User.query.all()

    return render_template('admin.html', users = users)

@app.route('/register', methods = ["POST"])
def register():
    global user
    name = request.form.get("username")
    license_phate = request.form.get("licenes-plates")
    re = User(name,license_phate)
    db.session.add(re)
    db.session.commit()
    users = User.query.all()
    
    return render_template('admin.html',users = users)
#App
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/video')
# @cache.cached(timeout=300)  # Set a suitable timeout value in seconds
def video():
    reader = easyocr.Reader(['en'], gpu=False)
    # Load the YOLOv8 model
    model = YOLO('best.pt')
    img_url = "http://192.168.226.121:8080/?action=snapshot.jpg"  # Replace with the actual IP address
    # img_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXQPFBiAwPdiL8Oev4FGu-4_6FSor4Z_s_9Q&usqp=CAU"  # Replace with the actual IP address
    response = requests.get(img_url, auth=('pi', '1'))
    img_array = np.array(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(img_array, -1)
    results = model(image)
    boxes = results[0].boxes
    # print(results)
    # cv2.imshow("Ảnh Gốc", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    mytext = ""
    newtext = ""
    if boxes.shape[0] > 0:
        x_min = int(boxes.xyxy[0][0])
        y_min = int(boxes.xyxy[0][1])
        x_max = int(boxes.xyxy[0][2])
        y_max = int(boxes.xyxy[0][3])
    # image = cv2.imread(img_array)
    # Cắt ảnh theo bounding box
        cropped_image = image[y_min:y_max, x_min:x_max]
    #Easy OCR 
    # Chuyển đổi ảnh sang dạng grayscale
        cv2.imwrite("static/cropped_image.jpg", cropped_image)
        gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    # Nhận diện biển số
        kq = reader.readtext(gray_image)
        for (bbox, text, prob) in kq:
            print(f"Văn bản: {text}, Độ chắc chắn: {prob:.2f}")
            mytext += text
        
    filtered_string = re.sub(r'[^A-Za-z0-9]', '', mytext)
    print(filtered_string)
    
    # Tạo một bản ghi mới và thêm vào cơ sở dữ liệu
    # Thực hiện truy vấn
    result = Manager.query.filter(Manager.license_phate == filtered_string, (Manager.checkin.is_(None) | Manager.checkout.is_(None))).first()
    local = datetime.now()
    print("Local:", local.strftime("%m/%d/%Y, %H:%M:%S"))
    tz_VN = pytz.timezone('Asia/Ho_Chi_Minh') 
    datetime_VN = datetime.now(tz_VN)
    
    if result is None:
        # Nếu không có dữ liệu, thực hiện INSERT
        
        new_record = Manager(license_phate=filtered_string, checkin=datetime_VN)
        db.session.add(new_record)
    else:
        # Nếu có dữ liệu, thực hiện UPDATE
        result.checkout = datetime_VN

    # Lưu các thay đổi vào cơ sở dữ liệu
    db.session.commit()

    return render_template('video.html', text = filtered_string)

# Đăng ký hàm xử lý /api/video với Lazy Views
# lazyviews.add('/api/video', video)

@app.route('/videoplayback')
def videoplayback():
    global data
    data = db.session.query(
    User.name,
    User.license_phate,
    Manager.id,
   
    func.strftime('%Y-%m-%d %H:%M:%S', Manager.checkout).label('formatted_checkout'),
    func.strftime('%Y-%m-%d %H:%M:%S', Manager.checkin).label('formatted_checkin')

).join(User, User.license_phate == Manager.license_phate).all()
    # s
    return render_template('videoplayback.html',data= data)
# Đăng ký hàm xử lý videoplayback với Lazy Views
# lazyviews.add('/videoplayback', videoplayback)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)


