"""Add user amendment requests table

Revision ID: add_user_amendment_requests
Revises: 
Create Date: 2026-04-26

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_user_amendment_requests'
down_revision = 'add_vendor_user_models'
branch_labels = None
depends_on = None


def upgrade():
    # Create user_amendment_requests table
    op.create_table(
        'user_amendment_requests',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False, index=True),
        sa.Column('requested_by', sa.Integer(), nullable=False, index=True),
        sa.Column('tenant_id', sa.Integer(), index=True),
        sa.Column('field_changes', sa.Text(), nullable=False),
        sa.Column('change_type', sa.String(20), nullable=False, default='basic'),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, default='pending'),
        sa.Column('approved_by', sa.Integer(), index=True),
        sa.Column('approved_at', sa.DateTime()),
        sa.Column('rejection_reason', sa.Text()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['approved_by'], ['users.id']),
        sa.ForeignKeyConstraint(['requested_by'], ['users.id']),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'])
    )


def downgrade():
    op.drop_table('user_amendment_requests')
