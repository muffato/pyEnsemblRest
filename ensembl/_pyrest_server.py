
import collections
import httplib2
import json
import time

import ensembl

content_types = {
"bed": "text/x-bed",
"fasta": "text/x-fasta",
"gff3": "text/x-gff3",
"json": "application/json",
"nh": "text/x-nh",
"phyloxml": "text/x-phyloxml+xml",
"xml": "text/x-phyloxml+xml",
"yaml": "text/x-yaml",
"text": "text/plain"
}

return_codes = {
200: ("OK", "Request was a success"),
400: ("Bad Request", "Occurs during exceptional circumstances such as the service is unable to find an ID"),
404: ("Not Found", "Indicates a badly formatted request. Check your URL"),
429: ("Too Many Requests", "You have been rate-limited; wait and retry"),
503: ("Service Unavailable", "The service is temporarily down; retry after a pause")
}

class RestServer:

    # the key is the time interval (in seconds)
    # the list stores the last x attempts
    last_requests = {
1: collections.deque([], 6-1),
3600: collections.deque([], 11100-1)
    }

    def __init__(self, server_url):
        self.server_url = server_url
        self.http = httplib2.Http(".cache")


    def get_json_answer(self, url, content_type=None):

        # Rate limiter
        for (i,l) in self.last_requests.items():
            if len(l) == l.maxlen:
                curr_time = time.time()
                oldest_time = l[0]
                if curr_time-oldest_time < i:
                    #print "sleep (%d)" % i, i - (curr_time-oldest_time)
                    time.sleep(i - (curr_time-oldest_time))

        curr_time = time.time()
        for (i,l) in self.last_requests.items():
            l.append(time.time())
            while l[0] < curr_time-i:
                #print "clear", i
                l.popleft()
        #print self.last_requests
        #print content_type
        print("getting "+self.server_url+"/"+url+" with the content_type:"+content_type)
        resp, content = self.http.request(self.server_url+"/"+url, method="GET", headers={"Content-Type":content_type})

        if resp.status not in return_codes:
            raise httplib2.HttpLib2Error( "Unknown response code: %d\n%s" % (resp.status, resp) )
        if return_codes[resp.status][0] != "OK":
            raise httplib2.HttpLib2Error( "Invalid response code: %s (%d)\n%s\n%s" % (return_codes[resp.status][0], resp.status, return_codes[resp.status][1], resp) )

        return content.decode('utf-8')


    def build_rest_answer(self, new_object, allowed_formats, optional_params, accessor, url, kwargs={}):

        format = kwargs.pop('format', None)
        if format is not None:
            format = format.lower()
            if format not in allowed_formats:
                #print "unrecognzied format", format
                format = None

        if len(kwargs):
            url = url + "?" + "&".join("%s=%s" % (p,kwargs[p]) for p in set(kwargs).intersection(optional_params))

        content = self.get_json_answer(url, content_types.get(format, content_types['json']))

        #print "Format", format
        if format is not None:
            return content

        j = json.loads(content)
        if accessor is not None:
            j = j[accessor]
        return ensembl.construct_object_from_json(j, new_object)


    def getArchiveEntry(self, id, **kwargs):
        """Uses the given identifier to return the archived sequence

Return type: ensembl.info.ArchiveEntry
Valid formats: json, xml
HTTP endpoint: archive/id/:id

Required parameters:
- id (String)
    An Ensembl stable ID

"""
        return self.build_rest_answer(ensembl.info.ArchiveEntry, ['json', 'xml'], [], None, 'archive/id/{0}'.format(id), kwargs)


    def getGeneTreeById(self, id, **kwargs):
        """Retrieves a gene tree dump for a gene tree stable identifier

Return type: ensembl.compara.GeneTree
Valid formats: phyloxml, nh, json
HTTP endpoint: genetree/id/:id

Required parameters:
- id (String)
    An Ensembl genetree ID

Optional parameters:
- compara (String)
    Name of the compara database to use. Multiple comparas can exist on a server if you are accessing Ensembl Genomes data
- aligned (Boolean)
    Return the aligned string if true. Otherwise, return the original sequence (no insertions)
- sequence (Enum(none, cdna, protein))
    The type of sequence to bring back. Setting it to none results in no sequence being returned
- nh_format (Enum(full, display_label_composite, simple, species, species_short_name, ncbi_taxon, ncbi_name, njtree, phylip))
    The format of a NH (New Hampshire) request.
"""
        return self.build_rest_answer(ensembl.compara.GeneTree, ['phyloxml', 'nh', 'json'], ['compara', 'aligned', 'sequence', 'nh_format'], None, 'genetree/id/{0}'.format(id), kwargs)


    def getGeneTreeByMemberId(self, id, **kwargs):
        """Retrieves a gene tree that contains the stable identifier

Return type: ensembl.compara.GeneTree
Valid formats: phyloxml, nh, json
HTTP endpoint: genetree/member/id/:id

Required parameters:
- id (String)
    An Ensembl stable ID

Optional parameters:
- species (String)
    Species name/alias
- db_type (String)
    Restrict the search to a database other than the default. Useful if you need to use a DB other than core
- object_type (String)
    Filter by feature type
- compara (String)
    Name of the compara database to use. Multiple comparas can exist on a server if you are accessing Ensembl Genomes data
- aligned (Boolean)
    Return the aligned string if true. Otherwise, return the original sequence (no insertions)
- sequence (Enum(none, cdna, protein))
    The type of sequence to bring back. Setting it to none results in no sequence being returned
- nh_format (Enum(full, display_label_composite, simple, species, species_short_name, ncbi_taxon, ncbi_name, njtree, phylip))
    The format of a NH (New Hampshire) request.
"""
        return self.build_rest_answer(ensembl.compara.GeneTree, ['phyloxml', 'nh', 'json'], ['species', 'db_type', 'object_type', 'compara', 'aligned', 'sequence', 'nh_format'], None, 'genetree/member/id/{0}'.format(id), kwargs)


    def getGeneTreeByMemberSymbol(self, species, symbol, **kwargs):
        """Retrieves a gene tree containing the gene identified by a symbol

Return type: ensembl.compara.GeneTree
Valid formats: phyloxml, nh, json
HTTP endpoint: genetree/member/symbol/:species/:symbol

Required parameters:
- species (String)
    Species name/alias
- symbol (String)
    Symbol or display name of a gene

Optional parameters:
- db_type (String)
    Restrict the search to a database other than the default. Useful if you need to use a DB other than core
- external_db (String)
    Filter by external database
- object_type (String)
    Filter by feature type
- compara (String)
    Name of the compara database to use. Multiple comparas can exist on a server if you are accessing Ensembl Genomes data
- aligned (Boolean)
    Return the aligned string if true. Otherwise, return the original sequence (no insertions)
- sequence (Enum(none, cdna, protein))
    The type of sequence to bring back. Setting it to none results in no sequence being returned
- nh_format (Enum(full, display_label_composite, simple, species, species_short_name, ncbi_taxon, ncbi_name, njtree, phylip))
    The format of a NH (New Hampshire) request.
"""
        return self.build_rest_answer(ensembl.compara.GeneTree, ['phyloxml', 'nh', 'json'], ['db_type', 'external_db', 'object_type', 'compara', 'aligned', 'sequence', 'nh_format'], None, 'genetree/member/symbol/{0}/{1}'.format(species, symbol), kwargs)


    def getAssemblyInfo(self, species, **kwargs):
        """List the currently available assemblies for a species.

Return type: ensembl.info.Assembly
Valid formats: json, xml
HTTP endpoint: info/assembly/:species

Required parameters:
- species (String)
    Species name/alias

Optional parameters:
- bands (Boolean(0,1))
    If set to 1, include karyotype band information. Only display if band information is available
"""
        return self.build_rest_answer(ensembl.info.Assembly, ['json', 'xml'], ['bands'], None, 'info/assembly/{0}'.format(species), kwargs)


    def getAssemblyInfoRegion(self, species, region_name, **kwargs):
        """Returns information about the specified toplevel sequence region for the given species.

Return type: ensembl.info.SeqRegion
Valid formats: json, xml
HTTP endpoint: info/assembly/:species/:region_name

Required parameters:
- species (String)
    Species name/alias
- region_name (String)
    The (top level) sequence region name.

Optional parameters:
- bands (Boolean(0,1))
    If set to 1, include karyotype band information. Only display if band information is available
"""
        return self.build_rest_answer(ensembl.info.SeqRegion, ['json', 'xml'], ['bands'], None, 'info/assembly/{0}/{1}'.format(species, region_name), kwargs)


    def getAnalysisList(self, species, **kwargs):
        """List the names of analyses involved in generating Ensembl data.

Return type: None
Valid formats: json, xml
HTTP endpoint: info/analysis/:species

Required parameters:
- species (String)
    Species name/alias

"""
        return self.build_rest_answer(None, ['json', 'xml'], [], None, 'info/analysis/{0}'.format(species), kwargs)


    def getBiotypesBySpecies(self, species, **kwargs):
        """List the functional classifications of gene models that Ensembl associates with a particular species. Useful for restricting the type of genes/transcripts retrieved by other endpoints.

Return type: ensembl.info.Biotype
Valid formats: json, xml
HTTP endpoint: info/biotypes/:species

Required parameters:
- species (String)
    Species name/alias

"""
        return self.build_rest_answer(ensembl.info.Biotype, ['json', 'xml'], [], None, 'info/biotypes/{0}'.format(species), kwargs)


    def compara_methods(self, **kwargs):
        """List all compara analyses available (an analysis defines the type of comparative data).

Return type: None
Valid formats: json, json, yaml, xml
HTTP endpoint: info/compara/methods


Optional parameters:
- compara (String)
    Name of the compara database to use. Multiple comparas may exist on a server when accessing Ensembl Genomes data.
- class (String)
    The class of the method to query for. Regular expression patterns are supported.
"""
        return self.build_rest_answer(None, ['json', 'json', 'yaml', 'xml'], ['compara', 'class'], None, 'info/compara/methods', kwargs)


    def compara_databases(self, **kwargs):
        """Lists all available comparative genomics databases and their data release.

Return type: None
Valid formats: json, xml
HTTP endpoint: info/comparas


"""
        return self.build_rest_answer(None, ['json', 'xml'], [], "comparas", 'info/comparas', kwargs)


    def getSpeciesSetByComparaMethod(self, method, **kwargs):
        """List all collections of species analysed with the specified compara method.

Return type: ensembl.compara.MethodLinkSpeciesSet
Valid formats: json, yaml, xml
HTTP endpoint: info/compara/species_sets/:method

Required parameters:
- method (String)
    Filter by compara method. Use one the methods returned by <a href="/documentation/info/compara_methods">/info/compara/methods</a> endpoint.

Optional parameters:
- compara (String)
    Name of the compara database to use. Multiple comparas may exist on a server when accessing Ensembl Genomes data.
"""
        return self.build_rest_answer(ensembl.compara.MethodLinkSpeciesSet, ['json', 'yaml', 'xml'], ['compara'], None, 'info/compara/species_sets/{0}'.format(method), kwargs)


    def available_releases(self, **kwargs):
        """Shows the data releases available on this REST server. May return more than one release (unfrequent non-standard Ensembl configuration).

Return type: None
Valid formats: json, xml
HTTP endpoint: info/data


"""
        return self.build_rest_answer(None, ['json', 'xml'], [], "releases", 'info/data', kwargs)


    def getExternalDatabasesBySpecies(self, species, **kwargs):
        """Lists all available external sources for a species.

Return type: ensembl.info.ExternalDatabase
Valid formats: json, xml
HTTP endpoint: info/external_dbs/:species

Required parameters:
- species (String)
    Species name/alias

Optional parameters:
- filter (String)
    Restrict external DB searches to a single source or pattern. SQL-LIKE patterns are supported.
"""
        return self.build_rest_answer(ensembl.info.ExternalDatabase, ['json', 'xml'], ['filter'], None, 'info/external_dbs/{0}'.format(species), kwargs)


    def ping(self, **kwargs):
        """Checks if the service is alive.

Return type: None
Valid formats: json, xml
HTTP endpoint: info/ping


"""
        return self.build_rest_answer(None, ['json', 'xml'], [], "ping", 'info/ping', kwargs)


    def rest_version(self, **kwargs):
        """Shows the current version of the Ensembl REST API.

Return type: None
Valid formats: json, xml
HTTP endpoint: info/rest


"""
        return self.build_rest_answer(None, ['json', 'xml'], [], "release", 'info/rest', kwargs)


    def ensembl_version(self, **kwargs):
        """Shows the current version of the Ensembl API used by the REST server.

Return type: None
Valid formats: json, xml
HTTP endpoint: info/software


"""
        return self.build_rest_answer(None, ['json', 'xml'], [], "release", 'info/software', kwargs)


    def species_list(self, **kwargs):
        """Lists all available species, their aliases, available adaptor groups and data release.

Return type: ensembl.info.Species
Valid formats: json, xml
HTTP endpoint: info/species


Optional parameters:
- division (String)
    Filter by Ensembl or Ensembl Genomes division.
"""
        return self.build_rest_answer(ensembl.info.Species, ['json', 'xml'], ['division'], "species", 'info/species', kwargs)



