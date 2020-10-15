from __future__ import with_statement
from alembic import context

# Added create_engine for Experts@Minnesota to support config via env vars.
from sqlalchemy import engine_from_config, pool, create_engine

from logging.config import fileConfig

# Added for Experts@Minnesota to support config via env vars.
import os
import dotenv_switch.auto

# Seems silly that I have to add this--probably a better way:
import sys
sys.path.append('.')
from experts_dw import db, models

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = models.Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Added for Experts@Minnesota to support config via env vars.
def get_url():
    return db.url('hotel')

exclude_tables = config.get_section('alembic:exclude').get('tables', '').split(',')

def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and name in exclude_tables:
        return False
    else:
        return True

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    # Modified for Experts@Minnesota to support config via env vars.
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        include_object=include_object,
        literal_binds=True,
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # Modified for Experts@Minnesota to support config via env vars.
    connectable = create_engine(get_url(),max_identifier_length=128)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
