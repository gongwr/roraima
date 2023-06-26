# everest

## Development

```bash
```

## Run

There are two ways to run the project:

The first one is to run the project with wsgi server, for example gunicorn:

```bash
gunicorn roraima.cmd.api:app_ --workers 4 -k uvicorn.workers.UvicornWorker
```

or

In development mode, you can run the project with uvicorn:

```bash
uvicorn roraima.cmd.api:app_ --reload
``` 

or

```bash
python roraima-api --config-file ./etc/roraima-api.conf
```