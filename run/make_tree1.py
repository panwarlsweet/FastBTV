#! /bin/env cmsRun
import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

options.register('reportEvery', 100,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    "Report every N events (default is N=10)"
)
options.register('wantSummary', False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Print out trigger and timing summary"
)

## 'maxEvents' is already registered by the Framework, changing default value
options.setDefault('maxEvents', -1)

options.parseArguments()

from Configuration.StandardSequences.Eras import eras
process = cms.Process("USER", eras.Run3)


process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mcRun3_2024_realistic_v4')

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

## Events to process
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

## Input files
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring("")
)


## Output file
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string("QCD_Run3.root")
)

## Options and Output Report
process.options   = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(options.wantSummary),
    allowUnscheduled = cms.untracked.bool(True)
)


#################################################
## Update PAT jets
#################################################

from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

## b-tag discriminators
bTagDiscriminators = [
    'pfCombinedInclusiveSecondaryVertexV2BJetTags',
    'pfDeepCSVJetTags:probudsg',        
    'pfDeepCSVJetTags:probb',           
    'pfDeepCSVJetTags:probc',           
    'pfDeepCSVJetTags:probbb',          
    'pfDeepFlavourJetTags:probb',
    'pfDeepFlavourJetTags:probbb',
    'pfDeepFlavourJetTags:probc',
    'pfDeepFlavourJetTags:probuds',
    'pfDeepFlavourJetTags:problepb',
    'pfDeepFlavourJetTags:probg',
]

from PhysicsTools.PatAlgos.tools.jetTools import *
"""updateJetCollection(
    process,
    jetSource = cms.InputTag('slimmedJets'),
    jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    btagDiscriminators = bTagDiscriminators
)"""

#update training
#process.pfDeepFlavourJetTags.graph_path = cms.FileInPath('RecoBTag/Combined/data/DeepFlavourV03_10X_training/constant_graph.pb')
#process.pfDeepFlavourJetTags.lp_names = cms.vstring('cpf_input_batchnorm/keras_learning_phase')

## Initialize analyzer
process.bTaggingExerciseIIAK4Jets = cms.EDAnalyzer(
    'FastBTV',
    jets = cms.InputTag('slimmedJets'), # input jet collection name
    puInfo=cms.InputTag("slimmedAddPileupInfo"),
    bDiscriminators = cms.PSet(
        CSVv2 = cms.vstring('pfCombinedInclusiveSecondaryVertexV2BJetTags'),
        DeepCSV = cms.vstring(
            'pfDeepCSVJetTags:probb',
            'pfDeepCSVJetTags:probbb'
            ),
        DeepFlavour = cms.vstring(
            'pfDeepFlavourJetTags:probb',
            'pfDeepFlavourJetTags:probbb',
            'pfDeepFlavourJetTags:problepb'
            ),
    )
)

process.task = cms.Task()
for mod in process.producers_().itervalues():
    process.task.add(mod)
for mod in process.filters_().itervalues():
    process.task.add(mod)

## Let it run
process.p = cms.Path(
     process.bTaggingExerciseIIAK4Jets
    ,process.task ) 

open('dump.py', 'w').write(process.dumpPython())
