from app import create_app

if __name__ == '__main__':
    app2 = create_app()
    app2.run(debug=True, host='0.0.0.0', port=80)

