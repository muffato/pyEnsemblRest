
"""
Ensembl REST Python interface

RestServer is a class that knows how to communicate with the Ensembl REST servers.
EnsemblRestServer and EnsemblGenomesRestServer are two instances of it, set up to access the Ensembl and Ensembl Genomes servers (respectively)
"""

from . import _pyrest_core
from ensembl._pyrest_core import BaseObject, dict_wrapper

#__MODULE_IMPORTS__

from . import _pyrest_server
from ensembl._pyrest_server import RestServer, EnsemblRestServer, EnsemblGenomesRestServer

__all__ = ['EnsemblRestServer', 'EnsemblGenomesRestServer', 'RestServer']

