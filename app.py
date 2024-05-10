from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wall.db'
app.config['SECRET_KEY'] = 'fc186fd3-3ace-46c8-8031-a819ec7d9a0e'
db = SQLAlchemy(app)


@login.user_loader
def load_user(id):
	return db.session.get(User, int(id))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer(), primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	content = db.Column(db.Text(), nullable=False)
	created_on = db.Column(db.DateTime(), default=datetime.utcnow)
	author = db.Column(db.Integer(), nullable=False)

	def __repr__(self):
		return "<{}:{}>".format(self.id,  self.title[:10])


class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(63), index=True, unique=True)
	password_hash = db.Column(db.String(128))

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<{}:{}>'.format(self.id, self.username[:10])


@app.route('/')
@app.route('/index')
def index():
	posts = Post.query.order_by(desc(Post.created_on)).all()

	return render_template('index.html', posts=posts)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		password2 = request.form['password2']

		if password != password2:
			flash('Пароли не совпадают')
			return render_template('reg.html')

		if len(username) > 63:
			flash('Длина имени пользователя не должна быть больше 63 символов')
			return render_template('reg.html')

		try:
			user = User(username=username)
			user.set_password(password)
			db.session.add(user)
			db.session.commit()
		except Exception as e:
			flash(f'Ошибка при создании пользователя: {e}')
			return render_template('reg.html')
		else:
			login_user(user)
			return redirect('index')

	return render_template('reg.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	
	if request.method == 'POST':
		user = db.session.query(User).filter(User.username == request.form['username']).first()

		if not user.check_password(request.form['password']):
			flash('Пароль неверный')
			return render_template('login.html')

		if user is not None:
			login_user(user)
			return redirect(url_for('index'))
		else:
			flash('Пользователя не существует. Проверьте имя пользователя или пароль.')

	return render_template('login.html')


@app.route('/profile/<username>')
def profile(username: str):
	posts = db.session.query(Post).filter(Post.author == username).order_by(desc(Post.created_on)).all()

	return render_template('profile.html', username=username, posts=posts)


@login_required
@app.route('/new', methods=['GET', 'POST'])
def new_post():
	if not current_user.is_authenticated:
		return redirect('login')

	if request.method == 'POST':
		title = request.form['title']
		content =  request.form['content']

		if len(title) > 0 and len(title) < 256 and len(content) > 0:
			post = Post(title=title, content=content, author=current_user.username)
			
			try:
				db.session.add(post)
				db.session.commit()
			except Exception as e:
				flash(f'Вознилка ошибка при записи в базу данных: {e}')
			else:
				return redirect('index')
		else:
			flash('Ошибка, длина заголовка поста не соответствует стандартам. Максимальное количество символов заголовка - 255.')
			return render_template('newpost.html')

	return render_template('newpost.html')


if __name__ == '__main__':
	app.run(debug=True, port=5000)
