from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) # debug will auto restart server when changes are made