---
description: Learn the syntax and schema for the `metadata.json` file used in the HKU Notes project, which contains information about how to build and present each document.
---

# Syntax Reference for `metadata.json`

The `metadata.json` file is used to define the metadata for each build target in the HKU Notes project.
This file is required for each build target as it contains information about how the target should be built,
how it should be displayed and presented on the website.

!!! info "Version Detection"

    The build pipeline automatically detects the schema version of each `metadata.json` file using the following priority:

    1. **`$schema` field** - If present and contains `schemas/v2.json`, the file is treated as v2
    2. **`@metadata_file_version` field** - Legacy method for both v1 and v2
    3. **Error** - If neither field is present, the build will fail

    For new files, use the `$schema` field (v2 format). Existing files with `@metadata_file_version` will continue to work.

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

## Schema (v2)

The current latest schema version is `2`. It has only one required field: `$schema`. All other fields are optional.
All keys and their behaviours remain unchanged as in version `1`, except for those listed below.

### Changes from `v1` to `v2`

- `static_site.primary_button` and `static_site.secondary_button` have been replaced with `static_site.buttons`, an array of button objects.
- Version is now specified using the `$schema` field instead of `@metadata_file_version`.

!!! note "Recommendation and Compatibility"

    For new build targets, it is recommended to use the `v2` schema with the `$schema` field.

    The build pipeline will automatically parse v1 formats and convert them to v2 internally,
    so existing build targets using v1 schema will continue to work without any changes.

### `$schema`

- **Required**: Yes
- **Description**: Reference to the JSON schema for validation and IDE support. Must be set to the v2 schema URL.
- **Type**: `string`
- **Value**: `"https://hku.jacobshing.com/statics/schemas/v2.json"`

### ~~`@metadata_file_version`~~ **[Deprecated]**

!!! warning "Deprecated Field"

    The `@metadata_file_version` field is deprecated in v2 and replaced by the `$schema` field.
    
    For backward compatibility, you may still include this field (set to `"2"`), but it is no longer
    required or recommended for new files. The build pipeline will prioritize `$schema` for version detection.

- **Required**: No (deprecated)
- **Description**: Legacy field for specifying metadata schema version. Replaced by `$schema` in v2.
- **Type**: `string`
- **Value**: `"2"` (if present)

### `static_site.buttons`

- **Description**: An array of button objects that define the buttons to be displayed on the static site.
Each button object must conform the structure described below.
- **Type**: `array` of `object`
- **Default**: `null`

!!! note "Default Value Behaviour"

    If the `static_site.buttons` key has the default value of `null`, the build pipeline will
    automatically create two buttons: a primary "Download" button and a secondary "View Source" button,
    with the same properties as in the v1 schema.

    However, if you wish to display no buttons, you must explicitly set `static_site.buttons` to an empty array `[]`.

### `static_site.buttons[i].{index}`

- **Description**: The index of the button in the array. Used to determine the order of buttons.
- **Type**: `integer`
- **Default**: `0`

!!! warning "Default Index Undefined Behaviour"

    By default, all buttons have an index of `0`, which means their order can be inconsistent between builds.
    You should explicitly set **distinct** indices for each button to ensure a consistent order.

### `static_site.buttons[i].{is_primary}`

- **Description**: Whether the button is a primary button or not.
- **Type**: `boolean`
- **Default**: `false`

!!! note "Multiple Primary Buttons and Ordering"

    It is allowed to have multiple primary buttons.
    
    The order of buttons is soley determined by their `index` values, regardless of whether they are primary or secondary.
    Buttons with lower index values are displayed before buttons with higher index values.

### `static_site.buttons[i].{text}`

- **Required**: Yes
- **Description**: The text to be displayed on the button. You must explicitly set this value for each button.
- **Type**: `string`

### `static_site.buttons[i].{icon}`

- **Description**: Defines the icon and href of the button.
- **Type**: `string`
- **Default**: `null` (no icon)
- **Accepted Values**: Any valid icon name specified in the [Material for MkDocs documentation](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/),

### `static_site.buttons[i].{href}`

- **Required**: Yes
- **Description**: The URL to be linked to when the button is clicked. You must explicitly set this value for each button.
- **Type**: `string`

### Other Keys

Refer to the next section for the keys carried over from v1 without changes.

## Schema (v1)

The following sections describe the keys available in the `metadata.json` file for schema version `1`.

### `@metadata_file_version`

- **Required**: Yes
- **Description**: The version of the metadata file schema. Set to `"1"` for this version.
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

!!! warning "Non-File Targets"

    If the build target does not produce a file (e.g., only a web page),
    you must create a dummy file with the name "NON_FILE_TARGET" in the source directory of the target.
    You must also point the `build.output_file` to this dummy file.

### `build.no_latex`

- **Description**: If set to `true`, the build pipeline will skip the LaTeX installation and proceed to the commands
specified in `build.prebuild_command`, `build.build_command`, and `build.postbuild_command` directly.
This is useful for targets that do not require LaTeX to build, such as HTML or Markdown documents.
- **Type**: `boolean`
- **Default**: `false`

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

### ~~`build.miktex_package_file`~~ **[Deprecated]**

!!! warning "Deprecated Key"

    The key `build.miktex_package_file` has been deprecated and will be removed in the future.
    TeX package hashing is now handled automatically by the python script, and is available as
    a runtime dynamic computed key `computed.tex_pkg_hash`.

    This key should no longer be used in new build targets.

    Although TeX packages are now automatically resolved, it is still a **mandatory code practice**
    to separate all `\usepackage` commands into a single file named `packages.tex` in the source directory.

