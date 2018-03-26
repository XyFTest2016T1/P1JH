# these directories are set up on the assumption that the three repos
# goc-gams, goc-sample-data, and eval-phase-one all sit in the same directory
# the path separator character is '/' but it will work on windows as well
# as on linux

'''
DATA_DIR = '../../../goc-sample-data/'
EVAL_DIR = '../../../eval-phase-one/'
GAMS_DIR = '../../'
'''

import gams, os, sys
sys.path.append(os.path.normpath(EVAL_DIR + 'src/'))
print sys.path
import psse, gams_utils

def test(raw_name=None, rop_name=None, inl_name=None, con_name=None, sol1_name=None, sol2_name=None, gdx_name=None, gms_name=None):

    print '\ntesting Psse'
    
    # read the psse files
    print 'reading psse files'
    p = psse.Psse()
    print 'reading raw file: %s' % raw_name
    if raw_name is not None:
        p.raw.read(os.path.normpath(raw_name))
    print 'reading rop file: %s' % rop_name
    if rop_name is not None:
        p.rop.read(os.path.normpath(rop_name))
    print 'reading inl file: %s' % inl_name
    if inl_name is not None:
        p.inl.read(os.path.normpath(inl_name))
    print 'reading con file: %s' % con_name
    if con_name is not None:
        p.con.read(os.path.normpath(con_name))
    print "buses: %u" % len(p.raw.buses)
    print "loads: %u" % len(p.raw.loads)
    print "fixed_shunts: %u" % len(p.raw.fixed_shunts)
    print "generators: %u" % len(p.raw.generators)
    print "nontransformer_branches: %u" % len(p.raw.nontransformer_branches)
    print "transformers: %u" % len(p.raw.transformers)
    #print "areas: %u" % len(p.raw.areas)
    print "switched_shunts: %u" % len(p.raw.switched_shunts)
    print "generator inl records: %u" % len(p.inl.generator_inl_records)
    print "generator dispatch records: %u" % len(p.rop.generator_dispatch_records)
    print "active power dispatch records: %u" % len(p.rop.active_power_dispatch_records)
    print "piecewise linear cost functions: %u" % len(p.rop.piecewise_linear_cost_functions)
    print 'contingencies: %u' % len(p.con.contingencies)

    # write to gdx
    print 'writing gdx file: %s' % gdx_name
    gams_utils.write_psse_to_gdx(p, os.path.normpath(gdx_name))

    # test gams
    print 'running gams model: %s' % gms_name
    ws = gams.GamsWorkspace()
    #ws.__init__(working_directory=os.getcwd())
    ws.__init__(working_directory=(os.path.normpath(GAMS_DIR + 'src/gams/')))
    job = ws.add_job_from_file(os.path.normpath(gms_name))
    opt = gams.GamsOptions(ws)
    opt.defines['ingdx'] = os.path.normpath(gdx_name)
    opt.defines['solution1'] = os.path.normpath(sol1_name)
    opt.defines['solution2'] = os.path.normpath(sol2_name)
    opt.nlp = 'knitro'
    complete = (
        raw_name is not None and
        rop_name is not None and
        inl_name is not None and
        con_name is not None and
        gdx_name is not None and
        gms_name is not None)
    if complete:
        job.run(gams_options=opt, output=sys.stdout)

def test_case14():
    '''The aim of this instance is to develop nontrivial uses of all the main model features.
    This instance was developed from the matpower case14 file.
    the cost functions are piecewise linear approximations of the original quadratic functions.
    The INL file uses the real power upper bounds for the participation factors.
    A few contingencies were made up.'''

    case_dir = DATA_DIR #+ 'case14/'
    gams_dir = GAMS_DIR #+ 'src/gams/'
    #raw_name = 'case14.raw'
    #rop_name = 'case14.rop'
    #con_name = 'case14.con'
    #inl_name = 'case14.inl'
    sol1_name = 'gams_solution1.txt'
    sol2_name = 'gams_solution2.txt'
    gdx_name = 'case14.gdx'
    gms_name = 'run_greedy.gms'
    test(
        case_dir + raw_name,
        case_dir + rop_name,
        case_dir + inl_name,
        case_dir + con_name,
        case_dir + sol1_name,
        case_dir + sol2_name,
        gams_dir + gdx_name,
        gams_dir + gms_name)
    
