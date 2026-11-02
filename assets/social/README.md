# Homepage institutional social preview

`praia-digital-institucional-v1.png` is the 1200×630 social card used **only by the homepage**. The editable SVG is original vector artwork created for Praia Digital, using the homepage wordmark and palette. The coastal illustration does not depict a specific property or location and uses no third-party photos.

Regenerate after changing the SVG (Inkscape 1.2+ and DejaVu Sans):

```sh
inkscape assets/social/praia-digital-institucional-v1.svg --export-type=png --export-filename=assets/social/praia-digital-institucional-v1.png
python3 -m unittest discover -s tests -p 'test_homepage_content.py' -v
```

Keep the PNG committed: social crawlers need a raster URL, not the source SVG. Keep image URLs absolute HTTPS, dimensions/alt synchronized, and change the versioned filename when changing the artwork. Do not replace individual property images or shared fallback assets.

After deployment, check the homepage raw HTML and that the PNG URL responds with HTTP 200 and `image/png`. Existing WhatsApp previews may remain cached; cache refresh timing is outside the site's control.
