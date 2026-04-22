def merge_data(data: dict, config: dict):

    # Start with base table
    if "orders" not in data:
        raise ValueError("❌ 'orders' dataset not found in data")

    df = data["orders"].copy()
    merge_config = config.get("merge", {}).get("steps", [])

    for step in merge_config:

        left_name = step["left"]
        right_name = step["right"]
        on_col = step["on"]
        how = step.get("how", "left")

        # --- Safety checks
        if right_name not in data:
            print(f"⚠️ Skipping: {right_name} not found")
            continue

        right_df = data[right_name]

        if on_col not in df.columns:
            print(f"⚠️ Skipping merge with {right_name}: '{on_col}' not in left df")
            continue

        if on_col not in right_df.columns:
            print(f"⚠️ Skipping merge with {right_name}: '{on_col}' not in right df")
            continue

        # --- Merge
        df = df.merge(right_df, on=on_col, how=how)

        print(f"✅ Merged {right_name} on '{on_col}'")

    return df