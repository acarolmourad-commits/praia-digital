"""Prepare Praia Digital's own contact links in the Pages artifact."""
import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import parse_qs, quote, urlsplit

EMAIL = 'comercial@praia.digital'
OWN_URL = r'(?:https?:)?//wa\.me/(?:55)?11954346288(?![0-9A-Za-z_/])'
OWN = re.compile(OWN_URL, re.I)
# Several older UTM rewrites left the text parameter outside the href's quotes.
MALFORMED = re.compile(r'(' + OWN_URL + r'''\?[^"'<>]*?)"text=([^"<>]*)"''', re.I)
HREF = re.compile(r'''(?P<prefix>\bhref\s*=\s*)(?P<q>["'])(?P<url>''' + OWN_URL + r'''[^"'<>]*)(?P=q)''', re.I)
ANCHOR = re.compile(r'<a\b(?P<attrs>[^<>]*?)>(?P<label>(?:(?!<a\b|</a\s*>).)*?)</a\s*>', re.I | re.S)
BLOCK = re.compile(r'(<!--.*?-->|<script\b[^>]*>.*?</script\s*>|<style\b[^>]*>.*?</style\s*>)', re.I | re.S)
FORM = re.compile(r'<form\b[^>]*>', re.I)
ACTION = re.compile(r'''\baction\s*=\s*(["'])''' + OWN_URL + r'''[^"']*\1''', re.I)
JS_STRING = re.compile(r'''(?P<q>["'`])(?P<url>''' + OWN_URL + r'''(?:(?!(?P=q))[^\r\n<>])*?)(?P=q)''', re.I)
TARGET = re.compile(r'''\s+target\s*=\s*(["'])_blank\1''', re.I)
COPY_URL = re.compile(OWN_URL + r'''(?:\?[^\s<>"'`]*)?''', re.I)
FORM_SCRIPT = '<script defer src="/js/contact-email-form.js"></script>'
WA_NAME = re.compile(r'\bwhats\s?app\b', re.I)
TITLE = re.compile(r'<title\b[^>]*>(.*?)</title\s*>', re.I | re.S)
SAME_AS = re.compile(r'"sameAs"\s*:\s*\[(?P<items>[^\]]*)\]')
TECHNICAL = {'.git', '.github', 'node_modules', 'tests', '__pycache__'}


def draft(subject, body=None):
    base = 'mailto:' + EMAIL + '?subject=' + quote(subject, safe='')
    return base if body is None else base + '&body=' + quote(body, safe='')


def label(value):
    value = re.sub(r'\b(?:via|pelo|no|por|do|ao)\s+WhatsApp\b', 'por e-mail', value, flags=re.I)
    value = WA_NAME.sub('E-mail', value)
    value = re.sub(r'(?:\+55[ -]*)?\(?11\)?[ -]*95434[ -]*6288', EMAIL, value)
    if value.strip() in ('W', ''):
        return 'E-mail'
    return value


def prepare_anchor(match, subject):
    attrs, contents = match['attrs'], match['label']
    field = HREF.search(attrs)
    if not field:
        return match.group()
    url = html.unescape(field['url'])
    body = parse_qs(urlsplit(url).query).get('text', [None])[0]
    dest = html.escape(draft(subject, body), quote=True)
    attrs = attrs[:field.start()] + field['prefix'] + '"' + dest + '"' + attrs[field.end():]
    attrs = TARGET.sub('', attrs)
    attrs = re.sub(r'''(\b(?:title|aria-label|alt)\s*=\s*)(["'])(.*?)\2''',
                   lambda a: a[1] + a[2] + label(a[3]) + a[2], attrs, flags=re.I | re.S)
    # Replace only text nodes, preserving child markup and identifiers.
    parts = re.split(r'(<[^>]*>)', contents)
    for i in range(0, len(parts), 2):
        if parts[i].strip():
            parts[i] = label(parts[i])
    contents = ''.join(parts)
    if '<svg' in contents.lower() and not re.sub(r'<[^>]*>', '', contents).strip():
        contents = 'E-mail'
    if not contents.strip():
        contents = 'E-mail'
    return '<a' + attrs + '>' + contents + '</a>'


def prepare_form(tag, subject):
    tag = re.sub(r'''\s+(?:method|enctype|target)\s*=\s*(["']).*?\1''', '', tag, flags=re.I)
    action = html.escape(draft(subject), quote=True)
    if ACTION.search(tag):
        tag = ACTION.sub(lambda _: 'action="' + action + '"', tag)
    else:
        tag = re.sub(r'\baction\s*=\s*(["\']).*?\1', '', tag, flags=re.I)
        tag = tag[:-1] + ' action="' + action + '">'
    return tag[:-1] + ' data-pd-email-form method="post" enctype="text/plain">'


def schema_contact(block):
    # A mailbox is a contact address, not an alternative identity in sameAs.
    def clean_array(match):
        try:
            urls = json.loads('[' + match['items'] + ']')
        except ValueError:
            return match[0]
        keep = [u for u in urls if not isinstance(u, str) or not OWN.match(u)]
        return match[0] if len(keep) == len(urls) else '"sameAs": ' + json.dumps(keep, ensure_ascii=False)
    block = SAME_AS.sub(clean_array, block)
    block = re.sub(r'("url"\s*:\s*")' + OWN_URL + r'[^"]*"', r'\1mailto:' + EMAIL + '"', block)
    return (block.replace('pelo WhatsApp: wa.me/5511954346288', 'por e-mail: ' + EMAIL)
            .replace('chame no WhatsApp para atendimento', 'escreva por e-mail para atendimento')
            .replace('Pelo WhatsApp ou formulário na página para atendimento', 'Por e-mail ou pelo formulário na página para atendimento'))


