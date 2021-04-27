#!/usr/bin/env python
import os, sys, json
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from PhysicsTools.NanoAODTools.postprocessing.modules.skimNRecoLeps import *

### SKIM 
#cut = 'Jet_pt > 200 && (nElectron + nMuon) >= 2 && nGenDressedLepton >= 2'
cut = '(nElectron + nMuon) >= 2'

### SLIM FILE
slimfilein  = "SlimFileIn.txt"
slimfileout = "SlimFileOut.txt"

isData    = 'data' in sys.argv[-1] or 'Data' in sys.argv[-1]

### Json file
jsonfile = runsAndLumis()
  
'''
if not isData: 
  if   year == 16:  
    mod.append(puWeight_2016())
    mod.append(PrefCorr2016())
  elif year == 17:  
    mod.append(puWeight_2017()) # puAutoWeight_2017 
    mod.append(PrefCorr2017())
  elif year == 18:  
    #jecfile  = "Autumn18_V19_MC"
    #jecarc   = "Autumn18_V19_MC"
    mod.append(puWeight_2018())
  else           :  mod.append(puWeight_2017())
'''

mod.append(skimRecoLeps())
print '>> Slim file in : ', slimfilein
print '>> Slim file out: ', slimfileout
print '>> cut: ', cut
print '>> ' + ('Is data!' if isData else 'Is MC!')
print '>> ' + ('Creating a TnP Tree' if doTnP else 'Creating a skimmed nanoAOD file')
if doJECunc: print '>> Adding JEC uncertainties'

#mod = [puAutoWeight(),jetmetUncertainties2017All(), skimRecoLeps()]
p=PostProcessor(".",inputFiles(),cut,slimfilein,mod,provenance=True,fwkJobReport=True,jsonInput=jsonfile,outputbranchsel=slimfileout) #jsonInput
p.run()

print "DONE"
os.system("ls -lR")
