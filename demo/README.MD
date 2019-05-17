# Demo dockers

## Pre-requisites

- docker
- docker-compose

## Quick start

Run the following command to start all services in background:

    docker-compose up -d
    
    or
    
    docker-compose up -d --build        #To rebuild all images

Fetching the logs:

`docker-compose logs -f`

Cleanup after demoing:

`docker-compose down`


## Changing the GNU/Linux distribution

The application containers and celery containers can be configured to use docker image based on different GNU/Linux distributions.
This is done by pointing to the folder where the Dockerfile resides.

```
demo/epp/
├── centos7               <──── choose this
│   └── Dockerfile
├── fedora                <──── or this
│   └── Dockerfile
├── ubuntu18              <──── or this
│   └── Dockerfile
├── bootstrap.sh
└── runtime_config.sh

```

Change the environment variable `APP_DIST` to either `centos7` or `ubuntu18` in the `.env` file.
You can also pass the variable like this:

```bash
APP_DIST=ubuntu18 docker-compose up -d
```
