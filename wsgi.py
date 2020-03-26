from helpline_backend import create_app

app = create_app()

if __name__ == "__main__":
    app.run(ssl_context='adhoc')

'''
if __name__ == '__main__':
    socketio.run(app)
'''
