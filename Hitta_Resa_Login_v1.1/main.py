from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# Detta är definitionen till att applikationen ska köras med debugging