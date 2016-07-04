#!/usr/bin/python

import yaml
import os
import log
import sys
 

applicationConfigs = {}
messages = {'NoFileExists' : {'message' : { 'en': 'No such file exists','se' : 'Ingen sadan fil existerar'}}}

class Commons(object):
    
    def __init__(self):
        
        self.settingsFileName = 'settings.yaml'
        self.servicesFileName = 'services.yaml'
        self.messagesFileName = 'messages.yaml'
        self.templateFileName = 'template.yaml'
        self.configFileLocationIdentifier = 'config'
        self.reportFileLocationIdentifier = 'reports'
        self.reportsFileName = 'report.html'
        self.applicationConfig = {}
        
        self.configFileBaseLocation = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),self.configFileLocationIdentifier)
        self.reportsFileBaseLocation = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),self.reportFileLocationIdentifier)
        self.servicesFileLocation = os.path.join(self.configFileBaseLocation,self.servicesFileName)
        self.settingsFileLocation = os.path.join(self.configFileBaseLocation,self.settingsFileName)
        self.messagesFileLocation = os.path.join(self.configFileBaseLocation,self.messagesFileName)
        self.reportsFileLocation = os.path.join(self.reportsFileBaseLocation,self.reportsFileName)
        self.templateFileLocation = os.path.join(self.configFileBaseLocation,self.templateFileName)
        
        self.logManager = log.Log(__name__)
        
        #self.__bootstrapApplication()
    
    
    def bootstrapApplication(self):
        
        global applicationConfigs
        global messages
        
        applicationConfigs = self.readYAMLFile(self.settingsFileLocation)
        data = self.readYAMLFile(self.messagesFileLocation)
        messages.update(data)
        
        self.logManager.logDebug('AppBootStrapped')
        
        
    def readYAMLFile(self,filepath):
        
          if os.path.exists(filepath):
               with open(filepath,'r') as stream:
                    data = yaml.load(stream)
               
               return data
          else:
               self.logManager.logDebug('NoFileExists', filepath)
               sys.exit(1)
        
        