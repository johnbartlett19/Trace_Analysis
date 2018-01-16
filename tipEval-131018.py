import dpkt, sys, socket, dpkt.rtp, os, pylab, csv, time
from matplotlib.backends.backend_pdf import PdfPages
JITBUF = 40  # size of jitter buffer for jitLoss calc

'''
These are the payload types used by Polycom
payloadType, Audio or Video, Codec, clock divisor
'''
payloadTypes = [
        (0,'Audio','PCMU',8000),
        (1,'Audio','Reserved',),
        (2,'Audio','G721',),
        (3,'Audio','GSM',8000),
        (4,'Audio','G723',8000),
        (5,'Audio','DVI4',8000),
        (6,'Audio','DVI4',16000),
        (7,'Audio','LPC',8000),
        (8,'Audio','PCMA',8000),
        (9,'Audio','G722',8000),
        (10,'Audio','L16',44100),
        (11,'Audio','L16',44100),
        (12,'Audio','QCELP',8000),
        (13,'Audio','CN',8000),
        (14,'Audio','MPA',90000),
        (15,'Audio','G728',8000),
        (16,'Audio','DVI4',11025),
        (17,'Audio','DVI4',22050),
        (18,'Audio','G729',8000),
        (19,'N/A','Reserved',),
        (20,'N/A','Unassigned',),
        (21,'N/A','Unassigned',),
        (22,'N/A','Unassigned',),
        (23,'N/A','Unassigned',),
        (24,'N/A','Unassigned',),
        (25,'N/A','CelB',90000),
        (26,'N/A','JPEG',90000),
        (27,'N/A','Unassigned',),
        (28,'N/A','nv',90000),
        (29,'N/A','Unassigned',),
        (30,'N/A','Unassigned',),
        (31,'Video','H261',90000),
        (32,'Video','MPV',90000),
        (33,'Video','MP2T',90000),
        (34,'Video','H263',90000),
        (35,'N/A','Unassigned',),
        (36,'N/A','Unassigned',),
        (37,'N/A','Unassigned',),
        (38,'N/A','Unassigned',),
        (39,'N/A','Unassigned',),
        (40,'N/A','Unassigned',),
        (41,'N/A','Unassigned',),
        (42,'N/A','Unassigned',),
        (43,'N/A','Unassigned',),
        (44,'N/A','Unassigned',),
        (45,'N/A','Unassigned',),
        (46,'N/A','Unassigned',),
        (47,'N/A','Unassigned',),
        (48,'N/A','Unassigned',),
        (49,'N/A','Unassigned',),
        (50,'N/A','Unassigned',),
        (51,'N/A','Unassigned',),
        (52,'N/A','Unassigned',),
        (53,'N/A','Unassigned',),
        (54,'N/A','Unassigned',),
        (55,'N/A','Unassigned',),
        (56,'N/A','Unassigned',),
        (57,'N/A','Unassigned',),
        (58,'N/A','Unassigned',),
        (59,'N/A','Unassigned',),
        (60,'N/A','Unassigned',),
        (61,'N/A','Unassigned',),
        (62,'N/A','Unassigned',),
        (63,'N/A','Unassigned',),
        (64,'N/A','Unassigned',),
        (65,'N/A','Unassigned',),
        (66,'N/A','Unassigned',),
        (67,'N/A','Unassigned',),
        (68,'N/A','Unassigned',),
        (69,'N/A','Unassigned',),
        (70,'N/A','Unassigned',),
        (71,'N/A','Unassigned',),
        (72,'N/A','Reserved',),
        (73,'N/A','Reserved',),
        (74,'N/A','Reserved',),
        (75,'N/A','Reserved',),
        (76,'N/A','Reserved',),
        (77,'N/A','Unassigned',),
        (78,'N/A','Unassigned',),
        (79,'N/A','Unassigned',),
        (80,'N/A','Unassigned',),
        (81,'N/A','Unassigned',),
        (82,'N/A','Unassigned',),
        (83,'N/A','Unassigned',),
        (84,'N/A','Unassigned',),
        (85,'N/A','Unassigned',),
        (86,'N/A','Unassigned',),
        (87,'N/A','Unassigned',),
        (88,'N/A','Unassigned',),
        (89,'N/A','Unassigned',),
        (90,'N/A','Unassigned',),
        (91,'N/A','Unassigned',),
        (92,'N/A','Unassigned',),
        (93,'N/A','Unassigned',),
        (94,'N/A','Unassigned',),
        (95,'N/A','Unassigned',),
        (96,'Audio','AAC-LD',),
        (97,'Audio','Siren_24K',),
        (98,'Audio','Siren_32K',),
        (99,'Audio','Siren_48K',),
        (100,'FECC','FECC',),
        (101,'Audio','G7221_24K',),
        (102,'Audio','G7221_32K',),
        (103,'Audio','G7221_16K',),
        (104,'Audio','Siren22_32K',),
        (105,'Audio','Siren22_48K',),
        (106,'Audio','Siren22_64K',),
        (107,'Video','H26L',),
        (108,'N/A','Unassigned',),
        (109,'Video','H264',),
        (110,'Video','Cisco?',),
        (111,'N/A','Unassigned',),
        (112,'Video','H264',),
        (113,'Audio','G7221C_24K',),
        (114,'Audio','G7221C_32K',),
        (115,'Audio','G7221C_48K',),
        (116,'FECC','LPR',),
        (117,'N/A','Unassigned',),
        (118,'Audio','SirenLPR',),
        (119,'N/A','Unassigned',),
        (120,'N/A','Unassigned',),
        (121,'Audio','SirenStereo_48K',),
        (122,'Audio','SirenStereo_56K',),
        (123,'Audio','SirenStereo_64K',),
        (124,'Audio','SirenStereo_96K',),
        (125,'Audio','Siren22Stereo_64K',),
        (126,'Audio','Siren22Stereo_96K',),
        (127,'Audio','Siren22Stereo_128K',)
        ]
