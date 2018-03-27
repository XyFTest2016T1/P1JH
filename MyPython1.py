import gams, os, sys
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
    ws.__init__(working_directory=(os.path.normpath(GAMS_DIR)))
    job = ws.add_job_from_file(gms_name)
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



def main():
	import sys
	
	args = sys.argv

	global GAMS_DIR
	GAMS_DIR = 'gams/'
	
	con = args[1]
	inl = args[2]
	raw = args[3]
	rop = args[4]
    	gdx = GAMS_DIR + 'case.gdx'
	gms = GAMS_DIR + 'run_greedy.gms'
	
	sol1_name = 'solution1.txt'
	sol2_name = 'solution2.txt'
	
	print("raw: " + raw)
	print("rop: " + rop)
	print("con: " + con)
	print("inl: " + inl)
	print("gdx: " + gdx)
	print("gms: " + gms)
	print("sol1:" + sol1_name)
	print("sol2:" + sol2_name)

    	test(raw,rop,inl,con,sol1_name,sol2_name, gdx,gms)

if __name__ == '__main__':
	main()
