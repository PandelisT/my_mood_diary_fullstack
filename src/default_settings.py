import os
class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "duck"
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024
    SECRET_KEY = '9OLWxND4o83j4K4iuopO'
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'yourId@gmail.com'
    MAIL_PASSWORD = '*****'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    @property
    def AWS_ACCESS_KEY_ID(self):
        value = os.getenv('AWS_ACCESS_KEY_ID')
        if not value:
            raise ValueError("AWS_ACCESS_KEY_ID is not set")
        return value
    
    @property
    def AWS_SECRET_ACCESS_KEY(self):
        value = os.getenv('AWS_SECRET_ACCESS_KEY')

        if not value:
            raise ValueError("AWS_SECRET_ACCESS_KEY is not set")
        return value
    
    @property
    def AWS_S3_BUCKET(self):
        value = os.getenv('AWS_S3_BUCKET')

        if not value:
            raise ValueError("AWS_S3_BUCKET is not set")

        return value

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # DB_URI for local development
        value = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
        
        # DB_URI for Docker
        # value =  f"{os.getenv('DB_URI')}"

        if not value:
            raise ValueError("DB_URI is not set")

        return value
class DevelopmentConfig(Config):
    DEBUG = True
class ProductionConfig(Config):
    @property
    def JWT_SECRET_KEY(self):
        value = os.getenv("JWT_SECRET_KEY")

        if not value:
            raise ValueError("JWT Secret Key is not set")
        
        return value
class TestingConfig(Config):
    TESTING = True

class WorkflowConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

environment = os.getenv("FLASK_ENV")

if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
elif environment == "workflow":
    app_config = WorkflowConfig()
else:
    app_config = DevelopmentConfig()