from flask import render_template,flash,url_for,session,redirect,request,g 
from app import app, db,lm,photos
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Rubbish,User,Punish
from app.forms import LoginForm,EditForm,RubbishForm,SignUpForm,ChangeForm,MessageForm
from datetime import datetime
import hashlib,time

@lm.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated:
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()	

@app.route('/',methods=['GET'])
@app.route('/index', methods = ['GET'])
@app.route('/index/<int:page>', methods = ['GET'])
@login_required
def index(page = 1):
	posts=Rubbish.query.filter_by(user_id = current_user.id).order_by(db.desc(Rubbish.time)).paginate(page,3, False)
	messages = Punish.query.filter_by(to_user=current_user.username).order_by(db.desc(Punish.time)).paginate(page, 3, False)
	return render_template('index.html',title='Home',posts = posts,messages=messages)

@app.route('/<index>/detail')
@login_required
def detail(index):
	post = Rubbish.query.filter_by(id=index).first()
	return render_template('detail.html',title='Detail',post = post)

@app.route('/write',methods=['GET','POST'])
@login_required
def write():
	form = RubbishForm()
	if form.validate_on_submit():
		post = Rubbish(type=form.type.data,weight = form.weight.data,community=form.community.data,user_id = current_user.id)
		db.session.add(post)
		db.session.commit()
		flash('You have submitted it!')
		return redirect(url_for('index'))
	return render_template('write.html',title='Write',form=form)


@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.login_check(request.form.get('username'),request.form.get('password'))
		if user:
			login_user(user)
			user.last_seen = datetime.now()
			try:
				db.session.add(user)
				db.session.commit()
			except:
				flash("The Database error!")
				return redirect('/login')
			flash('Your name: ' + request.form.get('username'))
			flash('remember me? ' + str(request.form.get('remember_me')))
			return redirect(url_for("index"))
		else:
			flash('Login failed, username or password error!')
			return redirect('/login')
	return render_template('login.html',form=form)

@app.route('/sign-up',methods=['GET','POST'])
def sign_up():
	form = SignUpForm()
	user = User()
	if form.validate_on_submit():
		user_name = request.form.get('username')
		user_password = request.form.get('password')
		register_check = User.query.filter(db.and_(User.username == user_name, User.password == user_password)).first()
		if register_check:
			return redirect('/sign-up')
		if len(user_name) and len(user_password):
			user.username = user_name
			user.password = user_password
		try:
			db.session.add(user)
			db.session.commit()
		except:
			return redirect('/sign-up')
		return redirect('/index')
	return render_template("sign_up.html",form=form)
		

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/statistic')
@login_required
def statistic():
	rubbish_type_recycling=Rubbish.query.filter(type="recycling").all()
	rubbish_type_other_rubbish=Rubbish.query.filter(type="other rubbish").all()
	rubbish_type_kitchen_waste = Rubbish.query.filter(type="kitchen waste").all()
	rubbish_type_hazardous_waste = Rubbish.query.filter(type="hazardous waste").all()
	rubbish_community_hazardous_waste = Rubbish.query.filter(type="hazardous waste").all()

@app.route('/user/<username>')
@login_required
def user(username,page = 1):
	user = User.query.filter_by(username = username).first()
	posts=Rubbish.query.filter_by(user_id = user.id).order_by(db.desc(Rubbish.time)).paginate(page,3, False)
	messages=Punish.query.filter_by(to_user=user.username).order_by(db.desc(Punish.time)).paginate(page,3, False)
	return render_template('user.html',user = user,posts = posts,messages=messages)

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
	form = EditForm(g.user.username)
	if form.validate_on_submit():
		g.user.username = form.username.data
		g.user.about_me = form.about_me.data
		db.session.add(g.user)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit'))
	form.username.data = g.user.username
	form.about_me.data = g.user.about_me
	return render_template('edit.html',form = form)

@app.route('/delete/<rubbish_id>',methods = ['POST'])
@login_required
def delete(rubbish_id):
	rubbish = Rubbish.query.filter_by(id = rubbish_id).first()
	db.session.delete(rubbish)
	db.session.commit()
	flash("delete rubbish successful!")
	return redirect(url_for('user',username=g.user.username))


@app.route('/edit/<rubbish_id>',methods = ['GET'])
@login_required
def editrubbish(rubbish_id):
	form = ChangeForm()
	post = Rubbish.query.filter_by(id = rubbish_id).first()
	form.type.data = post.type
	form.weight.data = post.weight
	form.community.data=post.community
	return render_template('change.html',form = form,post_id=post.id)

@app.route('/change/<rubbish_id>',methods = ['POST'])
@login_required
def change(rubbish_id):
	form = ChangeForm()
	post = Rubbish.query.filter_by(id = rubbish_id).first()
	if form.validate_on_submit():
		post.type = form.type.data
		post.weight = form.weight.data
		post.community=form.community.data
		print(post.type, post.weight, post.community)
		db.session.add(post)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('user',username=g.user.username))


# 上传文件
def Upload(file):
	#filename = hashlib.md5(current_user.username + str(time.time())).hexdigest()[:10]
	#filename.update(hash.encode("utf-8"))
	#photo = photos.save(file, name=filename + '.')
	photo = photos.save(file)
	if photo:
		url = photos.url(photo)
	return url

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
	form = MessageForm()
	if form.validate_on_submit():
		if request.method == 'POST' and 'photo' in request.files:
			#filename = photos.save(request.files['photo'])
			url = Upload(request.files['photo'])
			punish = Punish(message=form.message.data, to_user=form.to_user.data, url=url)
			db.session.add(punish)
			db.session.commit()
			flash('You have submitted it!')
			return redirect(url_for('index'))
	return render_template('upload.html', title='Upload', form=form)


