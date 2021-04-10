import os
from pathlib import Path
import shutil


class Filesystem:
    @staticmethod
    def create_dir(path: Path, access_rights=0o755) -> bool:
        try:
            print(f"* Creating dir {path}")
            os.makedirs(str(path), access_rights, exist_ok=True)
            return True
        except OSError as err:
            print(f"  creation failed: {err}")
            return False

    @staticmethod
    def remove_dir(path: Path) -> bool:
        try:
            print(f"* Removing dir {path}")
            shutil.rmtree(str(path), ignore_errors=True)
            return True
        except OSError as err:
            print(f"  removal failed: {err}")
            return False

    @staticmethod
    def write_file(path: Path, content: str) -> bool:
        try:
            print(f"* Writing file at {path}")
            with open(str(path), "w") as file:
                file.write(content)
            return True
        except OSError as err:
            print(f"  writing failed: {err}")
            return False

    @staticmethod
    def remove_file(path: Path) -> bool:
        try:
            print(f"* Removing file at {path}")
            os.remove(str(path))
            return True
        except OSError as err:
            print(f"  removal failed: {err}")
            return False


# ------------------------- Mocks -----------------------


class MockFilesystem(Filesystem):
    @staticmethod
    def create_dir(path: Path, access_rights=0o755) -> bool:
        print(f"* Creating dir {path}")
        return True

    @staticmethod
    def remove_dir(path: Path) -> bool:
        print(f"* Removing dir {path}")
        return True

    @staticmethod
    def write_file(path: Path, content: str) -> bool:
        print(f"* Writing file at {path}")
        return True

    @staticmethod
    def remove_file(path: Path) -> bool:
        print(f"* Removing file at {path}")
        return True