dscpTypes = {
    0: 'BE',
    9:'AF11',
    10:'AF12',
    11:'AF13',
    17:'AF21',
    18:'AF22',
    19:'AF23',
    25:'AF31',
    26:'AF32',
    27:'AF33',
    32:'AF41',
    33:'AF42',
    34:'AF43',
    8:'CS1',
    16:'CS2',
    24:'CS3',
    32:'CS4',
    46:'EF'
    }

''' 1) find valid RTP streams
    2) split into separate files (write pcap files?) with separate RTP streams
         using a naming convention that will define src, dst, ports and RTP type
    3) analyze each stream for loss, jitter (if possible), out of order
    4) report
    '''

def parsePkt(data):
    ether = dpkt.ethernet.Ethernet(data)
    ip = ether.data
    udp = ip.data
    rtp = dpkt.rtp.RTP(udp.data)
    return(ether,ip,udp,rtp)

class Stream():
    def __init__(self, streamTup):
        self.src = streamTup[0]
        self.sport = streamTup[1]
        self.dst = streamTup[2]
        self.dport = streamTup[3]
        self.ssrc = streamTup[4]
        self.pkts = []
        self.len = 0
        self.ptype = None
        self.loss = None
        self.jitLoss = None
        self.jit = None
        self.jitMax = None
        self.ooo = None
        self.bw = None
        self.cksum = None
        self.dscp = None
        self.pps = None
        
    def __str__(self):
        srcPr = socket.inet_ntoa(self.src)
        dstPr = socket.inet_ntoa(self.dst)
        return srcPr + '-' + str(self.sport) + ' -> ' + dstPr + '-' + str(self.dport) \
           + '_' + '{:0=8x}'.format(self.ssrc)
    
    def tsDelta(self):
        (tsl,datal) = self.pkts[-1]
        (tsf,dataf) = self.pkts[0]
        return tsl-tsf
    
    def rtpTsDelta(self):
        (tsl,data) = self.pkts[-1]
        ether, ip, udp, rtp = parsePkt(data)
        rtp_tsl = rtp.ts
        (ts2,data) = self.pkts[0]
        ether, ip, udp, rtp = parsePkt(data)
        rtp_tsf = rtp.ts
        return rtp_tsl - rtp_tsf
         
    def getClockDiv(self):
        clockD = self.rtpTsDelta() / self.tsDelta()
        if clockD == 0:
            clockD == 1
            return clockD
        return int(round(clockD, -3))

    def getClockDivAct(self):
        return self.rtpTsDelta() / self.tsDelta()

    def getTup(self):
        return tuple(self.src, self.sport, self.dst, self.dport, self.ssrc)

    def clockEst(self):
        return (self.lastRtpTs - self.firstRtpTs)/self.len

    def addPkt(self, ts, pkt):
        self.pkts.append((ts,pkt))
        self.len += 1
        if self.ptype == None:
            ether, ip, udp, rtp = parsePkt(pkt)
            self.ptype = rtp.ptype
        if self.dscp == None:
            ether, ip, udp, rtp = parsePkt(pkt)
            ip = ether.data
            self.dscp = ip.tos >> 2

    def getPkts(self):
        return self.pkts

    def findLoss(self):
        if self.loss != None:
            return self.loss
        first = True
        lost = 0
        for pkt in self.pkts:
            ts, data = pkt
            ether, ip, udp, rtp = parsePkt(data)
            seq = rtp.seq
            if first:
                lastSeq = seq - 1
                first = False
            if seq - lastSeq < -65000:
                lastSeq -= 65536
            lost += seq - lastSeq - 1
            lastSeq = seq
        self.loss = float(lost) / len(self.pkts)
        return self.loss
    
    def findLossArray(self, slot):
        # array for timeslots
        timeSlots = []
        # array for results
        lossSlots = []
        # walk through packets
            # += if in the slot
            # if past the slot, go to next slot
        first = True
        lost = 0
        slotNow = 0
        lastLost = 0
        for pkt in self.pkts:
            ts, data = pkt
            if first:
                tsFirst = ts
            tsRel = ts - tsFirst
            if tsRel > (slotNow + 1) * slot:
                timeSlots.append(slotNow)
                lossSlots.append(lost - lastLost)
                lastLost = lost    
                #lost = 0
                slotNow += 1
            ether, ip, udp, rtp = parsePkt(data)
            seq = rtp.seq
            if first:
                lastSeq = seq - 1
                first = False
            if seq - lastSeq < -65000:
                lastSeq -= 65536
            lost += seq - lastSeq - 1
            lastSeq = seq
        self.loss = float(lost) / len(self.pkts)
        return(lossSlots)


    def findJitLoss(self, jitBuffer):
        if self.jitLoss != None:
            return self.jitLoss
        clockDiv = max(float(self.getClockDiv() / 1000),1)
        first = True
        jitLoss = 0
        thisJit = 0
        for pkt in self.pkts:
            ts, data = pkt
            ether, ip, udp, rtp = parsePkt(data)
            if first:
                firstTs = ts
                firstRtpTs = rtp.ts
                first = False
                rtpStart = rtp.ts / clockDiv
                delta = 0.0
                smDelta = 0.0
            else:
                thisDelta = (ts-firstTs)* 1000 - (rtp.ts - firstRtpTs) / clockDiv
                smDelta = smDelta + (thisDelta - smDelta) / 64
                thisJit = thisDelta - smDelta
            if thisJit > jitBuffer:
                jitLoss += 1
        self.jitLoss = float(jitLoss) / len(self.pkts)
        return self.jitLoss

    def findJitLossArray(self, jitBuffer, slot):
        clockDiv = float(self.getClockDiv() / 1000)
        # array for timeslots
        timeSlots = []
        # array for results
        lossSlots = []
        # walk through packets
            # += if in the slot
            # if past the slot, go to next slot
        clockDiv = max(float(self.getClockDiv() / 1000),1)
        first = True
        jitLoss = 0
        thisJit = 0
        slotNow = 0
        lastLost = 0
        for pkt in self.pkts:
            ts, data = pkt
            if first:
                tsFirst = ts
            tsRel = ts - tsFirst
            if tsRel > (slotNow + 1) * slot:
                timeSlots.append(slotNow)
                lossSlots.append(jitLoss - lastLost)
                lastLost = jitLoss    
                slotNow += 1
            ether, ip, udp, rtp = parsePkt(data)
            seq = rtp.seq
            if first:
                firstTs = ts
                firstRtpTs = rtp.ts
                first = False
                rtpStart = rtp.ts / clockDiv
                delta = 0.0
                smDelta = 0.0
            else:
                thisDelta = (ts-firstTs)* 1000 - (rtp.ts - firstRtpTs) / clockDiv
                smDelta = smDelta + (thisDelta - smDelta) / 64
                thisJit = thisDelta - smDelta
            if thisJit > jitBuffer:
                jitLoss += 1
        self.jtloss = float(jitLoss) / len(self.pkts)
        return(lossSlots)

    def findJitter(self):
        clockDiv = float(self.getClockDiv() / 1000)
        first = True
        thisJit = 0
        cumJit = 0
        maxJit = 0
        for pkt in self.pkts:
            ts, data = pkt
            ether, ip, udp, rtp = parsePkt(data)
            if first:
                firstTs = ts
                firstRtpTs = rtp.ts
                first = False
                rtpStart = rtp.ts / clockDiv
                delta = (firstTs)* 1000 - (firstRtpTs) / clockDiv
                smDelta = delta
            else:
                thisDelta = (ts-firstTs)* 1000 - (rtp.ts - firstRtpTs) / clockDiv
                smDelta = smDelta + (thisDelta - smDelta) / 64
                thisJit = thisDelta - smDelta
            if thisJit > 0:
                cumJit += abs(thisJit)
            if thisJit > maxJit:
                maxJit = thisJit
        return (cumJit / len(self.pkts), maxJit)

    def findJitterArray(self, slot):
        clockDiv = float(self.getClockDiv() / 1000)
        # array for timeslots
        timeSlots = []
        # array for results
        jitterSlots = []
        jitterMax = []
        # walk through packets
            # += if in the slot
            # if past the slot, go to next slot
        clockDiv = max(float(self.getClockDiv() / 1000),1)
        first = True
        thisJit = 0
        cumJit = 0
        totCumJit = 0
        maxJit = 0
        totMaxJit = 0
        slotNow = 0
        count = 0
        for pkt in self.pkts:
            ts, data = pkt
            if first:
                tsFirst = ts
            tsRel = ts - tsFirst
            if tsRel > (slotNow + 1) * slot:
                timeSlots.append(slotNow)
                try:
                    jitterSlots.append(float(cumJit) / count)
                except ZeroDivisionError:
                    jitterSlots.append(0)
                jitterMax.append(maxJit)
                cumJit = 0
                maxJit = 0
                count = 0
                slotNow += 1
            ether, ip, udp, rtp = parsePkt(data)
            seq = rtp.seq
            if first:
                firstTs = ts
                firstRtpTs = rtp.ts
                first = False
                rtpStart = rtp.ts / clockDiv
                delta = (firstTs)* 1000 - (firstRtpTs) / clockDiv
                smDelta = delta
            else:
                thisDelta = (ts-firstTs)* 1000 - (rtp.ts - firstRtpTs) / clockDiv
                smDelta = smDelta + (thisDelta - smDelta) / 64
                thisJit = thisDelta - smDelta
            if thisJit > 0:
                cumJit += thisJit
                totCumJit += thisJit
                count += 1
            if thisJit > maxJit:
                maxJit = thisJit
            if thisJit > totMaxJit:
                totMaxJit = thisJit
        self.jit = float(totCumJit) / len(self.pkts)
        self.jitMax = totMaxJit
        return(jitterSlots, jitterMax)

    def findOoo(self):
        if self.ooo != None:
            return self.ooo
        first = True
        ooo = 0
        for pkt in self.pkts:
            ts, data = pkt
            ether, ip, udp, rtp = parsePkt(data)
            seq = rtp.seq
            if first:
                lastSeq = seq - 1
                first = False
            if seq - lastSeq < -65000:
                lastSeq -= 65536
            if seq < lastSeq:
                ooo += 1
            lastSeq = seq
        self.ooo = float(ooo) / len(self.pkts)
        return self.ooo

    def findOooArray(self, slot):
        # array for timeslots
        timeSlots = []
        # array for results
        oooSlots = []
        oooMax = []
        # walk through packets
            # += if in the slot
            # if past the slot, go to next slot
        first = True
        ooo = 0
        slotNow = 0
        lastOoo = 0
        seqMax = 0
        totOOO = 0
        for pkt in self.pkts:
            ts, data = pkt
            if first:
                tsFirst = ts
            tsRel = ts - tsFirst
            if tsRel > (slotNow + 1) * slot:
                timeSlots.append(slotNow)
                oooSlots.append(ooo)
                oooMax.append(seqMax)
                ooo = 0
                seqMax = 0
                slotNow += 1
            ether, ip, udp, rtp = parsePkt(data)
            seq = rtp.seq
            if first:
                lastSeq = seq - 1
                first = False
            if seq - lastSeq < -65000:
                lastSeq -= 65536
            if seq < lastSeq:   
                ooo += 1
                totOOO += 1
                seqSize = lastSeq - seq
                if seqMax < seqSize:
                    seqMax = seqSize
            lastSeq = seq
        self.ooo = float(totOOO) / len(self.pkts)
        return(oooSlots, oooMax)

    def findPPS(self):
        if self.pps != None:
            return self.pps
        self.pps = float(len(self.pkts))/self.tsDelta()
        return self.pps

    def findPPSArray(self, slot):
        # array for timeslots
        timeSlots = []
        # array for results
        ppsSlots = []
        # walk through packets
            # += if in the slot
            # if past the slot, go to next slot
        first = True
        pkts = 0
        totPkts = 0
        slotNow = 0
        for pkt in self.pkts:
            ts, data = pkt
            if first:
                tsFirst = ts
                first = False
            tsRel = ts - tsFirst
            if tsRel > (slotNow + 1) * slot:
                timeSlots.append(slotNow)
                ppsSlots.append(pkts)
                pkts = 0
                slotNow += 1
            pkts += 1
            totPkts += 1
        self.pps = float(totPkts) / self.tsDelta()
        return(ppsSlots)
    
    def findBW(self):
        if self.bw != None:
            return self.bw
        bytes = 0
        for pkt in self.pkts:
            ts, data = pkt
            ether = dpkt.ethernet.Ethernet(data)
            ip = ether.data
            bytes += ip.len + 18 #ip len plus ethernet header & trailer
        self.bw = float(bytes) * 8 / self.tsDelta()
        return self.bw

    def findBWArray(self, slot):
        # array for timeslots
        timeSlots = []
        # array for results
        bwSlots = []
        # walk through packets
            # += if in the slot
            # if past the slot, go to next slot
        first = True
        bytes = 0
        totBytes = 0
        slotNow = 0
        for pkt in self.pkts:
            ts, data = pkt
            ether = dpkt.ethernet.Ethernet(data)
            ip = ether.data
            if first:
                tsFirst = ts
                first = False
            tsRel = ts - tsFirst
            if tsRel > (slotNow + 1) * slot:
                timeSlots.append(slotNow)
                bwSlots.append(bytes * 8 / slot)
                bytes = 0
                slotNow += 1
            bytes += ip.len + 18 #ip len plus ethernet header & trailer
            totBytes += ip.len + 18 #ip len plus ethernet header & trailer
        self.bw = float(totBytes * 8) / self.tsDelta()
        return(bwSlots)

    def checkUDPsums(self):
        if self.cksum != None:
            return self.cksum
        def checkUDPsum(packet):
            def caa(a, b):
                c = a + b
                return (c & 0xffff) + (c >> 16)

            def checksum(msg, start):
                s = start
                for i in range(0, len(msg), 2):
                    try:
                        w = (ord(msg[i]) << 8) + ord(msg[i+1])
                    except:
                        w = (ord(msg[i]) << 8)
                    s = caa(s, w)
                return s

            ts, data = packet
            ether, ip, udp, rtp = parsePkt(data)
            chsum = udp.ulen
            chsum = caa(chsum, ip.p)
            chsum = checksum(ip.src, chsum)
            chsum = checksum(ip.dst, chsum)
            chsum = caa(udp.sport, chsum)
            chsum = caa(udp.dport, chsum)
            chsum = caa(udp.ulen, chsum)
            chsum = caa(udp.sum, chsum)
            chsum = checksum(udp.data, chsum)
            return chsum == 0xffff
        cksum = True
        for pkt in self.pkts:
            if not checkUDPsum(pkt):
                cksum = False
        self.cksum = cksum
        return cksum

