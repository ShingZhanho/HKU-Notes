---
description: Learn the syntax and schema for the `metadata.json` file used in the HKU Notes project, which contains information about how to build and present each document.
---

# Syntax Reference for `metadata.json`

The `metadata.json` file is used to define the metadata for each build target in the HKU Notes project.
This file is required for each build target as it contains information about how the target should be built,
how it should be displayed and presented on the website.

## Schema (v1)

The current latest schema version is `1`. It has only one required field, which is the version number. All other fields are optional.

!!! note "Key Naming Conventions"

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

### `@metadata_file_version`

- **Required**: Yes
- **Description**: The version of the metadata file schema. Must be set to `"1"`.
- **Type**: `string`

### `build.root_file`

- **Description**: Specifies the main file to be built for the target.
- **Type**: `string`
- **Default**: `[BUILD_TARGET].tex` where `[BUILD_TARGET]` is the name of the build target.

### `build.output_file`

- **Description**: Specifies the name of the output file to be generated after building the target.
The build pipeline looks for this file after executing the build command.
- **Type**: `string`
- **Default**: `[BUILD_TARGET].pdf` where `[BUILD_TARGET]` is the name of the build target.

### `build.requires`

- **Description**: A list of dependencies that are required to build the target.
- **Type**: `array` of `string`
- **Accepted Values**:
    - `python-minted-pkgs`: Instructs the pipeline to install the required Python packages for the `minted` LaTeX package.
- **Default**: `null`

### `build.prebuild_command`

- **Description**: A command to run before building the target.
This command is executed in the source directory of the build target, i.e., `/src/[BUILD_TARGET]`.
- **Type**: `string`
- **Default**: `null`

### `build.build_command`

- **Description**: The command to build the target.
This command is executed in the source directory of the build target, i.e., `/src/[BUILD_TARGET]`.
- **Type**: `string`
- **Default**: `latexmk -pdf -f -interaction=nonstopmode -cd -outdir=. ./[ROOT_FILE]` where `[ROOT_FILE]` is the value of `build.root_file`.

### `build.postbuild_command`

- **Description**: A command to run after building the target.
This command is executed in the source directory of the build target, i.e., `/src/[BUILD_TARGET]`.
- **Type**: `string`
- **Default**: `null`

### `build.miktex_package_file`

- **Description**: Specifies the `.tex` file that contains all the `\usepackage` commands for the target.
This file is used to generate a hash for retrieving the cached LaTeX packages for saving build time.
- **Type**: `string`
- **Default**: `packages.tex`

!!! note "Creating a `packages.tex` File"

    While `\usepackage` commands are not required to be in a separate file for
    general LaTeX documents, it is **mandatory** for documents in this repository
    to separate them into a single file for the purpose of caching LaTeX packages.

### `static_site.description`

- **Description**: A short description of the target, used in the static site.
- **Type**: `string`
- **Default**: `"-"` (a hyphen)

### `static_site.custom_md_file`

- **Description**: A custom Markdown file whose content will be copied to the end
of the static site page for the target. It should use the Markdown syntax for Material
MkDocs.
- **Type**: `string`
- **Default**: `""` (an empty string, meaning no custom Markdown file is used)

### `static_site.document_status`

- **Description**: The status of the document, used in the static site. It must be
one of the values in the `Accepted Values` section.
- **Type**: `string`
- **Accepted Values**: Refer to the [Document Statuses](../../downloads/document-status.md)
for the accepted three-letter codes and their meanings.
- **Default**: `"unk"` (Unknown)

### `static_site.alias_to`

- **Description**: Treats the target as an alias to another build target.
This is useful when a course has more than one course code.
- **Type**: `string`
- **Accepted Values**: The name of another **deployed** build target.
- **Default**: `null`

!!! note "Alias Targets"

    If a build target is an alias to another target, it will not be built.
    Therefore, all the commands specified in the `build` section will be ignored.
    Moreover, alias targets do not get their own page on the static site.
    Therefore, all other keys in the `static_site` section will be ignored as well.

    In the description field of the alias, it will display: "_(Alias to [TARGET_NAME])_".

    See the target `COMP2113-Cheatsheet` on the course catalogue page for an example of an alias target.

!!! warning "Alias Must Point to a Deployed Target"

    An alias target must point to a build target that has already been deployed,
    otherwise the build pipeline will fail.

    For example, if you would like to create a target `COMP2113-Cheatsheet` that points
    to `ENGG1340-Cheatsheet`. You must first add and successfully deploy the target
    `ENGG1340-Cheatsheet` before you can add the alias target `COMP2113-Cheatsheet`.

### `static_site.{primary_button, secondary_button}.disabled`

- **Description**: Whether the primary/secondary button is disabled or not.
A disabled button will not be displayed on the static site.
- **Type**: `boolean`
- **Default**: `false`

### `static_site.{primary_button, secondary_button}.text`

- **Description**: The text to be displayed on the primary/secondary button.
- **Type**: `string`
- **Default**: `"Download"` for primary button, and `"View Source"` for secondary button.

### `static_site.{primary_button, secondary_button}.icon`

- **Description**: The icon to be displayed on the primary/secondary button.
- **Type**: `string`
- **Default**: `"material-download"` for primary button, and `"material-github"` for secondary button.
- **Accepted Values**: Any valid icon name specified in the [Material for MkDocs documentation](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis.html),
or empty string for no icon.

### `static_site.{primary_button, secondary_button}.href`

- **Description**: The URL to be linked to when the primary/secondary button is clicked.
- **Type**: `string`
- **Default**: `"https://shingzhanho.github.io/HKU-Notes/files/[BUILD_TARGET]/[OUTPUT_FILE]"` for primary, `"https://github.com/ShingZhanho/HKU-Notes/tree/master/src/[BUILD_TARGET]"` for secondary,
where `[BUILD_TARGET]` is the name of the build target, and `[OUTPUT_FILE]` is the value of `build.output_file`.

### `authors`

- **Description**: A list of authors for the target. Each author must be a string, whose value is defined in `/site/docs/statics/authors/authors.json`.
- **Type**: `array` of `string`
- **Default**: `["jacob_shing"]` (an array containing a single string `jacob_shing`)
- **Accepted Values**: Any string that is a valid key in the `/site/docs/statics/authors/authors.json` file.

!!! note "Main Author and Coauthors"

    Add an exclamation mark (`!`) before the author string to indicate that this is the main author of the target.
    At most one author can be the main author. Having more than one main author will cause the build pipeline to fail.
    The unknown author `@unknown` cannot be the main author.

    If no main author is specified, the first author in the alphabetical order will be treated as the main author.

    All other authors are sorted in alphabetical order according to their `display_name` in the definition.

Also refer to the [syntax reference for `authors.json`](./authors.json.md) for the details about
how to define authors in the `authors.json` file.