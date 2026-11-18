const {test} = require('node:test');
const assert = require('node:assert/strict');
const {screenshot} = require('./screenshot.cjs');
test('recovers transient capture failure', async () => {
  let calls = 0;
  const page = {evaluate: async () => {}, screenshot: async () => {
    if (++calls < 3) throw Error('Protocol error (Page.captureScreenshot): Unable to capture screenshot');
    return 'image';
  }};
  assert.equal(await screenshot(page, {path: 'evidence.png'}), 'image');
  assert.equal(calls, 3);
});
test('persistent capture failure remains a failure', async () => {
  let calls = 0;
  const page = {evaluate: async () => {}, screenshot: async () => {calls++; throw Error('Unable to capture screenshot');}};
  await assert.rejects(screenshot(page, {}), /Unable to capture screenshot/);
  assert.equal(calls, 3);
});
test('does not retry unrelated failures', async () => {
  let calls = 0;
  const page = {screenshot: async () => {calls++; throw Error('Page closed');}};
  await assert.rejects(screenshot(page, {}), /Page closed/);
  assert.equal(calls, 1);
});
