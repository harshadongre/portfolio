from flask import Flask, render_template, request, flash, redirect, url_for, abort, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Add context processor to make current datetime and flash messages available in all templates
@app.context_processor
def inject_now():
    return {
        'now': datetime.utcnow(),
        'get_flashed_messages': get_flashed_messages
    }

db = SQLAlchemy(app)

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, nullable=False)  # 0-100
    category = db.Column(db.String(50))  # e.g., 'Language', 'Framework', 'Tool'
    icon = db.Column(db.String(50))  # Font Awesome icon class
    display_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Skill {self.name}>"

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100))
    github_url = db.Column(db.String(200))
    live_url = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    projects = Project.query.order_by(Project.date_created.desc()).all()
    skills = Skill.query.order_by(Skill.display_order, Skill.name).all()
    return render_template('index.html', projects=projects, skills=skills)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project_detail.html', project=project)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        new_contact = Contact(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()
        
        flash('Your message has been sent! I will get back to you soon.', 'success')
        return redirect(url_for('home'))
    
    return render_template('contact.html')

@app.route('/admin/skill/new', methods=['GET', 'POST'])
def new_skill():
    if request.method == 'POST':
        name = request.form.get('name')
        level = int(request.form.get('level', 0))
        category = request.form.get('category', 'Other')
        icon = request.form.get('icon', '').strip()
        display_order = int(request.form.get('display_order', 0) or 0)

        # Backend icon validation and auto-correction
        if not icon.startswith('fa-'):
            # Auto-assign brands for common languages
            lang_icons = ['python', 'js', 'javascript', 'java', 'php', 'html5', 'css3', 'node', 'react', 'vuejs', 'angular', 'github', 'git']
            if any(lang in name.lower() for lang in lang_icons):
                icon = f'fa-brands fa-{name.lower()}'
            else:
                icon = f'fa-solid fa-{icon}' if icon else 'fa-solid fa-code'

        skill = Skill(
            name=name,
            level=min(100, max(0, level)),  # Ensure level is between 0-100
            category=category,
            icon=icon,
            display_order=display_order
        )
        db.session.add(skill)
        db.session.commit()
        flash('Skill added successfully!', 'success')
        return redirect(url_for('home'))

    # Common Font Awesome icons for skills (brands and solid)
    common_icons = [
        'fa-brands fa-python', 'fa-brands fa-js', 'fa-brands fa-java', 'fa-brands fa-php', 'fa-brands fa-html5', 'fa-brands fa-css3',
        'fa-brands fa-node', 'fa-brands fa-react', 'fa-brands fa-vuejs', 'fa-brands fa-angular', 'fa-brands fa-github', 'fa-brands fa-git',
        'fa-solid fa-code', 'fa-solid fa-laptop-code', 'fa-solid fa-database', 'fa-solid fa-server', 'fa-solid fa-mobile-alt',
        'fa-solid fa-paint-brush', 'fa-solid fa-cogs', 'fa-solid fa-cloud', 'fa-solid fa-shield-alt', 'fa-solid fa-rocket'
    ]
    
    return render_template('admin/new_skill.html', common_icons=common_icons)

@app.route('/admin/project/new', methods=['GET', 'POST'])
def new_project():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        github_url = request.form.get('github_url')
        live_url = request.form.get('live_url')
        
        # Handle file upload
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '' and allowed_file(file.filename):
                # Generate a unique filename to prevent collisions
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                image = unique_filename
        
        # Create new project
        project = Project(
            title=title,
            description=description,
            image=image,
            github_url=github_url,
            live_url=live_url
        )
        
        db.session.add(project)
        db.session.commit()
        
        flash('Project added successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('admin/new_project.html')

if __name__ == '__main__':
    app.run(debug=True)
