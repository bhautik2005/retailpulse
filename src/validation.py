def validate_data(df, validation_config):

    errors = []

    # --- 1. Required columns
    for col in validation_config.get("required_columns", []):
        if col not in df.columns:
            errors.append(f"❌ Missing column: {col}")

    # --- 2. Non-null checks
    for col in validation_config.get("non_null_columns", []):
        if col in df.columns:
            if df[col].isnull().sum() > 0:
                errors.append(f"❌ {col} has null values")

    # --- 3. Positive value checks
    for col in validation_config.get("positive_columns", []):
        if col in df.columns:
            if not (df[col] > 0).all():
                errors.append(f"❌ {col} has invalid values (<= 0)")

    # --- 4. Range checks (advanced)
    for col, limits in validation_config.get("range_checks", {}).items():
        if col in df.columns:
            if not df[col].between(limits["min"], limits["max"]).all():
                errors.append(f"❌ {col} out of range [{limits['min']}, {limits['max']}]")

    # --- 5. Final decision
    if errors:
        print("\n".join(errors))
        raise ValueError("🚨 Data validation failed")
    
    print("✅ Validation passed")