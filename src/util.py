
def commasep_formatted_list(data, formatstring):
    l = ""
    for k in data:
        l += ", " + formatstring.format(k)
    return l[2:]
