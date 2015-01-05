
"""
Ensembl REST Python interface

RestServer is a class that knows how to communicate with the Ensembl REST servers.
EnsemblRestServer and EnsemblGenomesRestServer are two instances of it, set up to access the Ensembl and Ensembl Genomes servers (respectively)
"""

#__MODULE_IMPORTS__

from . import _pyrest_server
from ._pyrest_server import RestServer

__all__ = [ 'RestServer' ]

#__REST_INSTANCES__

