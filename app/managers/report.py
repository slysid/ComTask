#!/usr/bin/python

from jinja2 import Environment, PackageLoader
import commons
import log
import datetime

class Report(object):
    
    
    def __init__(self):
        
        self.env = Environment(loader=PackageLoader('app', 'templates'))
        self.template = self.env.get_template('template.html')
        self.logManager = log.Log(__name__)
        
    
    def renderHTMLFile(self,renderdata):
        
        common = commons.Commons()
        templateData =  common.readYAMLFile(common.templateFileLocation)
        
        self.logManager.logDebug(templateData)
        
        
        templateData['reporttime'] = datetime.datetime.now().strftime(templateData['dateformat'])
        
        
        reportHTML = self.template.render(datas=renderdata,templateData=templateData)
        
        
        fh = open(common.reportsFileLocation,'w+')
        fh.write(reportHTML)
        fh.close()
        
        self.logManager.logInfo('FileDownload',' ',common.reportsFileLocation )