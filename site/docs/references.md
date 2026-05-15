# Technical References

This page groups together all technical references that are useful for understanding the build pipeline and the codebase.
See the categories to navigate quickly to the relevant reference.

## About Contributing to HKU Notes

You may check the [contributing guidelines](contribution/index.md) for community guidelines.

## About Document Status

Each document has a status badge that provides important information about the document, e.g. whether it is a work in progress, whether it is obsolete, etc.
The meaning of each badge is explained in the [document status reference](downloads/document-status.md).

## About the Syntax of Configuration Files for the Build Pipeline

The build pipeline and the website generation process rely on several configuration files.
They all serve different purposes and have a custom syntax.

### `authors.json`

This is where you define authors of the documents.
When you adds documents to this website, you might want to credit the authors.
See the [authors.json syntax reference](contribution/syntax-reference/authors.json.md) for more details.

### `build-targets.txt`

This file tells the build pipeline which documents to build.
It is a simple text file with some indentation requirements.
Checkout the [build-targets.txt syntax reference](contribution/syntax-reference/build-targets.txt.md) for more details.

### `metadata.json`

This file is necessary for each build target.
It tells the build pipeline how to build the document, where to find the built artefacts, etc.
It also controls the content on the description page of the document on the website.
It comes with two schema versions, v1 (deprecated) and v2 (current).
See the [metadata.json syntax reference](contribution/syntax-reference/metadata.json/index.md) for more details.