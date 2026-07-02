# build.spec
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('core', 'core'),
        ('ui', 'ui'),
        ('utils', 'utils'),
    ],
    hiddenimports=[
        'core.storage',
        'core.models',
        'ui.ribbon',
        'ui.file_explorer',
        'ui.editor',
        'ui.status_bar',
        'ui.graph_widget',
        'ui.search_panel',
        'ui.tags_panel',
        'ui.daily_notes_panel',
        'ui.templates_panel',
        'ui.daily_note_dialog',
        'ui.gamedev_panel',
        'ui.gamedev_window',
        'ui.gamedev_main_window',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ObsidianClone',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
)