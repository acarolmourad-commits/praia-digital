// Compile the audited legacy HTML without executing scripts or sending requests.
// HTMLParser (Python's standard library) preserves script raw text and decodes
// event-handler attributes as a browser does, including quoted > and entities.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { spawnSync } = require('node:child_process');

const root = path.resolve(__dirname, '..');
const pages = JSON.parse(fs.readFileSync(path.join(__dirname, 'legacy-html-pages.json'), 'utf8'));
assert(Array.isArray(pages) && pages.length > 0, 'The audited HTML manifest must not be empty');
assert.equal(new Set(pages).size, pages.length, 'Duplicate HTML paths in the manifest');
for (const file of pages) {
  assert(typeof file === 'string' && file.endsWith('.html'), `Invalid HTML path: ${file}`);
  assert(!path.isAbsolute(file) && !file.split('/').includes('..'), `Unsafe HTML path: ${file}`);
  assert(fs.statSync(path.join(root, file)).isFile(), `Missing audited page: ${file}`);
}

const parser = String.raw`
import json, re, sys
from html.parser import HTMLParser
from pathlib import Path

class InlineParser(HTMLParser):
    def __init__(self, name):
        super().__init__(convert_charrefs=True)
        self.name, self.current = name, None
        self.scripts, self.handlers, self.errors = [], [], []
    def handle_starttag(self, tag, attrs):
        attributes = {}
        for key, value in attrs:
            attributes.setdefault(key, value if value is not None else '')
        for key, value in attributes.items():
            if re.fullmatch(r'on[a-z]+', key):
                self.handlers.append({'file': self.name, 'line': self.getpos()[0], 'attribute': key, 'source': value})
        if tag == 'script':
            self.current = {'file': self.name, 'line': self.getpos()[0], 'attrs': attributes, 'source': ''}
    def handle_data(self, data):
        if self.current is not None:
            self.current['source'] += data
    def handle_endtag(self, tag):
        if tag == 'script' and self.current is not None:
            self.scripts.append(self.current)
            self.current = None
    def close(self):
        super().close()
        if self.current is not None:
            self.errors.append({'file': self.name, 'line': self.current['line'], 'kind': 'html', 'message': 'Unclosed script element'})

request = json.load(sys.stdin)
result = {'scripts': [], 'handlers': [], 'errors': []}
for entry in request:
    parser = InlineParser(entry['file'])
    parser.feed(entry.get('source') if 'source' in entry else Path(entry['file']).read_text(encoding='utf-8'))
    parser.close()
    for key in result:
        result[key].extend(getattr(parser, key))
print(json.dumps(result, ensure_ascii=False))
`;

function extract(entries) {
  const child = spawnSync('python3', ['-c', parser], {
    cwd: root, input: JSON.stringify(entries), encoding: 'utf8', maxBuffer: 32 * 1024 * 1024,
  });
  if (child.error) throw child.error;
  assert.equal(child.status, 0, `HTML extraction failed: ${child.stderr}`);
  return JSON.parse(child.stdout);
}

function compileModule(source, filename) {
  // --check parses ESM, including imports and top-level await, without loading it.
  const child = spawnSync(process.execPath, ['--input-type=module', '--check'], {
    input: source, encoding: 'utf8', maxBuffer: 1024 * 1024,
  });
  if (child.error) throw child.error;
  if (child.status !== 0) throw new SyntaxError(`${filename}: ${child.stderr.trim()}`);
}

// Guard the extractor against common HTML/JS boundary mistakes.
const fixture = extract([{ file: 'parser-fixture.html', source: `
<!-- <script>not valid javascript</script> -->
<button onclick="if (event.detail &gt; 0) return '&quot;';">Test</button>
<script>const raw = '&amp;'; if (1 > 0) { /* compile only */ }</script>
<script type="application/ld+json">{"name":"<example>"}</script>
<script type="module">import value from './not-loaded.js'; await Promise.resolve(value);</script>
<script src="/not-loaded.js"></script>` }]);
assert.equal(fixture.scripts.length, 4);
assert.equal(fixture.handlers.length, 1);
assert.equal(fixture.handlers[0].source, `if (event.detail > 0) return '"';`);
assert(fixture.scripts[0].source.includes("'&amp;'"), 'Script raw text must not decode HTML entities');
assert.deepEqual(fixture.errors, []);
new vm.Script(fixture.scripts[0].source);
JSON.parse(fixture.scripts[1].source);
compileModule(fixture.scripts[2].source, 'parser-fixture.html');

const extracted = extract(pages.map(file => ({ file })));
const failures = [...extracted.errors];
const counts = { pages: pages.length, scripts: 0, handlers: 0, json: 0, modules: 0, external: 0, inert: 0 };
const javascriptTypes = new Set([
  '', 'application/javascript', 'application/ecmascript', 'application/x-javascript',
  'text/javascript', 'text/ecmascript', 'text/jscript', 'text/livescript',
  'text/x-javascript', 'text/x-ecmascript',
  ...Array.from({ length: 6 }, (_, i) => `text/javascript1.${i}`),
]);
function check(item, kind, operation) {
  try { operation(); }
  catch (error) { failures.push({ file: item.file, line: item.line, kind, message: error.message }); }
}

for (const item of extracted.scripts) {
  const type = (item.attrs.type || '').trim().toLowerCase();
  if (Object.hasOwn(item.attrs, 'src')) {
    counts.external++;
    continue;
  }
  if (type === 'module') {
    counts.modules++;
    check(item, 'module', () => compileModule(item.source, item.file));
  } else if (type === 'importmap' || type === 'speculationrules' || type === 'application/json' || type.endsWith('+json')) {
    counts.json++;
    check(item, 'json', () => JSON.parse(item.source));
  } else if (javascriptTypes.has(type)) {
    counts.scripts++;
    check(item, 'script', () => new vm.Script(item.source, { filename: `${item.file}:${item.line}` }));
  } else {
    counts.inert++;
  }
}
for (const item of extracted.handlers) {
  counts.handlers++;
  check(item, item.attribute, () => new vm.Script(`(function(event) {\n${item.source}\n})`, {
    filename: `${item.file}:${item.line}:${item.attribute}`,
  }));
}

console.log(JSON.stringify({ ...counts, failures: failures.length }));
if (failures.length) {
  for (const failure of failures) console.error(JSON.stringify(failure));
  process.exitCode = 1;
}
