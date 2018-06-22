import random
import requests
import datetime
import re

# url to sms gate: http://198.245.50.106:13006/cgi-bin/sendsms?username=tester&password=t3st3r&from=%2B14422209344&to=%2B14844249683&text=test&smsc=Tyntec
# log: 2018-06-19 00:43:31 Receive SMS [SMSC:Tyntec] [SVC:] [ACT:ipc] [BINF:] [FID:] [META:?smpp?] [from:+17192126172] [to:+16573423795] [flags:-1:0:-1:0:-1] [msg:132:WeChat verification code (7745) may only be used once to verify mobile number. For account safety, don't forward the code to others.] [udh:0:]

def smstest(fromnumberlist, tonumberlist):
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
                #print(gennum + ' - ' + bignum)
                sendsms(fromnumber, bignum)
        else:
            sendsms(fromnumber, tonumber)

def sendsms(fromn, ton):

    url = "http://198.245.50.106:13006/cgi-bin/sendsms?username=tester&password=t3st3r&from=%2B1{fromnum}&to=%2B1{tonum}&text=test&smsc=Tyntec".format(fromnum=fromn, tonum = ton)
    print(url)
    response = requests.get(url)
    print(response)
    print(response.content)



def openlog(filename, dt, frn, ton):
    f = open(filename)
    ppp = []
    for line in f:

        #print(line)
        part1 = line[0:line.find('[')]
        date1 = part1[:19]
        stat = part1[19:].strip()
        print(stat)
        mydate = datetime.datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')

        if mydate == dt:

            print(part1)
            part2 = line[line.find('['):]
            print(part2)

            part3 = part2.split('[')
            part3.pop(0)
            pp = [stat]
            print(part3)
            for p in part3:
                pp.append(p[:p.find(']')])
            print(pp)
            ppp.append(pp)

    f.close()
    testlog(ppp, frn, ton)

def testlog(logs, frn, ton):

    #print(logstr[7])
    #print(logstr[7][-10:] + ' - ' + frn)

    #print(logstr[8])
    #print(logstr[8][-10:] + ' - ' + ton)

    r = False
    s = False
    out = []
    vsp = ''
    for logstr in logs:
        if frn == logstr[7][-10:]:
            print(logstr[0])
            if logstr[0] == 'Receive SMS':
                r = True
                out.append(logstr)
                vsp = frn
                frn = ton
                ton = vsp
            if logstr[0] == 'Sent SMS' and r:
                s = True
                out.append(logstr)

    print(out)

def smstest2(fromnumberlist, tonumberbase):
    if len(fromnumberlist) > 0:
        fromnumber = random.choice(fromnumberlist)
    else:
        print("list of from_number is incorrect")


    nwidth = 10 - len(str(tonumberbase))

    for i in range(10**nwidth):
        gennum = str(i).zfill(nwidth)
        bignum = str(tonumberbase)+gennum
        print(gennum + ' - ' + bignum)


#smstest([4422209344], [4844249683])
#smstest2([4422209344], 48442496)
openlog('access.log', datetime.datetime.strptime('2018-04-05 16:08:48', '%Y-%m-%d %H:%M:%S'), '6824102022', '4242150000')