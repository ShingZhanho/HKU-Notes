## About This Document

This is a comprehensive collection of past paper solutions for the course ENGG1310 (Electricity and Electronics) covering exams from 2023 to 2024.
The solutions are organised by year, with an index for you to query easily by topic.

!!! info "Change of Syllabus"

    It has been observed that the examination format and difficulty have greatly changed since 2023.
    While the reason behind this is unknown, it is suspected that the syllabus has been changed.
    There is currently no plan to include solutions for exams before 2023, but if you are interested in contributing, please open a pull request.

!!! warning "Work in Progress"

    These past paper solutions are still being worked on.
    Many questions are still missing.
    Some solutions may be incomplete or incorrect.
    If you spot any errors, or if you are interested in contributing, please open a pull request.

### Preview of the File

<!-- % PDF_VIEWER % -->

## For Contributors

A set of LaTeX macros have been defined to make it easier to automate solution indexing, even for beginner LaTeX users.

To start a new set of exam paper, create a new file under `solutions/` with the name format `year-month.tex`. In the file, start with:

```latex
\startYear{year month} % e.g. \startYear{2024 May}

\subsection*{Section A -- Multiple-choice Questions}
\begin{multicols*}{2}

% questions go here

\end{multicols*}
```

Then, for each question, do:

```latex
\startQwTags{year}{month}{question number}{tags}
    % \startQwTags => start question with tags
    % This starts a question with specified tags (topics).
    % e.g., \startQwTags{2024}{May}{Q1}{\tgElectronics \tgElectronicsSemiconductor}
```

All the available tags are defined in the `tags.tex` file.
You can also define other tags if necessary, follow the instructions in the file.
Each question should have at least one primary tag.
If a question does not need to be tagged, do this instead:

```latex
\startQuestion{year}{month}{question number}
    % This starts a question without tags.
    % The question will not have a topic, so it will not appear in the by-topic index.
    % e.g., \startQuestion{2024}{May}{Q1}
```

!!! info "`question` environment"

    You do not need to wrap the questions in the `question` environment.
    The entire file is already wrapped in a `question` environment in `solutions/solutions.tex`.
    Nested `question` environments will mess up the indexing and layout.

Then, write the solution inside the `solution` environment, right after the question:

```latex
\startQwTags{2024}{May}{Q1}{\tgElectronics \tgElectronicsSemiconductor}
\begin{solution}
    \mcqAns{C}

    Some explanation.
\end{solution}
```

For MCQs, you can use the `\mcqAns{option}` command to indicate the correct answer, and then write an explanation for it.
For non-MCQs, you can write the solution as you normally would.

Finally, import this file in `solutions/solutions.tex` by adding the line:

```latex
\begin{questions}
    % ... other imports
    \input{solutions/2024-may.tex}
\end{questions}
```

Please arrange the imports in chronological order, with the most recent exam paper at the top.