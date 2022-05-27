# This code is not meant to be run, but instead serve as a reference to basic blog functionality

# Class representation of a blog post
class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime)

    def __init__(self, title, content, date_posted=datetime.now()):
        self.title = title
        self.content = content
        self.date_posted = date_posted
    

# Routes user to the blog page which shows all the current blog posts in the database
@app.route('/blog')
def blog_index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template("blog.html", posts=posts)

# Add a new blog post to blog.db using information from html form in blog.html
@app.route('/add_post', methods=["POST"])
def add_post():
    title = request.form['title']
    content = request.form['body']

    new_post = Blogpost(title, content)

    try:
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog_index'))
    except:
        return "There was an error adding your post!"

# Deletes blog post from blog.db based on the post's ID
@app.route('/delete_post/<int:id>')
def delete_post(id):
    post_to_delete = Blogpost.query.get_or_404(id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        return redirect(url_for('blog_index'))
    except:
        return "There was an error deleting your post!"

# Edits a post in blog.db based on the post's ID and information in form in update.html
@app.route('/edit_post/<int:id>', methods = ["GET", "POST"])
def edit_post(id):
    post_to_edit = Blogpost.query.get_or_404(id)

    if request.method == 'POST':
        post_to_edit.content = request.form['body']

        try:
            db.session.commit()
            return redirect(url_for('blog_index'))
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', post=post_to_edit)