---
description: Learn the syntax and schema for the `metadata.json` file used in the HKU Notes project, which contains information about how to build and present each document.
---

# Syntax Reference for `metadata.json`

The `metadata.json` file is used to define the metadata for each build target in the HKU Notes project.
This file is required for each build target as it contains information about how the target should be built,
how it should be displayed and presented on the website.

## Schema Versions

There are two versions of the `metadata.json` schema:

!!! danger "Schema v1 has been phased out"

    All existing build targets have been migrated to **schema v2**. Schema v1 is **no longer supported**.
    Pull requests that introduce build targets using v1 schema **will not be merged** until updated to v2.

<div class="grid cards" markdown>

-   :material-numeric-2-box:{ .lg .middle } **Schema v2** _(Required)_

    ---

    The only supported schema for all build targets. Features a flexible button system and uses the `$schema` field for version detection.

    [:octicons-arrow-right-24: View v2 Documentation](v2.md)

-   :material-numeric-1-box:{ .lg .middle } **Schema v1** _(Phased Out)_

    ---

    No longer supported. All targets have been migrated to v2. This documentation is kept for historical reference only.

    [:octicons-arrow-right-24: View v1 Documentation](v1.md)

</div>

## Version Detection

The build pipeline detects the schema version of each `metadata.json` file using the following priority:

1. **`$schema` field** - If present and contains `schemas/v2.json`, the file is treated as v2
2. **`@metadata_file_version` field** - Legacy fallback for historical v1 and v2 files
3. **Error** - If neither field is present, the build will fail

!!! tip "Using Schema v2"

    All build targets must use [schema v2](v2.md) with the `$schema` field.
    See the [v2 documentation](v2.md#changes-from-v1-to-v2) for the full list of fields.

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
