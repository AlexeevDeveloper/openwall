from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wall.db'
app.config['SECRET_KEY'] = 'fc186fd3-3ace-46c8-8031-a819ec7d9a0e'
db = SQLAlchemy(app)


class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer(), primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	content = db.Column(db.Text(), nullable=False)
	created_on = db.Column(db.DateTime(), default=datetime.utcnow)

	def __repr__(self):
		return "<{}:{}>".format(self.id,  self.title[:10])


@app.route('/')
@app.route('/index')
def index():
	posts = Post.query.order_by(desc(Post.created_on)).all()

	return render_template('index.html', posts=posts)


@app.route('/new', methods=['GET', 'POST'])
def new_post():
	if request.method == 'POST':
		title = request.form['title']
		content =  request.form['content']

		if len(title) > 0 and len(content) > 0:
			post = Post(title=title, content=content)
			db.session.add(post)
			db.session.commit()
			return redirect('index')
		else:
			return render_template('newpost.html')

	return render_template('newpost.html')


if __name__ == '__main__':
	app.run(debug=False, port=5000)