def printTup(stream):
    ''' Tup is a tuple (src, srcPort, dst, dstPort, rtpType)
        where src and dst are binary values, srcPort and dstPort are integers
        and rtpType is an integer
        Convert src and dst to printable IP addresses
        Convert rtpType to a Polycom or standard protocol if it maps,
          identify if it is audio or video
    '''
    srcAddr = socket.inet_ntoa(stream[0])
    srcPrt = str(stream[1])
    dstAddr = socket.inet_ntoa(stream[2])
    dstPrt = str(stream[3])
    ssrc = '{:0=8x}'.format(stream[4])
    return srcAddr + '-' + srcPrt + '_to_' + dstAddr + '-' + dstPrt + '_' + ssrc
    
def splitPcapRTP(pcapFile, types):
    ''' splits a pcap file into n separate files
        asks the user yes/no for each stream, based on src, dst, port and type
        Uses a tuple to identify a stream (src, srcPort, dst, dstPort, type)
    '''
    # initialize lists

    # read thru the file
    streams = {}
    pktNum = 0
    IP_RF		= 0x8000	# reserved
    IP_DF		= 0x4000	# don't fragment
    IP_MF		= 0x2000	# more fragments (not last frag)
    IP_OFFMASK	= 0x1fff	# mask for fragment offset
    
    print '%1s %12s %s' % (' ', 'FirstPktNum', 'Stream Name')
    for ts, data in pcapFile:
        pktNum += 1
        ether = dpkt.ethernet.Ethernet(data)
        if ether.type != dpkt.ethernet.ETH_TYPE_IP: continue
        ip = ether.data
        if ip.p != dpkt.ip.IP_PROTO_UDP: continue
        if (ip.off & (IP_MF|IP_OFFMASK)) != 0: continue
        udp = ip.data
        if len(udp) <= 20: continue
        try:
            rtp = dpkt.rtp.RTP(udp.data)
        except:
            print 'Packet number ', pktNum
            print 'Packet length ', len(udp), len(ip), len(ether), len(data)
            raise
        if rtp._get_version() != 2: continue
        if types[rtp._get_pt()][2] == 'Unassigned': continue
        if types[rtp._get_pt()][2] == 'Reserved': continue
        if types[rtp._get_pt()][1] == 'N/A': continue
        asdf = rtp.ssrc
        thisTup = (ip.src, udp.sport, ip.dst, udp.dport, rtp.ssrc)
        try:
            stream = streams[thisTup]
        except:
            streams[thisTup] = Stream(thisTup)
            stream = streams[thisTup]
            stream.ptype = rtp._get_pt()
            print '%6s %7d %s' % ('found:', pktNum, stream)
        stream.addPkt(ts, data)
    return streams
        
