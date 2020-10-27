import re


def plaintextify_letter(file):
    with open(file, 'r') as tex:
        (body,) = re.findall(r'%pt_begin(.*)%pt_end', tex.read(), re.DOTALL)
    body = remove_texenvs(body)
    body = remove_functions(body)
    body = adjust_spaces(body)
    body = make_bullets(body)
    return body


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
    letter = re.sub(r'\\vspace{(\d*)\\baselineskip}', convert_skip, letter)
    return letter


def make_bullets(letter):
    return re.sub(r'\\item +', r'\* ', letter)


def remove_functions(letter):
    def smallcaps_to_upper(match_obj):
        return match_obj[1].upper()
    # Convert smallcap-case to upper
    letter = re.sub(r'\\textsc{(\w+?)}', smallcaps_to_upper, letter)
    # Remove other commands
    letter = re.sub(r'\\.+?{(\w+?)}', r'\1', letter)
    return letter


