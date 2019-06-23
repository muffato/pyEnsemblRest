
import sys
import ensembl

rs = ensembl.EnsemblRestServer

human_assembly = rs.getAssemblyInfo('human')
for region in human_assembly.top_level_region:
    for i in range(1, region.length+1):
        seq_struct = rs.getSequenceOfRegion('human', '{0}:{1}..{2}'.format(region.name, i, i))
        seq = seq_struct.seq
        print(region.name, i, seq)

