const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

async function checkAppLinkTargets(page, root) {
  const hrefs = await page.locator('a[href^="/"]').evaluateAll(links =>
    links.map(link => link.getAttribute('href'))
  );
  const origin = new URL(page.url()).origin;
  for (const href of hrefs) {
    const url = new URL(href, origin);
    assert.equal(url.origin, origin, href);
    const pathname = decodeURIComponent(url.pathname);
    const file = path.join(root, pathname, pathname.endsWith('/') ? 'index.html' : '');
    assert.ok(fs.statSync(file, {throwIfNoEntry: false})?.isFile(), href);
  }
}

module.exports = {checkAppLinkTargets};
