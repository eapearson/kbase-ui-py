# Deployment Docker context

This directory is a placeholder. Contents other than this directory will not be checked in.

In the deployment process, this directory serves as the docker context. All files to be incorporated into the image are copied into this directory, and the entire contents copied to the image's /kb/deployment directory.

## Environment Variables

### docker-compose.yml

- `DEPLOY_ENV` - the short name for a KBase deployment environment: ci, next, appdev, narrative-dev, prod

### nginx.conf.tmpl

- `KBASE_UI_HOSTNAME` - hostname of the ui app, probably within the docker network; defaults to `kbase-ui:8000`
- `SERVICES_HOSTNAME` - hostname for kbase services; e.g. `ci.kbase.us`
- `UI_HOSTNAME` - hostname for kbase ui and narrative from the browser pov.
- `NARRATIVE_HOSTNAME` - flag indicating whether to map to a narrative running within the docker network; e.g. `narrative:8888`;
- `SERVICE_PROXY_HOSTNAMES` - list of services to proxy to; a comma-separated list string; each proxy name should be the hostname of a service container
- `DYNAMIC_SERVICE_PROXY_HOSTNAMES` - list of dynamic services to proxy to; a comma-separated list string; each proxy name should be the hostname of a service container, which in turn should be the service module name