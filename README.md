## Cron Expression Parser
This is a command app which parses a cron string and expands each field to show the times at which it will run.

### Build a docker image
```
docker build . -t cron
```
### Run a docker container using image above
```
docker run -it cron
```
### How to test
```
pytest -vv
```
