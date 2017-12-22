"""Added comments.

Revision ID: 92f0c5bb4344
Revises: ce5746d38b31
Create Date: 2017-06-10 12:11:14.615768

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '92f0c5bb4344'
down_revision = 'ce5746d38b31'
branch_labels = None
depends_on = None

def upgrade():
  op.execute("comment on table EXPERT.PUB is 'Research output. Named \"pub\", short for \"publication\", due to Oracle character-lenght limits.'");
  op.execute("comment on column EXPERT.PUB.UUID is 'Primary key, generated for this Experts@Minnesota database.'");

def downgrade():
  op.execute("comment on table EXPERT.PUB is NULL");
  op.execute("comment on column EXPERT.PUB.UUID is NULL");
