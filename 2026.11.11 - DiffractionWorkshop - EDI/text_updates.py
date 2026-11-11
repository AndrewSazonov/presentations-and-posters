"""Text review for this workshop deck; preserve all slide markup and timings."""
TEXT_UPDATES = {
    '11_user-friction.html': [
        ('What users ran into', 'Limits of existing tools'),
    ],
    '12_needs.html': [
        ('<h3>Needs</h3>', '<h3>What EasyDiffraction should offer</h3>'),
    ],
    '13_libraries.html': [
        ('We start from <span class="blue">the libraries</span>, not the programs.',
         'Reuse <span class="blue">the libraries</span> behind existing programs.'),
    ],
    '13b_library-capabilities.html': [
        ('Each for <span class="blue">the functionality we need</span>.',
         'Different libraries for <span class="blue">different analysis methods</span>.'),
    ],
    '18b_modern-analysis.html': [
        ('EasyDiffraction works today, but <span class="blue">not fast enough</span>.',
         'The earlier approach becomes <span class="blue">slow for large datasets</span>.'),
    ],
    '19_future.html': [
        ('A possible future: <span class="blue">alongside existing libraries</span>.',
         'A possible future: crysta <span class="blue">alongside existing libraries</span>.'),
    ],
    '26_magnetism.html': [
        ('Connect the fit with <span class="blue">a structural picture</span>.',
         'Inspect the <span class="blue">magnetic moments after refinement</span>.'),
    ],
    '35_ai-external.html': [
        ('External assistants can <span class="blue">prepare work for every interface</span>.',
         'External assistants can prepare <span class="blue">projects, scripts and notebooks</span>.'),
    ],
}

for filename, replacements in TEXT_UPDATES.items():
    path = S / filename
    content = path.read_text()
    for before, after in replacements:
        content = content.replace(before, after)
    path.write_text(content)
    heading = re.search(r'<h3[^>]*>(.*?)</h3>', content, re.S)
    if filename in meta and heading:
        meta[filename]['title'] = re.sub(r'<[^>]+>', '', heading.group(1))

# Keep repeated provenance notes once; regenerating slides must not duplicate them.
for path in S.glob('*.html'):
    def unique_notes(match):
        chunks = re.split(r'<br\s*/?>\s*', match.group(1))
        return '<aside class="notes">' + '<br>'.join(dict.fromkeys(c for c in chunks if c.strip())) + '</aside>'
    path.write_text(re.sub(r'<aside class="notes">(.*?)</aside>', unique_notes, path.read_text(), flags=re.S))
