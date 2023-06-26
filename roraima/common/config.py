# Copyright (c) 2023 WenRui Gong
# All Rights Reserved.

"""
Routines for configuring Roraima
"""

from oslo_config import cfg
from oslo_policy import opts
from oslo_policy import policy

from roraima.i18n import _
from roraima.version import version_info as version

common_opts = [
    cfg.IntOpt('limit_param_default', default=25, min=1,
               help=_("""
The default number of results to return for a request.

Responses to certain API requests, like list images, may return
multiple items. The number of results returned can be explicitly
controlled by specifying the ``limit`` parameter in the API request.
However, if a ``limit`` parameter is not specified, this
configuration value will be used as the default number of results to
be returned for any API request.

NOTES:
    * The value of this configuration option may not be greater than
      the value specified by ``api_limit_max``.
    * Setting this to a very large value may slow down database
      queries and increase response times. Setting this to a
      very low value may result in poor user experience.

Possible values:
    * Any positive integer

Related options:
    * api_limit_max

""")),
    cfg.IntOpt('api_limit_max', default=1000, min=1,
               help=_("""
Maximum number of results that could be returned by a request.

As described in the help text of ``limit_param_default``, some
requests may return multiple results. The number of results to be
returned are governed either by the ``limit`` parameter in the
request or the ``limit_param_default`` configuration option.
The value in either case, can't be greater than the absolute maximum
defined by this configuration option. Anything greater than this
value is trimmed down to the maximum value defined here.

NOTE: Setting this to a very large value may slow down database
      queries and increase response times. Setting this to a
      very low value may result in poor user experience.

Possible values:
    * Any positive integer

Related options:
    * limit_param_default

""")),
    cfg.HostAddressOpt('pydev_worker_debug_host',
                       sample_default='localhost',
                       help=_("""
Host address of the pydev server.

Provide a string value representing the hostname or IP of the
pydev server to use for debugging. The pydev server listens for
debug connections on this address, facilitating remote debugging
in roraima.

Possible values:
    * Valid hostname
    * Valid IP address

Related options:
    * None

""")),
    cfg.PortOpt('pydev_worker_debug_port',
                default=5678,
                help=_("""
Port number that the pydev server will listen on.

Provide a port number to bind the pydev server to. The pydev
process accepts debug connections on this port and facilitates
remote debugging in roraima.

Possible values:
    * A valid port number

Related options:
    * None

""")),
    cfg.StrOpt('worker_self_reference_url',
               default=None,
               help=_("""
The URL to this worker.

If this is set, other roraima workers will know how to contact this one
directly if needed. For image import, a single worker stages the image
and other workers need to be able to proxy the import request to the
right one.

If unset, this will be considered to be `public_endpoint`, which
normally would be set to the same value on all workers, effectively
disabling the proxying behavior.

Possible values:
    * A URL by which this worker is reachable from other workers

Related options:
    * public_endpoint

""")),
]

wsgi_opts = [
    cfg.IntOpt('task_pool_threads',
               default=16,
               min=1,
               help=_("""
The number of threads (per worker process) in the pool for processing
asynchronous tasks. This controls how many asynchronous tasks (i.e. for
image interoperable import) each worker can run at a time. If this is
too large, you *may* have increased memory footprint per worker and/or you
may overwhelm other system resources such as disk or outbound network
bandwidth. If this is too small, image import requests will have to wait
until a thread becomes available to begin processing.""")),
    cfg.StrOpt('python_interpreter',
               default=None,
               help=_("""
Path to the python interpreter to use when spawning external
processes. If left unspecified, this will be sys.executable, which should
be the same interpreter running Glance itself. However, in some situations
(for example, uwsgi) sys.executable may not actually point to a python
interpreter and an alternative value must be set.""")),
]

CONF = cfg.CONF
CONF.register_opts(common_opts)
CONF.register_opts(wsgi_opts, group='wsgi')
policy.Enforcer(CONF)


def parse_args(args=None, usage=None, default_config_files=None):
    CONF(args=args,
         project='roraima',
         version=version.cached_version_string(),
         usage=usage,
         default_config_files=default_config_files)


def set_config_defaults():
    """This method updates all configuration default values."""

    # TODO(gmann): Remove setting the default value of config policy_file
    # once oslo_policy change the default value to 'policy.yaml'.
    # https://github.com/openstack/oslo.policy/blob/a626ad12fe5a3abd49d70e3e5b95589d279ab578/oslo_policy/opts.py#L49
    DEFAULT_POLICY_FILE = 'policy.yaml'
    opts.set_defaults(cfg.CONF, DEFAULT_POLICY_FILE)
