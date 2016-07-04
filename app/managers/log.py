#!/usr/bin/python

import logging
import os
import yaml
import commons
import sys


class Log(object):
    
    
    def __init__(self,module):
        
        self.logger = logging.getLogger(module)
        self.console = logging.StreamHandler()
        
        self.__setLogLevel()
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.console.setFormatter(formatter)
        
        self.logger.addHandler(self.console)
        
        
    def __setLogLevel(self):
        
        settingsFileName = 'settings.yaml'
        configFileLocationIdentifier = 'config'
        
        configFileBaseLocation = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),configFileLocationIdentifier)
        settingsFileLocation = os.path.join(configFileBaseLocation,settingsFileName)
        
        with open(settingsFileLocation,'r') as stream:
                config = yaml.load(stream)
               
        level = config['log']['level']
        
        if level == 'DEBUG':
               self.logger.setLevel(logging.DEBUG)
               self.console.setLevel(logging.DEBUG)
        elif level == 'INFO':
               self.logger.setLevel(logging.INFO)
               self.console.setLevel(logging.INFO)
        elif level == 'WARNING':
               self.logger.setLevel(logging.WARN)
               self.console.setLevel(logging.WARN)
        elif level == 'ERROR':
               self.logger.setLevel(logging.ERROR)
               self.console.setLevel(logging.ERROR)
        elif level == 'CRITICAL':
               self.logger.setLevel(logging.CRITICAL)
               self.console.setLevel(logging.CRITICAL)
        else:
               self.logger.setLevel(logging.DEBUG)
               self.console.setLevel(logging.DEBUG)
               
    
    def __formalizeMessageForCode(self,msgCode,args):
        
        try:
            locale = commons.applicationConfigs['locale']
            try:
                message = commons.messages[msgCode]['message'][locale]
            except:
                message = commons.messages[msgCode]['message']['en']
          
            for msg in args:
                message = message + ' ' + str(msg)
            
            return message
        
        except Exception, e:
            
            return msgCode
        
    
    def logDebug(self,msgCode, *args):
          
          self.logger.debug(self.__formalizeMessageForCode(msgCode,args))
        
    def logInfo(self,msgCode, *args):
            
          self.logger.info(self.__formalizeMessageForCode(msgCode,args))
          
              
    def logWarn(self,msg):
        
        self.logger.warn(msg)
        
    
    def logError(self,msgCode, *args):
            
          self.logger.error(self.__formalizeMessageForCode(msgCode,args).upper())
          
        
    def logCritical(self,msg):
        
        self.logger.critical(msg)
        