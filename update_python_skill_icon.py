from app import app, db, Skill

with app.app_context():
    skill = Skill.query.filter_by(name="python").first()
    if skill:
        skill.icon = "fa-brands fa-python"
        db.session.commit()
        print("Python skill icon updated to fa-brands fa-python.")
    else:
        print("Python skill not found.")
