
from flask import Blueprint, request, render_template, flash, url_for, session, g, redirect, jsonify, Flask, current_app
from app.models import User, Product
from app import db
import functools
from ..forms import UserLoginForm
from ..forms import ProductForm
import sqlite3
import logging, logstash
import logging.handlers

test = Blueprint('test', __name__, url_prefix='/')

# 로그 파일 설정
logging.basicConfig(filename='test.log', level=logging.INFO)


# Logstash로 로그 데이터를 전송하는 함수
# def send_log_to_logstash(record):
#     host = '127.0.0.1'  # Logstash 서버의 호스트 주소
#     port = 5000  # Logstash 서버의 수신 포트
#     handler = logging.handlers.HTTPHandler(host, port, method='POST')
#     formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')
#     handler.setFormatter(formatter)
#     logger = logging.getLogger('flask_log')
#     logger.addHandler(handler)
#     logger.setLevel(logging.INFO)
#     logger.handle(record)

@test.route('/')
def hello():
        current_app.logger.debug('This is a debug message')
        current_app.logger.info('This is an info message')
        current_app.logger.warning('This is a warning message')

        handlers = current_app.logger.handlers
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')
        handler.setFormatter(formatter) ## 텍스트 포맷 설정
        handler.setFormatter(formatter)
        current_app.logger = logging.getLogger('flask_log')
        current_app.logger.addHandler(handler)
        current_app.logger.addHandler(handler)
        current_app.logger.setLevel(logging.INFO)

        for handler in handlers:
            if isinstance(handler, logging.FileHandler):
                log_file_path = handler.baseFilename
                print("로그 파일 경로:", log_file_path)
                break
        return render_template("index.html")

@test.route('/about')
def about():
    current_app.logger.info('This is an ABOUT PAGE')
    return "about World!"

@test.route('/cart/<int:id>')
def cart(id):
    current_app.logger.info('page for adding products')
    form = ProductForm()
    products = Product.query.get_or_404(id)
    print(products)
    return render_template('cart.html', products=products, form=form)


@test.route('/cart', methods=['GET'])
def get_cart_info():
    current_app.logger.info('cart api')
    try:
        print('장바구니 api 진입')
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()

        user_id = 'test_id'        # 로그인 정보를 확인 할 수 없어 하드코딩했어요!

        # product테이블과 cart테이블을 join하여 데이터를 조회합니다.
        sql = f"SELECT A.id AS product_id, " \
              f"       A.product_name AS product_name, " \
              f"       A.price AS price, " \
              f"       COUNT(B.product_id) AS quantity " \
              f"  FROM product A " \
              f" INNER JOIN cart B ON B.product_id = A.id " \
              f" WHERE B.user_id = '{user_id}' " \
              f" GROUP BY B.user_id, A.id;"
        cursor.execute(sql)

        # Sqlite3는 select문을 실행해도 컬럼명이 안나와서 아래와 같이 컬럼명과 value를 매핑하도록 했어요!
        columns = [column[0] for column in cursor.description]
        cart_product = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print("cart_product :: " + str(cart_product))

        # 총 가격 계산
        total_price = sum(item['price'] * item['quantity'] for item in cart_product)

        # 데이터베이스 연결 종료
        cursor.close()
        conn.close()

    except Exception as e:
        if conn is not None:
            # 예외가 발생할 경우 아래와 같이 데이터베이스의 연결을 닫아주셔야해요!
            conn.rollback()
            conn.close()
        print("error" + str(e))
        current_app.logger.info('error in process: ' + str(e))
        return render_template("cart.html", products=[], total_price=0)

    # 조회한 데이터와 총 가격을 cart.html 템플릿으로 전달
    return render_template("cart.html", products=cart_product, total_price=total_price)