def getFileList(type, recurse = True, query = True, allRet = True):
    ''' Uses os.walk to get all files with suffix equal to 'type',
        queries the user about which files to include if querey = True
        returns first file user gives a 'y' if allRet = False, otherwise
        returns all or all with a 'y' in a list
    '''
    def isType(filList, type):
        newList = []
        for handle in filList :
            if (handle[(-len(type)):] == type):
                newList.append(handle)
        return newList
    allFiles = [os.path.join(path,file) for (path, dirs, files) in os.walk('.') for file in files]
    useFiles = []
    if query:
        for filename in isType(allFiles, type):
            ans = raw_input('\nUse file ' + str(filename) + '? ')
            if(ans == 'y' or ans == 'Y'):
                useFiles.append(filename)
                if not allRet:  break
    print '\n'
    return useFiles

def findSlot(stream):
    # calculate the duration & timeslot
    intArray = [(500,1),(1500,5),(4500,15),(9000,30),(0,60)]
    traceDur = stream.tsDelta()
#    print 'Trace Length', traceDur, stream
    for (high, slot) in intArray:
        if high == 0:
            timeslot = slot
        elif traceDur > high: continue
        else:
            timeSlot = slot
            break
    return slot
   
def setUpPlots():
    plotTypes = []
    foundBug = False
    foundDone = False
    inputOK = ['bw', 'loss', 'pps', 'jitter', 'jitterloss', 'outoforder', 'all', 'done']
    plot = raw_input('What plot types do you want? (bw, loss, pps, jitter, jitterloss, outoforder, all, done)? ').replace(' ', '').lower().split(',')
    if plot == ['']:
        return plotTypes
    while True:
        for inpt in plot:
            if inpt not in inputOK:
                print 'Don\'t understand: ' + inpt
                foundBug = True
            elif inpt in plotTypes:
                pass
            elif inpt == 'all':
                plotTypes = ['bw', 'loss', 'pps', 'jitter', 'jitterloss', 'outoforder']
                foundDone = True
            elif inpt != 'done':
                plotTypes.append(inpt)
            else:
                foundDone = True
        if foundDone and not foundBug: break
        foundBug = False
        plot = raw_input('So far: '+ str(plotTypes)+ '(done to move on):').replace(' ', '').lower().split(',')
    print '\n'
    return plotTypes

