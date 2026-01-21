This "document" is in fact a link to the GitHub repository of our group project.
The group project has received a grade of 19.3 out of 20.


!!! tip "Important Notice!"

    There are a few things that you should bear in mind before exploring the repository
    or start working on your own group project:

    1. The course has specifically required you to create your C++ project with Makefile as the build system.
    This project has observed such requirement in its original version. After submission deadline, this project
    has been modified to use CMake as the build system. To study how the Makefile version was implemented,
    please **switch to the tag `v1.0.0`**. ([Learn How](#how-to-switch-to-the-v100-tag-on-github))

    2. Several concepts or skills (Object-Oriented Programming, Multi-threading, etc.) used
    in this project are beyond the scope of this course. It is highly recommended that you do not attempt to
    create your project like this one if you are just a beginner to programming. Focus on applying
    the skills **which have been taught in this course**.

    3. It is recommended that you clone and build the project on the HKU CS Linux servers, as it was designed
    mainly for that environment. It may also work on other Linux distributions or macOS.
    You must build the project from the `v1.0.0` tag as CMake is not available on the HKU CS Linux servers.
    ([Learn More](#how-to-switch-and-build-from-the-v100-tag))

    4. It is known that the programme does not work properly on Windows. This will not be fixed as the project
    requirements did not ask so.

## Guide

### How to switch to the `v1.0.0` tag on GitHub

1. Under the repository name, click on the branch name (e.g. `master` by default).
2. In the pop-up menu, select the "Tags" tab.
3. Select `v1.0.0` from the list.
4. You will be browsing the repository at the state of the `v1.0.0` tag.

### How to switch and build from the `v1.0.0` tag

1. Clone the repository if you haven't already:
   ```bash
   git clone https://github.com/ShingZhanho/ENGG1340-Project-25Spring.git
   ```
2. Change directory to the cloned repository:
   ```bash
   cd ENGG1340-Project-25Spring
   ```
3. Switch to the `v1.0.0` tag:
   ```bash
   git checkout v1.0.0
   ```
4. Build the project (please follow the instructions in the `README.md` file).
Ensure you are reading the `README.md` file in the `v1.0.0` tag for the correct build instructions.

## Binaries for Release v1.0.0

You can download the pre-compiled binary file for Release v1.0.0 directly, using the button above.
The binaries were built for Ubuntu 24.04 x86_64 systems.
Other Linux/Unix distributions or macOS should have no issues running the binaries as well.
Refer to the above section on how to build from source.

!!! failure "Support for Microsoft Windows"

   Due to unknown reasons, the programme does not work properly on Microsoft Windows.
   Currently, there is no plan to fix this issue as the project requirements did not ask for Windows support.