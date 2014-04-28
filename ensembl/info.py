
import ensembl


class Assembly(ensembl.BaseObject):
	pass

class SeqRegion(ensembl.BaseObject):
	pass

class ArchiveEntry(ensembl.BaseObject):
	pass


ensembl._pyrest.construction_rules.update({
	(Assembly, 'top_level_region'): SeqRegion
})


ensembl._pyrest.endpoint_2_class.update({
	'/archive/id/' : ArchiveEntry,
	'/assembly/info/' : Assembly
})