def getListIPAddr():
    ipIncludeList = []
    while True:
        ipAddIn = raw_input('IP Address to Include: ')
        if ipAddIn == '':
            break
        else:
            ipIncludeList.append(ipAddIn)
            print ipIncludeList
    return ipIncludeList

def splitToStreams():
    ''' get list of files named 'pcap', query user on which ones to use
         parse for rtp streams and return in dictionary where key
         is tuple srcAddr, srcPort, dstAddr, dstPort, rtpType
    '''
    useFiles = getFileList('.pcap', True, True)
    ## Split original file into separate RTP file streams
    print 'Splitting original file into UDP/RTP stream files'
    streams = {}
    for file_name in useFiles:
        try:
            pcapReader = dpkt.pcap.Reader(open(file_name, "rb"))
            streams.update(splitPcapRTP(pcapReader, payloadTypes))
        except ValueError, e:
            print e
            print 'File may be in pcapng format which this program does not yet support'
            print 'Please convert to pcap format using editcap -F libpcap infile outfile'
            raw_input('holding so you can read ... ')
            raise
    return streams

def displayStreams(streams):
    ''' print out display of streams '''
    print '\n\nDisplay streams and packet counts'
    print '%8s  %13s  %s' % ('Packets', 'Stream Type', 'Stream Name')
    for key in streams:
        print '%7d  %16s  %s' % (streams[key].len, payloadTypes[streams[key].ptype][2], printTup(key))
        #print printTup(key)
    print '\n'
    
