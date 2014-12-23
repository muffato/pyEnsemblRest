
import collections
import httplib2
import math
import json
import time
import urllib
import sys

import ensembl

content_types = {
"bed": "text/x-bed",
"fasta": "text/x-fasta",
"gff3": "text/x-gff3",
"json": "application/json",
"nh": "text/x-nh",
"phyloxml": "text/x-phyloxml+xml",
"xml": "text/xml",
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


class RestServerException(Exception):
    """Used when the server returned a non-OK code"""
    pass


class RestServer:

    def __init__(self, server_url):
        self.server_url = server_url
        self.http = httplib2.Http()
        self.last_headers = None


    def get_json_answer(self, url, content_type=None):

        # Rate limiter
        # FIXME: check whether it is ever used and delete otherwise
        if self.last_headers is not None:
            time_remaining = int(self.last_headers['x-ratelimit-reset'])
            requests_remaining = int(self.last_headers['x-ratelimit-remaining'])
            t = time_remaining * math.exp( -requests_remaining / time_remaining )
            if t > .001:
                print("sleeping", t, "seconds before calling", self.server_url)
                time.sleep(t)

        #print("getting "+self.server_url+"/"+url+" with the content_type:"+content_type)
        while True:
            resp, content = self.http.request(self.server_url+"/"+url, method="GET", headers={"Content-Type":content_type})
            if resp.status == 429:
                print(self.server_url, "asked to wait", resp['retry-after'], "seconds", file=sys.stderr)
                time.sleep(float(resp['retry-after']))
            else:
                break

        if resp.status not in return_codes:
            raise RestServerException( "Unknown response code: %d" % resp.status, resp, content )
        if return_codes[resp.status][0] != "OK":
            raise RestServerException( "Invalid response code: %s (%d)\n%s" % (return_codes[resp.status][0], resp.status, return_codes[resp.status][1]), resp, content )
        self.last_headers = resp

        return content.decode('utf-8')


    def build_rest_answer(self, new_object, allowed_formats, optional_params, accessor, url, kwargs={}):

        format = kwargs.pop('output_format', None)
        if format is not None:
            format = format.lower()
            if format not in allowed_formats:
                #print "unrecognzied format", format
                format = None

        if len(kwargs):
            ps = set(kwargs).intersection(optional_params)
            pairs = []
            for p in ps:
                vv = kwargs[p]
                if isinstance(vv, list):
                    pairs.extend( (p,_) for _ in vv)
                else:
                    pairs.append( (p,vv) )
            url = url + "?" + "&".join("%s=%s" % (p,urllib.parse.quote(str(v))) for (p,v) in pairs)

        content = self.get_json_answer(url, content_types.get(format, content_types['json']))

        #print "Format", format
        if format is not None:
            return content

        j = json.loads(content)
        if accessor is not None:
            j = j[accessor]
        return ensembl.construct_object_from_json(j, new_object, self)


    def getArchiveEntry(self, id, **kwargs):
        """Uses the given identifier to return the archived sequence

Return type: ensembl.info.ArchiveEntry
Valid formats: json, xml
HTTP endpoint: archive/id/:id

Required parameters:
- id (String)
    An Ensembl stable ID

"""
        return self.build_rest_answer(ensembl.info.ArchiveEntry, ['json', 'xml'], [], None, 'archive/id/{0}'.format(urllib.parse.quote(str(id))), kwargs)


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
        return self.build_rest_answer(ensembl.info.Assembly, ['json', 'xml'], ['bands'], None, 'info/assembly/{0}'.format(urllib.parse.quote(str(species))), kwargs)


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
        return self.build_rest_answer(ensembl.info.SeqRegion, ['json', 'xml'], ['bands'], None, 'info/assembly/{0}/{1}'.format(urllib.parse.quote(str(species)), urllib.parse.quote(str(region_name))), kwargs)


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
        return self.build_rest_answer(ensembl.compara.GeneTree, ['phyloxml', 'nh', 'json'], ['compara', 'aligned', 'sequence', 'nh_format'], None, 'genetree/id/{0}'.format(urllib.parse.quote(str(id))), kwargs)


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
        return self.build_rest_answer(ensembl.compara.GeneTree, ['phyloxml', 'nh', 'json'], ['species', 'db_type', 'object_type', 'compara', 'aligned', 'sequence', 'nh_format'], None, 'genetree/member/id/{0}'.format(urllib.parse.quote(str(id))), kwargs)


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
        return self.build_rest_answer(ensembl.compara.GeneTree, ['phyloxml', 'nh', 'json'], ['db_type', 'external_db', 'object_type', 'compara', 'aligned', 'sequence', 'nh_format'], None, 'genetree/member/symbol/{0}/{1}'.format(urllib.parse.quote(str(species)), urllib.parse.quote(str(symbol))), kwargs)


    def getHomologyByGeneSymbol(self, species, symbol, **kwargs):
        """Retrieves homology information (orthologs) by symbol

Return type: ensembl.compara.HomologyGroup
Valid formats: json, xml, orthoxml
HTTP endpoint: homology/symbol/:species/:symbol

Required parameters:
- species (String)
    Species name/alias
- symbol (String)
    Symbol or display name of a gene

Optional parameters:
- compara (String)
    Name of the compara database to use. Multiple comparas can exist on a server if you are accessing Ensembl Genomes data
- external_db (String)
    Filter by external database
- format (Enum(full,condensed))
    Layout of the response
- type (Enum(orthologues, paralogues, projections, all))
    The type of homology to return from this call. Projections are orthology calls defined between alternative assemblies and the genes shared between them. Useful if you need only one type of homology back from the service
- target_species (String)
    Filter by species. Supports all species aliases
- target_taxon (Integer)
    Filter by taxon
- aligned (Boolean)
    Return the aligned string if true. Otherwise, return the original sequence (no insertions)
- sequence (Enum(none, cdna, protein))
    The type of sequence to bring back. Setting it to none results in no sequence being returned
"""
        return self.build_rest_answer(ensembl.compara.HomologyGroup, ['json', 'xml', 'orthoxml'], ['compara', 'external_db', 'format', 'type', 'target_species', 'target_taxon', 'aligned', 'sequence'], "data", 'homology/symbol/{0}/{1}'.format(urllib.parse.quote(str(species)), urllib.parse.quote(str(symbol))), kwargs)


    def getHomologyByGeneStableID(self, id, **kwargs):
        """Retrieves homology information (orthologs) by Ensembl gene id

Return type: ensembl.compara.HomologyGroup
Valid formats: json, xml, orthoxml
HTTP endpoint: homology/id/:id

Required parameters:
- id (String)
    An Ensembl stable ID

Optional parameters:
- species (String)
    Species name/alias
- compara (String)
    Name of the compara database to use. Multiple comparas can exist on a server if you are accessing Ensembl Genomes data
- format (Enum(full, condensed))
    Layout of the response
- type (Enum(orthologues, paralogues, projections, all))
    The type of homology to return from this call. Projections are orthology calls defined between alternative assemblies and the genes shared between them. Useful if you need only one type of homology back from the service
- target_species (String)
    Filter by species. Supports all species aliases
- target_taxon (Integer)
    Filter by taxon
- aligned (Boolean)
    Return the aligned string if true. Otherwise, return the original sequence (no insertions)
- sequence (Enum(none, cdna, protein))
    The type of sequence to bring back. Setting it to none results in no sequence being returned
"""
        return self.build_rest_answer(ensembl.compara.HomologyGroup, ['json', 'xml', 'orthoxml'], ['species', 'compara', 'format', 'type', 'target_species', 'target_taxon', 'aligned', 'sequence'], "data", 'homology/id/{0}'.format(urllib.parse.quote(str(id))), kwargs)


    def getGenomicAlignmentByRegion(self, species, region, **kwargs):
        """Retrieves genomic alignments as separate blocks based on a region and species

Return type: ensembl.compara.GenomicAlignment
Valid formats: json, xml, phyloxml
HTTP endpoint: alignment/region/:species/:region

Required parameters:
- species (String)
    Species name/alias
- region (String)
    Query region. A maximum of 10Mb is allowed to be requested at any one time

Optional parameters:
- compara (String)
    Name of the compara database to use. Multiple comparas can exist on a server if you are accessing Ensembl Genomes data
- aligned (Boolean)
    Return the aligned string if true. Otherwise, return the original sequence (no insertions)
- mask (Enum(hard,soft))
    Request the sequence masked for repeat sequences. Hard will mask all repeats as N's and soft will mask repeats as lowercased characters.
- species_set_group (String)
    The species set group name of the multiple alignment. Should not be used with the species_set parameter. Use <a href="/documentation/info/compara_species_sets">/info/compara/species_sets/:method</a> with one of the methods listed above to obtain a valid list of group names.
- species_set (String)
    The set of species used to define the pairwise alignment (multiple values). Should not be used with the species_set_group parameter. Use <a href="/documentation/info/compara_species_sets">/info/compara/species_sets/:method</a> with one of the methods listed above to obtain a valid list of species sets. Any valid alias may be used.
- method (Enum(EPO, EPO_LOW_COVERAGE, PECAN, LASTZ_NET, BLASTZ_NET, TRANSLATED_BLAT_NET))
    The alignment method
- display_species_set (String)
    Subset of species in the alignment to be displayed (multiple values). All the species in the alignment will be displayed if this is not set. Any valid alias may be used.
- compact (Boolean)
    Applicable to EPO_LOW_COVERAGE alignments. If true, concatenate the low coverage species sequences together to create a single sequence. Otherwise, separates out all sequences.
"""
        return self.build_rest_answer(ensembl.compara.GenomicAlignment, ['json', 'xml', 'phyloxml'], ['compara', 'aligned', 'mask', 'species_set_group', 'species_set', 'method', 'display_species_set', 'compact'], None, 'alignment/region/{0}/{1}'.format(urllib.parse.quote(str(species)), urllib.parse.quote(str(region))), kwargs)


    def ping(self, **kwargs):
        """Checks if the service is alive.

Return type: None
Valid formats: json, xml
HTTP endpoint: info/ping


"""
        return self.build_rest_answer(None, ['json', 'xml'], [], "ping", 'info/ping', kwargs)


    def listSpecies(self, **kwargs):
        """Lists all available species, their aliases, available adaptor groups and data release.

Return type: ensembl.info.Species
Valid formats: json, xml
HTTP endpoint: info/species


Optional parameters:
- division (String)
    Filter by Ensembl or Ensembl Genomes division.
"""
        return self.build_rest_answer(ensembl.info.Species, ['json', 'xml'], ['division'], "species", 'info/species', kwargs)


    def listComparaDatabases(self, **kwargs):
        """Lists all available comparative genomics databases and their data release.

Return type: None
Valid formats: json, xml
HTTP endpoint: info/comparas


"""
        return self.build_rest_answer(None, ['json', 'xml'], [], "comparas", 'info/comparas', kwargs)


    def ensembl_version(self, **kwargs):
        """Shows the current version of the Ensembl API used by the REST server.

Return type: None
Valid formats: json, xml
HTTP endpoint: info/software


"""
        return self.build_rest_answer(None, ['json', 'xml'], [], "release", 'info/software', kwargs)


    def rest_version(self, **kwargs):
        """Shows the current version of the Ensembl REST API.

Return type: None
Valid formats: json, xml
HTTP endpoint: info/rest


"""
        return self.build_rest_answer(None, ['json', 'xml'], [], "release", 'info/rest', kwargs)


    def listAvailableReleases(self, **kwargs):
        """Shows the data releases available on this REST server. May return more than one release (unfrequent non-standard Ensembl configuration).

Return type: None
Valid formats: json, xml
HTTP endpoint: info/data


"""
        return self.build_rest_answer(None, ['json', 'xml'], [], "releases", 'info/data', kwargs)


    def getAnalysisList(self, species, **kwargs):
        """List the names of analyses involved in generating Ensembl data.

Return type: None
Valid formats: json, xml
HTTP endpoint: info/analysis/:species

Required parameters:
- species (String)
    Species name/alias

"""
        return self.build_rest_answer(None, ['json', 'xml'], [], None, 'info/analysis/{0}'.format(urllib.parse.quote(str(species))), kwargs)


    def getBiotypesBySpecies(self, species, **kwargs):
        """List the functional classifications of gene models that Ensembl associates with a particular species. Useful for restricting the type of genes/transcripts retrieved by other endpoints.

Return type: ensembl.info.Biotype
Valid formats: json, xml
HTTP endpoint: info/biotypes/:species

Required parameters:
- species (String)
    Species name/alias

"""
        return self.build_rest_answer(ensembl.info.Biotype, ['json', 'xml'], [], None, 'info/biotypes/{0}'.format(urllib.parse.quote(str(species))), kwargs)


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
        return self.build_rest_answer(ensembl.info.ExternalDatabase, ['json', 'xml'], ['filter'], None, 'info/external_dbs/{0}'.format(urllib.parse.quote(str(species))), kwargs)


    def getAllComparaMethods(self, **kwargs):
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
        return self.build_rest_answer(ensembl.compara.MethodLinkSpeciesSet, ['json', 'yaml', 'xml'], ['compara'], None, 'info/compara/species_sets/{0}'.format(urllib.parse.quote(str(method))), kwargs)


    def lookupIdentifier(self, id, **kwargs):
        """Find the species and database for a single identifier

Return type: ensembl.genome.feature_wrapper
Valid formats: json, xml
HTTP endpoint: lookup/id/:id

Required parameters:
- id (String)
    An Ensembl stable ID

Optional parameters:
- species (String)
    Species name/alias
- db_type (String)
    Restrict the search to a database other than the default. Useful if you need to use a DB other than core
- format (Enum(full,condensed))
    Specify the formats to emit from this endpoint
- expand (Boolean(0,1))
    Expands the search to include any connected features. e.g. If the object is a gene, its transcripts, translations and exons will be returned as well.
"""
        return self.build_rest_answer(ensembl.genome.feature_wrapper, ['json', 'xml'], ['species', 'db_type', 'format', 'expand'], None, 'lookup/id/{0}'.format(urllib.parse.quote(str(id))), kwargs)


    def lookupGeneSymbol(self, species, symbol, **kwargs):
        """Find the species and database for a symbol in a linked external database

Return type: ensembl.genome.feature_wrapper
Valid formats: json, xml
HTTP endpoint: lookup/symbol/:species/:symbol

Required parameters:
- species (String)
    Species name/alias
- symbol (String)
    A name or symbol from an annotation source has been linked to a genetic feature

Optional parameters:
- format (Enum(full,condensed))
    Specify the layout of the response
- expand (Boolean(0,1))
    Expands the search to include any connected features. e.g. If the object is a gene, its transcripts, translations and exons will be returned as well.
"""
        return self.build_rest_answer(ensembl.genome.feature_wrapper, ['json', 'xml'], ['format', 'expand'], None, 'lookup/symbol/{0}/{1}'.format(urllib.parse.quote(str(species)), urllib.parse.quote(str(symbol))), kwargs)


    def mapCoordinatesBetweenAssemblies(self, species, asm_one, region, asm_two, **kwargs):
        """Convert the co-ordinates of one assembly to another

Return type: ensembl.genome.CoordMapping
Valid formats: json, xml
HTTP endpoint: map/:species/:asm_one/:region/:asm_two

Required parameters:
- species (String)
    Species name/alias
- asm_one (String)
    Version of the input assembly
- region (String)
    Query region
- asm_two (String)
    Version of the output assembly

Optional parameters:
- coord_system (String)
    Name of the output coordinate system
"""
        return self.build_rest_answer(ensembl.genome.CoordMapping, ['json', 'xml'], ['coord_system'], "mappings", 'map/{0}/{1}/{2}/{3}'.format(urllib.parse.quote(str(species)), urllib.parse.quote(str(asm_one)), urllib.parse.quote(str(region)), urllib.parse.quote(str(asm_two))), kwargs)


    def mapCDNACoordinatesToGenome(self, id, region, **kwargs):
        """Convert from cDNA coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API.

Return type: ensembl.genome.Location
Valid formats: json, xml
HTTP endpoint: map/cdna/:id/:region

Required parameters:
- id (String)
    An Ensembl stable ID
- region (String)
    Query region

Optional parameters:
- species (String)
    Species name/alias
"""
        return self.build_rest_answer(ensembl.genome.Location, ['json', 'xml'], ['species'], "mappings", 'map/cdna/{0}/{1}'.format(urllib.parse.quote(str(id)), urllib.parse.quote(str(region))), kwargs)


    def mapCDSCoordinatesToGenome(self, id, region, **kwargs):
        """Convert from CDS coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API.

Return type: ensembl.genome.Location
Valid formats: json, xml
HTTP endpoint: map/cds/:id/:region

Required parameters:
- id (String)
    An Ensembl stable ID
- region (String)
    Query region

Optional parameters:
- species (String)
    Species name/alias
"""
        return self.build_rest_answer(ensembl.genome.Location, ['json', 'xml'], ['species'], "mappings", 'map/cds/{0}/{1}'.format(urllib.parse.quote(str(id)), urllib.parse.quote(str(region))), kwargs)


    def mapProteinCoordinatesToGenome(self, id, region, **kwargs):
        """Convert from protein (translation) coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API.

Return type: ensembl.genome.Location
Valid formats: json, xml
HTTP endpoint: map/translation/:id/:region

Required parameters:
- id (String)
    An Ensembl stable ID
- region (String)
    Query region

Optional parameters:
- species (String)
    Species name/alias
"""
        return self.build_rest_answer(ensembl.genome.Location, ['json', 'xml'], ['species'], "mappings", 'map/translation/{0}/{1}'.format(urllib.parse.quote(str(id)), urllib.parse.quote(str(region))), kwargs)


    def getOntologyByID(self, id, **kwargs):
        """Search for an ontological term by its namespaced identifier

Return type: ensembl.info.OntologyTerm
Valid formats: json, xml, yaml
HTTP endpoint: ontology/id/:id

Required parameters:
- id (String)
    An ontology term identifier

Optional parameters:
- relation (String)
    The types of relationships to include in the output. Fetches all relations by default
- simple (Boolean)
    If set the API will avoid the fetching of parent and child terms
"""
        return self.build_rest_answer(ensembl.info.OntologyTerm, ['json', 'xml', 'yaml'], ['relation', 'simple'], None, 'ontology/id/{0}'.format(urllib.parse.quote(str(id))), kwargs)


    def getOntologyByName(self, name, **kwargs):
        """Search for a list of ontological terms by their name

Return type: ensembl.info.OntologyTerm
Valid formats: json, xml, yaml
HTTP endpoint: ontology/name/:name

Required parameters:
- name (String)
    An ontology name. SQL wildcards are supported

Optional parameters:
- ontology (String)
    Filter by ontology. Used to disambiguate terms which are shared between ontologies such as GO and EFO
- relation (String)
    The types of relationships to include in the output. Fetches all relations by default
- simple (Boolean)
    If set the API will avoid the fetching of parent and child terms
"""
        return self.build_rest_answer(ensembl.info.OntologyTerm, ['json', 'xml', 'yaml'], ['ontology', 'relation', 'simple'], None, 'ontology/name/{0}'.format(urllib.parse.quote(str(name))), kwargs)


    def getAllAncestorsOfOntologyID(self, id, **kwargs):
        """Reconstruct the entire ancestry of a term from is_a and part_of relationships

Return type: ensembl.info.OntologyTerm
Valid formats: json, xml, yaml
HTTP endpoint: ontology/ancestors/:id

Required parameters:
- id (String)
    An ontology term identifier

Optional parameters:
- ontology (String)
    Filter by ontology. Used to disambiguate terms which are shared between ontologies such as GO and EFO
"""
        return self.build_rest_answer(ensembl.info.OntologyTerm, ['json', 'xml', 'yaml'], ['ontology'], None, 'ontology/ancestors/{0}'.format(urllib.parse.quote(str(id))), kwargs)


    def getAllDescendantsOfOntologyID(self, id, **kwargs):
        """Find all the terms descended from a given term. By default searches are conducted within the namespace of the given identifier

Return type: ensembl.info.OntologyTerm
Valid formats: json, xml
HTTP endpoint: ontology/descendants/:id

Required parameters:
- id (String)
    An ontology term identifier

Optional parameters:
- ontology (String)
    Filter by ontology. Used to disambiguate terms which are shared between ontologies such as GO and EFO
- subset (String)
    Filter terms by the specified subset
- closest_term (Boolean)
    If true return only the closest terms to the specified term
- zero_distance (Boolean)
    Return terms with a distance of 0
"""
        return self.build_rest_answer(ensembl.info.OntologyTerm, ['json', 'xml'], ['ontology', 'subset', 'closest_term', 'zero_distance'], None, 'ontology/descendants/{0}'.format(urllib.parse.quote(str(id))), kwargs)


    def getOntologyAncestorChart(self, id, **kwargs):
        """Reconstruct the entire ancestry of a term from is_a and part_of relationships.

Return type: ensembl.dict_wrapper(ensembl.info.OntologyEntry)
Valid formats: json, xml
HTTP endpoint: ontology/ancestors/chart/:id

Required parameters:
- id (String)
    An ontology term identifier

Optional parameters:
- ontology (String)
    Filter by ontology. Used to disambiguate terms which are shared between ontologies such as GO and EFO
"""
        return self.build_rest_answer(ensembl.dict_wrapper(ensembl.info.OntologyEntry), ['json', 'xml'], ['ontology'], None, 'ontology/ancestors/chart/{0}'.format(urllib.parse.quote(str(id))), kwargs)


    def getAllFeaturesOnFeatureID(self, id, **kwargs):
        """Retrieves features (e.g. genes, transcripts, variations etc.) that overlap a region defined by the given identifier.

Return type: ensembl.genome.feature_wrapper
Valid formats: json, xml, gff3, bed
HTTP endpoint: overlap/id/:id

Required parameters:
- id (String)
    An Ensembl stable ID

Optional parameters:
- species (String)
    Species name/alias.
- object_type (String)
    Filter by feature type
- db_type (String)
    Restrict the search to a database other than the default. Useful if you need to use a DB other than core
- feature (Enum(gene, transcript, cds, exon, repeat, simple, misc, variation, somatic_variation, structural_variation, somatic_structural_variation, constrained, regulatory, segmentation, motif, chipseq, array_probe))
    The type of feature to retrieve. Multiple values are accepted.
- species_set (String)
    Filter by species set for retrieving constrained elements.
- logic_name (String)
    Limit retrieval of genes, transcripts and exons by a given name of an analysis.
- so_term (String)
    Sequence Ontology term to narrow down the possible variations returned.
- misc_set (String)
    Miscellaneous set which groups together feature entries. Consult the DB or returned data sets to discover what is available.
- biotype (String)
    The functional classification of the gene or transcript to fetch. Cannot be used in conjunction with logic_name when querying transcripts.
"""
        return self.build_rest_answer(ensembl.genome.feature_wrapper, ['json', 'xml', 'gff3', 'bed'], ['species', 'object_type', 'db_type', 'feature', 'species_set', 'logic_name', 'so_term', 'misc_set', 'biotype'], None, 'overlap/id/{0}'.format(urllib.parse.quote(str(id))), kwargs)


    def getAllFeaturesOnRegion(self, species, region, **kwargs):
        """Retrieves multiple types of features for a given region.

Return type: ensembl.genome.feature_wrapper
Valid formats: json, xml, gff3, bed
HTTP endpoint: overlap/region/:species/:region

Required parameters:
- species (String)
    Species name/alias.
- region (String)
    Query region. A maximum of 5Mb is allowed to be requested at any one time

Optional parameters:
- db_type (String)
    Specify the database type to retrieve features from if not using the core database. We automatically choose the correct type of DB for variation, comparative and regulation features.
- feature (Enum(gene, transcript, cds, exon, repeat, simple, misc, variation, somatic_variation, structural_variation, somatic_structural_variation, constrained, regulatory, segmentation, motif, chipseq, array_probe))
    The type of feature to retrieve. Multiple values are accepted.
- species_set (String)
    The species set name for retrieving constrained elements.
- logic_name (String)
    Limit retrieval of genes, transcripts and exons by the name of analysis.
- so_term (String)
    Sequence Ontology term to restrict the variations found. Its descendants are also included in the search.
- cell_type (String)
    Cell type name in Ensembl's Regulatory Build, required for segmentation feature, optional for regulatory elements.
- misc_set (String)
    Miscellaneous set which groups together feature entries. Consult the DB or returned data sets to discover what is available.
- biotype (String)
    Functional classification of the gene or transcript to fetch. Cannot be used in conjunction with logic_name when querying transcripts.
- trim_upstream (Boolean)
    Do not return features which overlap upstream end of the region.
- trim_downstream (Boolean)
    Do not return features which overlap the downstream end of the region.
"""
        return self.build_rest_answer(ensembl.genome.feature_wrapper, ['json', 'xml', 'gff3', 'bed'], ['db_type', 'feature', 'species_set', 'logic_name', 'so_term', 'cell_type', 'misc_set', 'biotype', 'trim_upstream', 'trim_downstream'], None, 'overlap/region/{0}/{1}'.format(urllib.parse.quote(str(species)), urllib.parse.quote(str(region))), kwargs)


    def getAllFeaturesOnTranslation(self, id, **kwargs):
        """Retrieve features related to a specific Translation as described by its stable ID (e.g. domains, variations).

Return type: ensembl.genome.feature_wrapper
Valid formats: json, xml
HTTP endpoint: overlap/translation/:id

Required parameters:
- id (String)
    An Ensembl stable ID

Optional parameters:
- species (String)
    Species name/alias.
- db_type (String)
    Restrict the search to a database other than the default. Useful if you need to use a DB other than core
- feature (Enum(transcript_variation, protein_feature, residue_overlap, translation_exon, somatic_transcript_variation))
    Specify the type of features requested for the translation.
- type (String)
    Type of data to filter by. By default, all features are returned. Can specify a domain or consequence type.
- so_term (String)
    Sequence Ontology term to restrict the variations found. Its descendants are also included in the search.
"""
        return self.build_rest_answer(ensembl.genome.feature_wrapper, ['json', 'xml'], ['species', 'db_type', 'feature', 'type', 'so_term'], None, 'overlap/translation/{0}'.format(urllib.parse.quote(str(id))), kwargs)


    def getRegulatoryFeatureByID(self, species, id, **kwargs):
        """Returns a RegulatoryFeature given its stable ID (e.g. ENSR00001348195)

Return type: ensembl.funcgen.RegulatoryFeature
Valid formats: json, xml
HTTP endpoint: regulatory/:species/:id

Required parameters:
- species (String)
    Species name/alias
- id (String)
    RegulatoryFeature stable ID

"""
        return self.build_rest_answer(ensembl.funcgen.RegulatoryFeature, ['json', 'xml'], [], None, 'regulatory/{0}/{1}'.format(urllib.parse.quote(str(species)), urllib.parse.quote(str(id))), kwargs)


    def getFeatureSequenceByID(self, id, **kwargs):
        """Request multiple types of sequence by stable identifier.

Return type: ensembl.genome.Sequence
Valid formats: fasta, json, text, yaml
HTTP endpoint: sequence/id/:id

Required parameters:
- id (String)
    An Ensembl stable ID

Optional parameters:
- type (Enum(genomic,cds,cdna,protein))
    Type of sequence. Defaults to genomic where applicable, i.e. not translations. cdna refers to the spliced transcript sequence with UTR; cds refers to the spliced transcript sequence without UTR.
- species (String)
    Species name/alias
- object_type (String)
    Filter by feature type
- db_type (String)
    Restrict the search to a database other than the default. Useful if you need to use a DB other than core
- format (Enum(fasta))
    Format of the data
- mask (Enum(hard,soft))
    Request the sequence masked for repeat sequences. Hard will mask all repeats as N's and soft will mask repeats as lowercased characters. Only available when using genomic sequence type.
- mask_feature (Boolean)
    Mask features on the sequence. If sequence is genomic, mask introns. If sequence is cDNA, mask UTRs. Incompatible with the 'mask' option
- expand_5prime (Int)
    Expand the sequence upstream of the sequence by this many basepairs. Only available when using genomic sequence type.
- expand_3prime (Int)
    Expand the sequence downstream of the sequence by this many basepairs. Only available when using genomic sequence type.
- multiple_sequences (Boolean)
    Allow the service to return more than 1 sequence per identifier. This is useful when querying for a gene but using a type such as protein.
"""
        return self.build_rest_answer(ensembl.genome.Sequence, ['fasta', 'json', 'text', 'yaml'], ['type', 'species', 'object_type', 'db_type', 'format', 'mask', 'mask_feature', 'expand_5prime', 'expand_3prime', 'multiple_sequences'], None, 'sequence/id/{0}'.format(urllib.parse.quote(str(id))), kwargs)


    def getSequenceOfRegion(self, species, region, **kwargs):
        """Returns the genomic sequence of the specified region of the given species.

Return type: ensembl.genome.Sequence
Valid formats: fasta, json, text, yaml
HTTP endpoint: sequence/region/:species/:region

Required parameters:
- species (String)
    Species name/alias
- region (String)
    Query region. A maximum of 10Mb is allowed to be requested at any one time

Optional parameters:
- format (Enum(fasta))
    Format of the data.
- mask (Enum(hard,soft))
    Request the sequence masked for repeat sequences. Hard will mask all repeats as N's and soft will mask repeats as lower cased characters. Only available when using genomic sequence type.
- mask_feature (Boolean)
    Mask features on the sequence. If sequence is genomic, mask introns. If sequence is cDNA, mask UTRs. Incompatible with the 'mask' option
- expand_5prime (Int)
    Expand the sequence upstream of the sequence by this many basepairs. Only available when using genomic sequence type.
- expand_3prime (Int)
    Expand the sequence downstream of the sequence by this many basepairs. Only available when using genomic sequence type.
- coord_system (String)
    Filter by coordinate system name
- coord_system_version (String)
    Filter by coordinate system version
"""
        return self.build_rest_answer(ensembl.genome.Sequence, ['fasta', 'json', 'text', 'yaml'], ['format', 'mask', 'mask_feature', 'expand_5prime', 'expand_3prime', 'coord_system', 'coord_system_version'], None, 'sequence/region/{0}/{1}'.format(urllib.parse.quote(str(species)), urllib.parse.quote(str(region))), kwargs)


    def getTaxonomyEntryByID(self, id, **kwargs):
        """Search for a taxonomic term by its identifier or name

Return type: ensembl.compara.NCBITaxon
Valid formats: json, xml, yaml
HTTP endpoint: taxonomy/id/:id

Required parameters:
- id (String)
    A taxon identifier. Can be a NCBI taxon id or a name

Optional parameters:
- simple (Boolean)
    If set the API will avoid the fetching of parent and child terms
"""
        return self.build_rest_answer(ensembl.compara.NCBITaxon, ['json', 'xml', 'yaml'], ['simple'], None, 'taxonomy/id/{0}'.format(urllib.parse.quote(str(id))), kwargs)


    def getTaxonomyClassificationByID(self, id, **kwargs):
        """Return the taxonomic classification of a taxon node

Return type: ensembl.compara.NCBITaxon
Valid formats: json, xml, yaml
HTTP endpoint: taxonomy/classification/:id

Required parameters:
- id (String)
    A taxon identifier. Can be a NCBI taxon id or a name

"""
        return self.build_rest_answer(ensembl.compara.NCBITaxon, ['json', 'xml', 'yaml'], [], None, 'taxonomy/classification/{0}'.format(urllib.parse.quote(str(id))), kwargs)


    def getTaxonomyEntryByName(self, name, **kwargs):
        """Search for a taxonomic id by a non-scientific name

Return type: ensembl.compara.NCBITaxon
Valid formats: json, xml, yaml
HTTP endpoint: taxonomy/name/:name

Required parameters:
- name (String)
    A non-scientific species name. Can include SQL wildcards

"""
        return self.build_rest_answer(ensembl.compara.NCBITaxon, ['json', 'xml', 'yaml'], [], None, 'taxonomy/name/{0}'.format(urllib.parse.quote(str(name))), kwargs)


    def getVariationByID(self, species, id, **kwargs):
        """Uses a variation identifier (e.g. rsID) to return the variation features

Return type: ensembl.variation.Variation
Valid formats: json, xml
HTTP endpoint: variation/:species/:id

Required parameters:
- species (String)
    Species name/alias
- id (String)
    Variation id

Optional parameters:
- genotypes (Boolean(0,1))
    Include individual genotypes
- phenotypes (Boolean(0,1))
    Include phenotypes
- pops (Boolean(0,1))
    Include population allele frequencies
- population_genotypes (Boolean(0,1))
    Include population genotype frequencies
"""
        return self.build_rest_answer(ensembl.variation.Variation, ['json', 'xml'], ['genotypes', 'phenotypes', 'pops', 'population_genotypes'], None, 'variation/{0}/{1}'.format(urllib.parse.quote(str(species)), urllib.parse.quote(str(id))), kwargs)


    def getVariantConsequencesByRegionAllele(self, species, region, allele, **kwargs):
        """Fetch variant consequences

Return type: ensembl.variation.VEPResult
Valid formats: json, xml
HTTP endpoint: vep/:species/region/:region/:allele/

Required parameters:
- species (String)
    Species name/alias
- region (String)
    Query region. We only support the current assembly
- allele (String)
    Variation allele

Optional parameters:
- hgvs (Boolean)
    Include HGVS nomenclature based on Ensembl stable identifiers
- ccds (Boolean)
    Include CCDS transcript identifiers
- numbers (Boolean)
    Include affected exon and intron positions within the transcript
- domains (Boolean)
    Include names of overlapping protein domains
- canonical (Boolean)
    Include a flag indicating the canonical transcript for a gene
- protein (Boolean)
    Include Ensembl protein identifiers
- xref_refseq (Boolean)
    Include aligned RefSeq mRNA identifiers for transcript. NB: theRefSeq and Ensembl transcripts aligned in this way MAY NOT, AND FREQUENTLY WILL NOT, match exactly in sequence, exon structure and protein product
"""
        return self.build_rest_answer(ensembl.variation.VEPResult, ['json', 'xml'], ['hgvs', 'ccds', 'numbers', 'domains', 'canonical', 'protein', 'xref_refseq'], None, 'vep/{0}/region/{1}/{2}/'.format(urllib.parse.quote(str(species)), urllib.parse.quote(str(region)), urllib.parse.quote(str(allele))), kwargs)


    def getVariantConsequencesByVariationID(self, species, id, **kwargs):
        """Fetch variant consequences based on a variation identifier

Return type: ensembl.variation.VEPResult
Valid formats: json, xml
HTTP endpoint: vep/:species/id/:id

Required parameters:
- species (String)
    Species name/alias
- id (String)
    Query ID. Supports dbSNP, COSMIC and HGMD identifiers

Optional parameters:
- hgvs (Boolean)
    Include HGVS nomenclature based on Ensembl stable identifiers
- ccds (Boolean)
    Include CCDS transcript identifiers
- numbers (Boolean)
    Include affected exon and intron positions within the transcript
- domains (Boolean)
    Include names of overlapping protein domains
- canonical (Boolean)
    Include a flag indicating the canonical transcript for a gene
- protein (Boolean)
    Include Ensembl protein identifiers
- xref_refseq (Boolean)
    Include aligned RefSeq mRNA identifiers for transcript. NB: theRefSeq and Ensembl transcripts aligned in this way MAY NOT, AND FREQUENTLY WILL NOT, match exactly in sequence, exon structure and protein product
"""
        return self.build_rest_answer(ensembl.variation.VEPResult, ['json', 'xml'], ['hgvs', 'ccds', 'numbers', 'domains', 'canonical', 'protein', 'xref_refseq'], None, 'vep/{0}/id/{1}'.format(urllib.parse.quote(str(species)), urllib.parse.quote(str(id))), kwargs)


    def getVariantConsequencesByHGVS(self, species, hgvs_notation, **kwargs):
        """Fetch variant consequences based on a HGVS notation

Return type: ensembl.variation.VEPResult
Valid formats: json, xml
HTTP endpoint: vep/:species/hgvs/:hgvs_notation

Required parameters:
- species (String)
    Species name/alias
- hgvs_notation (String)
    HGVS notation. May be genomic (g), coding (c) or protein (p), with reference to chromosome name, gene name, transcript ID or protein ID.

Optional parameters:
- hgvs (Boolean)
    Include HGVS nomenclature based on Ensembl stable identifiers
- ccds (Boolean)
    Include CCDS transcript identifiers
- numbers (Boolean)
    Include affected exon and intron positions within the transcript
- domains (Boolean)
    Include names of overlapping protein domains
- canonical (Boolean)
    Include a flag indicating the canonical transcript for a gene
- protein (Boolean)
    Include Ensembl protein identifiers
- xref_refseq (Boolean)
    Include aligned RefSeq mRNA identifiers for transcript. NB: theRefSeq and Ensembl transcripts aligned in this way MAY NOT, AND FREQUENTLY WILL NOT, match exactly in sequence, exon structure and protein product
"""
        return self.build_rest_answer(ensembl.variation.VEPResult, ['json', 'xml'], ['hgvs', 'ccds', 'numbers', 'domains', 'canonical', 'protein', 'xref_refseq'], None, 'vep/{0}/hgvs/{1}'.format(urllib.parse.quote(str(species)), urllib.parse.quote(str(hgvs_notation))), kwargs)



ensembl._pyrest_core.construction_rules[(ensembl.info.Assembly,'top_level_region')] = ensembl.info.SeqRegion
ensembl._pyrest_core.construction_rules[(ensembl.info.OntologyTerm,'children')] = ensembl.info.OntologyTerm
ensembl._pyrest_core.construction_rules[(ensembl.info.OntologyTerm,'parents')] = ensembl.info.OntologyTerm
ensembl._pyrest_core.construction_rules[(ensembl.info.OntologyEntry,'is_a')] = ensembl.info.OntologyTerm
ensembl._pyrest_core.construction_rules[(ensembl.info.OntologyEntry,'term')] = ensembl.info.OntologyTerm
ensembl._pyrest_core.construction_rules[(ensembl.compara.HomologyGroup,'homologies')] = ensembl.compara.HomologyPair
ensembl._pyrest_core.construction_rules[(ensembl.compara.HomologyPair,'target')] = ensembl.compara.Homolog
ensembl._pyrest_core.construction_rules[(ensembl.compara.HomologyPair,'source')] = ensembl.compara.Homolog
ensembl._pyrest_core.construction_rules[(ensembl.compara.GenomicAlignment,'alignments')] = ensembl.compara.GenomicAlignmentEntry
ensembl._pyrest_core.construction_rules[(ensembl.genome.GeneFeature,'Transcript')] = ensembl.genome.TranscriptFeature
ensembl._pyrest_core.construction_rules[(ensembl.genome.TranscriptFeature,'Translation')] = ensembl.genome.TranslationFeature
ensembl._pyrest_core.construction_rules[(ensembl.genome.TranscriptFeature,'Exon')] = ensembl.genome.ExonFeature
ensembl._pyrest_core.construction_rules[(ensembl.genome.CoordMapping,'mapped')] = ensembl.genome.Location
ensembl._pyrest_core.construction_rules[(ensembl.genome.CoordMapping,'original')] = ensembl.genome.Location
ensembl._pyrest_core.construction_rules[(ensembl.variation.Variation,'population_genotypes')] = ensembl.variation.PopulationGenotype
ensembl._pyrest_core.construction_rules[(ensembl.variation.Variation,'populations')] = ensembl.variation.PopulationAllele
ensembl._pyrest_core.construction_rules[(ensembl.variation.Variation,'genotypes')] = ensembl.variation.Genotype
ensembl._pyrest_core.construction_rules[(ensembl.variation.Variation,'mappings')] = ensembl.variation.AlleleLocation
ensembl._pyrest_core.construction_rules[(ensembl.variation.VEPResult,'colocated_variants')] = ensembl.variation.Variant
ensembl._pyrest_core.construction_rules[(ensembl.variation.VEPResult,'transcript_consequences')] = ensembl.variation.Consequence

EnsemblRestServer = RestServer(server_url = "http://rest.ensembl.org")
EnsemblGenomesRestServer = RestServer(server_url = "http://test.rest.ensemblgenomes.org")



