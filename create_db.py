from webapp import app, db  # Adjust the import as necessary

# Create the application context
with app.app_context():
    db.create_all()
