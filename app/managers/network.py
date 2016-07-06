#!/usr/bin/python

from gevent import monkey
monkey.patch_all()
import log
import commons
import gevent
import socket
import subprocess
import datetime
import urllib2
import report
import sys


class Network(object):
     
     def __init__(self, ):
          
          self.logManager = log.Log(__name__)
          self.commonManager = commons.Commons()
          self.socketTimeout = 3
          self.maxPingCount = 3
          self.portResponseData = {}
          self.hostResponseData = {}
          self.dnsResponseData = {}
          self.threads = []
          
     
     
     def __getsocketType(self,protocol):
          
          socketTypes = {'tcp':socket.SOCK_STREAM,'udp':socket.SOCK_DGRAM}
          
          if protocol.lower() in socketTypes:
               return socketTypes[protocol.lower()]
          else:
               return socketTypes('tcp')
     
     
     def __portCheckReachability(self,host,port,protocol):
          
          socketType = self.__getsocketType(protocol)
          sock = socket.socket(socket.AF_INET,socketType)
          sock.settimeout(self.socketTimeout)
          
          try:
               sock.connect((host,port))
               data = {'message' : 'reachable','port':port,'protocol':protocol}
               self.portResponseData[host] = data
          except socket.error as e:
               data = {'message' : str(e),'port':port,'protocol':protocol}
               self.portResponseData[host] = data
               
          sock.close()
          
          self.logManager.logDebug('Port Reachability Check Completed for Host',host)
          
     
     def __getWebResponse(self,host,port,protocol):
          
          if protocol == 'tcp':
               
               try:
                     socket.inet_aton(host)
                     url = 'https://{0}:{1}'.format(host,port)
               except:
                    ip = socket.gethostbyname(host)     
                    url = 'https://{0}:{1}'.format(ip,port)
               
               try:
                    respTimes = []
                    for index in range(self.maxPingCount):
                         startTime = datetime.datetime.now()
                         response = urllib2.urlopen(url,timeout=2).read()
                         endTime = datetime.datetime.now()
                         diff = (endTime - startTime).total_seconds() * 1000
                         respTimes.append(diff)
                    
                    resp = {}
                    resp['min'] = min(respTimes)
                    resp['avg'] = round(sum(respTimes) / float(len(respTimes)),3)
                    resp['max'] = max(respTimes)
                    resp['msg'] = ''
                    
                    self.hostResponseData[host] = resp
                    
               except Exception,e:
                    self.__checkResponseTime(host)
          else:
               self.__checkResponseTime(host)
          
      
     def __checkResponseTime(self,host):
          
          #self.logManager.showDebugMessage('PingingHosts', host)
          
          resp = subprocess.Popen(['ping', '-c', str(self.maxPingCount), host],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
          out,err = resp.communicate()
          
          if err == '':
               self.__parsePingOutput(host,out)
          else:
               self.__parsePingOutput(host,err)
          
     
     def __parsePingOutput(self,host,response):
          
          startIndex = response.find('ping statistics')
          if startIndex > 0:
               startIndex = response.find('round-trip')
               if startIndex > 0:
                    responseRawData = response[startIndex:].split('=')
                    responseRawData = responseRawData[-1].replace(' ','').replace('\n','').replace('ms','').split('/')
          
                    resp = {}
                    resp['min'] = responseRawData[0]
                    resp['avg'] = responseRawData[1]
                    resp['max'] = responseRawData[2]
                    resp['msg'] = ''
          
                    self.hostResponseData[host] = resp
               else:
                    responseRawData = response.split('---')
                    
                    resp = {}
                    resp['min'] = '0'
                    resp['avg'] = '0'
                    resp['max'] = '0'
                    resp['msg'] = responseRawData[-1]
                    
                    self.hostResponseData[host] = resp
          else:
               resp = {}
               resp['min'] = '0'
               resp['avg'] = '0'
               resp['max'] = '0'
               resp['msg'] = response.replace('\n','')
               
               self.hostResponseData[host] = resp
               
          self.logManager.logDebug('Web response/Ping Check Completed for Host',host)
             
     
     
     def __resolveDNSAndResponseTime(self,host,protocol):
          
          try:
              socket.inet_aton(host)
              self.dnsResponseData[host] = { 'dns':'0.0'}
          except socket.error, e:
               try:
                    dnsTime = 0.0
                    dnsTimes = []
               
                    for index in range(self.maxPingCount):
                         startTime = datetime.datetime.now()
                         ip = socket.gethostbyname(host)
                         endTime = datetime.datetime.now()
                         diff = (endTime - startTime).total_seconds() * 1000
                         dnsTimes.append(diff)
                    dnsTime = sum(dnsTimes) / float(len(dnsTimes))
                    dnsTime = round(dnsTime,3)
                    data = {'dns':str(dnsTime)}
                    self.dnsResponseData[host] = data
               except Exception,e:
                    data = {'dns':'Not able to resolve'}
                    self.dnsResponseData[host] = data
                    
          self.logManager.logDebug('DNS Resoultion Check Completed for Host',host)
          
          
     def __renderHTML(self,renderdata):
          
          self.logManager.logInfo('RenderHTML')
          
          reportManager = report.Report()
          reportManager.renderHTMLFile(renderdata)
          
     
     def ping(self,services):
          
          for host in services:
               
               protocol = services[host]['protocol']
               port = services[host]['port']
               
               self.logManager.logDebug('Starting services for host ', host)
               
               self.logManager.logDebug('Port Reachability Check')
               thread = gevent.spawn(self.__portCheckReachability,host,port,protocol)
               self.threads.append(thread)
               
               self.logManager.logDebug('DNS Resolution Check')
               dnsThread = gevent.spawn(self.__resolveDNSAndResponseTime,host,protocol)
               self.threads.append(dnsThread)
               
               self.logManager.logDebug('Web/Ping Response Check')
               respThread = gevent.spawn(self.__getWebResponse,host,port,protocol)
               self.threads.append(respThread)
               
          
          try:     
               gevent.joinall(self.threads)
          except Exception, e:
               self.logManager.logError('GreenletJoinError')
               self.logManager.logError(str(e))
               
          
          self.logManager.logInfo('GreenLetCompletion')
          
          consolidateData = {}
          
          for key in self.portResponseData.viewkeys() | self.hostResponseData.viewkeys() | self.dnsResponseData.viewkeys():
               
                if key in self.portResponseData:
                    consolidateData.setdefault(key,{}).update(self.portResponseData[key])
                    
                if key in self.hostResponseData:
                    consolidateData.setdefault(key,{}).update(self.hostResponseData[key])
                    
                if key in self.dnsResponseData:
                    consolidateData.setdefault(key,{}).update(self.dnsResponseData[key])
           
          
          self.logManager.logDebug('**************')
          self.logManager.logDebug('Port Response Data') 
          self.logManager.logDebug(self.portResponseData)
          self.logManager.logDebug('**************')
          self.logManager.logDebug('**************')
          self.logManager.logDebug('DNS Response Data') 
          self.logManager.logDebug(self.dnsResponseData)
          self.logManager.logDebug('**************')
          self.logManager.logDebug('**************')
          self.logManager.logDebug('Ping Response Data') 
          self.logManager.logDebug(self.hostResponseData)
          self.logManager.logDebug('**************') 
          self.logManager.logDebug(consolidateData)
          self.logManager.logDebug('**************')
          
          self.__renderHTML(consolidateData)
          
          