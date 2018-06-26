import random
import requests
import datetime
import time
import options
import uuid
import csv

# url to sms gate: http://198.245.50.106:13006/cgi-bin/sendsms?username=tester&password=t3st3r&from=%2B14422209344&to=%2B14844249683&text=test&smsc=Tyntec
# log: 2018-06-19 00:43:31 Receive SMS [SMSC:Tyntec] [SVC:] [ACT:ipc] [BINF:] [FID:] [META:?smpp?] [from:+17192126172] [to:+16573423795] [flags:-1:0:-1:0:-1] [msg:132:WeChat verification code (7745) may only be used once to verify mobile number. For account safety, don't forward the code to others.] [udh:0:]

# dealy to get pause between sending process and reading logfile. Process of sending can take some time on Kannel, so give few seconds to it.
delaysec = 10

#function of checking input lists. Check length of number, choose random number for FROM field and check length number and generate numbers for TO field
def smstest(fromnumberlist, tonumberlist):
    starttime = datetime.datetime.now()
    if len(fromnumberlist) > 0:
        fromnumber = random.choice(fromnumberlist)
    else:
        print("list of from_number is incorrect")
    for tonumber in tonumberlist:
        if len(tonumber) < 10:
            nwidth = 10 - len(str(tonumber))
            for i in range(10**nwidth):
                gennum = str(i).zfill(nwidth)
                bignum = str(tonumber)+gennum
                sendsms(fromnumber, bignum)
                openlog(options.filename, starttime, fromnumber, bignum)
        else:
            sendsms(fromnumber, tonumber)
            openlog(options.filename, starttime, fromnumber, tonumber)

#function to request sending URL to send SMS
def sendsms(fromn, ton):
    url = "http://198.245.50.106:13006/cgi-bin/sendsms?username=tester&password=t3st3r&from=%2B1{fromnum}&to=%2B1{tonum}&text=test&smsc=Tyntec".format(fromnum=fromn, tonum = ton)
    print(url)
    response = requests.get(url)
    #print(response)
    #print(response.content)

#function to open log file, parse it and check does it has a data about sended or received SMS in needed time duration
def openlog(filename, dt, frn, ton):
    time.sleep(delaysec)
    f = open(filename)
    ppp = []
    for line in f:
        #devide log-line to 2 parts. part1 - data time and status, all info going to first [ symbol
        part1 = line[0:line.find('[')]
        #get data and time from part1
        date1 = part1[:19]
        #get status (after time to end of string and clear from spaces at begin and end of string
        stat = part1[19:].strip()
        #convert date-time from string to datetime format
        mydate = datetime.datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
        dtdelta = dt + datetime.timedelta(seconds=delaysec)
        if mydate >= dt and mydate <= dtdelta:
            #get part2 string from log-line, all going after first [ symbol
            part2 = line[line.find('['):]
            #convert part2 to list using biricks as separator
            part3 = part2.split('[')
            part3.pop(0)    #clear first list item, its just a space
            pp = [date1]
            pp.append(stat)     #write a new list, starts with status
            for p in part3:
                pp.append(p[:p.find(']')])
            ppp.append(pp)
    f.close()
    testlog(ppp, frn, ton)

#function to check list of lines catched from log file. and generate case-files.
def testlog(logs, frn, ton):
    r = False
    s = False
    out = []
    for logstr in logs:
        if (frn == logstr[8][-10:]) and (ton == logstr[9][-10:]):
            if logstr[1] == 'Receive SMS':
                r = True
                out.append(logstr)
            if logstr[1] == 'Sent SMS' and r :
                s = True
                out.append(logstr)
    print(out)
    if r and s:
        filename = str(uuid.uuid4()) + '_case1.csv'
    elif r and not s:
        filename = str(uuid.uuid4()) + '_case2.csv'
    elif not r:
        filename = str(uuid.uuid4()) + '_case3.csv'
    else:
        exit()
    with open(filename, 'wb') as f:
        fwriter = csv.writer(f)
        for item in out:
            fwriter.writerow(item)

#smstest([4422209344], [4844249683])
#smstest2([4422209344], 48442496)
#2018-06-17 15:33:52 Receive SMS [SMSC:Tyntec] [SVC:] [ACT:ipc] [BINF:] [FID:] [META:?smpp?] [from:+16144177400] [to:+16416522019] [flags:-1:0:-1:0:-1] [msg:132:WeChat verification code (1073) may only be used once to verify mobile number. For account safety, don't forward the code to others.] [udh:0:]

#openlog('access.log', datetime.datetime.strptime('2018-06-17 15:33:52', '%Y-%m-%d %H:%M:%S'), '6144177400', '6416522019')
#openlog(options.filename, datetime.datetime.strptime(options.startDate, '%Y-%m-%d %H:%M:%S'), options.fromNumber, options.toNumber)

smstest(options.fromNumberList, options.toNumberList)