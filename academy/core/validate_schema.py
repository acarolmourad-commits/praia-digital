"""
Academy database schema validator.
Run this against a live database to verify tables, relationships, and constraints.
"""
import sys
from sqlalchemy import inspect, text
from academy.core.database import engine, Base
from academy.core.models import *


def validate_schema():
    """Validate that all expected tables and columns exist."""
    inspector = inspect(engine)
    expected_tables = sorted([table.name for table in Base.metadata.tables])
    actual_tables = sorted(inspector.get_table_names())
    
    print("=== Schema Validation ===\n")
    
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
            print(f"✅ {table_name}: {len(expected_cols)} columns")
    
    # Check foreign keys
    print("\n=== Foreign Key Validation ===")
    for table_name in expected_tables:
        fks = inspector.get_foreign_keys(table_name)
        if fks:
            for fk in fks:
                print(f"  {table_name}.{fk['constrained_columns'][0]} → {fk['referred_table']}.{fk['referred_columns'][0]}")
    
    # Check indexes
    print("\n=== Index Validation ===")
    for table_name in expected_tables:
        indexes = inspector.get_indexes(table_name)
        for idx in indexes:
            print(f"  {table_name}: {idx['name']} ({', '.join(idx['column_names'])})")
    
    # Check unique constraints
    print("\n=== Unique Constraint Validation ===")
    for table_name in expected_tables:
        uqs = inspector.get_unique_constraints(table_name)
        for uq in uqs:
            print(f"  {table_name}: {uq['name']} ({', '.join(uq['column_names'])})")
    
    # Sample counts
    print("\n=== Data Summary ===")
    with engine.connect() as conn:
        for table_name in expected_tables:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.scalar()
            print(f"  {table_name}: {count} rows")
    
    print("\n✅ Schema validation complete")
    return True


if __name__ == "__main__":
    try:
        ok = validate_schema()
        sys.exit(0 if ok else 1)
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        sys.exit(1)
