# Build tools (not published — GitHub Pages ignores folders starting with "_")

- `python3 _tools/build_menu.py` — regenerates the full menu from `menu_data.py` and swaps it into
  `index.html` between the `<!--MENU:start-->` / `<!--MENU:end-->` markers. Edit prices there.
- `python3 _tools/build_pages.py` — rebuilds the policy pages, the redirects for old URLs,
  `robots.txt` and `sitemap.xml`, reusing the footer from `index.html`.

Popups live as `<template id="tpl-…">` blocks at the bottom of `index.html`. Any element with
`data-popup="deal-student"` opens `tpl-deal-student`, and so does visiting `/#deal-student`.
Forms post to `FORM_ENDPOINT` at the top of `js/main.js` (empty = demo mode).

## Font lab
Open `index.html?fontlab` for a switcher that swaps the whole site between type pairings
(`?font=beirut` jumps straight to one). Themes live at the end of `css/styles.css`
(`[data-font="…"]`) and in `FONT_THEMES` in `js/main.js`. `_fontlab/compare-*.png` shows all of them
side by side. Bricolage Grotesque is the default.
