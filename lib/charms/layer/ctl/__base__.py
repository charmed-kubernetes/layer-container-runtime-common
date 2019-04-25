class ContainerRuntimeCtlBase(object):
    """
    Base class for Container Runtime ctls.
    """
    def __init__(self):
        """
        :return: None
        """
        pass

    def _exec(self):
        """
        Call the underlying CLI.

        :return: String output
        """
        raise NotImplementedError

    def run(self, name, image, command=None, *args):
        """
        Run a container.

        :param name: String
        :param image: String
        :param command: String
        :param args: List String
        :return: String output
        """
        raise NotImplementedError

    def delete(self, *container_ids):
        """
        Delete a container.

        :param container_ids: String
        :return: String output
        """
        raise NotImplementedError
