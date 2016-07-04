#!/usr/bin/env python

import app.managers as Managers

class Main(object):
    
    def __init__(self, ):
        self.commonManager = Managers.Commons()
        self.logManager = Managers.Log(__name__)
        self.pingManager = Managers.Pinger()
        self.repotManager = Managers.Report()
        
        self.services = {}
    


    def __getServices(self):
        
        self.services = self.commonManager.readYAMLFile(self.commonManager.servicesFileLocation)['services']
    
    
    def __ping(self):
        
        self.pingManager.ping(self.services)
    
    def startTesting(self):
        
        self.logManager.logInfo('TestingStarted')
        
        self.__getServices()
        self.__ping()


if __name__ == '__main__':
    
    main = Main()
    main.startTesting()