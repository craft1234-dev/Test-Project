import os
import re
import shutil

class VersionUpdater:
    def __init__(self, source_path, build_num):
        self.source_path = source_path
        self.build_num = build_num
        self.files_to_update = [
            "SConstruct",
            "VERSION"
        ]

    def _get_file_path(self, filename):
        return os.path.join(self.source_path, "develop", "global", "src", filename)

    def _update_file(self, filename, pattern, replacement):
        file_path = self._get_file_path(filename)
        temp_path = file_path + ".tmp"

        try:
            with open(file_path, 'r') as fin, open(temp_path, 'w') as fout:
                for line in fin:
                    updated_line = re.sub(pattern, replacement, line)
                    fout.write(updated_line)

            os.chmod(file_path, 0o755)
            shutil.move(temp_path, file_path)

        except IOError as e:
            print(f"Error updating {filename}: {e}")

    def update_sconstruct(self):
        self._update_file(
            "SConstruct", 
            r"point=\d+", 
            f"point={self.build_num}"
        )

    def update_version_file(self):
        self._update_file(
            "VERSION", 
            r"ADLMSDK_VERSION_POINT=\d+", 
            f"ADLMSDK_VERSION_POINT={self.build_num}"
        )

    def execute(self):
        self.update_sconstruct()
        self.update_version_file()

def main():
    source_path = os.environ.get("SourcePath")
    build_num = os.environ.get("BuildNum")

    if not source_path or not build_num:
        raise ValueError("SourcePath and BuildNum environment variables must be set")

    updater = VersionUpdater(source_path, build_num)
    updater.execute()

if __name__ == "__main__":
    main()