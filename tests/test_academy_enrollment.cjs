const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {selectCourse, messageFor, contactLinks} = require('../education/assets/js/enrollment.js');
const course = {slug:'airbnb-do-zero',title:'Airbnb do Zero',price:29,path:'/education/cursos/airbnb-do-zero/index.html',kind:'guia'};
assert.equal(selectCourse([course], '?course=airbnb-do-zero&title=Fake&price=1'), course);
assert.equal(selectCourse([course], '?slug=airbnb-do-zero&price=99900'), course);
const aliasCourse={...course,aliases:['old-course-url']};
assert.equal(selectCourse([aliasCourse], '?slug=old-course-url&price=1'),aliasCourse);
assert.equal(selectCourse([course], '?course=unknown&title=Fake&price=1'), null);
assert.equal(selectCourse([course], ''), null);
assert.equal(selectCourse({}, '?course=airbnb-do-zero'), null);
assert.equal(selectCourse([{...course,price:'29'}], '?course=airbnb-do-zero'), null);
assert.equal(selectCourse([{...course,path:'//evil.test'}], '?course=airbnb-do-zero'), null);
assert.equal(selectCourse([{...course,path:'/education/\\evil.test'}], '?course=airbnb-do-zero'), null);
assert.match(messageFor(course), /29,00/);
assert.match(messageFor(course), /100% digital/);
assert.ok(!messageFor(null).includes('Valor anunciado'));
assert.equal(decodeURIComponent(contactLinks(course).whatsapp.split('text=')[1]),messageFor(course));
assert.ok(contactLinks(course).email.startsWith('mailto:comercial@praia.digital?'));
const checkout = fs.readFileSync(path.join(__dirname,'../education/checkout.html'),'utf8');
assert.ok(!checkout.includes('src="/education/assets/js/checkout.js'));
assert.ok(checkout.includes('enrollment.js'));
const login = fs.readFileSync(path.join(__dirname,'../education/aluno/login.html'),'utf8');
assert.match(login,/errorEl.hidden = false/);
assert.match(login,/role="alert"/);
assert.match(login,/if \(pending\) return/);
assert.match(login,/const apiBase = '\/academy'/);
assert.ok(!/id="error"[^>]*style=/.test(login));
console.log('Academy enrollment unit assertions passed');

// Optional offline browser regression, with all requests intercepted (no real login).
if (process.env.ACADEMY_BROWSER_TEST === '1') (async () => {
  const {chromium} = require('playwright');
  const browser = await chromium.launch({headless:true, ...(process.env.CHROMIUM_PATH ? {executablePath:process.env.CHROMIUM_PATH} : {})});
  try {
    for (const width of [390,1280]) {
      const context = await browser.newContext({viewport:{width,height:900}});
      let authRequests = 0;
      await context.route('**/*',async route => {
        const url = new URL(route.request().url());
        if(url.pathname === '/academy/auth/login') {
          authRequests++;
          await new Promise(resolve=>setTimeout(resolve,100));
          return route.fulfill({status:404,contentType:'text/html',body:'Unavailable'});
        }
        if(route.request().method() !== 'GET') throw new Error('Unexpected mutation');
        if(url.pathname === '/education/assets/catalog.json') return route.fulfill({contentType:'application/json',body:JSON.stringify([course])});
        const file = path.resolve(__dirname,'..','.'+url.pathname);
        if(!file.startsWith(path.resolve(__dirname,'..')+path.sep)) return route.abort();
        if(fs.existsSync(file)) return route.fulfill({body:fs.readFileSync(file),contentType:file.endsWith('.js')?'application/javascript':'text/html'});
        return route.abort();
      });
      const page = await context.newPage();
      await page.goto('https://praia.digital/education/checkout.html?course=airbnb-do-zero&price=1&title=Fake');
      await page.locator('#selected-course').waitFor({state:'visible'});
      assert.match(await page.locator('#course-price').innerText(),/29,00/);
      assert.equal(await page.locator('#course-title').innerText(),course.title);
      assert.match(decodeURIComponent(await page.locator('#contact-whatsapp').getAttribute('href')),/Airbnb do Zero/);
      assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
      await page.goto('https://praia.digital/education/checkout.html?course=unknown&title=Fake&price=1');
      await page.waitForFunction(()=>document.querySelector('#selection-status').textContent.includes('Nenhum'));
      assert.equal(await page.locator('#selected-course').isVisible(),false);
      await page.goto('https://praia.digital/education/aluno/login.html');
      await page.getByLabel('E-mail',{exact:true}).fill('offline-test@example.invalid');
      await page.getByLabel('Senha',{exact:true}).fill('offline-only');
      await page.locator('#loginForm').evaluate(form=>{form.dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}));form.dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}));});
      await page.locator('#error').waitFor({state:'visible'});
      assert.equal(authRequests,1);
      assert.match(await page.locator('#error').innerText(),/indisponível/);
      assert.equal(await page.locator('#password').inputValue(),'');
      assert.equal(await page.locator('#login-submit').isEnabled(),true);
      assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
      await context.close();
    }
    console.log('Academy offline browser: 390px + 1280px, context integrity, invalid slug, login error + repeated submit passed');
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exitCode=1;});

// Execute the actual login handler against a fake DOM and fake fetch only.
(async () => {
  const vm = require('node:vm');
  const elements = {};
  for (const id of ['loginForm','error','login-submit','email','password']) elements[id] = {
    value: id === 'email' ? 'offline-test@example.invalid' : 'offline-only', hidden:true,
    setAttribute(){},removeAttribute(){},focus(){this.focused=true;},
    addEventListener(event,callback){this.handler=callback;}
  };
  let fetches=0, release;
  const responsePromise=new Promise(resolve=>release=resolve);
  const script=login.match(/<script>([\s\S]*?)<\/script>/)[1];
  vm.runInNewContext(script,{document:{getElementById:id=>elements[id]},
    fetch:()=>{fetches++;return responsePromise;},AbortController,setTimeout,clearTimeout,
    localStorage:{setItem(){throw new Error('Unexpected token persistence');}},
    window:{location:{assign(){throw new Error('Unexpected navigation');}}}});
  const first=elements.loginForm.handler({preventDefault(){}});
  await elements.loginForm.handler({preventDefault(){}});
  assert.equal(fetches,1);
  assert.equal(elements['login-submit'].disabled,true);
  release({headers:{get:()=> 'text/html'},ok:false,status:404});
  await first;
  assert.equal(elements.error.hidden,false);
  assert.equal(elements.error.focused,true);
  assert.match(elements.error.textContent,/indisponível/);
  assert.equal(elements.password.value,'');
  assert.equal(elements['login-submit'].disabled,false);
  console.log('Academy login handler: mocked404, visible error, repeated submit and password cleanup passed');
})().catch(error=>{console.error(error);process.exitCode=1;});
