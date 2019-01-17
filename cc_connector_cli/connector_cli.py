"""
This module provides functionality to create standard-compliant red-connector-clis, from python classes, which implement
a subset of the following functions:
 - receive(access, internal)
 - send(access, internal)
 - receive_directory(access, internal, listing)

For additional functionality the given class can implement the following functions:
 - receive_validate(access)
 - send_validate(access)
 - receive_directory_validate(access)
"""

import argparse
import inspect


class ConnectorFunction:
    """
    Represents a function, which can be implemented by a connector.
    """

    def __init__(self, name, params):
        """
        Creates a new ConnectorFunction

        :param name: The name of the function
        :param params: A Description of the function parameters
        """
        self.name = name
        self.params = params


CONNECTOR_FUNCTIONS = [
    ConnectorFunction(name='receive', params=('access', 'internal')),
    ConnectorFunction(name='send', params=('access', 'internal')),
    ConnectorFunction(name='receive_directory', params=('access', 'internal', 'listing')),
    ConnectorFunction(name='receive_validate', params=('access',)),
    ConnectorFunction(name='send_validate', params=('access',)),
    ConnectorFunction(name='receive_directory_validate', params=('access',)),
]


def has_function(connector_class, func):
    """
    Returns True, if connector_class implements a function like func

    :param connector_class: The given ConnectorClass
    :param func: The connector function
    :return: True, if connector_class implements a function with name <func.name>, with the given parameters
    """
    try:
        f = getattr(connector_class, func.name)
        if not callable(f):
            return False
        spec = inspect.getfullargspec(f)
        if not spec.args == func.params:
            print('oh no')
            return False
    except AttributeError:
        raise
        # return False


def connector_class_to_string(connector_class):
    """
    Creates a string representation of the given ConnectorDescription.

    :param connector_class: The given ConnectorClass
    :return: A string describing this ConnectorDescription.
    """
    repr = ['ConnectorDescription({name})'.format(name=connector_class.__name__)]
    for f in CONNECTOR_FUNCTIONS:
        repr.append('\n  {func_name}={has_func}'.format(func_name=f.name,
                                                        has_func=has_function(connector_class, f)))
    return ''.join(repr)


def create_parser(connector_class):
    """
    Creates an ArgumentParser for the given connector class.

    :param connector_class: The connector class
    :return: An ArgumentParser
    """
    print(connector_class_to_string(connector_class))
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()
    subparsers.required = True

    receive_parser = subparsers.add_parser('receive')
    receive_parser.add_argument('access-file', action='store', type=str,
                                help='A json file with access information.')
    receive_parser.add_argument('internal-file', action='store', type=str,
                                help='A json file with internal information.')

    return parser


def analyse_connector(ConnectorClass):
    """
    Creates a ConnectorDescription of the given ConnectorClass.

    :param ConnectorClass:
    :return:
    """
