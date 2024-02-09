# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Hack4GoodBOT\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('./Hack4GoodBOT/config/credentials.json', 'config'), ('./Hack4GoodBOT/certificate/*.png', 'certificate'), ('./Hack4GoodBOT/certificate/*.ttf', 'certificate')],
    hiddenimports=[],
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
