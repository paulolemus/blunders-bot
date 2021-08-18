import logging
import os
import subprocess
import shutil

logger = logging.getLogger(__name__)

dirname = os.path.dirname(__file__)
# Blunders repository paths
submodule_folder = os.path.join(dirname, 'blunders')
engine_name = 'blunders'
engine_name_ext = 'blunders.exe'
engine_bin_folder = os.path.join(dirname, 'blunders/target/release/')

# Local engines path
engines_folder = os.path.join(dirname, 'engines')

def update_engine():
    """Build a local version of the Blunders engine.
    Requires the Blunders submodule to be pulled, and cargo to be installed locally.
    """
    args = dict(cwd=os.path.join(submodule_folder), capture_output=True, check=True)
    result = subprocess.run('cargo build --release', **args)

    if not result.returncode == 0:
        raise Exception(f"cargo build --release exited with returncode {result.returncode}")

    # Copy the built target over to the engines folder.
    engine_path = os.path.normpath(os.path.join(engine_bin_folder, engine_name))
    engine_path_ext = os.path.normpath(os.path.join(engine_bin_folder, engine_name_ext))

    if os.path.isfile(engine_path):
        logger.info(f"Copying from {engine_path} to {engines_folder}...")
        try:
            shutil.copy(engine_path, engines_folder)
        except shutil.SameFileError:
            pass

    elif os.path.isfile(engine_path_ext):
        logger.info(f"Copying from {engine_path_ext} to {engines_folder}...")
        try:
            shutil.copy(engine_path_ext, engines_folder)
        except shutil.SameFileError:
            pass

    else:
        raise Exception('Unable to copy Blunders executable to engines folder.')


if __name__ == '__main__':
    """Update engine without running bot."""
    update_engine()