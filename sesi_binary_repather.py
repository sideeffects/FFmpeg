import re
import sys

import subprocess

def main(localdir, binary):
    # Binaries produced by the FFmpeg build system contain absolute paths to the 
    # built libaries. This tool rewrites them to work within Houdini.
    otool_output = subprocess.check_output(['otool', '-L', binary]).decode('utf-8')
    libraries_to_repath = re.findall(localdir + '/lib/([^/]+\.dylib)', otool_output)

    for library_to_repath in libraries_to_repath:
        change_from = localdir + '/lib/' + library_to_repath
        change_to   = '@loader_path/../../Libraries/' + library_to_repath

        cmd = ['install_name_tool', '-change', change_from, change_to, binary]
        print(' '.join(cmd))

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.communicate()

        if proc.returncode != 0:
            return 1

    return 0

if __name__ == '__main__':
    (_, localdir, binary) = sys.argv
    sys.exit(main(localdir, binary))

