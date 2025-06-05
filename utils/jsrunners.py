import subprocess
import os
from typing import List, Union

# setup path incase it does not exist
if os.getenv("PATH", None) is None:
    os.environ["PATH"] = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

if "/bin" not in os.environ["PATH"]:
    os.environ["PATH"] = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin" + ":" + os.environ["PATH"]

class CommandRunner:

    @staticmethod
    def run(command: List[str]) -> subprocess.CompletedProcess:
        return subprocess.run(command, check=True, stdout=subprocess.PIPE)


class Installer:

    @staticmethod
    def install(url: str,
                target_folder_name: str = None,
                untar: bool = False,
                untar_file_name: str = None,
                relative_sys_paths_to_add: List[str] = None):
        print(f"Installing {url}")
        if target_folder_name is not None and os.path.exists(target_folder_name) is False:
            os.mkdir(target_folder_name)
        resp = CommandRunner.run(["wget", url])
        if resp.returncode == 0:
            if untar:
                file_name = untar_file_name or url.split("/")[-1]
                print(f"Untarring {file_name}")
                if target_folder_name is None:
                    resp = CommandRunner.run(["tar", "-xf", file_name])
                else:
                    resp = CommandRunner.run(
                        ["tar", "--strip-components", "1", "-xf", file_name, "-C", target_folder_name])
                if resp.returncode == 0:
                    os.remove(file_name)
            if relative_sys_paths_to_add:
                cwd = os.getcwd()
                for path in relative_sys_paths_to_add:
                    if path.startswith("/"):
                        path = path[1:]
                    print(f"Adding {cwd}/{path} to PATH")
                    os.environ["PATH"] = f"{cwd}/{path}:{os.environ['PATH']}"


class NodeJSLTS:
    V18_LTS = "v18.20.3"


class OperatingSystem:
    LINUX = "linux"
    MACOS = "macos"


class NodeJSInstaller:
    def __init__(self,
                 target_folder_name: str = None,
                 version=NodeJSLTS.V18_LTS,
                 _os=OperatingSystem.LINUX,
                 arch="x64"):
        self.version = version
        self.os = _os
        self.arch = arch
        self.target_folder_name = target_folder_name or "nodejs_download"

    def _download_url(self):
        return f"https://nodejs.org/dist/{self.version}/node-{self.version}-{self.os}-{self.arch}.tar.xz"

    def install(self):
        Installer.install(
            url=self._download_url(),
            target_folder_name=self.target_folder_name,
            untar=True,
            relative_sys_paths_to_add=[f"{self.target_folder_name}/bin"]
        )

    def sys_path(self):
        return f"{os.getcwd()}/{self.target_folder_name}/bin"

    def node_path(self):
        return f"{os.getcwd()}/{self.target_folder_name}/bin/node"

    def npm_path(self):
        return f"{os.getcwd()}/{self.target_folder_name}/bin/npm"

    def npx_path(self):
        return f"{os.getcwd()}/{self.target_folder_name}/bin/npx"


class GolangInstaller:

    def __init__(self,
                 target_folder_name: str = None,
                 version="1.22.4",
                 _os=OperatingSystem.LINUX,
                 arch="x64"):
        self.target_folder_name = target_folder_name or "go_download"
        self.version = version
        self.os = _os
        self.arch = arch

    def _download_url(self):
        # ex "https://go.dev/dl/go1.22.4.darwin-arm64.tar.gz"
        return f"https://go.dev/dl/go{self.version}.{self.os}-{self.arch}.tar.gz"

    def install(self):
        Installer.install(
            url=self._download_url(),
            target_folder_name=self.target_folder_name,
            untar=True,
            relative_sys_paths_to_add=[f"{self.target_folder_name}/bin"]
        )

    def sys_path(self):
        return f"{os.getcwd()}/{self.target_folder_name}/bin"

    def go_path(self):
        return f"{os.getcwd()}/{self.target_folder_name}/bin/go"


class BinaryCommandRunner:

    def __init__(self, ):
        self.binary_path = None

    def configure(self, binary_path: str):
        self.binary_path = binary_path

    def run(self, command: List[str]) -> subprocess.CompletedProcess:
        return subprocess.run([self.binary_path] + command, check=True)


class NodeJsEntrypoint:

    def __init__(self,
                 version=NodeJSLTS.V18_LTS,
                 _os=OperatingSystem.LINUX,
                 arch="x64"):
        self._installer = NodeJSInstaller(version=version, _os=_os, arch=arch)
        self.npm_command_runner = BinaryCommandRunner()
        self.npx_command_runner = BinaryCommandRunner()
        self._commands = []
        self._chdir = None

    def with_command(self, command: Union[List[str], str]):
        if isinstance(command, str):
            command = command.split(" ")
        if command[0] == "npm":
            command = command[1:]

        self._commands.append(command)
        return self

    def with_cwd(self, cwd: str):
        self._chdir = cwd
        return self

    def _configure_sys_path(self):
        if self._installer.sys_path() not in os.environ["PATH"]:
            os.environ["PATH"] = f"{self._installer.sys_path()}:{os.environ['PATH']}"

    def _setup_binaries(self):
        if self._chdir:
            os.chdir(self._chdir)

        node_path = self._installer.node_path()
        npm_path = self._installer.npm_path()
        npx_path = self._installer.npx_path()
        if os.path.exists(node_path) is False or os.path.exists(npm_path) is False:
            self._installer.install()

        self.npm_command_runner.configure(npm_path)
        self.npx_command_runner.configure(npx_path)

    def run(self):
        self._setup_binaries()
        self._configure_sys_path()
        for command in self._commands:
            print(f"Running {command}")
            resp = self.npm_command_runner.run(command)
            # resp = self.npx_command_runner.run(command)
            print(resp)


class GolangEntrypoint:

    def __init__(self,
                 version="1.22.4",
                 _os=OperatingSystem.LINUX,
                 arch="amd64"):
        self._installer = GolangInstaller(version=version, _os=_os, arch=arch)
        self.command_runner = BinaryCommandRunner()
        self._commands = []
        self._chdir = None

    def with_command(self, command: Union[List[str], str]):
        if isinstance(command, str):
            command = command.split(" ")
        if command[0] == "go":
            command = command[1:]

        self._commands.append(command)
        return self

    def with_cwd(self, cwd: str):
        self._chdir = cwd
        return self

    def _configure_sys_path(self):
        if self._installer.sys_path() not in os.environ["PATH"]:
            os.environ["PATH"] = f"{self._installer.sys_path()}:{os.environ['PATH']}"
        os.environ["GOCACHE"] = f"{os.getcwd()}/gocache"

    def _setup_binaries(self):
        if self._chdir:
            os.chdir(self._chdir)

        go_path = self._installer.go_path()
        if os.path.exists(go_path) is False:
            self._installer.install()

        self.command_runner.configure(go_path)

    def run(self):
        self._setup_binaries()
        self._configure_sys_path()
        for command in self._commands:
            print(f"Running {command}")
            resp = self.command_runner.run(command)
            if resp.returncode != 0:
                print(f"Error running {command}")
                break