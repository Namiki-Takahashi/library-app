from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired

class BookForm( FlaskForm ):
    title = StringField('タイトル', 
                       validators=[DataRequired(message="必須項目です")])
    author = StringField('著者', 
                       validators=[DataRequired(message="必須項目です")])
    genre = StringField('ジャンル', 
                       validators=[DataRequired(message="必須項目です")])
    stock = SelectField('在庫冊数', 
                    choices=[(i, str(i)) for i in range(11)], 
                    coerce=int,
                    validators=[InputRequired(message="必須項目です")])

    submit = SubmitField('登録する')