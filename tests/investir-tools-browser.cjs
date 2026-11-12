const { chromium } = require("playwright"),
  fs = require("fs"),
  path = require("path"),
  assert = require("node:assert/strict");
const root = path.resolve(__dirname, "..");
(async () => {
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.CHROMIUM_PATH
      ? { executablePath: process.env.CHROMIUM_PATH }
      : {}),
  });
  try {
    for (const width of [320, 390, 768, 1280]) {
      const page = await browser.newPage({
        viewport: { width, height: 900 },
        locale: "pt-BR",
      });
      const errors = [];
      page.on("pageerror", (e) => errors.push(e.message));
      let mode = "ok",
        requests = 0;
      await page.route("**/*", async (route) => {
        const u = new URL(route.request().url());
        if (u.hostname === "formsubmit.co") {
          requests++;
          if (mode === "network") return route.abort();
          if (mode === "slow") await new Promise((r) => setTimeout(r, 500));
          return route.fulfill({
            status: mode === "fail" ? 500 : 200,
            contentType: "application/json",
            body: JSON.stringify({ success: mode === "false" ? false : true }),
          });
        }
        if (u.hostname !== "pd.test") return route.abort();
        let f = path.join(root, decodeURIComponent(u.pathname));
        if (fs.existsSync(f) && fs.statSync(f).isDirectory())
          f = path.join(f, "index.html");
        if (!fs.existsSync(f)) return route.fulfill({ status: 404, body: "" });
        return route.fulfill({
          status: 200,
          contentType:
            {
              ".html": "text/html",
              ".js": "text/javascript",
              ".css": "text/css",
            }[path.extname(f)] || "text/plain",
          body: fs.readFileSync(f),
        });
      });
      await page.goto("https://pd.test/apps/calculadora-financiamento/");
      await page.getByRole("button", { name: "Comparar SAC e Price" }).click();
      assert.match(await page.locator("#rows").innerText(), /7\.195,56/);
      assert.equal(
        await page
          .locator("#result-title")
          .evaluate((e) => e === document.activeElement),
        true,
      );
      await page.locator("#entrada").fill("-1");
      assert.equal(await page.locator("#resultado").isVisible(), false);
      await page.getByRole("button", { name: "Comparar SAC e Price" }).click();
      assert.equal(
        await page.locator("#entrada").getAttribute("aria-invalid"),
        "true",
      );
      await page.locator("#entrada").fill("40000");
      await page.locator("#tipo").selectOption("effective");
      await page.getByRole("button", { name: "Comparar SAC e Price" }).click();
      assert.match(await page.locator("#rows").innerText(), /1\.614,00/);
      assert.equal(
        await page.evaluate(
          () => document.documentElement.scrollWidth > innerWidth + 1,
        ),
        false,
      );
      await page.screenshot({
        path: `/tmp/investir-fin-${width}.png`,
        fullPage: true,
      });
      await page.goto("https://pd.test/ferramentas/avaliacao-preco.html");
      await page
        .getByRole("button", { name: "Calcular cenário de preço" })
        .click();
      assert.match(await page.locator("#central").innerText(), /650\.850,00/);
      const download = page.waitForEvent("download");
      await page.locator("#download").click();
      assert.equal(
        (await download).suggestedFilename(),
        "cenario-preco-imovel.txt",
      );
      await page.locator("#cidade").selectOption("Bertioga");
      assert.equal(await page.locator("#referencia").inputValue(), "");
      await page
        .getByRole("button", { name: "Calcular cenário de preço" })
        .click();
      assert.equal(await page.locator("#resultado").isVisible(), false);
      await page.locator("#referencia").fill("10000");
      await page
        .getByRole("button", { name: "Calcular cenário de preço" })
        .click();
      assert.match(await page.locator("#basis").innerText(), /personalizada/);
      await page.locator("#lead-email").fill("teste@example.com");
      for (const m of ["fail", "false", "network"]) {
        mode = m;
        await page.locator("#enviar-simulacao").click();
        await page.waitForFunction(() =>
          document
            .getElementById("contact-status")
            .textContent.includes("Não foi possível"),
        );
        assert.doesNotMatch(
          await page.locator("#contact-status").innerText(),
          /confirmou/,
        );
      }
      mode = "slow";
      const before = requests;
      await page.locator("#enviar-simulacao").click();
      assert.equal(await page.locator("#enviar-simulacao").isDisabled(), true);
      await page.waitForFunction(() =>
        document
          .getElementById("contact-status")
          .textContent.includes("serviço confirmou"),
      );
      assert.equal(requests, before + 1);
      assert.equal(await page.locator("#enviar-simulacao").isDisabled(), true);
      await page.locator("#area").fill("80");
      assert.equal(await page.locator("#resultado").isVisible(), false);
      await page
        .getByRole("button", { name: "Calcular cenário de preço" })
        .click();
      assert.equal(await page.locator("#enviar-simulacao").isDisabled(), false);
      assert.equal(
        await page.evaluate(
          () => document.documentElement.scrollWidth > innerWidth + 1,
        ),
        false,
      );
      await page.screenshot({
        path: `/tmp/investir-avaliacao-${width}.png`,
        fullPage: true,
      });
      assert.deepEqual(errors, []);
      await page.close();
      console.log(
        `Browser ${width}px: calculations, validation, stale results, download, success/failure/duplicate contact passed (mocked, no external submissions).`,
      );
    }
  } finally {
    await browser.close();
  }
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
