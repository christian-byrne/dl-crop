import os


def to_figlet(msg, font=None, justification=None, size=None):
    '''
    font: banner, term, smslant, smshadow, smscript, slant, shadow,
          script, mnemonic, mini, lean, ivrit, digital, bubble,
          block, big, all (print in every font)
    justification: close, spaced, right, left, center, paragraph
    size: small, big (only works with default font)
    '''
    font_list = ["banner", "term", "smslant", "smshadow", "smscript", "slant", "shadow", "small",\
        "script", "mnemonic", "mini", "lean", "ivrit", "digital", "bubble", "block", "big", "all"]
    cm2 = "figlet "
    
    # Font and Size
    fontC = " -f standard"
    if font:
        fontC = " -f " + str(font)
    if font == True and font not in font_list:
        fontC = " -f big"
    if font and size:
        fontC = " -f " + str(size)
        if str(size) not in font_list:
            fontC = " -f big"
    if size and not font:
        if str(size) not in font_list:
            fontC = " -f big"
        else:
            fontC = " -f " + str(size)

    # Justification
    if justification:
        j = str(justification[:1])
        i = 0
        while not str(justification)[i:i+1].isalpha() and i < len(str(justification)):
            j = str(justification)[i:i+1]
            i += 1
        if j == "s":
            j = "k"
        if j == "c":
            j = "s"
        jc = " -" + j
        if j not in ["r", "c", "s", "S", "k", "l"]:
            jc = " -c"
        justification = " -" + str(justification[:1])
    if not justification:
        jc = " -c"

    cm2 += jc + fontC + " " + str(msg)  
    if font == "all":
        cm2 = "showfigfonts " + str(msg)
    os.system(cm2)