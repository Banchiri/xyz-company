"""Initial migration.

Revision ID: c30b3f528e03
Revises: 
Create Date: 2025-04-24 20:25:57.316861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c30b3f528e03'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('departments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('manager_ssn', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['manager_ssn'], ['employees.ssn'], name=op.f('fk_departments_manager_ssn_employees')),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('employees',
    sa.Column('ssn', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('salary', sa.Float(), nullable=False),
    sa.Column('gender', sa.String(), nullable=False),
    sa.Column('birthdate', sa.Date(), nullable=False),
    sa.Column('postal_address', sa.String(), nullable=False),
    sa.Column('tel_no', sa.String(), nullable=False),
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.Column('supervisor_ssn', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], name=op.f('fk_employees_department_id_departments')),
    sa.ForeignKeyConstraint(['supervisor_ssn'], ['employees.ssn'], name=op.f('fk_employees_supervisor_ssn_employees')),
    sa.PrimaryKeyConstraint('ssn')
    )
    op.create_table('dependents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('gender', sa.String(), nullable=False),
    sa.Column('birthdate', sa.Date(), nullable=False),
    sa.Column('relationship', sa.String(), nullable=False),
    sa.Column('employee_ssn', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['employee_ssn'], ['employees.ssn'], name=op.f('fk_dependents_employee_ssn_employees')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], name=op.f('fk_locations_department_id_departments')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('number', sa.String(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], name=op.f('fk_projects_department_id_departments')),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('number')
    )
    op.create_table('works_on',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('employee_ssn', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('hours_per_week', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['employee_ssn'], ['employees.ssn'], name=op.f('fk_works_on_employee_ssn_employees')),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], name=op.f('fk_works_on_project_id_projects')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('works_on')
    op.drop_table('projects')
    op.drop_table('locations')
    op.drop_table('dependents')
    op.drop_table('employees')
    op.drop_table('departments')
    # ### end Alembic commands ###
