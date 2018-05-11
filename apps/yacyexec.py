#!/usr/bin/python3
import sys # for arguments
import subprocess # To launch OS process
from time import sleep

print("Hello from Python")
print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
crawl_url = str(sys.argv[1])
print('URL:', crawl_url)

#subprocess.run(["ls", "-l"])  # doesn't capture output
#subprocess.run(["ls", "-l", "/iexec"])  # doesn't capture output

print('Script run as :')
subprocess.run(["whoami"])

print('Run IPFS daemon')
#subprocess.Popen(["/usr/local/bin/ipfs", "daemon"])
print('Run YaCy')
subprocess.Popen(["/bin/sh","/opt/yacy_search_server/startYACY.sh"])
print('Call index')
print('Sleep a bit')
sleep(5)
print('curl ', crawl_url)
subprocess.run(["/usr/bin/curl", crawl_url])
print('curl yacy to start crawling')
subprocess.run(["/usr/bin/curl", "http://localhost:8090"])
print('STOP YaCy')
subprocess.run(["/bin/sh","/opt/yacy_search_server/stopYACY.sh"])
print('Move index to /iexec')
subprocess.run(["cp", "-ra", "/opt/yacy_search_server/DATA", "/iexec"])
print('Put index on IPFS')
