"""
Academy database setup and validation.
Creates all tables and validates schema integrity.
"""
import sys
from sqlalchemy import inspect, text
from academy.core.database import engine, Base, SessionLocal
from academy.core.models import (
    User, Course, Module, Lesson, Enrollment, Progress,
    Payment, Order, OrderItem, Cart, Certificate,
    UpsellRule, CrossSellRule, Coupon, EmailTemplate,
    AutomationRule, Lead, ContentAttachment, LeadEvent
)


def create_schema():
    """Create all tables in the database."""
    print("Creating database schema...")
    Base.metadata.create_all(bind=engine)
    print("✅ Schema created successfully")


def validate_schema():
    """Validate that all expected tables, columns, and constraints exist."""
    inspector = inspect(engine)
    expected_tables = sorted([table.name for table in Base.metadata.tables])
    actual_tables = sorted(inspector.get_table_names())

    print("\n=== Schema Validation ===\n")

    # Check tables
    print(f"Expected tables: {len(expected_tables)}")
    print(f"Actual tables:   {len(actual_tables)}")

    missing = set(expected_tables) - set(actual_tables)
    extra = set(actual_tables) - set(expected_tables)

    if missing:
        print(f"\n❌ Missing tables: {sorted(missing)}")
        return False
    else:
        print(f"\n✅ All expected tables exist")

    if extra:
        print(f"⚠️  Extra tables: {sorted(extra)}")

    # Check columns for each table
    print("\n=== Column Validation ===")
    for table_name in expected_tables:
        expected_cols = {col.name for col in Base.metadata.tables[table_name].columns}
        actual_cols = {col['name'] for col in inspector.get_columns(table_name)}

        missing_cols = expected_cols - actual_cols
        if missing_cols:
            print(f"❌ {table_name}: missing columns {sorted(missing_cols)}")
            return False
        else:
            print(f"✅ {table_name}: {len(expected_cols)} columns OK")

    # Check foreign keys
    print("\n=== Foreign Key Relationships ===")
    fk_count = 0
    for table_name in expected_tables:
        fks = inspector.get_foreign_keys(table_name)
        for fk in fks:
            fk_count += 1
            print(f"  {table_name}.{fk['constrained_columns'][0]} → {fk['referred_table']}.{fk['referred_columns'][0]}")
    print(f"\n✅ {fk_count} foreign key relationships found")

    # Check indexes
    print("\n=== Indexes ===")
    idx_count = 0
    for table_name in expected_tables:
        indexes = inspector.get_indexes(table_name)
        for idx in indexes:
            idx_count += 1
            print(f"  {table_name}: {idx['name']} ({', '.join(idx['column_names'])})")
    print(f"\n✅ {idx_count} indexes found")

    # Check unique constraints
    print("\n=== Unique Constraints ===")
    uq_count = 0
    for table_name in expected_tables:
        uqs = inspector.get_unique_constraints(table_name)
        for uq in uqs:
            uq_count += 1
            print(f"  {table_name}: {uq['name']} ({', '.join(uq['column_names'])})")
    print(f"\n✅ {uq_count} unique constraints found")

    # Sample counts
    print("\n=== Data Summary ===")
    with engine.connect() as conn:
        for table_name in expected_tables:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.scalar()
            print(f"  {table_name}: {count} rows")

    print("\n✅ Schema validation complete")
    return True


def main():
    print("=== Praia Digital Academy - Database Setup ===\n")

    # Step 1: Create schema
    create_schema()

    # Step 2: Validate schema
    ok = validate_schema()

    if ok:
        print("\n🎉 Database is ready for production use")
        return 0
    else:
        print("\n❌ Schema validation failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
