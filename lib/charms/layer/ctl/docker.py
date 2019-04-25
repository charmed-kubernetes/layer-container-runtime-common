from subprocess import check_output

from .__base__ import ContainerRuntimeCtlBase


class DockerCtl(ContainerRuntimeCtlBase):
    """
    Control Containerd via `docker`.
    """
    def __init__(self):
        """
        :return: None
        """
        super().__init__()

    def _exec(self, *args):
        """
        Run `docker`.

        :param args: List args
        :return: String return from ctr
        """
        return check_output(['docker'] + list(args))

    def run(self, name, image, command=None, *args):
        """
        Run a container.

        :param name: String
        :param image: String
        :param command: String
        :param args: List String
        :return: String output
        """
        if command:
            return self._exec(
                'run', '--name', name, image, command, *args
            )
        else:
            return self._exec(
                'run', '--name', name, image, *args
            )

    def delete(self, *container_ids):
        """
        Delete a container.

        :param container_ids: String
        :return: String output
        """
        return self._exec(
            'rm', '-f', *container_ids
        )
