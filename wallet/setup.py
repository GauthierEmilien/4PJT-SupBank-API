import sys
from cx_Freeze import setup, Executable

import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
print(sys.platform)

options = {'build_exe': {
    # 'path': sys.path,
    'packages': ['asyncio', 'requests', 'engineio.async_drivers.threading', 'websocket'],
    'includes': ['idna.idnadata'],
    'include_msvcr': True
}
}
exe = Executable('main.py')

if sys.platform == 'win32':
    os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
    os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

    options['build_exe']['include_files'] = [
        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'libcrypto-1_1.dll'),
        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'libssl-1_1.dll')
    ]
    exe.targetName = 'Xatome.exe'

elif sys.platform == 'linux':
    exe.targetName = 'Xatome'

setup(name='XatomeCoin',
      version='0.1',
      description='Xatome Coin Miner',
      options=options,
      executables=[exe]
      )
