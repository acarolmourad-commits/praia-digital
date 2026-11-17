'use strict';

// Chromium can transiently reject Page.captureScreenshot after layout changes.
// Keep the evidence mandatory: retry only that protocol error, then fail the job.
async function captureEvidence(page, options) {
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      return await page.screenshot({ ...options, animations: 'disabled' });
    } catch (error) {
      if (attempt === 2 || !/Protocol error \(Page\.captureScreenshot\): Unable to capture screenshot/.test(String(error))) throw error;
      await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    }
  }
}

module.exports = { captureEvidence };
