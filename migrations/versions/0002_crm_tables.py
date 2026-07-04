"""crm tables

Revision ID: 0002_crm_tables
Revises: 0001_init_users
Create Date: 2026-07-04
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0002_crm_tables"
down_revision = "0001_init_users"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "crm_organizations",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ux_crm_organizations_name", "crm_organizations", ["name"], unique=True)

    op.create_table(
        "crm_leads",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "org_id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            sa.ForeignKey("crm_organizations.id"),
            nullable=False,
        ),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="new"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_crm_leads_email", "crm_leads", ["email"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_crm_leads_email", table_name="crm_leads")
    op.drop_table("crm_leads")
    op.drop_index("ux_crm_organizations_name", table_name="crm_organizations")
    op.drop_table("crm_organizations")

