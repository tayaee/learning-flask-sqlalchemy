from flask import Flask
from flask import render_template
from flask import request


def create_app():
    app = Flask(__name__)

    @app.route('/', methods=["GET", "POST"])
    def home():
        if request.form:
            print(request.form)
            data = request.get_data()
            print(data)
        return render_template('home.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