!!! failure "Not Applicable to v2 Schema"

    This key is not applicable to the v2 schema and should not be used in `metadata.json` files
    that use the v2 schema.

- ~~**Description**: Specifies the `.tex` file that contains all the `\usepackage` commands for the target.~~
~~This file is used to generate a hash for retrieving the cached LaTeX packages for saving build time.~~
- ~~**Type**: `string`~~
- ~~**Default**: `packages.tex`~~

!!! note "Creating a `packages.tex` File"

    While `\usepackage` commands are not required to be in a separate file for
    general LaTeX documents, it is **mandatory** for documents in this repository
    to separate them into a single file for the purpose of caching LaTeX packages.

### `static_site.description`

- **Description**: A short description of the target, used in the static site.
- **Type**: `string`
- **Default**: `"-"` (a hyphen)

### `static_site.meta_description`

- **Description**: A short description of the target, used in the HTML meta tags for SEO purposes.
If not specified, the tag will be `"Download [BUILD_TARGET] for free - [DESCRIPTION]"`,
where `[BUILD_TARGET]` is the name of the build target, and `[DESCRIPTION]` is the value of `static_site.description`.
- **Type**: `string`
- **Default**: `null`

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

### `static_site.pdf_viewer`

- **Description**: Where the PDF viewer (if available) should be displayed on the details page.
- **Type**: `string`
- **Accepted Values**: Any of the following:

    - `"at_head"`: Display the PDF viewer directly after the authors and the two buttons (at the head of the custom markdown page).
    - `"at_footer"`: Display the PDF viewer after the end of the custom markdown page.
    - `"at_tag"`: Insert the PDF viewer at the `<!-- % PDF_VIEWER % -->` tag in the custom markdown page.
    - `"hidden"`: Do not display the PDF viewer at all.
    
- **Default**: `"at_head"`

!!! note "PDF Viewer Placement"

    **General Reminder**: The PDF viewer will be displayed if and only if the output file is a PDF.
    When the output file is not a PDF file, setting this key will have no effect.

    **When using the `at_tag` option**: The custom markdown file must contain exactly one `<!-- % PDF_VIEWER % -->` tag (case-sensitive).
    Missing tag or duplicated tags will cause the build pipeline to fail.

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
- **Accepted Values**: Any valid icon name specified in the [Material for MkDocs documentation](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/),
or empty string for no icon.

### `static_site.{primary_button, secondary_button}.href`

- **Description**: The URL to be linked to when the primary/secondary button is clicked.
- **Type**: `string`
- **Default**: `"https://hku.jacobshing.com/files/[BUILD_TARGET]/[OUTPUT_FILE]"` for primary, `"https://github.com/ShingZhanho/HKU-Notes/tree/master/src/[BUILD_TARGET]"` for secondary,
where `[BUILD_TARGET]` is the name of the build target, and `[OUTPUT_FILE]` is the value of `build.output_file`.

### `authors`

- **Description**: A list of authors for the target. Each author must be a string, whose value is defined in `/site/docs/statics/authors/authors.json`.
- **Type**: `array` of `string`
- **Default**: `["jacob_shing"]` (an array containing a single string `jacob_shing`)
- **Accepted Values**: Any string that is a valid key in the `/site/docs/statics/authors/authors.json` file, or a pseudo-author.

!!! note "Pseudo-Authors"

    In addition to the authors defined in the `authors.json` file, you can also use pseudo-authors
    to control the behaviour and display of authors.

    The following pseudo-authors are supported:

    - `@unknown`: Represents an unknown author. This will display as "Unknown Author" on the static site.
        Defining more than one `@unknown` in the authors list will display a plural form "Unknown Authors".
        
    - `@do_not_sort`: Preserves the order of authors as defined in the list.
        By default, authors are sorted alphabetically by their `display_name`, with the main author always appearing first,
        and unknown authors appearing at the end. Using this pseudo-author will disable sorting for non-main authors and non-unknown authors.

!!! note "Main Author and Coauthors"

    Add an exclamation mark (`!`) before the author string to indicate that this is the main author of the target.
    At most one author can be the main author. Having more than one main author will cause the build pipeline to fail.

    If no main author is specified, the first author in the alphabetical order will be treated as the main author.

    All other authors are sorted in alphabetical order according to their `display_name` in the definition.

Also refer to the [syntax reference for `authors.json`](./authors.json.md) for the details about
how to define authors in the `authors.json` file.

!!! note "Computed Keys"

    The following keys are computed dynamically at runtime by the metada parser.
    Their values are not stored in the `metadata.json` file, but can be accessed
    through the **methods** in the `Metadata` class.

    Specifying these keys in the `metadata.json` file will have no effect.

### `computed.tex_pkg_hash`

- **Description**: The hash of the TeX packages used in the target.
This is computed by traversing the `\usepackage`, `\RequirePackage`, and `\documentclass` commands
in all `.tex` files in the source directory of the target. When `build.no_latex` is `true`, or when
`computed.is_alias` is `true`, this value will be `"0"`.
- **Type**: `string`
- **Access By**: `Metadata.computed__tex_pkg_hash()`

### `computed.is_alias`

- **Description**: Whether the target is an alias to another target. Evaluates to `true` if `static_site.alias_to` is not `null`,
`false` otherwise.
- **Type**: `boolean`
- **Access By**: `Metadata.computed__is_alias()`

### `computed.is_non_file_target`

- **Description**: Whether the target is a non-file target. Evaluates to `true` if `build.output_file` is `"NON_FILE_TARGET"`,
`false` otherwise.
- **Type**: `boolean`
- **Access By**: `Metadata.computed__is_non_file_target()`