
"""
Ensembl REST Python interface

RestServer is a class that knows how to communicate with the Ensembl REST servers.
EnsemblRestServer and EnsemblGenomesRestServer are two instances of it, set up to access the Ensembl and Ensembl Genomes servers (respectively)
"""

from . import _pyrest_core
from ._pyrest_core import BaseObject, dict_wrapper

from . import genome
from . import info
from . import compara
from . import funcgen
from . import variation

from . import _pyrest_server
from ._pyrest_server import RestServer

EnsemblRestServer = _pyrest_server.RestServer(server_url = "http://rest.ensembl.org")
EnsemblGenomesRestServer = _pyrest_server.RestServer(server_url = "http://rest.ensemblgenomes.org")

__all__ = [ 'RestServer' ]

__all__.append('EnsemblRestServer')
__all__.append('EnsemblGenomesRestServer')