def filterStreams(streams):
    delSet = []
    # query delete threshold here ...
    goodInput = False
    threshold = None
    delSet = []
    while goodInput == False:
        ans = raw_input('Stream byte threshold (value)? ')
        if ans == '': ans = 0
        try:
            threshold = int(ans)
            goodInput = True
        except:
            print 'Please provide an integer value or no value'
    if threshold != None:
        for key in streams:
            if streams[key].len < threshold:
                delSet.append(key)
        for key in delSet:
            del streams[key]

    # filter streams based on IP addresses here
    
    displayStreams(streams)
    ans = 'y'
    while ans == 'y':
        ans = raw_input('Filter streams based on IP addresses involved? (y|n) ')
        if ans == 'y':
            ipAddrs = getListIPAddr()
            delSet = []
            for key in streams:
                src = socket.inet_ntoa(key[0])
                dst = socket.inet_ntoa(key[2])
                if src not in ipAddrs and dst not in ipAddrs:
                    delSet.append(key)
            for key in delSet:
                del streams[key]
        displayStreams(streams)
            
    #query delete individual streams here ...
    ans = 'y'
    while ans == 'y':
        ans = raw_input('Review streams individually to delete or save? (y|n) ')
        if ans == 'y':
            delSet = []
            for key in streams:
                prStr = '%5d  %16s  %s' % (streams[key].len, payloadTypes[streams[key].ptype][2], streams[key])
                ans = raw_input('Keep ' + prStr + '? ')
                if ans == 'y' or ans == 'Y':
                    pass
                else:
                    delSet.append(key)

            for key in delSet:
                del streams[key]
        displayStreams(streams)
    print '\n'
    return streams

