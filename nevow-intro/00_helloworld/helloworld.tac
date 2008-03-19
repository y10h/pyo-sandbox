from nevow import appserver
from twisted.application import service, strports
import helloworld

site = appserver.NevowSite(helloworld.HelloWorld())
application = service.Application('NevowHelloWorld')
httpd = strports.service("tcp:8000", site)
httpd.setServiceParent(application)
