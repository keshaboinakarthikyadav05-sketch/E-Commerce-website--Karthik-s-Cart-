import os
from flask import Flask, abort, jsonify, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound
from sqlalchemy.exc import SQLAlchemyError
from app.config import Config
from app.database import initialize_database, register_database_commands
from app.models import db, bcrypt, jwt

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__, static_folder=None)
    app.config.from_object(config_class)

    frontend_dist = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'dist')
    )

    # Enable CORS for frontend Vite dev server & production origin
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.categories import categories_bp
    from app.routes.categories import get_categories
    from app.routes.cart import cart_bp
    from app.routes.wishlist import wishlist_bp
    from app.routes.orders import orders_bp
    from app.routes.payments import payments_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(cart_bp, url_prefix='/api/cart')
    app.register_blueprint(wishlist_bp, url_prefix='/api/wishlist')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(payments_bp, url_prefix='/api/payments')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.add_url_rule(
        '/api/products/categories',
        endpoint='product_categories',
        view_func=get_categories,
        methods=['GET'],
    )

    if os.path.isfile(os.path.join(frontend_dist, 'index.html')):
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def serve_frontend(path):
            if path == 'api' or path.startswith('api/'):
                abort(404)

            if path:
                try:
                    return send_from_directory(frontend_dist, path)
                except NotFound:
                    pass

            return send_from_directory(frontend_dist, 'index.html')

    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        try:
            db.session.execute(db.text('SELECT 1'))
        except SQLAlchemyError:
            app.logger.exception('Database health check failed')
            db.session.rollback()
            return jsonify({
                'status': 'unhealthy',
                'service': "Karthik's Cart E-Commerce API",
                'database': 'disconnected',
                'version': '1.0.0'
            }), 503

        return jsonify({
            'status': 'healthy',
            'service': "Karthik's Cart E-Commerce API",
            'database': 'connected',
            'version': '1.0.0'
        }), 200

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'message': 'API endpoint not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

    @app.errorhandler(SQLAlchemyError)
    def database_error(error):
        app.logger.exception('Database request failed', exc_info=error)
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Database is temporarily unavailable. Please retry shortly.'
        }), 503

    @jwt.unauthorized_loader
    def unauthorized_response(callback):
        return jsonify({'success': False, 'message': 'Missing or invalid authentication token'}), 401

    @jwt.expired_token_loader
    def expired_token_response(jwt_header, jwt_payload):
        return jsonify({'success': False, 'message': 'Authentication token has expired. Please login again.'}), 401

    register_database_commands(app)
    initialize_database(app)

    return app
