from pathlib import Path

certs_dir = Path('/root/cdk')
ca_crt_path = certs_dir / 'ca.crt'
server_crt_path = certs_dir / 'server.crt'
server_key_path = certs_dir / 'server.key'
client_crt_path = certs_dir / 'client.crt'
client_key_path = certs_dir / 'client.key'
