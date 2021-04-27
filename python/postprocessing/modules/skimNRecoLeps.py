import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import TLorentzVector

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class skipNRecoLeps(Module):
    def __init__(self, isdata = False, year = 17, recalibjets = '', era = ''):
        self.minelpt    =  8
        self.minmupt    =  8
        self.leadleppt  = 20
        self.maxeleta = 2.5
        self.maxmueta = 2.5
        self.isData = isdata
        self.year = year
        self.era = era
        self.filenameJECrecal = recalibjets
        #self.jetReCalibrator = self.OpenJECcalibrator()
        
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        #jets = Collection(event, 'Jet')
        return True
        elec = Collection(event, 'Electron')
        muon = Collection(event, 'Muon')

        nlepgood = 0; minptLeading = False
        lepCharge = []
        for mu in muon:
          if mu.pt > self.minmupt and abs(mu.eta) < self.maxmueta:# and (mu.tightId or mu.mediumId): 
            nlepgood += 1
            lepCharge.append(mu.charge)
            if mu.pt >= self.leadleppt: minptLeading = True
        for el in elec:
          if el.pt > self.minelpt and abs(el.eta) < self.maxeleta: #and (el.cutBased >= 1): 
            nlepgood += 1
            lepCharge.append(el.charge)
            if el.pt >= self.leadleppt: minptLeading = True

        #if   nlepgood < 2:   return False
        #elif nlepgood == 2:  return ((lepCharge[0] * lepCharge[1] > 0) and minptLeading)
        #else              :  return minptLeading
        
        return nlepgood >= 2 and minptLeading

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

skimRecoLeps = lambda : skipNRecoLeps()
