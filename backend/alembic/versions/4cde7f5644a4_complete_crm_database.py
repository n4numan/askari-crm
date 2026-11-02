
"""complete crm database

Revision ID: 4cde7f5644a4
Revises: 150ebd2f86ff
Create Date: 2026-10-29 13:15:10.605507

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers
revision: str = "4cde7f5644a4"
down_revision: Union[str, Sequence[str], None] = "150ebd2f86ff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade the database to the complete CRM schema."""

    # 1. Create follow-ups table
    op.create_table(
        "follow_ups",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("tutor_id", sa.Integer(), nullable=True),
        sa.Column("follow_up_at", sa.DateTime(), nullable=False),
        sa.Column("method", sa.String(length=30), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("outcome", sa.Text(), nullable=True),
        sa.Column("next_action", sa.Text(), nullable=True),
        sa.Column("next_action_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["lead_id"],
            ["leads.id"],
            name="fk_follow_ups_lead_id_leads",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["tutor_id"],
            ["tutors.id"],
            name="fk_follow_ups_tutor_id_tutors",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_follow_ups_id"),
        "follow_ups",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_follow_ups_lead_id"),
        "follow_ups",
        ["lead_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_follow_ups_tutor_id"),
        "follow_ups",
        ["tutor_id"],
        unique=False,
    )

    # 2. Create tuitions table
    op.create_table(
        "tuitions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("tutor_id", sa.Integer(), nullable=True),
        sa.Column("monthly_fee", sa.Integer(), nullable=False),
        sa.Column("academy_commission", sa.Integer(), nullable=True),
        sa.Column("closing_date", sa.Date(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["lead_id"],
            ["leads.id"],
            name="fk_tuitions_lead_id_leads",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["tutor_id"],
            ["tutors.id"],
            name="fk_tuitions_tutor_id_tutors",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("lead_id", name="uq_tuitions_lead_id"),
    )

    op.create_index(
        op.f("ix_tuitions_id"),
        "tuitions",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_tuitions_lead_id"),
        "tuitions",
        ["lead_id"],
        unique=True,
    )
    op.create_index(
        op.f("ix_tuitions_tutor_id"),
        "tuitions",
        ["tutor_id"],
        unique=False,
    )

    # 3. Update demos table
    op.add_column(
        "demos",
        sa.Column("result", sa.String(length=50), nullable=True),
    )

    op.create_index(
        op.f("ix_demos_lead_id"),
        "demos",
        ["lead_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_demos_tutor_id"),
        "demos",
        ["tutor_id"],
        unique=False,
    )

    # Keep existing demo foreign keys unchanged to avoid
    # dropping constraints whose names may differ by database.

    # 4. Update leads table
    op.add_column(
        "leads",
        sa.Column("tutor_id", sa.Integer(), nullable=True),
    )

    # Add as nullable first so existing rows remain valid.
    op.add_column(
        "leads",
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )

    op.execute(
        "UPDATE leads "
        "SET updated_at = CURRENT_TIMESTAMP "
        "WHERE updated_at IS NULL"
    )

    op.alter_column(
        "leads",
        "updated_at",
        existing_type=sa.DateTime(),
        nullable=False,
    )

    op.alter_column(
        "leads",
        "lead_code",
        existing_type=sa.VARCHAR(length=20),
        type_=sa.String(length=30),
        existing_nullable=False,
    )

    op.create_index(
        op.f("ix_leads_status"),
        "leads",
        ["status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_leads_tutor_id"),
        "leads",
        ["tutor_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_leads_tutor_id_tutors",
        "leads",
        "tutors",
        ["tutor_id"],
        ["id"],
        ondelete="SET NULL",
    )

    # 5. Update tutors table
    op.add_column(
        "tutors",
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )

    op.execute(
        "UPDATE tutors "
        "SET updated_at = CURRENT_TIMESTAMP "
        "WHERE updated_at IS NULL"
    )

    op.alter_column(
        "tutors",
        "updated_at",
        existing_type=sa.DateTime(),
        nullable=False,
    )

    op.create_index(
        op.f("ix_tutors_phone"),
        "tutors",
        ["phone"],
        unique=False,
    )


def downgrade() -> None:
    """Reverse the complete CRM schema migration."""

    # 1. Revert tutors changes
    op.drop_index(
        op.f("ix_tutors_phone"),
        table_name="tutors",
    )
    op.drop_column("tutors", "updated_at")

    # 2. Revert leads changes
    op.drop_constraint(
        "fk_leads_tutor_id_tutors",
        "leads",
        type_="foreignkey",
    )

    op.drop_index(
        op.f("ix_leads_tutor_id"),
        table_name="leads",
    )
    op.drop_index(
        op.f("ix_leads_status"),
        table_name="leads",
    )

    op.alter_column(
        "leads",
        "lead_code",
        existing_type=sa.String(length=30),
        type_=sa.VARCHAR(length=20),
        existing_nullable=False,
    )

    op.drop_column("leads", "updated_at")
    op.drop_column("leads", "tutor_id")

    # 3. Revert demos changes
    op.drop_index(
        op.f("ix_demos_tutor_id"),
        table_name="demos",
    )
    op.drop_index(
        op.f("ix_demos_lead_id"),
        table_name="demos",
    )
    op.drop_column("demos", "result")

    # 4. Drop tuitions table
    op.drop_index(
        op.f("ix_tuitions_tutor_id"),
        table_name="tuitions",
    )
    op.drop_index(
        op.f("ix_tuitions_lead_id"),
        table_name="tuitions",
    )
    op.drop_index(
        op.f("ix_tuitions_id"),
        table_name="tuitions",
    )
    op.drop_table("tuitions")

    # 5. Drop follow-ups table
    op.drop_index(
        op.f("ix_follow_ups_tutor_id"),
        table_name="follow_ups",
    )
    op.drop_index(
        op.f("ix_follow_ups_lead_id"),
        table_name="follow_ups",
    )
    op.drop_index(
        op.f("ix_follow_ups_id"),
        table_name="follow_ups",
    )
    op.drop_table("follow_ups")
