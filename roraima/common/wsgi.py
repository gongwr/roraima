"""
Utility methods for working with WSGI servers
"""

from oslo_config import cfg
from oslo_log import log as logging
from osprofiler import opts as profiler_opts

from roraima.i18n import _

bind_opts = [
    cfg.HostAddressOpt('bind_host',
                       default='0.0.0.0',
                       help=_("""
IP address to bind the roraima servers to.

Provide an IP address to bind the roraima server to. The default
value is ``0.0.0.0``.

Edit this option to enable the server to listen on one particular
IP address on the network card. This facilitates selection of a
particular network interface for the server.

Possible values:
    * A valid IPv4 address
    * A valid IPv6 address

Related options:
    * None

""")),

    cfg.PortOpt('bind_port',
                help=_("""
Port number on which the server will listen.

Provide a valid port number to bind the server's socket to. This
port is then set to identify processes and forward network messages
that arrive at the server. The default bind_port value for the API
server is 9292 and for the registry server is 9191.

Possible values:
    * A valid port number (0 to 65535)

Related options:
    * None

""")),
]

cli_opts = []

LOG = logging.getLogger(__name__)

CONF = cfg.CONF
CONF.register_opts(bind_opts)


def register_cli_opts():
    CONF.register_cli_opts(cli_opts)


profiler_opts.set_defaults(CONF)


def get_bind_addr(default_port=None):
    """Return the host and port to bind to."""
    return CONF.bind_host, CONF.bind_port or default_port
