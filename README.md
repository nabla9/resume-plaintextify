# resume-plaintextify: a tool for copy-pasting LaTeX cover letters
## What is it?
The module `plaintextify.py` converts  a cover letter for copy-and-paste into a plaintext submission field.
This module's functionality is rather basic compared to tools like Pandoc but lightweight and tailored to my CV style.

## Installation
Required packages are in `requirements.txt`.
These can be installed by running `pip3 install -r requirements.txt` (Python 3).

## Main components
### Functions
The file `plaintextify.py` contains all the functions needed.
The main function `plaintextify_letter(file)` calls several subfunctions:
1. `remove_texenvs`: strips tex environments of the form `\begin{env}`,`\end{thing}`;
1. `remove_functions`: strips escaped functions of the form `\fun{thing}`;
1. `adjust_spaces`: puts document in block-paragraph format; 
1. `make_bullets`: converts an `itemize` block with nested `\item`s into a plaintext list with `*` bullets.

### Required input
It is assumed that the user marks the LaTeX block they want to convert in their file.
Only code nested within a `%pt_begin` and `%pt_end` (on lines immediately before and after code to convert) will be used.

Additionally, single `\n` line breaks within the LaTeX code will be converted to different sentences within a paragraph.
A double break or `\newline` will be converted to a new paragraph. 
Refer to `sample.tex` for an example of this formatting.

## Sample
This example uses `sample.tex` for conversion. 
With `plaintextify.py` in the same directory as `sample.tex`, call the converter function:

    import plaintextify as pt
    pt.plaintextify_letter('sample.tex')

This will create the plaintext file `sample.txt` in the same directory for copying and pasting directly.
 