def genPlots(streams, plotTypes):
    fig = 0
    for tuple in streams:
        slot = findSlot(streams[tuple])
        fileName = printTup(tuple) + '-Plots.pdf'
        print 'Generating plots for', fileName
        pdf = PdfPages(fileName)

        for plot in plotTypes:
            fig += 1
            pylab.figure(fig)
            pylab.xlabel('Time(sec)')
            if plot == 'loss':
                pylab.ylabel('packets')
                loss = streams[tuple].findLossArray(slot)
                xaxis = [i*slot for i in range(len(loss))]
                pylab.plot(xaxis, loss, 'b', label='Packet Loss (pkts)')
                pylab.legend(loc='best')
                pylab.title('Packet Loss in ' + str(streams[tuple]))
            elif plot == 'pps':
                pylab.ylabel('pps')
                pps = streams[tuple].findPPSArray(slot)
                xaxis = [i*slot for i in range(len(bw))]
                pylab.plot(xaxis, pps, 'b', label='Packets/sec(pps)')
                pylab.legend(loc='best')
                pylab.title('PPS in ' + str(streams[tuple]))
            elif plot == 'bw':
                pylab.ylabel('bps')
                bw = streams[tuple].findBWArray(slot)
                xaxis = [i*slot for i in range(len(bw))]
                pylab.plot(xaxis, bw, 'b', label='Bandwidth (bps)')
                pylab.legend(loc='best')
                pylab.title('Bandwidth in ' + str(streams[tuple]))
            elif plot == 'jitter':
                pylab.ylabel('ms')
                jta, jtm = streams[tuple].findJitterArray(slot)
                xaxis = [i*slot for i in range(len(jta))]
                pylab.plot(xaxis, jta, 'b', label='Jitter (ms)')
                pylab.plot(xaxis, jtm, 'g', label='Jitter Max (ms)')
                pylab.legend(loc='best')
                pylab.title('Jitter in ' + str(streams[tuple]))
            elif plot == 'jitterloss':
                pylab.ylabel('packets')
                jl = streams[tuple].findJitLossArray(JITBUF,slot)
                xaxis = [i*slot for i in range(len(jl))]
                pylab.plot(xaxis, jl, 'b', label='Jitter Loss (pkts)')
                pylab.legend(loc='best')
                pylab.title('Jitter Loss in ' + str(streams[tuple]))
            elif plot == 'outoforder':
                pylab.ylabel('packets')
                ooo, xxx = streams[tuple].findOooArray(slot)
                xaxis = [i*slot for i in range(len(ooo))]
                pylab.plot(xaxis, ooo, 'b', label='OOO Packets (pkts)')
                pylab.plot(xaxis, xxx, 'r', label='Positions OOO (pkts)')
                pylab.legend(loc='best')
                pylab.title('OutOfOrder Pkts in ' + str(streams[tuple]))
            else:
                raise ValueError('Found plot type not on my list')
            #pylab.show(fig)
            pdf.savefig(fig)
        pdf.close()

def streamsToFile(streams):
    save = raw_input("Save the streams into separate pcap files? ")
    if save == 'y' or save == 'Y':
        for key in streams:
            fileName = printTup(key) + '.pcap'
            stream = streams[key]
            stream.fileName = fileName
            stream.handle = dpkt.pcap.Writer(open(fileName, "wb"))
            for pkt in stream.getPkts():
                (ts, data) = pkt
                stream.handle.writepkt(data, ts)
            stream.handle.close()

