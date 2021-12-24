from typing import List
def split(text: str, sep: str) -> List[str]:
    parts = []
    index = 0
    while index < len(text):
        part = ''
        while text[index] != sep or index < len(text):
            part += text[index]
            index += 1
        if part != '':
            parts.append(part)
        index += 1
    return parts

print(split('xa', 'x'))