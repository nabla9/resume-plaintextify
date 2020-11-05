import re
import os


def plaintextify_letter(file):
    """
    Takes a .tex file as input and outputs a plaintext-formatted cover letter (for copy and paste into a field).

    This function applies sub-functions remove_texenvs, remove_functions, adjust_spaces, and make_bullets.
    :param file: An input .tex file
    """
    with open(file, 'r') as tex:
        (body,) = re.findall(r'%pt_begin\n?(.*)%pt_end', tex.read(), re.DOTALL)
    body = remove_texenvs(body)
    body = remove_functions(body)
    body = adjust_spaces(body)
    body = make_bullets(body)

    new_file = re.sub(r'(.*).tex', r'\1.txt', file)
    with open(new_file, 'w') as txt:
        txt.write(body)


def remove_texenvs(letter):
    """
    Strips a string of tex environments.

    This function removes opening/closing environments in the following way:
    \begin{equation*}
        2x+3+5                  becomes         2x+3+5
    \end{equation*}

    :param str letter: An input text string.
    :return str: A string with opening/closing tex environments stripped.
    """
    subs = 1
    while subs != 0:
        letter, subs = re.subn(r'\\begin{([^\n]*?)}(.+?)\\end{\1}', r'\2', letter, flags=re.DOTALL)  # TODO: work from inside out
    return letter


def adjust_spaces(letter):
    """
    Converts linebreaks to single spaces and newlines to new paragraphs.

    This function assumes a .tex document is formatted for Git version control, with each sentence on its own line.
    It does the following:
    1. Converts linebreaks (with any padding spaces) into a single space;
    2. Converts newlines (with any padding linebreaks and spaces) into a double newline;
    3. Converts \\ (with any space padding) into a single newline.

    :param str letter: An input text string.
    :return str: A string with spaces adjusted into block-paragraph format.
    """
    # Single spaces within paragraphs
    letter = re.sub(r'( )*(\n)( )*', ' ', letter)
    # Paragraph breaks
    letter = re.sub(r'[ \n]*\\newline[ \n]*', r'\n\n', letter)
    # Single line breaks
    letter = re.sub(r'[ \n]*\\\\[ \n]*', r'\n', letter)

    def convert_skip(match_obj):
        """
        Converts vertical space environment into an appropriate number of newlines.

        Each \baselineskip is converted into the same number (+1) of linebreaks.

        :param re.Match match_obj: A match object from the module 're'.
        :return str: A string with baselineskips converted.
        """
        coeff = 2 if not match_obj[1] else int(match_obj[1])+1
        return '\n'*coeff
    # Baseline skips
    letter = re.sub(r'[ \n]*\\vspace{(\d*)\\baselineskip}[ \n]*', convert_skip, letter)
    return letter


def make_bullets(letter):
    """
    Converts each item to a plaintext bullet indicated by an asterisk.

    :param str letter: An input text string.
    :return str: A string with bullets converted.
    """
    return letter.replace(r'\item ', '\n* ')


def remove_functions(letter):
    """
    Strips LaTeX functions of the form \fun{thing}.

    Functions are stripped and thing is returned instead, *although* \textsc function returns an all-caps string.

    :param str letter: An input text string.
    :return str: A string with functions removed.
    """
    def smallcaps_to_upper(match_obj):
        return match_obj[1].upper()
    # Convert smallcap-case to upper
    letter = re.sub(r'\\textsc{(\w+?)}', smallcaps_to_upper, letter)
    # Remove other commands (but not vspace)
    letter = re.sub(r'\\(?!vspace)\w+?{(.*?)}', r'\1', letter)  # TODO: just split up vspace component of that function
    return letter


# Allows this module to be run as a script rather than imported
if __name__ == '__main__':
    tex_paths = [path for path in os.listdir('.') if path[-4:] == '.tex']
    if not tex_paths:
        print('No tex file found...')
    elif len(tex_paths) == 1:
        print('Found single file! converting %s' % tex_paths[0])
        plaintextify_letter(tex_paths[0])
    else:
        print('Found .tex files! Input number to convert.')
        for idx, path in enumerate(tex_paths):
            print('%s: %s' % (idx, path))
        choice = int(input('Choice:'))
        plaintextify_letter(tex_paths[choice])
