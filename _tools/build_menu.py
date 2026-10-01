from html import escape
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from menu_data import MENU

PHOTOS = {
    'sandwiches': ('shawarma-wrap.jpg', 340, 577, 'Shawarma sandwich wrapped in fresh pita'),
    'veggie': ('falafel-avocado-wrap.jpg', 340, 577, 'Falafel wrap with fresh avocado'),
    'plates': ('shawarma-plate.jpg', 682, 454, 'Shawarma dinner plate with fries, salad and falafel'),
    'veg-plates': ('falafel-plate.jpg', 720, 482, 'Falafel dinner plate with salad and pickled turnips'),
    'salads': ('middle-eastern-salad.jpg', 682, 454, 'Middle Eastern salad with grape leaves, olives and feta'),
    'pies-sides': ('pies.jpg', 340, 577, 'Golden homemade pies'),
    'drinks': ('baklava.jpg', 341, 270, 'Baklava and sweet pastries'),
}
TAGS = {'veg': ('tag-veg', 'Vegetarian'), 'spicy': ('tag-spicy', 'Spicy'), 'fav': ('tag-fav', 'Signature')}
I = '    '
out = []
w = lambda depth, s: out.append(I * depth + s)

w(2, '<section class="section menu" id="menu" aria-labelledby="menu-title">')
w(3, '<div class="container">')
w(4, '<header class="section-head">')
w(5, '<p class="eyebrow">The full menu</p>')
w(5, '<h2 id="menu-title" class="shout">61 dishes, one family kitchen.</h2>')
w(5, '<p>All of our meats are 100% halal. Look for <span class="tag tag-fav">Signature</span> dishes — the ones our regulars keep coming back for.</p>')
w(4, '</header>')
w(0, '')
w(4, '<div class="menu-tabs" role="tablist" aria-label="Menu categories">')
for key, label, _ in MENU:
    w(5, f'<button class="menu-tab" role="tab" id="tab-{key}" aria-controls="panel-{key}" type="button">{escape(label)}</button>')
w(4, '</div>')
w(0, '')
w(4, '<!-- Prices and items from the online-ordering menu. Update here when prices change. -->')
w(4, '<div class="menu-panels">')
for key, label, groups in MENU:
    src, pw, ph, alt = PHOTOS[key]
    w(5, f'<div class="menu-panel" role="tabpanel" id="panel-{key}" aria-labelledby="tab-{key}">')
    w(6, f'<figure class="menu-photo"><img src="images/{src}" alt="{escape(alt)}" width="{pw}" height="{ph}" loading="lazy"><figcaption>{escape(label)}</figcaption></figure>')
    w(6, '<div class="menu-items">')
    w(6, f'<h3 class="panel-title">{escape(label)}</h3>')
    for gtitle, note, items in groups:
        w(6, '<div class="menu-group">')
        w(7, f'<h4 class="group-title">{escape(gtitle)}</h4>')
        if note:
            w(7, f'<p class="group-note">{escape(note)}</p>')
        w(7, '<ul class="dish-list">')
        for name, price, desc, tags in items:
            tag_html = ''.join(f' <span class="tag {TAGS[t][0]}">{TAGS[t][1]}</span>' for t in tags)
            w(8, '<li class="dish">')
            w(9, f'<p class="dish-row"><span class="dish-name">{escape(name)}</span><span class="dish-price">${price}</span></p>')
            if desc or tag_html:
                w(9, f'<p class="dish-desc">{escape(desc)}{tag_html}</p>'.replace('"> <span', '"><span'))
            w(8, '</li>')
        w(7, '</ul>')
        w(6, '</div>')
    w(6, '</div>')
    w(5, '</div>')
w(4, '</div>')
w(0, '')
w(4, '<p class="menu-note">Prices are from our online menu and may vary slightly between locations. Please let us know about any allergies.</p>')
w(3, '</div>')
w(2, '</section>')

frag = '\n'.join(out).lstrip()
import re, sys
from pathlib import Path
p = Path(__file__).resolve().parent.parent / 'index.html'
s = p.read_text()
block = '<!--MENU:start-->\n    ' + frag + '\n    <!--MENU:end-->'
if '<!--MENU-->' in s:
    s = s.replace('<!--MENU-->', block)
else:
    s, n = re.subn(r'<!--MENU:start-->.*?<!--MENU:end-->', lambda m: block, s, flags=re.S)
    if not n: sys.exit('no menu markers found in index.html')
p.write_text(s)
print('menu inserted:', frag.count('class="dish"'), 'dishes,', frag.count('role="tabpanel"'), 'tabs')
