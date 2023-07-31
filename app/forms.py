# 화면에서 입력받은 데이터를 묶어서 백엔드로 전달하는 것

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length

class UserLoginForm(FlaskForm):
    user_id = StringField("사용자ID", validators=[DataRequired(), Length(5, 15, "ID는 5글자 이상 15글자 이내여야 합니다.")])
    password = StringField("비밀번호", validators=[DataRequired()])

class ProductForm(FlaskForm):
    id = IntegerField("상품번호", validators=[DataRequired()])
    product_name = StringField("상품명", validators=[DataRequired()])
    price = IntegerField("가격", validators=[DataRequired()]) #(5,2) 추가하려면 어떡해야하죠
    # number = IntegerField("가격", validators=[DataRequired()])
    quantity = IntegerField("수량", validators=[DataRequired()]) #default=1 추가하려면 어떡해야하죠

# init에 저장해야한다.
