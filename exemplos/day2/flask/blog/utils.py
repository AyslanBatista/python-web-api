import re
import unicodedata


def slugify(title: str) -> str:
    # Remove acentos (ex: ç -> c, é -> e)
    title = (
        unicodedata.normalize('NFKD', title)
        .encode('ascii', 'ignore')
        .decode('utf-8')
    )

    # Remove caracteres especiais
    title = re.sub(r'[^a-zA-Z0-9\s-]', '', title)

    # Substitui espaços e underscores por hífen
    title = re.sub(r'[\s_]+', '-', title)

    return title.lower().strip('-')
