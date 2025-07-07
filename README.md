# Portfolio Website

A modern, responsive portfolio website built with Flask and Tailwind CSS. Showcase your projects, skills, and contact information in a clean and professional manner.

## Features

- Responsive design that works on all devices
- Project showcase with detailed project pages
- Skills section with progress bars
- Contact form with email functionality
- Clean and modern UI with smooth animations
- Easy to customize and extend

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/portfolio-website.git
   cd portfolio-website
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   ```

## Running the Application

1. Initialize the database:
   ```bash
   flask shell
   >>> db.create_all()
   >>> exit()
   ```

2. Run the development server:
   ```bash
   flask run
   ```

3. Open your browser and navigate to `http://127.0.0.1:5000/`

## Adding Projects

You can add projects in two ways:

1. **Using the Flask shell**:
   ```bash
   flask shell
   >>> from app import db, Project
   >>> project = Project(
   ...     title="Project Title",
   ...     description="Project description goes here...",
   ...     image="project-image.jpg",  # Place images in static/uploads/
   ...     github_url="https://github.com/yourusername/project",
   ...     live_url="https://project-demo.com"
   ... )
   >>> db.session.add(project)
   >>> db.session.commit()
   >>> exit()
   ```

2. **Using the admin interface (to be implemented)**:
   Coming soon!

## Customization

- **Profile Information**: Update the hero section in `templates/index.html`
- **Skills**: Modify the skills section in `templates/index.html`
- **Styling**: Customize colors and styles in `static/css/style.css`
- **Projects**: Add or modify projects as described above

## Deployment

### Deploying to Heroku

1. Install the Heroku CLI and login:
   ```bash
   heroku login
   ```

2. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

3. Set up the database:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. Deploy your application:
   ```bash
   git push heroku main
   ```

5. Run database migrations:
   ```bash
   heroku run flask db upgrade
   ```

## License

This project is open source and available under the [MIT License](LICENSE).

## Credits

- [Flask](https://flask.palletsprojects.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Font Awesome](https://fontawesome.com/)

## Support

For support, please open an issue on the GitHub repository or contact me directly.