ensembl._pyrest_core.construction_rules[(ensembl.info.Assembly,'top_level_region')] = ensembl.info.SeqRegion
ensembl._pyrest_core.construction_rules[(ensembl.compara.GeneTree,'tree')] = ensembl.compara.GeneTreeNode
ensembl._pyrest_core.construction_rules[(ensembl.compara.GeneTreeNode,'taxonomy')] = ensembl.compara.NCBITaxon
ensembl._pyrest_core.construction_rules[(ensembl.compara.GeneTreeNode,'events')] = ensembl.compara.GeneTreeEvent
ensembl._pyrest_core.construction_rules[(ensembl.compara.GeneTreeNode,'confidence')] = ensembl.compara.GeneTreeNodeConfidence
ensembl._pyrest_core.construction_rules[(ensembl.compara.GeneTreeNode,'children')] = ensembl.compara.GeneTreeNode
ensembl._pyrest_core.construction_rules[(ensembl.compara.GeneTreeNode,'sequence')] = ensembl.compara.GeneTreeMember
ensembl._pyrest_core.construction_rules[(ensembl.compara.GeneTreeNode,'id')] = ensembl.genome.Identifier
ensembl._pyrest_core.construction_rules[(ensembl.compara.GeneTreeMember,'id')] = ensembl.genome.Identifier
ensembl._pyrest_core.construction_rules[(ensembl.compara.GeneTreeMember,'mol_seq')] = ensembl.genome.Sequence

EnsemblRestServer = RestServer(server_url = "http://rest.ensembl.org")
EnsemblGenomesRestServer = RestServer(server_url = "http://test.rest.ensemblgenomes.org")



