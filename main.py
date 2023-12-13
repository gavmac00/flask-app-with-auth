from website import create_app

application = create_app()

"""Comment out the below for deployment."""
# if __name__ == '__main__':
#     app.run(debug=True) # debug will auto restart server when changes are made