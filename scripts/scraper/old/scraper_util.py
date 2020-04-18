def stringify_soup(soup):
    if soup.string is not None:
        return soup.string

    text = ''
    for child in soup.children:
        text += stringify_soup(child)

    return text