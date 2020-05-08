from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField,TextField,TextAreaField,SubmitField,BooleanField,IntegerField
from wtforms.validators import Required, Length

class LoginForm(Form):
	username = StringField(validators=[Required(), Length(max=15)])
	password = StringField(validators=[Required(), Length(max=15)])
	remember_me = BooleanField('remember me', default=False)
	submit = SubmitField('Login')

class SignUpForm(Form):
	username = StringField(validators=[Required(), Length(max=15)])
	password = StringField(validators=[Required(), Length(max=15)])
	submit = SubmitField('Sign up')

class MessageForm(Form):
	to_user = StringField(validators=[Required(), Length(max=15)])
	message = TextAreaField('message', validators=[Length(min=0, max=120)])

class EditForm(Form):
	username = TextField('username', validators = [Required()])
	about_me = TextAreaField('about_me', validators = [Length(min = 0, max =140)])
	def __init__(self, original_username, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.original_username = original_username
	def validate(self):
		if not Form.validate(self):
			return False
		if self.username.data == self.original_username:
			return True
		user = User.query.filter_by(username = self.username.data).first()
		if user != None:
			return False
		return True

class ChangeForm(Form):
	type = TextField('type', validators=[Required(Length(min=0, max=120))])
	weight = IntegerField('weight', validators=[Required()])
	community = TextAreaField('community', validators=[Length(min=0, max=120)])

class RubbishForm(Form):
	#title = TextField('title', validators = [Required(Length(min =0,max=120))])
	#content = TextAreaField('content', validators = [Length(min = 0, max=1200)])
	type = TextField('type', validators=[Required(Length(min=0, max=120))])
	weight=IntegerField('weight',validators=[Required()])
	community = TextAreaField('community', validators=[Length(min=0, max=120)])
