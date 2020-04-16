# layer-container-runtime-common

This is a library layer for common functions that exist across the container
runtimes.

## Configuration

### Custom Registry CA

If the container runtime needs to pull images from an external registry with
self-signed TLS certificates, you will need to configure the runtime with the
CA used to sign those certs:

```bash
juju config containerd custom-registry-ca=$(base64 /path/to/ca.crt)
```

>Note: this is not required when following the
[Private Docker Registry][docker-registry] documentation, as the
`docker-registry` charm is related to the same certificate provider as the
rest of the Charmed Kubernetes cluster.

## Tests

To run tests use:

```bash
python -m pytest ./tests
```

<!-- LINKS -->
[docker-registry]: https://ubuntu.com/kubernetes/docs/docker-registry
