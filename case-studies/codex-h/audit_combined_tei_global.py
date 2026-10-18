#!/usr/bin/env python3
"""Audit every TEI/body in Glasgow dataset 2105; source structure only.

No ancient K1 is established by a matching number, Greek word or modern label.
"""
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import unicodedata
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET
import zipfile

URL = 'https://researchdata.gla.ac.uk/2105/1/2105_data.zip'
DOI = '10.5525/gla.researchdata.2105'
MAX_ZIP = 3 * 1024 * 1024
MAX_UNCOMPRESSED = 40 * 1024 * 1024
MAX_MEMBER = 8 * 1024 * 1024
XID = '{http://www.w3.org/XML/1998/namespace}id'
FOCUS = {'86v', '87r'}
STEMS = {
    'didask': '\u03b4\u03b9\u03b4\u03b1\u03c3\u03ba',
    'epited': '\u03b5\u03c0\u03b9\u03c4\u03b7\u03b4',
    'diakon': '\u03b4\u03b9\u03b1\u03ba\u03bf\u03bd',
    'apeith': '\u03b1\u03c0\u03b5\u03b9\u03b8',
}


def local(tag):
    return tag.rsplit('}', 1)[-1] if isinstance(tag, str) else ''


def norm(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text or '').casefold()
                   if unicodedata.category(c) != 'Mn')


def brief(text, limit=100):
    return re.sub(r'\s+', ' ', text or '').strip()[:limit]


def nearest(element, parents, target):
    while element in parents:
        element = parents[element]
        if local(element.tag) == target:
            return element
    return None


def scope(element, parents):
    b = nearest(element, parents, 'body')
    t = nearest(element, parents, 'TEI')
    d = nearest(element, parents, 'div')
    return {
        'tei_id': t.get(XID) if t is not None else None,
        'body_index': None,
        'div_type': d.get('type') if d is not None else None,
        'div_n': d.get('n') if d is not None else None,
    }, b


def inspect_xml(name, raw):
    root = ET.fromstring(raw)
    elements = list(root.iter())
    parents = {ch: par for par in elements for ch in par}
    bodies = [e for e in elements if local(e.tag) == 'body']
    body_ids = {e: i + 1 for i, e in enumerate(bodies)}
    tags = Counter(local(e.tag) for e in elements)
    pbs = [e for e in elements if local(e.tag) == 'pb']
    divs = [e for e in elements if local(e.tag) == 'div']
    nums = [e for e in elements if local(e.tag) == 'num']

    def scoped(e):
        s, b = scope(e, parents)
        s['body_index'] = body_ids.get(b)
        return s

    all_pages = [dict(n=e.get('n'), **scoped(e)) for e in pbs]
    chapters = []
    for e in nums:
        if e.get('type') != 'chapNum':
            continue
        row = dict(n=e.get('n'), reading=brief(''.join(e.itertext()), 30), **scoped(e))
        chapters.append(row)

    # Scan each body independently. Previous G0.9 inspected only the first body.
    body_rows = []
    for i, body in enumerate(bodies, 1):
        seq = list(body.iter())
        bpages = [e.get('n') for e in seq if local(e.tag) == 'pb']
        bnums = [e for e in seq if local(e.tag) == 'num' and e.get('type') == 'chapNum']
        bdivs = [e for e in seq if local(e.tag) == 'div']
        titles = [e for e in seq if local(e.tag) in ('head', 'title')]
        stems = Counter()
        for word in (e for e in seq if local(e.tag) in ('w', 'head', 'title')):
            word_text = norm(''.join(word.itertext()))
            for label, needle in STEMS.items():
                if needle in word_text:
                    stems[label] += 1
        body_rows.append({
            'body_index': i,
            'tei_id': scoped(body)['tei_id'],
            'page_breaks': bpages,
            'chapter_numbers': [x.get('n') for x in bnums],
            'division_count': len(bdivs),
            'division_identifiers': [dict(type=e.get('type'), n=e.get('n'),
                                          subtype=e.get('subtype')) for e in bdivs[:20]],
            'heading_count': len(titles),
            'heading_examples': [brief(''.join(e.itertext()), 80) for e in titles[:4]],
            'lexical_stem_matches': dict(stems),
        })

    # B17K1V5 is a modern reference; it does NOT mean an ancient K1.
    focus_attributes = []
    for e in elements:
        for k, value in e.attrib.items():
            if value in FOCUS or re.search(r'\bTitus\b|\bTite\b', value, re.I):
                focus_attributes.append({
                    'tag': local(e.tag), 'attribute': local(k), 'value': brief(value),
                    **scoped(e),
                })

    return {
        'member': name, 'xml_bytes': len(raw), 'xml_sha256': hashlib.sha256(raw).hexdigest(),
        'root': local(root.tag), 'root_attributes': dict(root.attrib),
        'element_count': len(elements), 'tag_counts': dict(sorted(tags.items())),
        'tei_count': tags['TEI'], 'text_count': tags['text'], 'body_count': len(bodies),
        'pb_total': len(pbs), 'pb_with_n': sum(p.get('n') is not None for p in pbs),
        'all_pb_n': [p.get('n') for p in pbs],
        'exact_86v_pb': sum(p.get('n') == '86v' for p in pbs),
        'exact_87r_pb': sum(p.get('n') == '87r' for p in pbs),
        'pb_folio_records': all_pages,
        'num_types': dict(sorted(Counter(e.get('type') or '(no type)' for e in nums).items())),
        'chapnum_count': len(chapters),
        'chapnum_n_one_count': sum(e.get('n') == '1' for e in nums if e.get('type') == 'chapNum'),
        'chapnum_n_one_records': [e for e in chapters if e.get('n') == '1'],
        'chapnum_candidates_near_focus': [e for e in chapters if e.get('n') in ('1','2','3','4','5','6') and
                                            e.get('body_index') in {p['body_index'] for p in all_pages if p['n'] in FOCUS}],
        'div_identifiers': [dict(type=d.get('type'), n=d.get('n'), subtype=d.get('subtype'),
                                 **scoped(d)) for d in divs],
        'explicit_titus_divisions': [dict(type=d.get('type'), n=d.get('n'),
                                           **scoped(d)) for d in divs
                                     if any('titus' in (d.get(k) or '').lower() for k in ('type','n','subtype'))],
        'focus_attribute_records': focus_attributes,
        'bodies': body_rows,
        'caution': 'Structural and lexical candidate inventory only; no GA015 Titus K1 attestation or reading.'
    }


