"""Role-aware listing-image audit; does not execute scripts or tracking pixels."""
from urllib.parse import urlsplit
from bs4 import BeautifulSoup


def image_issues(text):
    soup=BeautifulSoup(text,'html.parser'); issues=[]
    preloads=[tag.get('href','') for tag in soup.find_all('link')
              if 'preload' in tag.get('rel',[]) and tag.get('as')=='image']
    for src in preloads:
        if urlsplit(src).hostname in {'www.facebook.com','facebook.com'}:
            issues.append('tracking_pixel_preloaded')
    for img in soup.find_all('img'):
        src=img.get('src',''); host=urlsplit(src).hostname
        pixel=(host in {'www.facebook.com','facebook.com'} and urlsplit(src).path=='/tr'
               and img.get('width')=='1' and img.get('height')=='1'
               and img.find_parent('noscript') is not None
               and 'display:none' in img.get('style','').replace(' ',''))
        if pixel: continue  # Tracking is not visible content or a preload target.
        if img.find_parent('noscript') is not None:
            issues.append('unclassified_noscript_image')
        if img.get('decoding')!='async': issues.append('missing_async_decoding')
        section=img.find_parent('section')
        hero=(section is not None and 'hero' in section.get('class',[])
              and img.find_parent('picture') is not None)
        if hero:
            # Missing loading is the browser's eager default, not lazy loading.
            if img.get('loading') not in (None,'eager','auto'): issues.append('hero_is_lazy')
            if img.get('fetchpriority')!='high': issues.append('hero_priority_not_high')
            if src not in preloads: issues.append('hero_preload_mismatch')
            for dim in ['width','height']:
                if not str(img.get(dim,'')).isdigit() or int(img.get(dim,'0'))<=0:
                    issues.append('hero_missing_dimensions')
        elif img.get('loading')!='lazy': issues.append('noncritical_image_not_lazy')
    return issues
