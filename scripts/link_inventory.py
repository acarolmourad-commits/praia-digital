"""Extract real HTML links and resolve site URLs without executing JavaScript."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ORIGIN = 'https://praia.digital/'
HOSTS = {'praia.digital', 'www.praia.digital'}

class Links(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.base = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'base':
            if self.base is None:
                self.base = attrs.get('href')
            return
        for key in ('href', 'src'):
            value = attrs.get(key)
            if value and '${' not in value and '{{' not in value:
                self.links.append(value.strip())

def classify(link, page, base=None):
    if not link or link.startswith('#'):
        return 'skip', link
    page_url = urljoin(ORIGIN, page)
    url = urljoin(urljoin(page_url, base) if base else page_url, link)
    try:
        parsed = urlsplit(url)
        if parsed.scheme not in ('http', 'https'):
            return 'skip', url
        if parsed.hostname not in HOSTS:
            return 'external', url.split('#', 1)[0]
        return 'internal', unquote(parsed.path)
    except ValueError:
        return 'invalid', link

def exists(path, root=Path('.')):
    root = root.resolve()
    candidate = (root / path.lstrip('/')).resolve()
    if not candidate.is_relative_to(root):
        return False
    # A directory exists only as a page when it contains an index.
    return any(p.is_file() for p in (candidate, Path(str(candidate) + '.html'), candidate / 'index.html'))

def inspect_links(text, page, root=Path('.')):
    parsed = Links(text)
    broken, external = [], []
    for link in dict.fromkeys(parsed.links):
        kind, target = classify(link, page, parsed.base)
        if kind == 'external':
            external.append(target)
        elif kind == 'invalid' or (kind == 'internal' and not exists(target, root)):
            broken.append({'page': page, 'link': link})
    return broken, external
