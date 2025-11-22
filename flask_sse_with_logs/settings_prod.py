from environs import Env

env = Env()
env.read_env()

# Override in .env for local development
DEBUG = env.bool("FLASK_DEBUG", default=False)
# SECRET_KEY is required
SECRET_KEY = env.str("FLASK_SECRET")

# SQL-ALCHEMY
# will change (env.str("SQLALCHEMY_DATABASE_URI")) to use HOSTED_POSTGRES_URL once in production 
SQLALCHEMY_DATABASE_URI = env.str("SQLALCHEMY_DATABASE_URI")