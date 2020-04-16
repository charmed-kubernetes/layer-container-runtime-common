from base64 import b64decode
from subprocess import check_call

from charms.layer import status
from charms.reactive import (
    data_changed,
    set_flag,
    when_any,
    when_not
)

from charmhelpers.core import hookenv, host


@when_not('cgroups.modified')
def enable_grub_cgroups():
    """
    Run script to enable cgroups
    in GRUB.  Be aware, this will
    reboot the host.

    :return: None
    """
    cfg = hookenv.config()
    if cfg.get('enable-cgroups'):
        hookenv.log('Calling enable_grub_cgroups.sh and rebooting machine.')
        check_call(['scripts/enable_grub_cgroups.sh'])
        set_flag('cgroups.modified')


@when_any('config.set.custom-registry-ca', 'config.changed.custom-registry-ca')
def install_custom_ca():
    """
    Installs a configured CA cert into the system-wide location.
    """
    ca_cert = hookenv.config().get('custom-registry-ca')
    if ca_cert and data_changed('custom-registry-ca', ca_cert):
        try:
            # decode to bytes, as that's what install_ca_cert wants
            _ca = b64decode(ca_cert)
        except Exception:
            status.blocked('Invalid value for custom-registry-ca config')
            return
        else:
            hookenv.log('Installing custom registry CA')
            host.install_ca_cert(_ca, name='juju-custom-registry')
