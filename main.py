from app import create_app
from authorization_handler import AuthorizationHandler

if __name__ == '__main__':
    auth_handler = AuthorizationHandler("secretxyz")
    app2 = create_app(auth_handler)
    app2.run(debug=True, host='0.0.0.0', port=80)

