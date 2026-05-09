"""add vendor user models

Revision ID: add_vendor_user_models
Revises: add_subscription_models
Create Date: 2026-04-29

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'add_vendor_user_models'
down_revision = 'add_subscription_models'
branch_labels = None
depends_on = None


def upgrade():
    # Create vendor_users table
    op.create_table(
        'vendor_users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('vendor_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), nullable=False),
        sa.Column('is_primary', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('can_view_own_data', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('can_edit_own_data', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=str(datetime.utcnow())),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ),
        sa.UniqueConstraint('vendor_id', 'user_id', name='uq_vendor_user'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vendor_users_tenant_id'), 'vendor_users', ['tenant_id'], unique=False)
    op.create_index(op.f('ix_vendor_users_user_id'), 'vendor_users', ['user_id'], unique=False)
    op.create_index(op.f('ix_vendor_users_vendor_id'), 'vendor_users', ['vendor_id'], unique=False)

    # Create vendor_field_permissions table
    op.create_table(
        'vendor_field_permissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('vendor_user_id', sa.Integer(), nullable=False),
        sa.Column('field_name', sa.String(length=100), nullable=False),
        sa.Column('field_category', sa.String(length=50), nullable=False),
        sa.Column('can_view', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('can_edit', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('is_required', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=str(datetime.utcnow())),
        sa.ForeignKeyConstraint(['vendor_user_id'], ['vendor_users.id'], ),
        sa.UniqueConstraint('vendor_user_id', 'field_name', name='uq_vendor_user_field'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vendor_field_permissions_vendor_user_id'), 'vendor_field_permissions', ['vendor_user_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_vendor_field_permissions_vendor_user_id'), table_name='vendor_field_permissions')
    op.drop_table('vendor_field_permissions')
    op.drop_index(op.f('ix_vendor_users_vendor_id'), table_name='vendor_users')
    op.drop_index(op.f('ix_vendor_users_user_id'), table_name='vendor_users')
    op.drop_index(op.f('ix_vendor_users_tenant_id'), table_name='vendor_users')
    op.drop_table('vendor_users')
