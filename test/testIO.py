import unittest as U
from parse_KGML import *
from nose import SkipTest

class _BaseKGMLFile(U.TestCase):
    """
    base test class
    """
    known_values = {
        'nodes': [],
        'edges': [],
        'genes': [],
    }

    pathway_file = ''
    pathway_type = ''

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=None)
        if (not cls.known_values['edges'] or not cls.known_values['nodes'] or not cls.pathway_file): #TODO: update
            raise SkipTest("incomplete test unit")

        (tree, graph, nodes, genes, reactions) = KGML2Graph(cls.pathway_file)
        cls.graph = graph
        cls.genes_graph = graph.get_genes()

    def setUp(self):
        pass

    def test_nodes(self):
        """
        Assert that Kegg2Graph parses nodes correctly
        """
        self.assertEqual(sorted(self.known_values['nodes']), sorted(self.graph.nodes()))

    def test_genes(self):
        known_genes = sorted(self.known_values['genes'])
        graph_genes = sorted(self.genes_graph.nodes())
        print set(known_genes).difference(set(graph_genes))
        print set(graph_genes).difference(set(known_genes))
        self.assertEqual(known_genes, graph_genes)

class _BaseKOFile(_BaseKGMLFile):
    """
    KGML file corresponding to a KO pathway
    (beginning with ko)
    """
    pathway_type = 'ko'

class _BaseOrganismFile(_BaseKGMLFile):
    """
    KGML file corresponding to an organism
    (i.e. not a 'ko0000x' file)
    """
    pathway_type = 'o'

class test_GlycolisisHSA00010(_BaseOrganismFile):
    pathway_file = './data/hsa00010.xml'
    known_values = {
        'nodes': ['Pyruvate metabolism', 'C00068', 'C00024', 'C00103', 'BPGM', 
            'C00022', 'C00267', 'Carbon fixation in photosynthetic organisms', 
            'GAPDH', 'LDHAL6A', 'TPI1', 'AKR1A1', 'FBP1', 'C05378', 'GPI', 
            'C06188', 'PKLR', 'C01451', 'C05125', 'C00031', 'C15972', 'C06186', 
            'C06187', 'PFKL', 'C00668', 'C00197', 'C00236', 'PGK1', 'C00036', 
            'C15973', 'PDHA1', 'C00111', 'C00033', 'Starch and sucrose metabolism', 
            'DLD', 'ACSS2', 'GCK', 'PGM1', 'C00074', 'C00118', 'ENO1', 'DLAT', 
            'ALDH3A1', 'ALDOA', 'GALM', 'C05345', 'C00084', 'C00631', 'C00221', 
            'Propanoate metabolism', 'C01172', 'C01159', 'G6PC', 'PGAM4', 
            'ALDH2', 'Pentose phosphate pathway', 'PCK1', 'C00469', 'ADH1A', 
            'C00186', 'C16255', 'Citrate cycle (TCA cycle)', 
            'TITLE:Glycolysis / Gluconeogenesis'],
        'genes': ['PCK1', 'BPGM', 'ALDH3A1', 'GAPDH', 'LDHAL6A', 'TPI1', 'AKR1A1', 
            'FBP1', 'PKLR', 'PFKL', 'PGK1', 'PDHA1', 'GPI',  'ACSS2', 'GCK', 
            'PGM1', 'ENO1', 'DLAT', 'ALDOA', 'GALM', 'G6PC', 'PGAM4', 'ALDH2', 
            'ADH1A', 'DLD'],
         'edges': ['']
    }

class test_NglycanHSA00510(_BaseOrganismFile):
    pathway_file = './data/hsa00510.xml'
    known_values = {
        'nodes': ['ALG8', 'ALG9', 'GCS1', 'ST6GAL1', 'ALG2', 'ALG3', 
            'Fructose and mannose metabolism', 'ALG6', 'GANAB', 'ALG5', 
            'G00003', 'G00002', 'G00001', 'ALG10B', 'G00007', 'G00006', 'G00005', 
            'G00004', 'G00009', 'G00008', 'DAD1', 'G10598', 'C00621', 
            'Other glycan degradation', 'G00021', 'G00020', 
            'Keratan sulfate biosynthesis', 'G00022', 
            'High-mannose type N-glycan biosynthesis', 'C01246', 'MGAT5B', 
            'MAN1A2', 'B4GALT1', 'DPM3', 'DPM2', 'C00096', 'MGAT2', 'ALG1', 
            'C00110', 'C03862', 'MAN2A1', 'G00014', 'G00015', 'G00016', 'G00017', 
            'G00011', 'G00012', 'G00013', 'ALG14', 'ALG11', 'ALG12', 'ALG13', 
            'G00018', 'G00019', 'TITLE:N-Glycan biosynthesis', 
            'Glycosylphosphatidylinositol(GPI)-anchor biosynthesis', 'DOLPP1', 
            'G10526', 'MGAT1', 'C00381', 'G00171', 'MGAT3', 'G10599', 'C03021', 
            'DPM1', 'MGAT4B', 'RFT1', 'DPAGT1', 'G10597', 'G10595', 'G10596', 
            'FUT8'  ], 
         'genes': ['RPN1', 'ALG8','ALG9', 'GCS1','ST6GAL1','ALG2','ALG3','ALG1',
            'ALG6','RPN2','ALG5','DOLPP1','DDOST','ALG11','MGAT5','DAD1','MGAT5B',
            'B4GALT1','B4GALT3','B4GALT2','DPM3','DPM2','DPM1','DPAGT1','GANAB',
            'MAN2A1','MGAT1','MGAT2','MAN1C1','MGAT3','ALG10','STT3B','ALG12',
            'ALG13','ALG14','MAN1A1','MAN1A2','MAN1B1','ALG10B','MGAT4A','MGAT4B',
            'RFT1','FUT8'],          # These values have been annotated manually 
#         'genes': [
#            'ALG8', 'ALG9', 'GCS1', 'ST6GAL1', 'ALG2', 'ALG3', 'ALG1', 'ALG6', 
#            'GANAB', 'ALG5', 'DOLPP1', 'ALG10B', 'DAD1', 
#            'MGAT5B', 'B4GALT1', 'DPM3', 'DPM2', 'DPM1', 'DPAGT1', 'MAN2A1', 'MGAT1', 
#            'MGAT2', 'MGAT3', 'ALG11', 'ALG12', 
#            'ALG13', 'ALG14', 'MAN1A2', 'MGAT4B', 'RFT1', 'FUT8'
#            ], 
        'edges': ['']
    }

