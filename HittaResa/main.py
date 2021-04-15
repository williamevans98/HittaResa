from website import create_app

# create_app körs som ligger i __init__.py
app = create_app()

# Detta är definitionen till att applikationen ska köras med debugging
if __name__ == '__main__':
    app.run(debug=True)