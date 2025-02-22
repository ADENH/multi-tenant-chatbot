from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from app.models import Base  # Import your SQLAlchemy Base
from alembic import context

# This is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

# Other configurations...