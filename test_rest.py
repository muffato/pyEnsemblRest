
import sys
import ensembl

rs = ensembl.EnsemblRestServer

def test_GeneTree():
    g = rs.getGeneTreeById('ENSGT00390000003602')
    print(g.tree.taxonomy.scientific_name)
    print(type(g))
    print(g.__class__)
    #print(g.tree)
    print(type(g.tree))
    print(type(g.tree.taxonomy))
    print(type(g.tree.taxonomy.scientific_name))
    print(type(g.tree.children))
    print(type(g.tree.children[0]))

    print(g.get_all_leaves)
    print(g.get_all_leaves.__doc__)
    print(g.tree.__doc__)
    #print g.get_all_leaves()
    print(rs.getGeneTreeById('ENSGT00390000003602', aligned=1, output_format='phyloxml'))
    rs.getGeneTreeByMemberId("ENSG00000139618")
    rs.getGeneTreeByMemberSymbol("human", "brca2")

def test_Assembly():
    g = rs.getAssemblyInfo('human')

    print(type(g))
    print(g.__class__)
    print(g.assembly_date)
    print(g.coord_system_versions)
    print(g.top_level_region[0])
    print(g.top_level_region[0].length)

    print(rs.getAssemblyInfoRegion('human', 19, output_format='json', badarg=4))

def test_Archive():
    g = rs.getArchiveEntry('ENSG00000157764')

    print(type(g))
    print(g.__class__)
    print(g)

def test_others():
    print("ping", rs.ping())
    print("rest_version", rs.rest_version())
    print("ensembl_version", rs.ensembl_version())
    print("compara_databases", rs.listComparaDatabases())
    print("compara_methods", rs.getAllComparaMethods())
    print("1 species", rs.listSpecies()[0])
    print("chicken logic_names", rs.getAnalysisList('chicken'))
    print("MLSS", rs.getSpeciesSetByComparaMethod('EPO'))
    print("releases", rs.listAvailableReleases())
    print("funcgen", rs.getRegulatoryFeatureByID('human', 'ENSR00001348195'))

def test_Compara():
    print("alignment", rs.getGenomicAlignmentByRegion("taeniopygia_guttata", "2:106040000-106040050:1", species_set_group="sauropsids"))
    print("homologs", rs.getHomologyByGeneStableID("ENSG00000139618"))

def test_Lookup():
    print("gene lookup", rs.lookupIdentifier('ENSG00000157764', expand=1))
    print("transcript lookup", rs.lookupIdentifier('ENST00000496384', expand=1))
    print("translation lookup", rs.lookupIdentifier('ENSP00000419060'))
    print("exon lookup", rs.lookupIdentifier('ENSE00003685923'))

def test_Mapping():
    print("genome", rs.mapCoordinatesBetweenAssemblies('human', 'GRCh37', 'X:1000000..1000100:1', 'GRCh38'))
    print("cdna", rs.mapCDNACoordinatesToGenome('ENST00000288602', '100..300'))
    print("cds", rs.mapCDSCoordinatesToGenome('ENST00000288602', '1..1000'))
    print("translation", rs.mapProteinCoordinatesToGenome('ENSP00000288602', '100..300'))

def test_Sequence():
    print("prot", rs.getFeatureSequenceByID('ENSP00000288602'))
    print("gene", rs.getFeatureSequenceByID('ENSG00000157764'))
    print("ccds", rs.getFeatureSequenceByID('CCDS5863.1'))
    print("ccds cds only", rs.getFeatureSequenceByID('CCDS5863.1', object_type='transcript', db_type='otherfeatures', type='cds', species='human'))
    print("transcript cdna", rs.getFeatureSequenceByID('ENST00000288602', type='cdna'))
    print("transcript cds", rs.getFeatureSequenceByID('ENST00000288602', type='cds'))
    print("exon genomic", rs.getFeatureSequenceByID('ENSE00001154485', type='genomic'))
    print("exon with_5_prime", rs.getFeatureSequenceByID('ENSE00001154485', type='genomic', expand_5prime=10))
    print("genscan", rs.getFeatureSequenceByID('GENSCAN00000000001', object_type='predictiontranscript', db_type='core', type='protein', species='human'))
    print("multi seq", rs.getFeatureSequenceByID('ENSG00000157764', multiple_sequences=1, type='protein'))
    print("region", rs.getSequenceOfRegion('human', 'X:1000000..1000100:1'))
    print("region contig", rs.getSequenceOfRegion('human', 'ABBA01004489.1:1..100', coord_system='seqlevel'))
    print("region", rs.getSequenceOfRegion('human', 'X:1000000..1000100:1', expand_5prime=60, expand_3prime=60))
    print("region", rs.getSequenceOfRegion('human', 'X:1000000..1000100:1', mask='soft'))

def test_Variation():
    print("variation", rs.getVariationByID('human', 'rs56116432'))
    print("variation genotypes", rs.getVariationByID('human', 'rs56116432', genotypes=1))
    print("variation populations", rs.getVariationByID('human', 'rs56116432', populations=1))
    print("variation population_genotypess", rs.getVariationByID('human', 'rs56116432', population_genotypes=1))

def test_Taxonomy():
    print("human", rs.getTaxonomyEntryByID(9606))
    print("human classification", len(rs.getTaxonomyClassificationByID(9606)))
    print("homo wildcard", len(rs.getTaxonomyEntryByName('homo%')))

def test_Ontology():
    print("id", rs.getOntologyByID('GO:0005667'))
    print("name", rs.getOntologyByName('transcription factor complex'))
    print("descendants", rs.getAllDescendantsOfOntologyID('GO:0005667'))
    print("ancestors", rs.getAllAncestorsOfOntologyID('GO:0005667'))
    print("ancestor_chart", rs.getOntologyAncestorChart('GO:0005667'))

def test_Overlap():
    print("id", rs.getAllFeaturesOnFeatureID('ENSG00000157764', feature=["cds","gene"]))
    print("region", rs.getAllFeaturesOnRegion('human', '7:140424943-140624564', feature=['transcript', 'exon']))
    print("translation", rs.getAllFeaturesOnTranslation('ENSP00000288602'))

def test_VEP():
    print("id", rs.getVariantConsequencesByVariationID('human', 'COSM476'))
    print("id", rs.getVariantConsequencesByVariationID('human', 'rs116035550'))
    print("region_allele", rs.getVariantConsequencesByRegionAllele('human', '9:22125503-22125502:1', 'C'))
    print("region_allele", rs.getVariantConsequencesByRegionAllele('human', '1:6524705:6524705', 'T'))
    print("region_allele", rs.getVariantConsequencesByRegionAllele('human', '7:100318423-100321323:1', 'DUP'))
    print("region_allele", rs.getVariantConsequencesByHGVS('human', 'AGT:c.803T>C'))
    print("region_allele", rs.getVariantConsequencesByHGVS('human', 'ENST00000003084:c.1431_1433delTTC'))
    print("region_allele", rs.getVariantConsequencesByHGVS('human', '9:g.22125504G>C'))


test_VEP()
test_Overlap()
test_Ontology()
test_Mapping()
test_Lookup()
test_Sequence()
test_Variation()
test_Taxonomy()
test_Archive()
test_GeneTree()
test_Compara()
test_Assembly()
test_others()

sys.exit(0)
test_Archive()
import time
time.sleep(4)
test_Archive()
test_Archive()