def prepare_script(block, subject):
    if re.search(r'<script\b[^>]*application/ld\+json', block, re.I):
        return schema_contact(block)
    if 'document.getElementById("leadForm")' in block and 'var WA="5511954346288"' in block and 'academy.praia.digital/leads' in block:
        return ''
    block = ANCHOR.sub(lambda m: prepare_anchor(m, subject), block)
    prefix = draft(subject) + '&body='
    def string_url(m):
        raw, q = m['url'], m['q']
        # These forms append an already encoded message to the base URI.
        if raw.endswith('text=') or block[m.end():].lstrip().startswith('+') or 'const base = ' in block[max(0,m.start()-16):m.start()]:
            return q + prefix + q
        if '${' in raw and 'text=' in raw:
            return q + prefix + raw.split('text=', 1)[1] + q
        body = parse_qs(urlsplit(html.unescape(raw)).query).get('text', [None])[0]
        return q + draft(subject, body) + q
    block = JS_STRING.sub(string_url, block)
    if 'mailto:' + EMAIL in block and ('addEventListener' in block or 'handlePageLead' in block or 'abrirVendaWhatsApp' in block):
        # Some mirrored form scripts lost their || tokens during legacy HTML generation.
        block = re.sub(r"(!(?:servico|nome|telefone))\s*(?=!(?:nome|telefone|cidade|tipo))", r"\1 || ", block)
        block = re.sub(r"(\.value(?:\.trim\(\))?)\s+('')", r"\1 || \2", block)
        block = block.replace("horario  '", "horario || '").replace("interesse  'Não informado'", "interesse || 'Não informado'")
    return block


def transform(source, path):
    old_form = 'var WA="5511954346288"' in source and 'academy.praia.digital/leads' in source
    if not OWN.search(source) and not old_form:
        return source
    t = TITLE.search(source)
    subject = 'Contato — ' + (' '.join(html.unescape(t[1]).split())[:140] if t else path.stem)
    parts = BLOCK.split(source)
    has_form = False
    for i, part in enumerate(parts):
        if i % 2:
            if part.lower().startswith('<script'):
                parts[i] = prepare_script(part, subject)
            continue
        part = MALFORMED.sub(lambda m: m[1] + '&text=' + m[2] + '"', part)
        # Repair three legacy onclick attributes with a stray double quote.
        part = re.sub(r'''onclick="window\.location\.href='(''' + OWN_URL + r'''[^']*)'"''',
                      lambda _: 'onclick="window.location.href=\'' + draft(subject) + '\'"', part, flags=re.I)
        part = ANCHOR.sub(lambda m: prepare_anchor(m, subject), part)
        if '"sameAs"' in part:
            part = schema_contact(part)
        # Also update the visitor-facing directions beside converted actions.
        for previous, new in (
            ('Envie seus dados pelo WhatsApp', 'Envie seus dados por e-mail'),
            ('Envie dados básicos do imóvel pelo WhatsApp', 'Envie dados básicos do imóvel por e-mail'),
            ('O WhatsApp será aberto', 'Seu aplicativo de e-mail será aberto'),
            ('revisar e enviar a mensagem no WhatsApp', 'revisar e enviar a mensagem por e-mail'),
            ('Revisar e enviar no WhatsApp', 'Revisar e enviar por e-mail'),
        ):
            part = part.replace(previous, new)

        def form_tag(m):
            nonlocal has_form
            tag = m[0]
            if ACTION.search(tag) or (old_form and re.search(r'''\bid=["'](?:leadForm|courseLeadForm)["']''', tag, re.I)):
                has_form = True
                return prepare_form(tag, subject)
            return tag
        part = FORM.sub(form_tag, part)
        if has_form or 'window.location' in source or 'window.open' in source:
            part = re.sub(r'(<button\b[^>]*>)([^<>]*WhatsApp[^<>]*)(</button>)',
                          lambda b:b[1]+label(b[2])+b[3], part,flags=re.I)
        part = re.sub(r'(?:WhatsApp|Fale no WhatsApp)(\s*:\s*<a\b[^<>]*?href="mailto:comercial@praia\.digital)',
                      r'E-mail\1', part, flags=re.I)
        parts[i] = part
    result = ''.join(parts)
    # These outreach pages include copyable examples of the company's own contact address.
    if 'outreach' in path.parts:
        result = re.sub(r'(?:WhatsApp|Whatsapp)\s*:\s*' + OWN_URL, 'E-mail: ' + EMAIL, result)
        result = COPY_URL.sub('mailto:' + EMAIL, result)

    if has_form:
        pos = result.lower().rfind('</body>')
        result = result[:pos] + FORM_SCRIPT + '\n' + result[pos:] if pos >= 0 else result + FORM_SCRIPT
    return result


def build(root):
    changed = []
    for path in sorted(root.rglob('*.html')):
        rel = path.relative_to(root)
        if any(p.startswith('.') or p in TECHNICAL for p in rel.parts[:-1]):
            continue
        src = path.read_bytes().decode('utf-8', 'surrogateescape')
        out = transform(src, rel)
        if out != src:
            path.write_bytes(out.encode('utf-8', 'surrogateescape'))
            changed.append(rel.as_posix())
    return changed


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--root', type=Path, default=Path('.'))
    cli.add_argument('--report', type=Path)
    args = cli.parse_args()
    pages = build(args.root)
    if args.report:
        args.report.write_text(json.dumps(pages, ensure_ascii=False), encoding='utf-8')
    print(f'Prepared email contacts in {len(pages)} HTML files.')