def test_uiuc150():
    '''The raw file comes from Tom Overbye's website.
    The other files are made up.
    INL is defined by taking all participation factors equal to
    the real power upper bounds.
    Cost functions are all constant marginal cost,
    equal to 100 dol per 5000 MW (could be 100 kdol per 5000 MW by a unit transformation).
    For the CON file, 2 contingencies were constructed,
    one for the outage of the first line listed in the RAW file,
    and the other for the outage of the second generator.'''

    case_dir = DATA_DIR + 'uiuc150/'
    gams_dir = GAMS_DIR + 'src/gams/'
    raw_name = 'uiuc150.raw'
    inl_name = 'uiuc150.inl'
    rop_name = 'uiuc150.rop'
    con_name = 'uiuc150.con'
    gdx_name = 'uiuc150.gdx'
    gms_name = 'run_greedy.gms'
    sol1_name = 'gams_solution1.txt'
    sol2_name = 'gams_solution2.txt'
    test(
        case_dir + raw_name,
        case_dir + rop_name,
        case_dir + inl_name,
        case_dir + con_name,
        case_dir + sol1_name,
        case_dir + sol2_name,
        gams_dir + gdx_name,
        gams_dir + gms_name)
    
def test_activsg200():
    '''The source of the RAW file and the procedure for generating
    INL, CON, and ROP files are the same as in uiuc150(),
    i.e. Tom Overbye, and minimal functioning product.'''

    case_dir = DATA_DIR + 'activsg200/'
    gams_dir = GAMS_DIR + 'src/gams/'
    raw_name = 'activsg200.raw'
    inl_name = 'activsg200.inl'
    rop_name = 'activsg200.rop'
    con_name = 'activsg200.con'
    gdx_name = 'activsg200.gdx'
    gms_name = 'run_greedy.gms'
    sol1_name = 'gams_solution1.txt'
    sol2_name = 'gams_solution2.txt'
    test(
        case_dir + raw_name,
        case_dir + rop_name,
        case_dir + inl_name,
        case_dir + con_name,
        case_dir + sol1_name,
        case_dir + sol2_name,
        gams_dir + gdx_name,
        gams_dir + gms_name)
    
def test_activsg500():
    '''The source of the RAW file and the procedure for generating
    INL, CON, and ROP files are the same as in uiuc150(),
    i.e. Tom Overbye, and minimal functioning product.'''

    case_dir = DATA_DIR + 'activsg500/'
    gams_dir = GAMS_DIR + 'src/gams/'
    raw_name = 'activsg500.raw'
    inl_name = 'activsg500.inl'
    rop_name = 'activsg500.rop'
    con_name = 'activsg500.con'
    gdx_name = 'activsg500.gdx'
    gms_name = 'run_greedy.gms'
    sol1_name = 'gams_solution1.txt'
    sol2_name = 'gams_solution2.txt'
    test(
        case_dir + raw_name,
        case_dir + rop_name,
        case_dir + inl_name,
        case_dir + con_name,
        case_dir + sol1_name,
        case_dir + sol2_name,
        gams_dir + gdx_name,
        gams_dir + gms_name)
    
def test_activsg2000():
    '''The source of the RAW file and the procedure for generating
    INL, CON, and ROP files are the same as in uiuc150(),
    i.e. Tom Overbye, and minimal functioning product.'''

    case_dir = DATA_DIR + 'activsg2000/'
    gams_dir = GAMS_DIR + 'src/gams/'
    raw_name = 'activsg2000.raw'
    inl_name = 'activsg2000.inl'
    rop_name = 'activsg2000.rop'
    con_name = 'activsg2000.con'
    gdx_name = 'activsg2000.gdx'
    gms_name = 'run_greedy.gms'
    sol1_name = 'gams_solution1.txt'
    sol2_name = 'gams_solution2.txt'
    test(
        case_dir + raw_name,
        case_dir + rop_name,
        case_dir + inl_name,
        case_dir + con_name,
        case_dir + sol1_name,
        case_dir + sol2_name,
        gams_dir + gdx_name,
        gams_dir + gms_name)
    
def test_sdet700():
    '''700 bus instance from SDET project'''

    case_dir = DATA_DIR + 'sdet700/'
    gams_dir = GAMS_DIR + 'src/gams/'
    #raw_name = '4_19_0_bus700_2591.raw'
    raw_name = '4_19_10_bus700_2601_volfix.raw'
    inl_name = 'bus700_testinl.inl'
    rop_name = 'sdet700.rop' # constant (0) cost
    #rop_name = '4_19_11_bus700_2602_volfix.rop' # from Renke
    #rop_name = 'sdet700_real.rop' # from Renke - change to space separated
    #con_name = '700_bus_contin_list.con' # 99 contingencies - model runs out of memory
    #con_name = '700_bus_contin_list_mod_v2.con' # modified to make it feasible
    con_name = '700_bus_contin_list_mod_v2_mod.con' # remove some contingencies
    #con_name = '700_bus_contin_list_mod_v2_nois.con' # Renke removed the island contingencies
    #con_name = 'sdet700.con' # just a few contingencies
    gdx_name = 'sdet700.gdx'
    gms_name = 'run_greedy.gms'
    sol1_name = 'gams_solution1.txt'
    sol2_name = 'gams_solution2.txt'
    test(
        case_dir + raw_name,
        case_dir + rop_name,
        case_dir + inl_name,
        case_dir + con_name,
        case_dir + sol1_name,
        case_dir + sol2_name,
        gams_dir + gdx_name,
        gams_dir + gms_name)
    