@test.route('/cart', methods=['POST'])
def add_to_cart():
    current_app.logger.info('장바구니 페이지 진입')
    try:
        data = request.get_json()                                       # 클라이언트에서 전달한 데이터를 JSON 형태로 받옵니다.
        product_id = data.get('product_id')                             # product_id 추출
        current_app.logger.info(f"product_id : {str(product_id)}")
        user_id = 'test_id'                                             # 로그인 정보를 확인 할 수 없어서 우선 하드코딩했어요. 나중에 로그인 후 세션에 저장된 아이디를 불러와서 처리해주면 됩니다!

        if not product_id or not str(product_id).isdigit():
            return jsonify(message="장바구니에 상품 번호가 없습니다."), 200

        """
        장바구니에 담는다.
        """
        conn = sqlite3.connect('test.db')                               # DB connect
        cursor = conn.cursor()

        # 아래 쿼리문은 1줄로 작성하셔도 됩니다. 실무에서는 아래와 같이 보기 좋게 작성하는 편이에요.
        sql = f"INSERT INTO cart(" \
              f"                    user_id," \
              f"                    product_id" \
              f"                )" \
              f"            VALUES (" \
              f"                        '{user_id}'," \
              f"                        {product_id}" \
              f"                    );"

        cursor.execute(sql)                             # 쿼리 실행
        conn.commit()                                   # 커밋
        conn.close()

        """
        장바구니에 담은 상품의 이름을 조회한다.
        """
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()

        # cart 테이블의 모든 데이터 조회
        sql = f"SELECT product_name " \
              f"  FROM product " \
              f" WHERE id = {product_id}" \
              f";"
        cursor.execute(sql)

        product_name = cursor.fetchall()[0][0]

        ret_msg = f"장바구니에 {product_name}를 추가했습니다!"              # 응답해줄 메시지를 정의했어요

        conn.close()

    except Exception as e:
        if conn is not None:
            # 예외가 발생할 경우 아래와 같이 데이터베이스의 연결을 닫아주셔야해요!
            conn.rollback()
            conn.close()
        print("오류가 발생했습니다.\n" + str(e))
        current_app.logger.info("error in process: " + str(e))
        return jsonify(message="can't add any product in your cart"), 200

    return jsonify(message=ret_msg), 200


@test.route('/kakaopay/<int:id>')
def kakaopay(id):
    current_app.logger.info('결제 페이지 진입 중')
    form = ProductForm()
    products = Product.query.get_or_404(id)
    if form.validate_on_submit():
        form.populate_obj(products)
        db.session.commit()
    return redirect(url_for('cart.html', products=products, form=form))


    # # products = [
    # #     Product(id=1, product_name='베이글 1', price=4800, quantity=1),
    # #     Product(id=2, product_name='베이글 2', price=5100, quantity=1),
    # #     Product(id=3, product_name='베이글 3', price=5500, quantity=1),
    # #     Product(id=4, product_name='베이글 4', price=4000, quantity=1),
    # #     Product(id=5, product_name='베이글 5', price=5000, quantity=1),
    # #     Product(id=6, product_name='베이글 6', price=6000, quantity=1),
    # #     Product(id=7, product_name='베이글 7', price=4500, quantity=1),
    # #     Product(id=8, product_name='베이글 8', price=5100, quantity=1)
    # # ]
    # products = Product.query.get_or_404(id)
    # if request.method == 'GET':  # POST 요청
    #     form = ProductForm()
    #     if form.validate_on_submit():
    #         form.populate_obj(products)
    #         db.session.commit()
    #         return render_template('cart.html', products=products, form=form)
    # else:  # GET 요청
    #     form = ProductForm(obj=products)
    # return render_template('cart.html', form=form)

#데이터를 등록하기 위한 함수를 만들어야 한다.
# @test.route('/login')
# def login():
#     email_address = request.args.get('email_address')
#     passwd = request.args.get('passwd')
#     print(email_address, passwd)

#     # if email_address == 'dave@gmail.com' and passwd == '111':

#     #     return_data = {'auth': 'success'}
#     # else:
#     #     return_data = {'auth': 'failed'}
#     # return jsonify(return_data)
#     return render_template("login_rawtest.html")

@test.route('/login', methods=('GET', 'POST'))
def login():
    current_app.logger.info('로그인 페이지 진입')
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
		# 폼 입력으로 받은 username으로 데이터베이스에 해당 사용자가 있는지를 검사한다. 만약 사용자가 없으면 "존재하지 않는 사용자입니다."라는 오류를 발생시키고, 사용자가 있다면 폼 입력으로 받은 password와 check_password_hash 함수를 사용하여 데이터베이스의 비밀번호와 일치하는지를 비교합니다.
        user = User.query.filter_by(user_id=form.user_id.data).first()
        # 로그인 자체가 막혀버림 
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif (user.password != form.password.data):
            error = "비밀번호가 올바르지 않습니다."
            
        # 아무 문제가 없으면 
        if error is None:
            # 사용자도 존재하고 비밀번호도 일치한다면 플라스크 서버의 나를 위한 저장소인 세션(session)에 사용자 정보를 저장합니다.

						# 세션에 user_id라는 객체 생성
            session.clear()
            session['user_id'] = user.user_id
            print(user.user_id)
            _next = request.args.get('next', '')
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('test.hello'))
                
        # 에러메시지를 flash 한테 넘깁니다
        # 문제가 있으면 그 문제를 form_errors.html로 보내버리는 역할 
        print(session['user_id'])
        flash(error)
    return render_template("login_rawtest.html", form=form)


@test.route('/html_test')
def hello_html():
    # html file은 templates 폴더에 위치해야 함
    return render_template('login_rawtest.html')
