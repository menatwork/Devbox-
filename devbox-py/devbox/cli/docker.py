import subprocess


class DockerCmd(object):
    cmd_args: 'list[str]' = []

    def __init__(self, cmd_name: str, args: 'list[str]' = None):
        self.cmd_name = cmd_name
        if args:
            self.cmd_args = args

    def arg(self, value: str):
        self.cmd_args.append(value)

    def args(self, args: 'list[str]'):
        self.cmd_args.extend(args)

    def run(self):
        subprocess.run(['docker', self.cmd_name, *self.cmd_args], check=True)


def docker(cmd_name, *args):
    """
    Convenience function for DockerCmd(...).run()
    """
    DockerCmd(cmd_name, args).run()
