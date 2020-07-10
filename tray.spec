# -*- mode: python ; coding: utf-8 -*-

# pyinstaller tray.spec --distpath=D:\PythonVENV\mist-app\dist --workpath=D:\PythonVENV\mist-app\build

block_cipher = None

additional_files = [
    ("assets/icons/*.*", "assets/icons"),
    ("server", "server"),
    ("tracker", "tracker"),
    ("main_config.ini", "."),
]

a = Analysis(['tray.py'],
             pathex=['D:\\OneDrive\\Development\\Mist_App'],
             binaries=[],
             datas=additional_files,
             hiddenimports=['win32timezone', 'plyer.platforms.win.notification', 'pkg_resources.py2_warn'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='tray',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='tray')
