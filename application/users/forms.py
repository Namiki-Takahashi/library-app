from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,EmailField
from wtforms.validators import DataRequired, Email

class UserForm( FlaskForm ):
    name = StringField('お名前', 
                       validators=[DataRequired(message="名前は必須です")])
    kana = StringField('ふりがな', 
                       validators=[DataRequired(message="名前は必須です")])
    email = EmailField('メールアドレス', 
                       validators=[DataRequired(message="メールアドレスは必須です"), 
                        Email(message="正しいメールアドレスを入力してください")])
    submit = SubmitField('登録する')