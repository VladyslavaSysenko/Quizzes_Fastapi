import connections
import sqlalchemy

metadata = sqlalchemy.MetaData()
db = connections.get_db()

User = sqlalchemy.Table(
    "User",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String, unique=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
)
