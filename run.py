from app import create_app, db

# Create the Flask app using the factory function
app = create_app()

# Ensure tables are created
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

