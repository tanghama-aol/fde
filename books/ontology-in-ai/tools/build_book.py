"""Build the combined Markdown, EPUB 3, and local XHTML preview from the manuscript."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import posixpath
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit
from xml.etree import ElementTree as ET

from markdown_it import MarkdownIt

BOOK = Path(__file__).resolve().parents[1]
REPO = BOOK.parents[1]
TUTORIAL = REPO / 'tutorials/ontology-ai'
TITLE = '本体在 AI 中的应用：原理、工程与实战'
REPO_URL = 'https://github.com/tanghama-aol/fde'
EDITION = '2026-09-14'
XHTML = 'http://www.w3.org/1999/xhtml'
LINK = re.compile(r'(!?\[[^\]\n]*\]\()([^\s)]+)(\))')
ANCHOR = re.compile(r'<a\s+id="([^"]+)"\s*></a>')


@dataclass
class Document:
    path: Path
    key: str
    title: str
    text: str


def write(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value.encode('utf-8'))


def slug(value: str) -> str:
    value = re.sub(r'<[^>]+>', '', value).strip().lower()
    value = re.sub(r'[^\w\s-]', '', value, flags=re.UNICODE)
    return re.sub(r'\s', '-', value)


def headings(text: str) -> set[str]:
    result = set(ANCHOR.findall(text))
    seen = {}
    fence = False
    for line in text.splitlines():
        if line.startswith('```'):
            fence = not fence
        if not fence and re.match(r'^#{1,6} ', line):
            base = slug(line.split(' ', 1)[1])
            number = seen.get(base, 0)
            seen[base] = number + 1
            result.add(base + (f'-{number}' if number else ''))
    return result


def documents() -> list[Document]:
    paths = [(BOOK / 'preface.md', 'preface')]
    paths += [(p, f'ch{i:02}') for i, p in enumerate(sorted((BOOK / 'chapters').glob('*.md')), 1)]
    paths += [(BOOK / 'glossary.md', 'glossary'), (BOOK / 'exercise-answers.md', 'answers'),
              (BOOK / 'references/README.md', 'references'), (TUTORIAL / 'README.md', 'tutorial')]
    paths += [(p, f'lesson{i:02}') for i, p in enumerate(sorted((TUTORIAL / 'lessons').glob('*.md')), 1)]
    result = []
    for path, key in paths:
        text = path.read_text(encoding='utf-8')
        title = next(line[2:] for line in text.splitlines() if line.startswith('# '))
        result.append(Document(path.resolve(), key, title, text))
    return result


def target_path(source: Path, target: str) -> tuple[Path, str]:
    parsed = urlsplit(target.strip('<>'))
    destination = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source
    if destination.is_dir() and (destination / 'README.md').is_file():
        destination /= 'README.md'
    return destination, unquote(parsed.fragment)


def transform(doc: Document, all_docs: list[Document], mode: str) -> str:
    by_path = {d.path: d for d in all_docs}

    def replace(match: re.Match) -> str:
        target = match[2]
        parsed = urlsplit(target.strip('<>'))
        if parsed.scheme or target.startswith('//'):
            return match[0]
        destination, fragment = target_path(doc.path, target)
        if destination == BOOK / 'README.md':
            rewritten = '#book-title' if mode == 'markdown' else 'title.xhtml'
        elif destination in by_path:
            other = by_path[destination]
            if mode == 'markdown':
                rewritten = '#' + other.key + ('--' + fragment if fragment else '')
            else:
                rewritten = other.key + '.xhtml' + ('#' + fragment if fragment else '')
        elif mode == 'markdown':
            import os
            rewritten = Path(os.path.relpath(destination, BOOK)).as_posix()
            if fragment:
                rewritten += '#' + fragment
        else:
            relative = destination.relative_to(REPO).as_posix()
            kind = 'tree' if destination.is_dir() else 'blob'
            rewritten = f'{REPO_URL}/{kind}/main/{quote(relative)}'
            if fragment:
                rewritten += '#' + quote(fragment)
        return match[1] + rewritten + match[3]

    output = []
    fence = False
    seen = {}
    for line in doc.text.splitlines():
        if line.startswith('```'):
            fence = not fence
            output.append(line)
            continue
        if not fence:
            line = LINK.sub(replace, line)
            if mode == 'markdown':
                line = ANCHOR.sub(lambda m: f'<a id="{doc.key}--{m[1]}"></a>', line)
                heading = re.match(r'^(#{1,6}) (.+)$', line)
                if heading:
                    base = slug(heading[2])
                    count = seen.get(base, 0)
                    seen[base] = count + 1
                    anchor = base + (f'-{count}' if count else '')
                    output.extend([f'<a id="{doc.key}--{anchor}"></a>', ''])
                    line = '#' * min(len(heading[1]) + 1, 6) + ' ' + heading[2]
        output.append(line)
    return '\n'.join(output) + '\n'


def render(markdown: str) -> str:
    parser = MarkdownIt('commonmark', {'html': True, 'xhtmlOut': True}).enable('table')
    tokens = parser.parse(markdown)
    seen = {}
    for index, token in enumerate(tokens):
        if token.type == 'heading_open':
            base = slug(tokens[index + 1].content)
            count = seen.get(base, 0)
            seen[base] = count + 1
            token.attrSet('id', base + (f'-{count}' if count else ''))
    return parser.renderer.render(tokens, parser.options, {})


CSS = '''@charset "UTF-8";
html { color: #172d3a; background: #fff; }
body { margin: 6%; font-family: "Noto Serif CJK SC", "Source Han Serif SC", "Microsoft YaHei", serif;
       font-size: 1em; line-height: 1.8; text-align: left; }
h1,h2,h3,h4 { font-family: "Noto Sans CJK SC", "Microsoft YaHei", sans-serif; line-height: 1.4;
              color: #143c4c; page-break-after: avoid; }
h1 { font-size: 1.85em; margin: 0 0 1.3em; border-bottom: 2px solid #87b9bb; padding-bottom: .65em; }
h2 { font-size: 1.35em; margin-top: 2em; }
h3 { font-size: 1.1em; margin-top: 1.6em; }
p { margin: .85em 0; orphans: 2; widows: 2; }
a { color: #126776; text-decoration: underline; overflow-wrap: anywhere; }
ul,ol { padding-left: 1.6em; }
li { margin: .4em 0; }
table { border-collapse: collapse; width: 100%; font-size: .82em; margin: 1.2em 0; }
th,td { border-bottom: 1px solid #d6e1e4; text-align: left; vertical-align: top; padding: .65em .5em;
        overflow-wrap: anywhere; }
th { background: #edf4f3; color: #143c4c; font-weight: bold; }
th:first-child, td:first-child { overflow-wrap: normal; word-break: normal; }
tr { page-break-inside: avoid; }
code { font-family: Consolas, "Noto Sans CJK SC", monospace; font-size: .86em; overflow-wrap: anywhere; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; word-break: break-word; background: #f2f5f6;
      padding: 1em; border-left: 3px solid #87b9bb; line-height: 1.6; }
pre code { font-size: .8em; }
blockquote { margin: 1em 0; padding: .3em 1em; border-left: 3px solid #87b9bb; color: #48636c; }
.cover { min-height: 75vh; padding: 2em 0; }
.eyebrow { font-family: sans-serif; font-size: .85em; letter-spacing: .12em; color: #397b80; }
.cover h1 { font-size: 2.5em; border: none; margin-top: 1.3em; margin-bottom: .6em; }
.subtitle { font-size: 1.4em; color: #48636c; }
.cover .edition { margin-top: 4em; font-size: .9em; }
nav ol { list-style: none; padding-left: 0; }
nav li { border-bottom: 1px solid #e8eeee; padding: .35em 0; }
@media screen { body { max-width: 50em; margin: 3em auto; padding: 0 1.2em; } }
'''


def page(title: str, content: str) -> str:
    return ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
            f'<html xmlns="{XHTML}" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="zh-CN" lang="zh-CN">'
            f'<head><meta charset="utf-8"/><title>{html.escape(title)}</title>'
            '<meta name="viewport" content="width=device-width, initial-scale=1"/>'
            '<link rel="stylesheet" type="text/css" href="style.css"/></head><body>'
            + content + '</body></html>\n')


def validate_epub(entries: dict[str, bytes]) -> dict:
    documents = {}
    for name, data in entries.items():
        if name.endswith(('.xhtml', '.opf', '.xml')):
            documents[name] = ET.fromstring(data)
    anchors = {}
    for name, root in documents.items():
        ids = [element.attrib['id'] for element in root.iter() if 'id' in element.attrib]
        if len(ids) != len(set(ids)):
            raise ValueError(f'Duplicate IDs in {name}')
        anchors[name] = set(ids)
    checked = 0
    for name, root in documents.items():
        for element in root.iter():
            for attr in ('href', 'src'):
                value = element.get(attr)
                if not value:
                    continue
                url = urlsplit(value)
                if url.scheme:
                    continue
                target = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(url.path))) if url.path else name
                if target not in entries:
                    raise ValueError(f'Broken EPUB link: {name}: {value}')
                if url.fragment and unquote(url.fragment) not in anchors.get(target, set()):
                    raise ValueError(f'Broken EPUB anchor: {name}: {value}')
                checked += 1
    return {'xml_documents': len(documents), 'internal_links_checked': checked}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview-dir', type=Path, default=REPO / '.cache/ontology-book/preview')
    args = parser.parse_args()
    docs = documents()
    if len(list((BOOK / 'chapters').glob('*.md'))) != 18 or len(list((TUTORIAL / 'lessons').glob('*.md'))) != 10:
        raise ValueError('Expected 18 chapters and 10 lessons.')

    combined = ['<a id="book-title"></a>', '', f'# {TITLE}', '',
                f'第一版 · 中文 · 资料核验日期：{EDITION}', '',
                '本文件由分章书稿自动合并。末尾收录 10 课教程文字；运行代码与完整实测记录见仓库。', '', '## 目录', '']
    combined += [f'- [{doc.title}](#{doc.key})' for doc in docs]
    for doc in docs:
        combined += ['', '---', '', f'<a id="{doc.key}"></a>', '', transform(doc, docs, 'markdown')]
    markdown = '\n'.join(combined).rstrip() + '\n'
    write(BOOK / 'book.md', markdown)

    entries = {'mimetype': b'application/epub+zip',
               'META-INF/container.xml': b'<?xml version="1.0" encoding="UTF-8"?>\n<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>',
               'OEBPS/style.css': CSS.encode('utf-8')}
    title_content = ('<section class="cover" epub:type="titlepage"><p class="eyebrow">AI 工程实践</p>'
                     '<h1>本体在 AI 中<br/>的应用</h1><p class="subtitle">原理、工程与实战</p>'
                     '<p>从知识表示到有证据、可校验的智能应用</p>'
                     f'<p class="edition">第一版 · 中文<br/>资料核验日期：{EDITION}<br/>'
                     '18 章正文 · 10 课教程 · 36 道习题参考答案</p>'
                     f'<p><a href="{REPO_URL}">配套代码与实测记录</a></p></section>')
    entries['OEBPS/title.xhtml'] = page(TITLE, title_content).encode('utf-8')
    toc = '<h1>目录</h1><nav epub:type="toc" id="toc"><ol>'
    toc += '<li><a href="title.xhtml">书名页</a></li>'
    toc += ''.join(f'<li><a href="{doc.key}.xhtml">{html.escape(doc.title)}</a></li>' for doc in docs)
    toc += '</ol></nav>'
    entries['OEBPS/nav.xhtml'] = page('目录', toc).encode('utf-8')
    for doc in docs:
        entries[f'OEBPS/{doc.key}.xhtml'] = page(doc.title, render(transform(doc, docs, 'epub'))).encode('utf-8')

    manifest = '<item id="style" href="style.css" media-type="text/css"/>'
    manifest += '<item id="title" href="title.xhtml" media-type="application/xhtml+xml"/>'
    manifest += '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>'
    manifest += ''.join(f'<item id="{doc.key}" href="{doc.key}.xhtml" media-type="application/xhtml+xml"/>' for doc in docs)
    spine = '<itemref idref="title"/><itemref idref="nav"/>' + ''.join(f'<itemref idref="{doc.key}"/>' for doc in docs)
    package = ('<?xml version="1.0" encoding="utf-8"?>\n'
               '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id" xml:lang="zh-CN">'
               '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
               f'<dc:identifier id="book-id">{REPO_URL}/books/ontology-in-ai/edition-1</dc:identifier>'
               f'<dc:title>{html.escape(TITLE)}</dc:title><dc:language>zh-CN</dc:language>'
               '<dc:creator>FDE 知识库</dc:creator><dc:publisher>tanghama-aol/fde</dc:publisher>'
               f'<dc:date>{EDITION}</dc:date><meta property="dcterms:modified">{EDITION}T00:00:00Z</meta>'
               '</metadata><manifest>' + manifest + '</manifest><spine>' + spine + '</spine></package>')
    entries['OEBPS/package.opf'] = package.encode('utf-8')
    checks = validate_epub(entries)
    epub = BOOK / 'dist/ontology-in-ai.epub'
    epub.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(epub, 'w') as archive:
        for name, data in entries.items():
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 14, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED if name == 'mimetype' else zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    for name, data in entries.items():
        if name.startswith('OEBPS/') and name != 'OEBPS/package.opf':
            path = args.preview_dir / name.removeprefix('OEBPS/')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    report = {'schema_version': '1.0', 'edition_date': EDITION, 'chapters': 18, 'lessons': 10,
              'included_documents': len(docs), 'cjk_characters_in_combined_book': len(re.findall(r'[\u3400-\u9fff]', markdown)),
              'epub_bytes': epub.stat().st_size, 'epub_sha256': hashlib.sha256(epub.read_bytes()).hexdigest(),
              'markdown_sha256': hashlib.sha256(markdown.encode('utf-8')).hexdigest(),
              'builder_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'internal_validation': checks,
              'sources': {doc.path.relative_to(REPO).as_posix(): hashlib.sha256(doc.path.read_bytes()).hexdigest() for doc in docs}}
    write(BOOK / 'build-report.json', json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'sources'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