def test_tamugo500():

    case_dir = DATA_DIR + 'tamugo500/'
    gams_dir = GAMS_DIR + 'src/gams/'
    raw_name = 'TAMUGO_Stage0_500_Scenario01_031700_FEASIBLE.raw'
    inl_name = '500case.inl'
    #rop_name = '500case_bad_pmax.rop'
    rop_name = '500case.rop'
    con_name = '500case.con'
    sol1_name = 'gams_solution1.txt'
    sol2_name = 'gams_solution2.txt'
    gdx_name = 'tamu500.gdx'
    gms_name = 'run_greedy.gms'
    test(
        case_dir + raw_name,
        case_dir + rop_name,
        case_dir + inl_name,
        case_dir + con_name,
        case_dir + sol1_name,
        case_dir + sol2_name,
        gams_dir + gdx_name,
        gams_dir + gms_name)

def test_tamugo2000():

    case_dir = DATA_DIR + 'tamugo2000/'
    gams_dir = GAMS_DIR + 'src/gams/'
    #raw_name = 'TAMUGO_Stage0_2000_Scenario02_081107.raw'
    raw_name = 'TAMUGO_Stage0_2000_010300_FEASIBLE.raw'
    #raw_name = 'TAMUGO_Stage0_2000_010300_STARTING.raw'
    inl_name = '2000case.inl'
    #rop_name = '2000case_bad_pmax.rop' # cost functions do not cover the full range PMIN,PMAX
    rop_name = '2000case.rop'
    #rop_name = '2000case_single_cost.rop'
    con_name = '2000case.con'
    gdx_name = 'tamu2000.gdx'
    sol1_name = 'gams_solution1.txt'
    sol2_name = 'gams_solution2.txt'
    gms_name = 'run_greedy.gms'
    test(
        case_dir + raw_name,
        case_dir + rop_name,
        case_dir + inl_name,
        case_dir + con_name,
        case_dir + sol1_name,
        case_dir + sol2_name,
        gams_dir + gdx_name,
        gams_dir + gms_name)

def test_uw2000():
    '''1400 bus system from Chris DeMarco and Byungkwon Park (UW - Madison).
    represents Wisconsin grid'''

    case_dir = DATA_DIR + 'uw2000/'
    gams_dir = GAMS_DIR + 'src/gams/'
    #raw_name = 'WI2000ShuntsCase4.raw' # unable to read this - not enough columns
    raw_name = 'WI2000Shunt4Revised.raw'
    inl_name = 'part_fact_1.inl'
    rop_name = 'cost_0.rop'
    #con_name = 'Contingency-List-Easy-WIShunt4.con'
    con_name = 'Contingency-List-Hard-WIShunt4.con'
    gdx_name = 'uw2000.gdx'
    sol1_name = 'gams_solution1.txt'
    sol2_name = 'gams_solution2.txt'
    gms_name = 'run_greedy.gms'
    test(
        case_dir + raw_name,
        case_dir + rop_name,
        case_dir + inl_name,
        case_dir + con_name,
        case_dir + sol1_name,
        case_dir + sol2_name,
        gams_dir + gdx_name,
        gams_dir + gms_name)

def main():
	import sys
	
	args = sys.args

	#global DATA_DIR
	global EVAL_DIR
	global GAMS_DIR
	
	EVAL_DIR="."
	GAMS_DIR = 'gams/'
	
	raw = args[1]
	rop = args[2]
	con= args[3]
	inl = args[4]
    	gdx_name = 'case.gdx'
	gms_name = 'run_greedy.gms'
	
	sol1_name = 'solution1.txt'
	sol2_name = 'solution2.txt'

    	test(raw,rop,inl,con,sol1_name,sol2_name,gams_dir + gdx_name,gams_dir + gms_name)



'''
def test_all():

    #test_case14()
    #test_uiuc150()
    #test_activsg200()
    #test_activsg500()
    #test_activsg2000()
    #test_sdet700()
    #test_tamugo500()
    #test_tamugo2000()
    #test_uw2000()
'''

if __name__ == '__main__':
	main()
