import json, os
from pathlib import Path
from html import escape
SITE = str(Path(__file__).resolve().parent.parent)
DOMAIN = 'https://www.boston-shawarma.com'
policies = json.load(open(Path(__file__).with_name('policies.json')))

TITLES = {'privacy-policy': 'Privacy Policy',
          'return-and-refund-policy': 'Return & Refund Policy',
          'terms-and-conditions': 'Terms & Conditions'}

def policy_body(blocks):
    # the policy text sits between the page title/breadcrumb and the old footer ("Blind & partially...")
    start = next(i for i, (t, _) in enumerate(blocks) if t == 'h1') + 2
    end = next(i for i, (t, x) in enumerate(blocks) if x.startswith('Blind & partially'))
    html = []
    for tag, text in blocks[start:end]:
        is_heading = len(text) < 50 or text.endswith('?')
        html.append(f'      <h2>{escape(text)}</h2>' if is_heading else f'      <p>{escape(text)}</p>')
    return '\n'.join(html)

page = open(f'{SITE}/index.html').read()
# Re-use the real footer so every page stays in sync; point its links back at the homepage
footer = page[page.index('  <footer class="site-footer">'):page.index('</footer>') + len('</footer>')]
footer = (footer.replace('href="#', 'href="../#').replace(' data-open-order', '')
                .replace('src="images/', 'src="../images/').replace('href="privacy-policy/', 'href="../privacy-policy/')
                .replace('href="return-and-refund-policy/', 'href="../return-and-refund-policy/')
                .replace('href="terms-and-conditions/', 'href="../terms-and-conditions/'))

for slug, title in TITLES.items():
    os.makedirs(f'{SITE}/{slug}', exist_ok=True)
    open(f'{SITE}/{slug}/index.html', 'w').write(f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} | Boston Shawarma</title>
  <meta name="robots" content="noindex, nofollow">  <!-- PREVIEW: remove before launch -->
  <meta name="description" content="{escape(title)} for Boston Shawarma, 315 Huntington Ave, Boston and 880 Walnut St, Newton.">
  <link rel="canonical" href="{DOMAIN}/{slug}/">
  <link rel="icon" type="image/png" href="../images/favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,200..800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/styles.css">
  <script>document.documentElement.classList.add('js')</script>
  <script src="../js/main.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="../" aria-label="Boston Shawarma — home">
        <img src="../images/logo.png" alt="" width="70" height="44">
        <span class="brand-name">Boston Shawarma</span>
      </a>
      <a class="btn btn-primary" href="../#order">Order now</a>
    </div>
  </header>

  <main id="main" class="legal">
    <article class="container legal-inner">
      <p class="eyebrow"><a href="../">Home</a> / {escape(title)}</p>
      <h1>{escape(title)}</h1>
{policy_body(policies[slug])}
      <aside class="legal-contact">
        <h2>Questions?</h2>
        <p>Call us at <a href="tel:+16176700460">(617) 670-0460</a> (Boston) or <a href="tel:+16177950342">(617) 795-0342</a> (Newton).</p>
      </aside>
    </article>
  </main>

{footer}
</body>
</html>
''')
    print('wrote', slug)

# Old URLs that should keep working: send them to the matching part of the new homepage
REDIRECTS = {
    'about-us': '../#story', 'contact-us': '../#visit',
    **{s: '../' for s in ['boston-shawarma', 'best-shawarma-in-boston', 'halal-meats-boston',
                           'mediterranean-cuisine-boston', 'middle-eastern-flavors-boston',
                           'shawarma-delivery-boston', 'authentic-shawarma-experience',
                           'delicious-mediterranean-dishes', 'fresh-halal-meats-selection',
                           'rich-middle-eastern-flavors', 'convenient-shawarma-delivery-service']},
}
for slug, target in REDIRECTS.items():
    os.makedirs(f'{SITE}/{slug}', exist_ok=True)
    canonical = DOMAIN + '/' + target.replace('../', '')
    open(f'{SITE}/{slug}/index.html', 'w').write(f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Boston Shawarma</title>
  <!-- This page moved. The redirect keeps old links and search results working. -->
  <meta http-equiv="refresh" content="0; url={target}">
  <meta name="robots" content="noindex">  <!-- PREVIEW: remove before launch -->
  <link rel="canonical" href="{canonical}">
</head>
<body>
  <p>This page has moved to <a href="{target}">Boston Shawarma</a>.</p>
</body>
</html>
''')
print('redirects:', len(REDIRECTS))

open(f'{SITE}/robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n')
urls = ['/'] + [f'/{s}/' for s in TITLES]
open(f'{SITE}/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'  <url><loc>{DOMAIN}{u}</loc></url>\n' for u in urls) + '</urlset>\n')
print('wrote robots.txt, sitemap.xml')
