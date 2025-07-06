from app import create_app,db

app = create_app()
# 🔧 Create tables on first run (only once!)
with app.app_context():
    db.create_all()