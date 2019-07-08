import os
import shutil
from pathlib import Path

from charmhelpers.core.hookenv import log


certs_dir = Path('/root/cdk')
ca_crt_path = certs_dir / 'ca.crt'
server_crt_path = certs_dir / 'server.crt'
server_key_path = certs_dir / 'server.key'
client_crt_path = certs_dir / 'client.crt'
client_key_path = certs_dir / 'client.key'


def manage_registry_certs(cert_dir, remove=False):
    """
    Add or remove TLS data for a specific registry.

    When present, the container runtime will use certificates when
    communicating with a specific registry.

    :param cert_dir: String directory to store the client certificates
    :param remove: Boolean remove cert data (defauts to add)
    :return: None
    """
    if remove:
        if os.path.isdir(cert_dir):
            log('Disabling registry TLS: {}.'.format(cert_dir))
            shutil.rmtree(cert_dir)
    else:
        os.makedirs(cert_dir, exist_ok=True)
        client_tls = {
            client_crt_path: os.path.join(cert_dir, 'client.cert'),
            client_key_path: os.path.join(cert_dir, 'client.key')
        }
        for f, link in client_tls.items():
            try:
                os.remove(link)
            except FileNotFoundError:
                pass
            log('Creating registry TLS link: {}.'.format(link))
            os.symlink(f, link)
