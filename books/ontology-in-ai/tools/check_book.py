"""Check manuscript completeness, local links, metadata, and the built EPUB."""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
from build_book import BOOK, REPO, TUTORIAL, documents, headings, target_path, validate_epub, write


def main() -> None:
    issues = []
    chapters = sorted((BOOK / 'chapters').glob('*.md'))
    lessons = sorted((TUTORIAL / 'lessons').glob('*.md'))
    if len(chapters) != 18 or len(lessons) != 10:
        issues.append('Expected 18 chapters and 10 lessons.')
    for number, chapter in enumerate(chapters, 1):
        text = chapter.read_text(encoding='utf-8')
        questions = text.split('## 思考题\n', 1)
        if len(questions) != 2 or re.findall(r'^(\d)\. ', questions[-1], re.M) != ['1', '2']:
            issues.append(f'Chapter {number} does not contain exactly two numbered questions.')
    answers = re.findall(r'^### (\d{2}\.\d) ', (BOOK / 'exercise-answers.md').read_text(encoding='utf-8'), re.M)
    expected_answers = [f'{i:02}.{j}' for i in range(1, 19) for j in (1, 2)]
    if answers != expected_answers:
        issues.append('Answer identifiers do not cover all 36 questions.')
    registry = json.loads((BOOK / 'references/registry.json').read_text(encoding='utf-8'))
    source_ids = {r['id'] for r in registry['sources']}
    if source_ids != {f'R{i:02}' for i in range(1, 41)} or registry['count'] != 40 or len(registry['sources']) != 40:
        issues.append('Reference registry must contain R01–R40 exactly once.')
    if any(r['http_status'] != 200 for r in registry['sources']):
        issues.append('A reference was not successfully retrieved.')

    parser = MarkdownIt('commonmark', {'html': True}).enable('table')
    markdown_files = [REPO / 'README.md', *sorted(BOOK.rglob('*.md')), *sorted(TUTORIAL.rglob('*.md'))]
    markdown_files = [p for p in markdown_files if '.runs' not in p.parts and '.venv' not in p.parts]
    local_links = 0
    external_links = set()
    for path in markdown_files:
        text = path.read_text(encoding='utf-8')
        if '\ufffd' in text or '\x00' in text:
            issues.append(f'Invalid replacement or NUL character: {path.relative_to(REPO)}')
        if len(re.findall(r'^```', text, re.M)) % 2:
            issues.append(f'Unbalanced code fence: {path.relative_to(REPO)}')
        for token in parser.parse(text):
            for child in token.children or []:
                target = child.attrGet('href') if child.type == 'link_open' else child.attrGet('src') if child.type == 'image' else None
                if not target:
                    continue
                parsed = urlsplit(target)
                if parsed.scheme or target.startswith('//'):
                    external_links.add(target)
                    continue
                destination, fragment = target_path(path.resolve(), target)
                if destination == BOOK / 'validation-report.json':
                    # This command writes that report after completing all checks.
                    local_links += 1
                    continue
                if not destination.exists():
                    issues.append(f'Missing link from {path.relative_to(REPO)}: {target}')
                elif fragment and destination.suffix == '.md' and unquote(fragment) not in headings(destination.read_text(encoding='utf-8')):
                    issues.append(f'Missing anchor from {path.relative_to(REPO)}: {target}')
                local_links += 1

    for folder in (BOOK, TUTORIAL):
        for path in folder.rglob('*.json'):
            if '.runs' not in path.parts and '.venv' not in path.parts:
                json.loads(path.read_text(encoding='utf-8'))

    build = json.loads((BOOK / 'build-report.json').read_text(encoding='utf-8'))
    for doc in documents():
        relative = doc.path.relative_to(REPO).as_posix()
        if build['sources'].get(relative) != hashlib.sha256(doc.path.read_bytes()).hexdigest():
            issues.append(f'Rebuild required for changed source: {relative}')
    if build['builder_sha256'] != hashlib.sha256((BOOK / 'tools/build_book.py').read_bytes()).hexdigest():
        issues.append('Builder changed after the recorded build.')
    epub_path = BOOK / 'dist/ontology-in-ai.epub'
    if hashlib.sha256(epub_path.read_bytes()).hexdigest() != build['epub_sha256']:
        issues.append('EPUB hash differs from the build record.')
    if hashlib.sha256((BOOK / 'book.md').read_bytes()).hexdigest() != build['markdown_sha256']:
        issues.append('Combined Markdown hash differs from the build record.')
    with zipfile.ZipFile(epub_path) as archive:
        if archive.testzip() is not None:
            issues.append('EPUB ZIP CRC failed.')
        first = archive.infolist()[0]
        if first.filename != 'mimetype' or first.compress_type != zipfile.ZIP_STORED or archive.read('mimetype') != b'application/epub+zip':
            issues.append('EPUB mimetype packaging failed.')
        epub_checks = validate_epub({name: archive.read(name) for name in archive.namelist()})

    verification = json.loads((TUTORIAL / 'reports/verification.json').read_text(encoding='utf-8'))
    digest = hashlib.sha256()
    for path in sorted((TUTORIAL / 'ontology_lab').glob('*.py')):
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    if verification['implementation_sha256'] != digest.hexdigest():
        issues.append('Tutorial implementation changed after its verification report.')
    for relative, expected in verification['input_sha256'].items():
        if hashlib.sha256((TUTORIAL / relative).read_bytes()).hexdigest() != expected:
            issues.append(f'Tutorial input changed after verification: {relative}')
    report = {'chapters': len(chapters), 'lessons': len(lessons), 'answers': len(answers),
              'references': len(source_ids), 'markdown_files': len(markdown_files),
              'local_links_checked': local_links, 'unique_external_links': len(external_links),
              'external_link_scope': 'Structural inventory only; research source access is recorded separately.',
              'epub': epub_checks, 'issues': issues, 'passed': not issues}
    write(BOOK / 'validation-report.json', json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if issues:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