def checkUDP(streams):
    check = raw_input("Check all streams for UDP checksum errors? ")
    ckOK = '{0:>58s} {1:6s}'
    if check == 'y' or check == 'Y':
        print ckOK.format('Stream Name','Cksum')
        for key in streams:
            ckStat = streams[key].checkUDPsums()
            if ckStat == True:
                prStat = 'OK'
            if ckStat == False:
                prStat = 'Bad'
            print ckOK.format(printTup(key), prStat)
    else:
        for key in streams:
            streams[key].cksum = 'Off'
            
def timeStr(timestamp):
    fmtTime = '{0.tm_year}-{0.tm_mon:02d}-{0.tm_mday:02d}_{0.tm_hour:02d}:{0.tm_min:02d}:{0.tm_sec:02.0f}_{1:03.0f}'
    aa = time.gmtime(timestamp)
    bb = (timestamp - int(timestamp))*1000
    strTime = fmtTime.format(aa,bb)
    return strTime

def overview(streams):
    fmtData = '{0[0]:>55s} {0[1]:3d} {0[2]:18s} {0[3]:6d} {0[4]:7.0f}K {0[5]:7.0f} {0[6]:0=6.2%} {0[7]:0=6.2%} {0[8]:0=6.2%} {0[9]:5s} {0[10]:5.0f} {0[11]:5.1f} {0[12]:14s} {0[13]:4d}'
    fmtHdr = '{0[0]:^55s} {0[1]:3s} {0[2]:^18s} {0[3]:>6s} {0[4]:>7s} {0[5]:>7s} {0[6]:^6s} {0[7]:^6s} {0[8]:^6s} {0[9]:5s} {0[10]:5s} {0[11]:^5s} {0[12]:^23s} {0[13]:11s}'
    hdrRow = ['ipSrc-udpSrcPort-ipDst-udpDstPort-SSRC', 'Typ', 'Codec', 'Pkts', 'BW ', 'PPS', 'Loss', 'JtLs', 'OOO', 'Cksum', 'ClkDiv', 'Len', 'Start', 'DSCP']
    print
    print 'Overview of all streams in this run:'
    print fmtHdr.format(hdrRow)
    def getStats(stream):
        name = printTup(key)
        typ = stream.ptype
        typName = payloadTypes[stream.ptype][2]
        bw = stream.findBW() / 1000
        pps = stream.findPPS()
        loss = stream.findLoss()
        jitLoss = stream.findJitLoss(JITBUF)
        ooo = stream.findOoo()/100
        tstChksum = stream.checkUDPsums()
        if tstChksum == True:
            cksum = 'OK'
        elif tstChksum == False:
            cksum = 'Bad'
        elif tstChksum == 'Off':
            cksum = 'Off'
        else:
            raise ValueError('Unexpected result from checkUDPsums()')
        clkDiv = stream.getClockDivAct()
        streamLen = stream.tsDelta()
        dscp = stream.dscp
        start, data = stream.pkts[0]
        timeStart = timeStr(start)
        return [name, typ, typName, stream.len, bw, pps, loss, jitLoss, ooo, cksum, clkDiv, streamLen, timeStart, dscp]
        
    for key in streams:         #print to the screen
        print fmtData.format(getStats(streams[key]))
    # Print to file?
    outFileName = raw_input('Save summary data to file?(filename?): ')
    if outFileName == 'Y' or outFileName == 'y':
        outFileName = raw_input('Will create CSV format file. Filename? ')
    if outFileName != '' and outFileName != 'N' and outFileName != 'n':
        if outFileName[-4:] != '.csv':
            outFileName = outFileName + '.csv'
        summary = open(outFileName, 'wb')
        sumWriter = csv.writer(summary, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        sumWriter.writerow(hdrRow)
        for key in streams:
            sumWriter.writerow(getStats(streams[key]))
        summary.close()
        print 'Summary saved to ', outFileName, '\n'
    else:
        print 'No summary file created \n'
        
            
##******************************************************************************
## Main routine

def main():
    streams = splitToStreams()
    displayStreams(streams)
    streams = filterStreams(streams)
    plotTypes = setUpPlots()
    if len(plotTypes) > 0:
        genPlots(streams, plotTypes)
    streamsToFile(streams)
    checkUDP(streams)
    overview(streams)
    return streams
# DONE - Build an overview output
# DONE - Include UDP checksum error check
# Include reading of RTCP packets to see how receiver loss compares to loss
#  at this location in the network, very cool
# DONE - add filter for source and/or destination IP address
# DONE - set up plot X-axis in seconds not slots
# DONE - print SSRC in Hex
# DONE - for overview add trace length, start time, DSCP mark
# DONE - remove dependency on custom rtp.py module
# DONE - run full suite loss, jit, etc. during plot generation and save in stream
# DONE - change printout during plot generation to make more sense
# Len calculation assumes we have full packet, affects BW charts, can this be
#  changed to use Len field in UDP header instead?

aa = main()
