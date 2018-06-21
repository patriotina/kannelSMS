import datetime
import csv

'''
Input: Begin Date, End Date, Send/Receive, To-Number, From-Number

We need 4 files created:

SMS-Sending-Group-by-To-Number
Fields: Number, Count, Earliest-Date, Latest-Date

SMS-Sending-Group-by-From-Number
Fields: Number, Count, Earliest-Date, Latest-Date

SMS-Receiving-Group-by-To-Number
Fields: Number, Count, Earliest-Date, Latest-Date

SMS-Receiving-Group-by-From-Number
Fields: Number, Count, Earliest-Date, Latest-Date
'''

def openfile(filename, beginDate, endDate, fromNum, toNum):
    f = open(filename, 'r')
    ppp = []
    for line in f:
        part1 = line[0:line.find('[')]
        date1 = part1[:19]
        mydate = datetime.datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
        pp = []
        if mydate >= beginDate and mydate <= endDate:
            pp = [mydate]
            part2 = line[line.find('['):]       #cut part of line after date and status

            part3 = part2.split('[')            #split string by [ as devider
            part3.pop(0)                        # clean first symbol
            stat = part1[19:].strip()           #cut status from datetime part of line
            pp.append(stat)

            for p in part3:                     #go throw line and add to list an items finished by ] symbol
                pp.append(p[:p.find(']')])
            print(pp)
            ppp.append(pp)
    f.close()


    analytic(ppp, 'Sent SMS', 8, fromNum, 'from')
    analytic(ppp, 'Sent SMS', 9, toNum, 'to')
    analytic(ppp, 'Receive SMS', 8, fromNum, 'from')
    analytic(ppp, 'Receive SMS', 9, toNum, 'to')


def analytic(pList, statusSms, typeNum, telNum, direction):
    eDate = pList[0][0]
    lDate = pList[0][0]
    tCount = 0
    for item in pList:
        if item[1] == statusSms:
            if item[typeNum][-10:] == telNum:
                if item[0] < eDate: eDate = item[0]
                if item[0] > lDate: lDate = item[0]
                tCount = tCount + 1
    writefile(statusSms, telNum, tCount, eDate, lDate, direction)


def writefile(statusSms, telNum, tCount, eDate, lDate, direction):
    filename = statusSms + '-' + direction + '-' + str(telNum) + '.csv'
    with open(filename, 'w', newline='') as f:
        fwriter = csv.writer(f)
        fwriter.writerow([telNum, tCount, eDate, lDate])



startDate = datetime.datetime.strptime('2018-06-16 06:39:44', '%Y-%m-%d %H:%M:%S')
finDate = datetime.datetime.strptime('2018-06-18 09:03:42', '%Y-%m-%d %H:%M:%S')
openfile('access.log', startDate, finDate, '7192126175', '5154455218')
# [from:+17192126174] [to:+16419422466]