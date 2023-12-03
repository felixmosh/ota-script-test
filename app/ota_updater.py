from app.lib.http_client import HttpClient
from app.lib.tarfile import TarFile
from app.lib.gzip import decompress
import os


class OTAUpdater:
    def __init__(
        self,
        github_repo,
        app_dir="app",
        new_version_dir="next",
    ):
        self.http_client = HttpClient(headers={"User-Agent": "MicroPython Client"})
        self.github_repo = github_repo.rstrip("/")
        self.app_dir = app_dir
        self.new_version_dir = new_version_dir

    def __del__(self):
        self.http_client = None

    def download_release(self, latest_release):
        tar_url = latest_release.get("tarball_url")

        print('Downloading "%s"...' % tar_url)

        local_filename = (
            self.new_version_dir
            + "/"
            + self.get_latest_version(latest_release)
            + ".tar.gz"
        )

        if not self._exists_dir(self.new_version_dir):
            self.mkdir(self.new_version_dir)

        self.http_client.get(tar_url, saveToFile=local_filename)
        decompress
        with open(local_filename[:-3], "wb") as f:
            f.write
        t = TarFile(local_filename)
        for i in t:
            print(i.name)

    def compare_versions(self, current_version: str, latest_version: str):
        if latest_version.startswith("v"):
            latest_version = latest_version[1:]

        if current_version.startswith("v"):
            current_version = current_version[1:]

        print(
            "currentVersion: %s, latestVersion: %s" % (current_version, latest_version)
        )

        return self._version_as_tuple(latest_version) > self._version_as_tuple(
            current_version
        )

    def get_latest_version(self, latest_release):
        latest_version = "0.0.0"

        if latest_release:
            latest_version = latest_release.get("tag_name", "v0.0.0")

        return latest_version

    def get_latest_release(self):
        print("Fetching latest release...")
        latest_release = self.http_client.get(
            f"https://api.github.com/repos/{self.github_repo}/releases/latest",
        )

        try:
            if latest_release.status_code == 200:
                latest_release = latest_release.json()
                return latest_release
        except Exception as e:
            print("Exception", e)
        return None

    def mkdir(self, path: str):
        try:
            os.mkdir(path)
        except OSError as exc:
            if exc.args[0] == 17:
                pass

    def _version_as_tuple(self, v: str):
        return tuple(map(int, (v.split("."))))

    def _exists_dir(self, path) -> bool:
        try:
            os.listdir(path)
            return True
        except:
            return False
