// Retry only the transient Chromium capture failure. Assertions still fail normally.
async function screenshot(page, options) {
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      return await page.screenshot({ animations: 'disabled', ...options });
    } catch (error) {
      if (attempt === 2 || !String(error.message).includes('Unable to capture screenshot')) throw error;
      console.warn(`Chromium capture retry ${attempt + 1}: ${options.path}`);
      await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    }
  }
}
module.exports = { screenshot };
