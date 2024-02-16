import os

from flask import Flask

def create_app(test_config=None):
    # create configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # 내 db에 대한 application 의 cli 에서
    # init_db_command 를 사용 하도록 함.
    # db 가 down 될 때는 close_db를 통해 리소스 회수 하는
    # 코드를 실행 하도록 함.
    from . import db
    db.init_app(app)

    # 내 Application에 bp Blueprint 적용
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app