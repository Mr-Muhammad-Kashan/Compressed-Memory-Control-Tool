# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/OneDrive/Desktop/Compressed Memory/compressed_memory_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/OneDrive/Desktop/Compressed Memory/Personal_Picture.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='compressed_memory_gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\OneDrive\\Desktop\\Compressed Memory\\Personal_Picture.ico'],
)
