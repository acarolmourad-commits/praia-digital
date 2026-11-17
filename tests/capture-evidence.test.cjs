const { test } = require('node:test');
const assert = require('node:assert/strict');
const { captureEvidence } = require('./capture-evidence.cjs');
const transient = new Error('page.screenshot: Protocol error (Page.captureScreenshot): Unable to capture screenshot');
test('transient capture failure recovers without dropping required evidence', async () => {
  let calls = 0, layouts = 0;
  const page = { screenshot: async opts => { assert.equal(opts.path, 'proof.png'); assert.equal(opts.fullPage, true); assert.equal(opts.animations, 'disabled'); if (++calls === 1) throw transient; return 'proof'; }, evaluate: async () => { layouts++; } };
  assert.equal(await captureEvidence(page, { path: 'proof.png', fullPage: true }), 'proof');
  assert.equal(calls, 2); assert.equal(layouts, 1);
});
test('persistent failure still fails after three attempts', async () => {
  let calls = 0;
  await assert.rejects(captureEvidence({ screenshot: async () => { calls++; throw transient; }, evaluate: async () => {} }, {}), /Unable to capture/);
  assert.equal(calls, 3);
});
test('file and other errors fail immediately', async () => {
  let calls = 0;
  await assert.rejects(captureEvidence({ screenshot: async () => { calls++; throw new Error('EACCES'); }, evaluate: async () => { throw new Error('unexpected retry'); } }, {}), /EACCES/);
  assert.equal(calls, 1);
});
