# -*- mode: python -*-
a = Analysis(['crop-test.py'],
             pathex=['C:\\Users\\Eyal\\Documents\\GitHub\\hs_identify'],
             hiddenimports=[],
             hookspath=['.'],
             runtime_hooks=None)

def extra_datas(mydir):
    def rec_glob(p, files):
        import os
        import glob
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
            rec_glob("%s/*" % d, files)
    files = []
    rec_glob("%s/*" % mydir, files)
    extra_datas = []
    for f in files:
        extra_datas.append((f, f, 'DATA'))

    return extra_datas

a.datas += [('dimensions_config', 'dimensions_config', 'DATA')]
a.datas += extra_datas('cards')

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='crop-test.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='crop-test')
