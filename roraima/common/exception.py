# Copyright (c) 2023 WenRui Gong
# All Rights Reserved.

"""roraima exception subclasses"""

import urllib.parse as urlparse

from roraima.i18n import _

_FATAL_EXCEPTION_FORMAT_ERRORS = False


class RedirectException(Exception):
    def __init__(self, url):
        self.url = urlparse.urlparse(url)


class RoraimaException(Exception):
    """
    Base roraima Exception

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """
    message = _("An unknown exception occurred")

    def __init__(self, message=None, *args, **kwargs):
        if not message:
            message = self.message
        try:
            if kwargs:
                message = message % kwargs
        except Exception:
            if _FATAL_EXCEPTION_FORMAT_ERRORS:
                raise
            else:
                # at least get the core message out if something happened
                pass
        self.msg = message
        super(RoraimaException, self).__init__(message)


class MissingCredentialError(RoraimaException):
    message = _("Missing required credential: %(required)s")


class BadAuthStrategy(RoraimaException):
    message = _("Incorrect auth strategy, expected \"%(expected)s\" but "
                "received \"%(received)s\"")


class NotFound(RoraimaException):
    message = _("An object with the specified identifier was not found.")


class Duplicate(RoraimaException):
    message = _("An object with the same identifier already exists.")


class Conflict(RoraimaException):
    message = _("An object with the same identifier is currently being "
                "operated on.")


class AuthBadRequest(RoraimaException):
    message = _("Connect error/bad request to Auth service at URL %(url)s.")


class AuthUrlNotFound(RoraimaException):
    message = _("Auth service at URL %(url)s not found.")


class AuthorizationFailure(RoraimaException):
    message = _("Authorization failed.")


class NotAuthenticated(RoraimaException):
    message = _("You are not authenticated.")


class Forbidden(RoraimaException):
    message = _("You are not authorized to complete %(action)s action.")


class ProtectedMetadefNamespaceDelete(Forbidden):
    message = _("Metadata definition namespace %(namespace)s is protected"
                " and cannot be deleted.")


class ProtectedMetadefNamespacePropDelete(Forbidden):
    message = _("Metadata definition property %(property_name)s is protected"
                " and cannot be deleted.")


class ProtectedMetadefObjectDelete(Forbidden):
    message = _("Metadata definition object %(object_name)s is protected"
                " and cannot be deleted.")


class ProtectedMetadefResourceTypeAssociationDelete(Forbidden):
    message = _("Metadata definition resource-type-association"
                " %(resource_type)s is protected and cannot be deleted.")


class ProtectedMetadefResourceTypeSystemDelete(Forbidden):
    message = _("Metadata definition resource-type %(resource_type_name)s is"
                " a seeded-system type and cannot be deleted.")


class ProtectedMetadefTagDelete(Forbidden):
    message = _("Metadata definition tag %(tag_name)s is protected"
                " and cannot be deleted.")


class Invalid(RoraimaException):
    message = _("Data supplied was not valid.")


class InvalidSortKey(Invalid):
    message = _("Sort key supplied was not valid.")


class InvalidSortDir(Invalid):
    message = _("Sort direction supplied was not valid.")


class InvalidPropertyProtectionConfiguration(Invalid):
    message = _("Invalid configuration in property protection file.")


class InvalidFilterOperatorValue(Invalid):
    message = _("Unable to filter using the specified operator.")


class InvalidFilterRangeValue(Invalid):
    message = _("Unable to filter using the specified range.")


class InvalidOptionValue(Invalid):
    message = _("Invalid value for option %(option)s: %(value)s")


class ReadonlyProperty(Forbidden):
    message = _("Attribute '%(property)s' is read-only.")


class ReservedProperty(Forbidden):
    message = _("Attribute '%(property)s' is reserved.")


class AuthorizationRedirect(RoraimaException):
    message = _("Redirecting to %(uri)s for authorization.")


class ClientConnectionError(RoraimaException):
    message = _("There was an error connecting to a server")


class ClientConfigurationError(RoraimaException):
    message = _("There was an error configuring the client.")


class MultipleChoices(RoraimaException):
    message = _("The request returned a 302 Multiple Choices. This generally "
                "means that you have not included a version indicator in a "
                "request URI.\n\nThe body of response returned:\n%(body)s")


class LimitExceeded(RoraimaException):
    message = _("The request returned a 413 Request Entity Too Large. This "
                "generally means that rate limiting or a quota threshold was "
                "breached.\n\nThe response body:\n%(body)s")

    def __init__(self, *args, **kwargs):
        self.retry_after = (int(kwargs['retry']) if kwargs.get('retry')
                            else None)
        super(LimitExceeded, self).__init__(*args, **kwargs)


class ServiceUnavailable(RoraimaException):
    message = _("The request returned 503 Service Unavailable. This "
                "generally occurs on service overload or other transient "
                "outage.")

    def __init__(self, *args, **kwargs):
        self.retry_after = (int(kwargs['retry']) if kwargs.get('retry')
                            else None)
        super(ServiceUnavailable, self).__init__(*args, **kwargs)


class ServerError(RoraimaException):
    message = _("The request returned 500 Internal Server Error.")


class UnexpectedStatus(RoraimaException):
    message = _("The request returned an unexpected status: %(status)s."
                "\n\nThe response body:\n%(body)s")


class InvalidContentType(RoraimaException):
    message = _("Invalid content type %(content_type)s")


class BadRegistryConnectionConfiguration(RoraimaException):
    message = _("Registry was not configured correctly on API server. "
                "Reason: %(reason)s")


class BadDriverConfiguration(RoraimaException):
    message = _("Driver %(driver_name)s could not be configured correctly. "
                "Reason: %(reason)s")


class MaxRedirectsExceeded(RoraimaException):
    message = _("Maximum redirects (%(redirects)s) was exceeded.")


class InvalidRedirect(RoraimaException):
    message = _("Received invalid HTTP redirect.")


class NoServiceEndpoint(RoraimaException):
    message = _("Response from Keystone does not contain a roraima endpoint.")


class WorkerCreationFailure(RoraimaException):
    message = _("Server worker creation failed: %(reason)s.")


class SchemaLoadError(RoraimaException):
    message = _("Unable to load schema: %(reason)s")


class InvalidObject(RoraimaException):
    message = _("Provided object does not match schema "
                "'%(schema)s': %(reason)s")


class FailedToGetScrubberJobs(RoraimaException):
    message = _("Scrubber encountered an error while trying to fetch "
                "scrub jobs.")


class SIGHUPInterrupt(RoraimaException):
    message = _("System SIGHUP signal received.")


class RPCError(RoraimaException):
    message = _("%(cls)s exception was raised in the last rpc call: %(val)s")


class DuplicateLocation(Duplicate):
    message = _("The location %(location)s already exists")


class InvalidParameterValue(Invalid):
    message = _("Invalid value '%(value)s' for parameter '%(param)s': "
                "%(extra_msg)s")


class RoraimaEndpointNotFound(NotFound):
    message = _("%(interface)s roraima endpoint not "
                "found for region %(region)s")
