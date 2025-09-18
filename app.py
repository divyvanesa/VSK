from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from functools import wraps
import os
from werkzeug.utils import secure_filename
from datetime import datetime
# NEW: Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'vsk-gujarat-secret-key-2023'
app.config.from_pyfile('config.py')

# --- DATABASE SETUP ---
# NEW: Configure the database URI. This tells SQLAlchemy where to find the database.
# 'sqlite:///database.db' means we are using SQLite and the file is named database.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# NEW: Initialize the SQLAlchemy extension
db = SQLAlchemy(app)


# --- DATABASE MODELS ---
# NEW: Each class represents a table in the database.

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def excerpt(self):
        return self.content[:150] + '...' if len(self.content) > 150 else self.content


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def excerpt(self):
        return self.content[:150] + '...' if len(self.content) > 150 else self.content


class GalleryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'image' or 'video'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    filename = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ImportantDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(50), nullable=False)  # Storing date as string for simplicity
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class OtherItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# REMOVED: In-memory data storage lists are no longer needed.
# news_data = []
# articles_data = []
# ... and so on


# Admin authentication required decorator (no changes needed)
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in to access admin panel', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)

    return decorated_function


# File upload functions (no changes needed)
def allowed_file(filename, file_type='image'):
    if file_type == 'image':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_IMAGE_EXTENSIONS']
    elif file_type == 'video':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_VIDEO_EXTENSIONS']
    return False


def save_uploaded_file(file, folder='images'):
    if file and allowed_file(file.filename, 'image' if folder == 'images' else 'video'):
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], folder, filename)
        file.save(file_path)
        return filename
    return None


# --- Client Routes (MODIFIED to use database) ---
@app.route('/')
def index():
    # MODIFIED: Query the database for recent items
    recent_news = News.query.order_by(News.created_at.desc()).limit(3).all()
    recent_articles = Article.query.order_by(Article.created_at.desc()).limit(3).all()
    return render_template('index.html',
                           recent_news=recent_news,
                           recent_articles=recent_articles)


@app.route('/news')
def news():
    # MODIFIED: Query all news from the database
    all_news = News.query.order_by(News.created_at.desc()).all()
    return render_template('news.html', news=all_news)


@app.route('/news/<int:news_id>')
def news_detail(news_id):
    # MODIFIED: Get a specific news item by ID or return a 404 error
    news_item = News.query.get_or_404(news_id)
    return render_template('news-detail.html', news=news_item)


@app.route('/articles')
def articles():
    all_articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('articles.html', articles=all_articles)


