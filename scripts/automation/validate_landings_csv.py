#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Valida imoveis/landings.csv:
- Campos obrigatórios
- Duplicatas de slug/título
- URLs de WhatsApp válidas
- Relacionamentos quebrados (slug referenciado existe?)
- Imagens com extensão permitida
"""
import csv
import re
import sys
from pathlib import Path

REPO = Path('.').resolve()
CSV_PATH = REPO / 'imoveis' / 'landings.csv'
LANDINGS_DIR = REPO / 'imoveis'
ALLOWED_IMG_EXT = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}

def exists_file(slug):
    return (LANDINGS_DIR / f'{slug}.html').exists()

def validate_row(row, idx, existing_slugs, existing_titles):
    errors = []
    slug = row.get('slug', '').strip()
    title = row.get('title', '').strip()
    desc = row.get('description', '').strip()
    city = row.get('city', '').strip()
    type_ = row.get('type', '').strip()
    price = row.get('price', '').strip()
    bedrooms = row.get('bedrooms', '').strip()
    area = row.get('area', '').strip()
    image = row.get('image', '').strip()
    tags = row.get('tags', '').strip()
    related = row.get('related', '').strip()
    whatsapp_link = row.get('whatsapp_link', '').strip()

    if not slug:
        errors.append('slug vazio')
    if not title:
        errors.append('title vazio')
    if not desc:
        errors.append('description vazio')
    if not city:
        errors.append('city vazio')
    if not type_:
        errors.append('type vazio')
    if not price:
        errors.append('price vazio')
    if not area:
        errors.append('area vazio')
    if not image:
        errors.append('image vazio')
    if not whatsapp_link:
        errors.append('whatsapp_link vazio')

    if slug:
        if slug in existing_slugs:
            errors.append(f'slug duplicado: {slug}')
        existing_slugs.add(slug)
    if title:
        if title in existing_titles:
            errors.append(f'título duplicado: {title}')
        existing_titles.add(title)

    if image:
        ext = Path(image).suffix.lower()
        if ext not in ALLOWED_IMG_EXT:
            errors.append(f'extensão de imagem não permitida: {image}')

    if whatsapp_link and not re.search(r'https://wa\.me/\d{10,15}', whatsapp_link):
        errors.append(f'whatsapp_link inválido: {whatsapp_link}')

    # Relacionamentos
    if related:
        rel_slugs = re.findall(r'href="([^"]+\.html)"', related)
        for link in rel_slugs:
            ref_slug = Path(link).stem
            if not exists_file(ref_slug):
                errors.append(f'relacionamento quebrado: {link}')

    return errors

def main():
    if not CSV_PATH.exists():
        print('ERRO: landings.csv não encontrado')
        sys.exit(1)

    rows = []
    with CSV_PATH.open('r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    existing_slugs = set()
    existing_titles = set()
    all_errors = []
    for idx, row in enumerate(rows, start=2):
        errs = validate_row(row, idx, existing_slugs, existing_titles)
        if errs:
            all_errors.append((idx, row.get('slug', '<sem slug>'), errs))

    print(f'CSV_LINES {len(rows)}')
    if all_errors:
        print(f'ERRORS {len(all_errors)}')
        for idx, slug, errs in all_errors[:50]:
            print(f'  line {idx} | {slug} | ' + '; '.join(errs))
        sys.exit(1)
    else:
        print('CSV_OK 0 errors')
        sys.exit(0)

if __name__ == '__main__':
    main()
