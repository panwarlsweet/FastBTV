name   =   'QCD_1'
from   CRABClient.UserUtilities import config, getUsernameFromSiteDB
config   =   config()
config.General.workArea   =   'crab_'+name
config.General.transferOutputs   =   True
config.General.transferLogs   =   True
config.General.requestName   =   'QCD_1'
config.JobType.pluginName   =   'Analysis'
config.JobType.psetName   ='make_tree.py'
config.JobType.maxMemoryMB   =   2400
config.JobType.maxJobRuntimeMin   =   2750
config.JobType.outputFiles   =   ['out_tree_qcd.root']
config.Data.inputDBS   =   'global'
config.Data.splitting   =   'FileBased'
config.Data.publication   =   False
config.Data.allowNonValidInputDataset = True
config.Data.inputDataset   =  '/RelValQCD_FlatPt_15_3000HS_13/CMSSW_10_4_0-PU25ns_103X_mc2017_realistic_v2_HS_ref-v1/MINIAODSIM'
config.Data.unitsPerJob   =  1
config.Data.totalUnits   =   -1
config.Data.outputDatasetTag = 'QCD_1'
config.Data.outLFNDirBase = '/store/user/%s/t3store2/QCD_1' % (getUsernameFromSiteDB())
config.Site.storageSite = 'T2_IN_TIFR'