@app.route('/articles/<int:article_id>')
def article_detail(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article-detail.html', article=article)


@app.route('/gallery')
def gallery():
    gallery_items = GalleryItem.query.order_by(GalleryItem.created_at.desc()).all()
    return render_template('gallery.html', gallery_items=gallery_items)


@app.route('/publications')
def publications():
    all_publications = Publication.query.order_by(Publication.created_at.desc()).all()
    return render_template('publications.html', publications=all_publications)


@app.route('/important-days')
def important_days():
    days = ImportantDay.query.order_by(ImportantDay.created_at.desc()).all()
    return render_template('important-days.html', important_days=days)


@app.route('/others')
def others():
    other_items = OtherItem.query.order_by(OtherItem.created_at.desc()).all()
    return render_template('others.html', others=other_items)


# Static file serving for uploads (no changes needed)
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# --- Admin Routes (MODIFIED to use database) ---

# Admin Login/Logout (no changes needed)
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('admin/login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('admin_login'))


@app.route('/admin')
@admin_required
def admin_dashboard():
    # MODIFIED: Get counts directly from database tables
    stats = {
        'news_count': News.query.count(),
        'articles_count': Article.query.count(),
        'gallery_count': GalleryItem.query.count(),
        'publications_count': Publication.query.count(),
        'important_days_count': ImportantDay.query.count(),
        'others_count': OtherItem.query.count(),
    }
    return render_template('admin/dashboard.html', stats=stats)


# --- Admin News Management (MODIFIED) ---
@app.route('/admin/news', methods=['GET', 'POST'])
@admin_required
def admin_news():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image = request.files.get('image')

        if title and content:
            image_filename = save_uploaded_file(image) if image else None
            # MODIFIED: Create a News object and add it to the database session
            new_entry = News(title=title, content=content, image=image_filename)
            db.session.add(new_entry)
            db.session.commit()  # Commit saves the changes to the database
            flash('News added successfully!', 'success')
            return redirect(url_for('admin_news'))
        else:
            flash('Title and content are required', 'error')

    # MODIFIED: Fetch all news from the DB to display on the admin page
    all_news = News.query.order_by(News.created_at.desc()).all()
    return render_template('admin/news.html', news=all_news)


@app.route('/admin/news/delete/<int:news_id>')
@admin_required
def delete_news(news_id):
    # MODIFIED: Find the news item by ID and delete it
    news_to_delete = News.query.get_or_404(news_id)
    # You might also want to delete the associated image file from the server here
    db.session.delete(news_to_delete)
    db.session.commit()
    flash('News deleted successfully', 'success')
    return redirect(url_for('admin_news'))


# --- Admin Articles Management (MODIFIED) ---
@app.route('/admin/articles', methods=['GET', 'POST'])
@admin_required
def admin_articles():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image = request.files.get('image')

        if title and content:
            image_filename = save_uploaded_file(image) if image else None
            new_article = Article(title=title, content=content, image=image_filename)
            db.session.add(new_article)
            db.session.commit()
            flash('Article added successfully!', 'success')
            return redirect(url_for('admin_articles'))
        else:
            flash('Title and content are required', 'error')

    all_articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('admin/articles.html', articles=all_articles)


@app.route('/admin/articles/delete/<int:article_id>')
@admin_required
def delete_article(article_id):
    article_to_delete = Article.query.get_or_404(article_id)
    db.session.delete(article_to_delete)
    db.session.commit()
    flash('Article deleted successfully', 'success')
    return redirect(url_for('admin_articles'))


# --- Admin Gallery Management (MODIFIED) ---
@app.route('/admin/gallery', methods=['GET', 'POST'])
@admin_required
def admin_gallery():
    if request.method == 'POST':
        title = request.form.get('title')
        file = request.files.get('file')
        file_type = request.form.get('type', 'image')

        if title and file:
            filename = save_uploaded_file(file, 'videos' if file_type == 'video' else 'images')
            if filename:
                new_gallery_item = GalleryItem(title=title, filename=filename, type=file_type)
                db.session.add(new_gallery_item)
                db.session.commit()
                flash('Gallery item added successfully!', 'success')
                return redirect(url_for('admin_gallery'))
            else:
                flash('Invalid file format', 'error')
        else:
            flash('Title and file are required', 'error')

    gallery_items = GalleryItem.query.order_by(GalleryItem.created_at.desc()).all()
    return render_template('admin/gallery.html', gallery_items=gallery_items)


@app.route('/admin/gallery/delete/<int:gallery_id>')
@admin_required
def delete_gallery_item(gallery_id):
    item_to_delete = GalleryItem.query.get_or_404(gallery_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    flash('Gallery item deleted successfully', 'success')
    return redirect(url_for('admin_gallery'))


# And so on for Publications, Important Days, and Others...
# The pattern is the same: replace list operations with db.session operations.

# --- Admin Publications Management (MODIFIED) ---
@app.route('/admin/publications', methods=['GET', 'POST'])
@admin_required
def admin_publications():
    if request.method == 'POST':
        # ... form processing ...
        new_publication = Publication(
            title=request.form.get('title'),
            description=request.form.get('description'),
            filename=save_uploaded_file(request.files.get('file'), 'publications')
        )
        db.session.add(new_publication)
        db.session.commit()
        flash('Publication added successfully!', 'success')
        return redirect(url_for('admin_publications'))

    all_publications = Publication.query.order_by(Publication.created_at.desc()).all()
    return render_template('admin/publications.html', publications=all_publications)


@app.route('/admin/publications/delete/<int:publication_id>')
@admin_required
def delete_publication(publication_id):
    item_to_delete = Publication.query.get_or_404(publication_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    flash('Publication deleted successfully', 'success')
    return redirect(url_for('admin_publications'))


# --- Admin Important Days Management (MODIFIED) ---
@app.route('/admin/important-days', methods=['GET', 'POST'])
@admin_required
def admin_important_days():
    if request.method == 'POST':
        # ... form processing ...
        new_day = ImportantDay(
            title=request.form.get('title'),
            date=request.form.get('date'),
            description=request.form.get('description'),
            image=save_uploaded_file(request.files.get('image'))
        )
        db.session.add(new_day)
        db.session.commit()
        flash('Important day added successfully!', 'success')
        return redirect(url_for('admin_important_days'))

    days = ImportantDay.query.order_by(ImportantDay.created_at.desc()).all()
    return render_template('admin/important-days.html', important_days=days)


@app.route('/admin/important-days/delete/<int:day_id>')
@admin_required
def delete_important_day(day_id):
    item_to_delete = ImportantDay.query.get_or_404(day_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    flash('Important day deleted successfully', 'success')
    return redirect(url_for('admin_important_days'))


# --- Admin Others Management (MODIFIED) ---
@app.route('/admin/others', methods=['GET', 'POST'])
@admin_required
def admin_others():
    if request.method == 'POST':
        # ... form processing ...
        new_item = OtherItem(
            title=request.form.get('title'),
            content=request.form.get('content'),
            category=request.form.get('category')
        )
        db.session.add(new_item)
        db.session.commit()
        flash('Item added successfully!', 'success')
        return redirect(url_for('admin_others'))

    items = OtherItem.query.order_by(OtherItem.created_at.desc()).all()
    return render_template('admin/others.html', others=items)


@app.route('/admin/others/delete/<int:other_id>')
@admin_required
def delete_other(other_id):
    item_to_delete = OtherItem.query.get_or_404(other_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    flash('Item deleted successfully', 'success')
    return redirect(url_for('admin_others'))


if __name__ == '__main__':
    # Create upload directories if they don't exist
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'images'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'videos'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'publications'), exist_ok=True)

    # NEW: Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)