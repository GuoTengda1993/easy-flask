# easy-flask
Automatic generate a flask server project by command

# Start
Install
```bash
pip3 install easy-flask-restful
```
Make a flask server project at current dir:
```bash
easy-flask -n demo_server
# or
easy-flask --new=demo_server

# start server in debug mode
cd demo_server
python3 app.py
# or
sh control.sh start|restart|stop
```

# Introduce
By this tool you don`t need care how to make a flask server project.
What you need to do is write api-file in easy format inside dir ``api``.
This project will automatically load uri by api-file, and pack json response with same format.

Project structure
```base
.
├── api
│   ├── __init__.py
│   └── demo
│       ├── __init__.py
│       └── demo_api.py
├── conf
│   ├── __init__.py
│   ├── config.ini
├── internal
│   ├── __init__.py
│   ├── error.py
│   └── utils.py
├── app.py
├── start.py
├── control.sh
└── logs
    └── app.log

```

``api`` - write api files here.

``internal.error`` - define error info here.

``app.py`` - start app by this file, you can rename it.

``conf`` - config for application

``control.sh`` - run app with command by gunicorn

## Write Api File
For example:
```python3
from flask import g

from internal import Resource
from utils.parser import Type, Required, Default, Min, Max


class DemoApi(Resource):

    uri = ['/api/demo']

    def get(self):
        pattern = {
            'num': {Type: int, Min: 10, Max: 100},
            'print': {Type: str, Required: True},
            'default': {Type: str, Default: 'demo'}
        }

        data, err = self.parse_request_data(pattern=pattern)
        if err:
            g.logger.warning(err)
            return err
        g.logger.info('success')
        return {'result': data}
```

``uri`` - required by all api file

``g.logger`` is loaded before each request for making different log_id.

``self.parse_request_data`` can help you to parse params, it will return ``ParamsError`` when param invalid.

Normal response:
```json
{
    "errno": 0,
    "data": {
        "result": {
            "num": 100,
            "print": "aaaa",
            "default": "demo"
        }
    },
    "msg": "success",
    "log_id": "f40c889d1b5744c7a87a9045aea8595c"
}
```

Error response:

return ``errno`` and ``msg`` according to ``error.py``.
```json
{
    "errno": 2,
    "msg": "params error:num check max invalid",
    "log_id": "7c53531b93a4406e9d3050bae5b99968"
}
```

## Suggest
A real project must have complex logic and interactions with DB or other service.
By this tool, you just can get a simple framework. So I give some suggestions here for writing better code.

- ``logic`` dir (or other name) for writing complex logic, keep simple in api file.
- if you need db operation, use ``flask-sqlalchemy``, and mkdir ``dto``.
- ``client`` dir for interact with other service, and make ``BaseClient`` class(inherited by other client), because you never want to write same code for many times.
