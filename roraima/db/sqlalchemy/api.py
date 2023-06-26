# Copyright (c) 2023 WenRui Gong
# All Rights Reserved.

"""Defines interface for DB access."""

import threading

import osprofiler.sqlalchemy
import sqlalchemy
from oslo_config import cfg
from oslo_db.sqlalchemy import session
from oslo_log import log as logging

sa_logger = None
LOG = logging.getLogger(__name__)

CONF = cfg.CONF
CONF.import_group("profiler", "roraima.common.wsgi")

_FACADE = None
_LOCK = threading.Lock()


def _create_facade_lazily():
    global _LOCK, _FACADE
    if _FACADE is None:
        with _LOCK:
            if _FACADE is None:
                _FACADE = session.EngineFacade.from_config(CONF)

                if CONF.profiler.enabled and CONF.profiler.trace_sqlalchemy:
                    osprofiler.sqlalchemy.add_tracing(sqlalchemy,
                                                      _FACADE.get_engine(),
                                                      "db")
    return _FACADE


def get_engine():
    facade = _create_facade_lazily()
    return facade.get_engine()


def get_session(expire_on_commit=False):
    facade = _create_facade_lazily()
    return facade.get_session(expire_on_commit=expire_on_commit)
