import os
import shutil
import ipaddress
from pathlib import Path

from charmhelpers.core.hookenv import (
    log,
    env_proxy_settings
)


certs_dir = Path('/root/cdk')
ca_crt_path = certs_dir / 'ca.crt'
server_crt_path = certs_dir / 'server.crt'
server_key_path = certs_dir / 'server.key'
client_crt_path = certs_dir / 'client.crt'
client_key_path = certs_dir / 'client.key'


def get_hosts(config):
    if config is not None:
        hosts = []
        for address in config.get('NO_PROXY', "").split(","):
            address = address.strip()
            try:
                net = ipaddress.ip_network(address)
                ip_addresses = [str(ip) for ip in net.hosts()]
                if ip_addresses == []:
                    hosts.append(address)
                else:
                    hosts += ip_addresses
            except ValueError:
                hosts.append(address)
        parsed_hosts = ",".join(hosts)
        return parsed_hosts


def merge_config(config, environment):

    for key in ['HTTP_PROXY', 'http_proxy', 'HTTPS_PROXY', 'https_proxy',
                'NO_PROXY', 'no_proxy']:
        # We make the assumption here that
        # all environment keys are upper and lower case.
        if config.get(key.lower(), '') == '' and \
               config.get(key.upper(), '') == '' and environment.get(key, '') != '':
            value = environment.get(key)
            config[key.upper()] = value
            config[key.lower()] = value

    return config


def check_for_juju_https_proxy(config):
    # If juju environment variables are defined, take precedent
    # over config.yaml.
    # See: https://github.com/dshcherb/charm-helpers/blob/eba3742de6a7023f22778ba58fbbb0ac212d2ea6/charmhelpers/core/hookenv.py#L1455
    # &: https://bugs.launchpad.net/charm-layer-docker/+bug/1831712
    environment_config = env_proxy_settings()
    charm_config = dict(config())

    if environment_config is None or \
            charm_config.get('disable-juju-proxy'):
        return charm_config

    no_proxy = get_hosts(environment_config)

    environment_config.update({
        'NO_PROXY': no_proxy,
        'no_proxy': no_proxy
    })

    return merge_config(charm_config, environment_config)


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
