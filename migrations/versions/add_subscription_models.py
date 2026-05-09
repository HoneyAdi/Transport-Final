"""Add subscription models

Revision ID: add_subscription_models
Revises: 
Create Date: 2026-04-26

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_subscription_models'
down_revision = 'c1f2e3d4a5b6'
branch_labels = None
depends_on = None


def upgrade():
    # Create subscription_plans table
    op.create_table(
        'subscription_plans',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('monthly_price', sa.Numeric(10, 2), nullable=False),
        sa.Column('annual_price', sa.Numeric(10, 2), nullable=False),
        sa.Column('max_vehicles', sa.Integer(), nullable=False),
        sa.Column('max_drivers', sa.Integer(), nullable=False),
        sa.Column('max_users', sa.Integer(), nullable=False),
        sa.Column('max_storage_gb', sa.Integer(), nullable=False),
        sa.Column('features', sa.Text()),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False)
    )

    # Create tenant_subscriptions table
    op.create_table(
        'tenant_subscriptions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('tenant_id', sa.Integer(), nullable=False, index=True),
        sa.Column('plan_id', sa.Integer()),
        sa.Column('custom_monthly_price', sa.Numeric(10, 2)),
        sa.Column('custom_annual_price', sa.Numeric(10, 2)),
        sa.Column('discount_percentage', sa.Numeric(5, 2), default=0),
        sa.Column('billing_cycle', sa.String(20), default='monthly'),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('expiry_date', sa.Date(), nullable=False),
        sa.Column('current_vehicles', sa.Integer(), default=0),
        sa.Column('current_drivers', sa.Integer(), default=0),
        sa.Column('current_users', sa.Integer(), default=0),
        sa.Column('current_storage_mb', sa.Integer(), default=0),
        sa.Column('status', sa.String(20), default='active'),
        sa.Column('auto_renew', sa.Boolean(), default=True),
        sa.Column('payment_method', sa.String(50), default='manual'),
        sa.Column('last_payment_date', sa.Date()),
        sa.Column('next_payment_date', sa.Date()),
        sa.Column('payment_notes', sa.Text()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['plan_id'], ['subscription_plans.id']),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'])
    )

    # Create subscription_payments table
    op.create_table(
        'subscription_payments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('subscription_id', sa.Integer(), nullable=False, index=True),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('payment_date', sa.Date(), nullable=False),
        sa.Column('payment_method', sa.String(50)),
        sa.Column('transaction_id', sa.String(100)),
        sa.Column('status', sa.String(20), default='success'),
        sa.Column('notes', sa.Text()),
        sa.Column('invoice_url', sa.String(255)),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['subscription_id'], ['tenant_subscriptions.id'])
    )


def downgrade():
    op.drop_table('subscription_payments')
    op.drop_table('tenant_subscriptions')
    op.drop_table('subscription_plans')
