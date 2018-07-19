#! /bin/env cmsRun
import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

options.register('reportEvery', 10,
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

process = cms.Process("USER")


process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '101X_upgrade2018_realistic_HEmiss_v1')

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

## Events to process
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

## Input files
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles)
)


## Output file
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(options.outputFile)
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
updateJetCollection(
    process,
    jetSource = cms.InputTag('slimmedJets'),
    jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    btagDiscriminators = bTagDiscriminators
)

## Initialize analyzer
process.bTaggingExerciseIIAK4Jets = cms.EDAnalyzer(
    'FastBTV',
    jets = cms.InputTag('selectedUpdatedPatJets'), # input jet collection name
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