def inspect_zip(archive):
    if len(archive) > MAX_ZIP:
        raise ValueError('ZIP too large')
    out = {'dataset_doi': DOI, 'source_url': URL,
           'zip_sha256': hashlib.sha256(archive).hexdigest(), 'members': []}
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        names = z.infolist()
        if len(names) > 300 or sum(x.file_size for x in names) > MAX_UNCOMPRESSED:
            raise ValueError('oversized ZIP inventory')
        for x in names:
            if x.file_size > MAX_MEMBER or x.filename.startswith('/') or '..' in x.filename.split('/'):
                raise ValueError('unsafe ZIP member')
            if x.filename.endswith('.xml'):
                out['members'].append(inspect_xml(x.filename, z.read(x)))
    return out


def main():
    p = argparse.ArgumentParser()
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--zip', type=Path)
    group.add_argument('--download', action='store_true')
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    if args.download:
        with urlopen(Request(URL, headers={'User-Agent': 'CODH01-Global-TEI-Audit/0.1'}), timeout=45) as r:
            raw = r.read(MAX_ZIP + 1)
    else:
        raw = args.zip.read_bytes()
    obj = inspect_zip(raw)
    result = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    if args.output:
        args.output.write_text(result, encoding='utf-8')
    for m in obj['members']:
        print(json.dumps({
            'doi': DOI, 'zip_sha256': obj['zip_sha256'], 'member': m['member'],
            'xml_sha256': m['xml_sha256'], 'root': m['root'],
            'tei': m['tei_count'], 'text': m['text_count'], 'bodies': m['body_count'],
            'pbs': m['pb_total'], 'all_pb_n': m['all_pb_n'],
            'num_types': m['num_types'], 'chapnum_count': m['chapnum_count'],
            'chapnum_one_count': m['chapnum_n_one_count'],
            'chapnum_one_records': m['chapnum_n_one_records'],
            'titus_divs': m['explicit_titus_divisions'],
            'focus_attrs': m['focus_attribute_records'],
            'body_overview': [{k: b[k] for k in ('body_index', 'tei_id', 'page_breaks',
                               'chapter_numbers', 'division_count', 'lexical_stem_matches')}
                               for b in m['bodies']],
        }, ensure_ascii=False, sort_keys=True))
    print('NO K1 MATERIAL READING CERTIFIED. See full JSON manifest for all div/head/tag records.')


if __name__ == '__main__':
    main()
