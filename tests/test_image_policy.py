from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from image_policy import image_issues
import pytest

HERO='<section class="hero"><picture><img src="/hero.webp" width="800" height="600" decoding="async" fetchpriority="high"></picture></section>'
PRELOAD='<link rel="preload" as="image" href="/hero.webp">'
PIXEL='<noscript><img width="1" height="1" src="https://www.facebook.com/tr?id=test" style="display:none"></noscript>'

def test_eager_default_hero_and_pixel(): assert image_issues(PRELOAD+HERO+PIXEL)==[]
def test_explicit_eager_hero(): assert image_issues(PRELOAD+HERO.replace('<img ','<img loading="eager" '))==[]
def test_index_pixel_requires_no_preload(): assert image_issues(PIXEL)==[]
def test_hero_lazy_is_rejected(): assert 'hero_is_lazy' in image_issues(PRELOAD+HERO.replace('<img ','<img loading="lazy" '))
def test_missing_hero_preload_rejected(): assert 'hero_preload_mismatch' in image_issues(HERO)
def test_mismatched_preload_rejected(): assert 'hero_preload_mismatch' in image_issues(PRELOAD.replace('/hero.webp','/other.webp')+HERO)
def test_pixel_preload_rejected(): assert 'tracking_pixel_preloaded' in image_issues('<link rel="preload" as="image" href="https://www.facebook.com/tr?id=test">'+PIXEL)
def test_noncritical_lazy(): assert image_issues('<img src="/below.webp" loading="lazy" decoding="async">')==[]
def test_noncritical_eager_rejected(): assert 'noncritical_image_not_lazy' in image_issues('<img src="/below.webp" decoding="async">')
def test_decode_missing_rejected(): assert 'missing_async_decoding' in image_issues(PRELOAD+HERO.replace('decoding="async"',''))
def test_dimension_missing_rejected(): assert 'hero_missing_dimensions' in image_issues(PRELOAD+HERO.replace('width="800"',''))
def test_noscript_content_not_silently_excluded(): assert 'unclassified_noscript_image' in image_issues('<noscript><img src="/real.webp"></noscript>')
