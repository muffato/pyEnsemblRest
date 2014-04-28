
import ensembl

rs = ensembl.RestServer()

def test_GeneTree():
	g = rs.getGeneTreeById('ENSGT00390000003602')

	print g.tree.taxonomy.scientific_name
	print type(g)
	print g.__class__
	print g.tree
	print type(g.tree)
	print type(g.tree.taxonomy)
	print type(g.tree.taxonomy.scientific_name)
	print type(g.tree.children)
	print type(g.tree.children[0])

	print g.get_all_leaves
	print g.get_all_leaves.__doc__
	print g.tree.__doc__
	#print g.get_all_leaves()
	print rs.getGeneTreeById('ENSGT00390000003602', format='nh')

def test_Assembly():
	g = rs.getAssemblyInfo('human')

	print type(g)
	print g.__class__
	print g.assembly_date
	print g.coord_system_versions
	print g.top_level_region[0]
	print g.top_level_region[0].length

def test_Archive():
	g = rs.getArchiveEntry('ENSG00000157764')

	print type(g)
	print g.__class__
	print g

test_GeneTree()
test_Archive()
test_Assembly()
test_Archive()
import time
time.sleep(4)
test_Archive()
test_Archive()
