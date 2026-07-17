from pathlib import Path

repo = Path('.')
bairros_dir = repo/'bairros'
bairros_dir.mkdir(exist_ok=True)

pages = {
  'ubatuba-centro.html': """<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ubatuba — Centro | Praia Digital</title>
...