
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


test_Archive()
test_GeneTree()
test_Assembly()
test_others()

sys.exit(0)
test_Archive()
import time
time.sleep(4)
test_Archive()
test_Archive()
