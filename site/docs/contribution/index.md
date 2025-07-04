---
description: "Learn how to contribute to the HKU Notes project, including guidelines for using the automated compilation pipeline, contributing new materials, and more."
---

# Contribution Guide

Thank you for being interested in contributing to the HKU Notes project! This article will walk you through the
process of how all the materials are compiled from source and deployed on GitHub Pages. Understanding this process
is crucial for contributing new materials or improving existing ones.

## Automated Compilation Pipeline

All the source codes for generating the notes are stored in the `/src` directory. Whenever there is a push to the `master`
branch, GitHub Actions will be triggered (defined in the
[`build-and-deploy.yml`](https://github.com/ShingZhanho/HKU-Notes/blob/master/.github/workflows/build-and-deploy.yml) file).
Here's what happens in the pipeline:

### 1. Resolve Build Targets

??? question inline end "What is a build target?"

    Generally, a build target is a PDF document that will be generated from the source code.
    For example, the file `COMP2120-Notes.pdf` is the product of the build target `COMP2120-Notes`.

The pipeline needs to know what are the targets to build. All build targets are defined in the file `/build/build-targets.txt`,
and are resolved by the script `/build/resolve-targets.py`.

`build-targets.txt` uses its own unique but simple syntax and provides shortcuts for defining targets in a tree-like structure.
You should read the [syntax reference for `build-targets.txt`](./syntax-reference/build-targets.txt.md) before editing it.

### 2. Resolve Target Metadata

Each build target **MUST** have a `metadata.json` file in its source directory, i.e., `/src/[BUILD_TARGET]/metadata.json`.
This file contains information about how the target should be built, how it should be displayed and presented on the website,
and other information for changing the build behaviour.

Most importantly, it specifies the commands to run before, for, and after building the target. The pipeline is mainly designed
to build PDF documents from LaTeX source code, but with the customisable commands, you can also use this pipeline to include
other types of files.

You should refer to the [syntax reference for `metadata.json`](./syntax-reference/metadata.json.md) for the details about
what information can you include in the file.

### 3. Source Code Checksum

!!! note inline end "Overriding Checksum Behaviour"

    If the head commit message contains `@force-rebuild`, the build target will always be rebuilt regardless of the checksum.

To avoid unnecessary rebuilds, the GitHub Action will obtain the checksum of all the files under the `/src/[BUILD_TARGET]` directory.
This value is compared with the previous build's checksum (can be accessed from
`https://shingzhanho.github.io/HKU-Notes/files/[BUILD_TARGET]/src-checksum.txt`). If the checksum is the same, the build will be skipped
and the previous output will be reused.

### 4. Build the Target

After setting up the environment according to instructions in `metadata.json`, the pipeline will run the commands specified in the file,
and generate the output files.

### 5. Generate the Website and Deploy

The pipeline will then generate the website using the output files and metadata, and deploy it to GitHub Pages.

## Steps for Creating New Materials

Now that you have a basic understanding of how the pipeline works, here are the steps to create new materials:

1. **Define a New Build Target**: Add a new entry in the `/build/build-targets.txt` file for your new material.
   - Use the syntax defined in the [syntax reference for `build-targets.txt`](./syntax-reference/build-targets.txt.md).
2. **Create the Source Directory**: Create a new directory under `/src/[NEW_BUILD_TARGET]` for your new material.
    The directory name must match the build target name you defined in the previous step.
3. **Create `metadata.json`**: Create a `metadata.json` file in the new source directory.
   - Use the syntax defined in the [syntax reference for `metadata.json`](./syntax-reference/metadata.json.md).
4. **Add Source Files**: Add the source files for your new material in the new source directory.
    Most importantly, if you are adding a LaTeX document, you MUST separate all the `\usepackage` commands into a separate file
    called `packages.tex` in the source directory.
5. **Commit and Push**: Ensure your sources compile successfully on your local machine, then push to the remote and
    create a pull request.

## Contributing to Existing Materials

If you spot an issue or want to improve existing materials, you can simply fork the repository and modify the source files.
When you finish, create a pull request with your changes.

## Contributing to the Compilation Pipeline

You may also contribute to the compilation pipeline itself. The pipeline is implemented with YAML (GitHub Actions), Bash Scripts, and Python Scripts.
You can find those scripts in the `/build` directory. It is recommended to test the pipeline in your forked repository, which would require you to
set up GitHub Actions in your fork and change all the URLs in the scripts to point to your forked repository.

!!! warning "Deploying to GitHub Pages"

    If you are testing the pipeline in your forked repository, we kindly request that you remove the deployment step in the
    `build-and-deploy.yml` file and **NOT** deploy to GitHub Pages, as this will create duplicated content on the web
    and cause confusion for users.

    **Please also note that failure to follow this guideline may result in copyright infringement.**

## Attributing Your Contributions

If you are contributing to this project, we would like to attribute your contributions.
To do so, please refer to the [syntax reference for `authors.json`](./syntax-reference/authors.json.md) to add your information,
and then refer to the [`authors` field in `metadata.json`](./syntax-reference/metadata.json.md#authors) to add your name to the build target.

Of course, whether you want to remain anonymous or not is entirely up to you.