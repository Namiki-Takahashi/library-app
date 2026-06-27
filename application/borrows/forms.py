from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class BorrowForm( FlaskForm ):
    name = StringField('利用者', 
                       validators=[DataRequired(message="名前は必須です")])
    book = StringField('本', 
                       validators=[DataRequired(message="名前は必須です")])
    stock = IntegerField('在庫冊数', 
            validators=[NumberRange(min=1, message="在庫が0のため貸出できません")])
    
    submit = SubmitField('登録する')