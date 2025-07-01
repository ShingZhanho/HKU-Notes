---
description: Learn the syntax for defining build targets in the `build-targets.txt` file, which is used to specify what documents to compile in the HKU Notes project.
---

# Syntax Reference for `build-targets.txt`

The `build-targets.txt` file is used to define the build targets for the HKU Notes project. It uses a simple syntax to specify
the documents to be compiled.

## Syntax Overview

Consider the following snippet:

``` text title="Example build-targets.txt"
# COMP2120 - Computer Organisation
COMP2120-
    Notes
    Cheatsheet

# MATH1851 - Calculus & ODE
MATH1851-
    Notes
    Assignment
        1
        2
```

This snippet defines 5 build targets: `COMP2120-Notes`, `COMP2120-Cheatsheet`, `MATH1851-Notes`, `MATH1851-Assignment1`, and `MATH1851-Assignment2`.

Notice that the build targets are defined in a tree-like structure, where each line represents a level of hierarchy.
Each level **MUST** be indented with **TABS** (not spaces).

Comments are allowed and start with a `#` character. They **MUST** be placed at the beginning of a line.

Each defined build target is a concatenation of all the parent nodes and the current node. Note that hyphens are not
automatically added to the build target names, so you should include them if you want them to be part of the name.

All defined build targets must have a matching directory in the `/src` directory, i.e., `/src/COMP2120-Notes`, `/src/COMP2120-Cheatsheet`.
etc. The build pipeline will look for files to build in these directories. Since target names are for direcotories, use of spaces
and special characters is not recommended and not tested.

### Repeated Build Targets

If targets of the same name are defined, the resolver will only produce one build target with that name.
For example, if the following snippet is used:

``` text title="Repeated Build Targets"
# COMP2120 - Computer Organisation
COMP2120-
    Notes
COMP2120-Notes
```

Only one build target `COMP2120-Notes` will be produced.

### Separated Trees

Separated trees structures will be merged automatically and are allowed.
For example, the following snippet:

``` text title="Separated Trees"
FREN1001-
    Notes
    Writing1

# ... some other targets ...

FREN1001-
    Writing2
```

will produce the build targets `FREN1001-Notes`, `FREN1001-Writing1`, and `FREN1001-Writing2`.
Please be careful when using this feature, as it may lead to confusion if the same target is defined in multiple places.