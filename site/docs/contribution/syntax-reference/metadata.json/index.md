---
description: Learn the syntax and schema for the `metadata.json` file used in the HKU Notes project, which contains information about how to build and present each document.
---

# Syntax Reference for `metadata.json`

The `metadata.json` file is used to define the metadata for each build target in the HKU Notes project.
This file is required for each build target as it contains information about how the target should be built,
how it should be displayed and presented on the website.

## Schema Versions

There are two versions of the `metadata.json` schema:

<div class="grid cards" markdown>

-   :material-numeric-2-box:{ .lg .middle } **Schema v2** _(Recommended)_

    ---

    The current recommended schema for new build targets. Features a flexible button system and uses the `$schema` field for version detection.

    [:octicons-arrow-right-24: View v2 Documentation](v2.md)

-   :material-numeric-1-box:{ .lg .middle } **Schema v1** _(Legacy)_

    ---

    The legacy schema maintained for backward compatibility. Uses `@metadata_file_version` for version detection and supports primary/secondary button structure.

    [:octicons-arrow-right-24: View v1 Documentation](v1.md)

</div>

## Version Detection

The build pipeline automatically detects the schema version of each `metadata.json` file using the following priority:

1. **`$schema` field** - If present and contains `schemas/v2.json`, the file is treated as v2
2. **`@metadata_file_version` field** - Legacy method for both v1 and v2
3. **Error** - If neither field is present, the build will fail

!!! tip "Choosing a Schema Version"

    - **For new build targets**: Use [schema v2](v2.md) with the `$schema` field
    - **For existing build targets**: No changes needed - v1 files will continue to work
    - **Migrating from v1 to v2**: See the [v2 documentation](v2.md#changes-from-v1-to-v2) for key differences

## Common Concepts

Both schema versions share common naming conventions and structural concepts:

### Key Naming Conventions

All keys in the `metadata.json` file should be in `snake_case` format.
In this documentation, dots (`.`) are used to represent a hierarchy of keys.
Keys should not contain dots in their names.

??? example

    The key `build.build_command` would mean:

    ```json title="Correct Interpretation"
    {
        "build": {
            "build_command": "..."
        }
    }
    ```
    
    rather than:

    ```json title="Incorrect Interpretation"
    {
        "build.build_command": "..."
    }
    ```

An arbitrary object of an array is denoted using `[i]`. The keys of the object are enclosed
within curly braces `{}`.

??? example

    The key `static_site.buttons[i].{text}` would mean:

    ```json
    {
        "static_site": {
            "buttons": [
                {
                    "text": "Button 1"
                },
                {
                    "text": "Button 2"
                }
            ]
        }
    }
    ```

## Next Steps

Select the appropriate schema version documentation for detailed field references:

- [Schema v2 Documentation](v2.md) - Recommended for new projects
- [Schema v1 Documentation](v1.md) - Reference for legacy projects
