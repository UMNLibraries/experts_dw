def upgrade():
  # Alter PKs:
  op.drop_constraint(
    'SYS_C00264304',
    'mds_person_internet_id',
    type_='primary'
  )
  op.create_primary_key(
    None,
    'mds_person_internet_id',
    ['uuid', 'timestamp']
  )

  # Make emplid nullable (this should remove an index that would otherwise cause problems):
  op.alter_column(
    'mds_person_internet_id',
    'emplid',
    existing_type=sa.VARCHAR(length=11),
    nullable=True
  )

  # Remove emplid FK:
  op.drop_constraint('SYS_C00281671', 'mds_person_internet_id', type_='foreignkey')

  # Remove emplid column:
  op.drop_column('mds_person_internet_id', 'emplid')

def downgrade():
  # Re-create emplid column:
  op.add_column('mds_person_internet_id', sa.Column('emplid', sa.VARCHAR(length=11), nullable=True))

  # Probably need an emplid re-populating step here...

  # Re-create old emplid FK:
  op.create_foreign_key('SYS_C00281671', 'mds_person_internet_id', 'mds_person_emplid', ['emplid'], ['emplid'], ondelete='CASCADE')

  # Drop new PK and restore old emplid-based PK:
  op.drop_constraint(
    None, # Not sure this will work. Would probably have to add the Oracle-generated name.
    'mds_person_internet_id',
    type_='primary'
  )
  op.create_primary_key(
    None,
    'mds_person_internet_id',
    ['emplid','timestamp']
  )

