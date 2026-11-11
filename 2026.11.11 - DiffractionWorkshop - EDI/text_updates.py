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

# Pass 2: grammar, terminology and plain wording.
GRAMMAR_UPDATES = {'11_user-friction.html': [('Not the best UX', 'Difficult interface'),
                           ('High entrance barrier', 'Hard to get started'),
                           ('input files with cryptic labels', 'input files with unclear labels'),
                           ('XQuartz to install on macOS', 'XQuartz needed on macOS'),
                           ('Not cross-platform', 'Limited platform support'),
                           ('Gaps for the ESS instruments, and <span class="blue">a steep start</span> for '
                            'new users.',
                            'Gaps for ESS instruments and <span class="blue">a difficult start</span> for '
                            'new users.')],
 '13b_library-capabilities.html': [('mature, wide coverage', 'broad diffraction support'),
                                   ('more polarised-neutron options', 'polarised-neutron analysis')],
 '15_ux.html': [('cleaner, lighter', 'a clearer interface'),
                ('the same shape,', 'a familiar layout,'),
                ('still intuitive', 'the same workflow')],
 '16_ux-review.html': [('Then they reviewed <span class="blue">our interface</span>.',
                        'Review of <span class="blue">the EasyDiffraction interface</span>.')],
 '22_physics.html': [('neutron single crystal', 'neutron single-crystal')],
 '27c_fit-loop.html': [('10 &ndash; 200 parameters', '10&ndash;200 parameters')],
 '34_ai-desktop.html': [('Ask, inspect the actions, and <span class="blue">check the resulting fit</span>.',
                         'Ask, inspect the actions and <span class="blue">check the fit</span>.')],
 '35_ai-external.html': [('documentation and fit stages', 'documentation and refinement stages'),
                         ('Use it in Python, the web or desktop app, or the command line',
                          'Use Python, the web or desktop app, or the command line')],
 '36_software.html': [('Source and issue tracking on GitHub', 'Source code and issue tracking on GitHub'),
                      ('Step backwards or forwards through edits', 'Undo or redo changes'),
                      ('Choose the display you prefer', 'Choose the theme you prefer')],
 '37_status.html': [('Work in progress / Next steps', 'Work in progress / next steps')],
 '38_hands-on.html': [('No preparation or advance download of materials needed',
                       'No preparation or downloads needed in advance'),
                      ('A flexible set of examples, with help when you need it',
                       'Choose examples and ask for help when needed')]}
for filename, replacements in GRAMMAR_UPDATES.items():
    TEXT_UPDATES.setdefault(filename, []).extend(replacements)

# Pass 3: a fresh consistency and clarity review of the complete sequence.
CONSISTENCY_UPDATES = {'18_advanced-library.html': [('HRPT / PSI · DREAM</p>', 'HRPT / PSI · DREAM sampler</p>')],
 '18b_modern-analysis.html': [('huge parameter spaces', 'large parameter spaces'),
                              ('experiments that run themselves', 'repeatable analysis'),
                              ('no human in the loop', 'less manual intervention')],
 '27_verification.html': [('WISH 2+9', 'WISH · banks 2+9'),
                          ('3977 points', '3,977 points'),
                          ('Largest difference 3.9 of 7527 counts: <span class="blue">0.05&nbsp;%</span>.',
                           'Maximum difference: 3.9 of 7,527 counts (<span '
                           'class="blue">0.05&nbsp;%</span>).'),
                          ('7527-count peak', '7,527-count peak')],
 '28_speed.html': [('same start</span>', 'Same start</span>')],
 '24_application.html': [('Measured data, model and <span class="blue">fitted parameters together</span>.',
                          'Data, model and <span class="blue">fitted parameters in one view</span>.')],
 '26_magnetism.html': [('Inspect the <span class="blue">magnetic moments after refinement</span>.',
                        'View the <span class="blue">refined magnetic moments</span>.')],
 '37_status.html': [('Port existing capabilities', 'Port earlier capabilities'),
                    ('PDF and Bayesian analysis · available before crysta', 'PDF and Bayesian analysis')]}
for filename, replacements in CONSISTENCY_UPDATES.items():
    TEXT_UPDATES.setdefault(filename, []).extend(replacements)

# Independent review: clarify the percentage and align the AI outputs.
REVIEW_UPDATES = {'27_verification.html': [('Maximum difference: 3.9 of 7,527 counts (<span '
                           'class="blue">0.05&nbsp;%</span>).',
                           'Maximum difference: 3.9 counts (<span class="blue">0.05% of peak '
                           'height</span>).')],
 '35_ai-external.html': [('Ask for a notebook or project', 'Ask for a project, script or notebook')]}
for filename, replacements in REVIEW_UPDATES.items():
    TEXT_UPDATES.setdefault(filename, []).extend(replacements)

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
