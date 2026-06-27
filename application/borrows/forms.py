from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class BorrowForm( FlaskForm ):
    
    user_id = SelectField('利用者名', coerce=int, validators=[DataRequired()])
    book_id = SelectField('本タイトル', coerce=int, validators=[DataRequired()])

    submit = SubmitField('登録する')