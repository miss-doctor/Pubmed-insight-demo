#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS

from config import HOST, PORT, STATIC_DIR, TEMPLATE_DIR
from routes.api import bp as api_bp


def create_app():
    """创建并配置 Flask 应用。"""
    app = Flask(
        __name__,
        static_folder=STATIC_DIR,
        template_folder=TEMPLATE_DIR,
    )
    CORS(app)
    app.register_blueprint(api_bp)
    return app


app = create_app()


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True, use_reloader=False)
