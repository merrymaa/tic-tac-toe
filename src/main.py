from web.app import create_app


def main():
    app = create_app()
    print("Сервер запущен на http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == "__main__":
    main()
