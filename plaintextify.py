import re
import os


def plaintextify_letter(file):
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
    subs = 1
    while subs != 0:
        letter, subs = re.subn(r'\\begin{([^\n]*?)}(.+?)\\end{\1}', r'\2', letter, flags=re.DOTALL)  # TODO: work from outside in
    return letter


def adjust_spaces(letter):
    # Single spaces within paragraphs
    letter = re.sub(r'( )*(\n)( )*', ' ', letter)
    # Paragraph breaks
    letter = re.sub(r'[ \n]*\\newline[ \n]*', r'\n\n', letter)
    # Single line breaks
    letter = re.sub(r'[ \n]*\\\\[ \n]*', r'\n', letter)

    def convert_skip(match_obj):
        coeff = 2 if not match_obj[1] else int(match_obj[1])+1
        return '\n'*coeff
    # Baseline skips
    letter = re.sub(r'[ \n]*\\vspace{(\d*)\\baselineskip}[ \n]*', convert_skip, letter)
    return letter


def make_bullets(letter):
    return letter.replace(r'\item ', '\n* ')


def remove_functions(letter):
    def smallcaps_to_upper(match_obj):
        return match_obj[1].upper()
    # Convert smallcap-case to upper
    letter = re.sub(r'\\textsc{(\w+?)}', smallcaps_to_upper, letter)
    # Remove other commands (but not vspace)
    letter = re.sub(r'\\(?!vspace).+?{(.*?)}', r'\1', letter)  # TODO: just split up vspace component of that function
    return letter


if __name__ == '__main__':
    # pick file to be first encountered if plaintextify run as a script
    for path in os.listdir('.'):
        if path[-4:] == '.tex':
            tex_file = path
            break
    print('Found file! converting %s' % tex_file)
    plaintextify_letter(tex_file)
