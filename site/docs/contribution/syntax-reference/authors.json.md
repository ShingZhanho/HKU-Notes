---
description: This document provides a syntax reference for the `authors.json` file used in the HKU Notes project.
---

# Syntax Reference for `authors.json`

The `authors.json` file is found under the `/site/docs/statics/authors/` directory.
It contains information about the authors of the documents in the HKU Notes project.

Each author is represented as a JSON object, with its unique identifier as the key.

!!! warning "Naming Convention for Author Identifiers"

    Identifiers with a leading at sign (`@`) are reserved for system use.
    While they will not cause issues in the build process, pull requests that use these identifiers will not be accepted.

Each author object must define all of the following fields:

## `display_name`

- **Description**: The name of the author as it should be displayed.
- **Type**: `string`
- **Example**: `"John Appleseed"`

## `avatar`

- **Description**: The URL of the author's avatar image.
- **Type**: `string` or `null`
- **Example**: `"https://example.com/avatar.jpg"`

Authors without a hosted avatar can place their avatar image in the `/site/docs/statics/authors/` directory,
and reference it using `https://shingzhanho.github.io/hku-notes/statics/authors/[avatar_filename]`. Or,
if they wish, leave this field as `null` to use the default avatar.

## `href`

- **Description**: A URL to the author's profile or homepage. Leave this field as `null` if the author does not wish to provide a link.
- **Type**: `string` or `null`
- **Example**: `"https://example.com/profile"`

# Example

```json
{
    "john_appleseed": {
        "display_name": "John Appleseed",
        "avatar": "https://example.com/avatar.jpg",
        "href": "https://example.com/profile"
    }
}
```
