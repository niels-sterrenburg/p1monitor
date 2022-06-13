#!/usr/bin/python

import sys
import serial
import os
import getopt
clear = lambda: os.system('clear')

##############################################################################
# Sentimentally define printf :'( because we can :D
##############################################################################
def printf(format, *args):
    sys.stdout.write(format % args)

##############################################################################
# Class for P1 data elements
##############################################################################
class P1:
    floval = 0.0
    intval = -1
    strval = ""
    todb   = 0
    dbname = ""
    iden   = ""
    form   = ""
    unit   = ""
    desc   = ""

    def __init__(self, floval, intval, strval, todb, dbname, iden, form, unit, desc):
        self.floval = floval
        self.intval = intval
        self.strval = strval
        self.todb   = todb
        self.dbname = dbname
        self.iden   = iden  
        self.form   = form  
        self.unit   = unit  
        self.desc   = desc  

##############################################################################
# Array for P1 class objects
##############################################################################
P1D = []

####################################################################################################
standard_version = "v5.02"
standard_source  = "https://www.netbeheernederland.nl/_upload/Files/Slimme_meter_15_a727fce1f1.pdf"
####################################################################################################
#              <--value-->  DB DBname           OBI            Format      Unit   Description
P1D.append(P1( 0.0, -1, '', 1, "version             ",  '1-3:0.2.8',   'str',      '',    'Version information for P1 output'))
P1D.append(P1( 0.0, -1, '', 1, "timestamp           ",  '0-0:1.0.0',   'datetime', '',    'Date-time stamp of the P1 message (YYMMDDhhmmss)'))
P1D.append(P1( 0.0, -1, '', 0, "                    ",  '0-0:96.1.1',  'str',      '',    'Equipment identifier'))
P1D.append(P1( 0.0, -1, '', 1, "totalusagenight     ",  '1-0:1.8.1',   'flo',      'kWh', 'Meter Reading electricity delivered to client (Tariff 1) in 0,001 kWh'))
P1D.append(P1( 0.0, -1, '', 1, "totalusageday       ",  '1-0:1.8.2',   'flo',      'kWh', 'Meter Reading electricity delivered to client (Tariff 2) in 0,001 kWh'))
P1D.append(P1( 0.0, -1, '', 1, "totaldeliverynight  ",  '1-0:2.8.1',   'flo',      'kWh', 'Meter Reading electricity delivered by client (Tariff 1) in 0,001 kWh'))
P1D.append(P1( 0.0, -1, '', 1, "totaldeliveryday    ",  '1-0:2.8.2',   'flo',      'kWh', 'Meter Reading electricity delivered by client (Tariff 2) in 0,001 kWh'))
P1D.append(P1( 0.0, -1, '', 1, "tarif               ",  '0-0:96.14.0', 'int',      '',    'Tariff indicator electricity (Tariff 1: low Tariff 2: normal).'))
P1D.append(P1( 0.0, -1, '', 1, "actualusage         ",  '1-0:1.7.0',   'flo',      'kW',  'Actual electricity power delivered (+P) in 1 Watt resolution'))
P1D.append(P1( 0.0, -1, '', 1, "actialdelivery      ",  '1-0:2.7.0',   'flo',      'kW',  'Actual electricity power received (-P) in 1 Watt resolution'))
P1D.append(P1( 0.0, -1, '', 1, "failures            ",  '0-0:96.7.21', 'int',      '',    'Number of power failures in any phase'))
P1D.append(P1( 0.0, -1, '', 1, "longfailures        ",  '0-0:96.7.9',  'int',      '',    'Number of long power failures in any phase'))
P1D.append(P1( 0.0, -1, '', 0, "                    ",  '1-0:99.97.0', 'str',      '',    'Power Failure Event Log (long power failures)'))
P1D.append(P1( 0.0, -1, '', 1, "voltagesagsL1       ",  '1-0:32.32.0', 'int',      '',    'Number of voltage sags in phase L1'))
P1D.append(P1( 0.0, -1, '', 1, "voltagesagsL2       ",  '1-0:52.32.0', 'int',      '',    'Number of voltage sags in phase L2'))
P1D.append(P1( 0.0, -1, '', 1, "voltagesagsL3       ",  '1-0:72.32.0', 'int',      '',    'Number of voltage sags in phase L3'))
P1D.append(P1( 0.0, -1, '', 1, "voltageswellsL1     ",  '1-0:32.36.0', 'int',      '',    'Number of voltage swells in phase L1'))
P1D.append(P1( 0.0, -1, '', 1, "voltageswellsL2     ",  '1-0:52.36.0', 'int',      '',    'Number of voltage swells in phase L2'))
P1D.append(P1( 0.0, -1, '', 1, "voltageswellsL3     ",  '1-0:72.36.0', 'int',      '',    'Number of voltage swells in phase L3'))
P1D.append(P1( 0.0, -1, '', 0, "                    ",  '0-0:96.13.0', 'str',      '',    'Text message max 1024 characters.'))
P1D.append(P1( 0.0, -1, '', 1, "voltL1              ",  '1-0:32.7.0',  'flo',      'V',   'Instantaneous voltage L1 in V resolution'))
P1D.append(P1( 0.0, -1, '', 1, "voltL2              ",  '1-0:52.7.0',  'flo',      'V',   'Instantaneous voltage L2 in V resolution'))
P1D.append(P1( 0.0, -1, '', 1, "voltL3              ",  '1-0:72.7.0',  'flo',      'V',   'Instantaneous voltage L3 in V resolution'))
P1D.append(P1( 0.0, -1, '', 1, "ampsL1              ",  '1-0:31.7.0',  'flo',      'A',   'Instantaneous current L1 in A resolution'))
P1D.append(P1( 0.0, -1, '', 1, "ampsL2              ",  '1-0:51.7.0',  'flo',      'A',   'Instantaneous current L2 in A resolution'))
P1D.append(P1( 0.0, -1, '', 1, "ampsL3              ",  '1-0:71.7.0',  'flo',      'A',   'Instantaneous current L3 in A resolution'))
P1D.append(P1( 0.0, -1, '', 1, "usageL1             ",  '1-0:21.7.0',  'flo',      'kW',  'Instantaneous active power L1 (+P) in W resolution'))
P1D.append(P1( 0.0, -1, '', 1, "usageL2             ",  '1-0:41.7.0',  'flo',      'kW',  'Instantaneous active power L2 (+P) in W resolution'))
P1D.append(P1( 0.0, -1, '', 1, "usageL3             ",  '1-0:61.7.0',  'flo',      'kW',  'Instantaneous active power L3 (+P) in W resolution'))
P1D.append(P1( 0.0, -1, '', 1, "deliveryL1          ",  '1-0:22.7.0',  'flo',      'kW',  'Instantaneous active power L1 (-P) in W resolution'))
P1D.append(P1( 0.0, -1, '', 1, "deliveryL2          ",  '1-0:42.7.0',  'flo',      'kW',  'Instantaneous active power L2 (-P) in W resolution'))
P1D.append(P1( 0.0, -1, '', 1, "deliveryL3          ",  '1-0:62.7.0',  'flo',      'kW',  'Instantaneous active power L3 (-P) in W resolution'))
# TODO add gas & water

##############################################################################
# Example P1 read
##############################################################################

#   b'\x00\n'
#   b'/CTA5ZIV-METER\r\n'
#   b'\r\n'
#   b'1-3:0.2.8(50)\r\n'
#   b'0-0:1.0.0(220601203913S)\r\n'
#   b'0-0:96.1.1(4530303737303030373235393939303231)\r\n'
#   b'1-0:1.8.1(000337.022*kWh)\r\n'
#   b'1-0:1.8.2(000036.206*kWh)\r\n'
#   b'1-0:2.8.1(000000.002*kWh)\r\n'
#   b'1-0:2.8.2(000000.000*kWh)\r\n'
#   b'0-0:96.14.0(0002)\r\n'
#   b'1-0:1.7.0(00.351*kW)\r\n'
#   b'1-0:2.7.0(00.000*kW)\r\n'
#   b'0-0:96.7.21(00023)\r\n'
#   b'0-0:96.7.9(00011)\r\n'
#   b'1-0:99.97.0(2)(0-0:96.7.19)(211117215315W)(0000000000*s)(211123131043W)(0000000000*s)\r\n'
#   b'1-0:32.32.0(00000)\r\n'
#   b'1-0:52.32.0(00000)\r\n'
#   b'1-0:72.32.0(00000)\r\n'
#   b'1-0:32.36.0(00005)\r\n'
#   b'1-0:52.36.0(00002)\r\n'
#   b'1-0:72.36.0(00003)\r\n'
#   b'0-0:96.13.0()\r\n'
#   b'1-0:32.7.0(231.0*V)\r\n'
#   b'1-0:52.7.0(225.0*V)\r\n'
#   b'1-0:72.7.0(226.0*V)\r\n'
#   b'1-0:31.7.0(001*A)\r\n'
#   b'1-0:51.7.0(000*A)\r\n'
#   b'1-0:71.7.0(000*A)\r\n'
#   b'1-0:21.7.0(00.344*kW)\r\n'
#   b'1-0:41.7.0(00.007*kW)\r\n'
#   b'1-0:61.7.0(00.000*kW)\r\n'
#   b'1-0:22.7.0(00.000*kW)\r\n'
#   b'1-0:42.7.0(00.000*kW)\r\n'
#   b'1-0:62.7.0(00.000*kW)\r\n'
#   b'!2DD1\r\n'
#   b'/CTA5ZIV-METER\r\n'


##############################################################################
# Usage
##############################################################################

def usage():
    printf("Usage:\n\n\t %s [-d /dev/ttyUSBx || --device=/dev/ttyUSBx] [-m maria.cfg || --maria-config=maria.cfg] \n\n", os.path.basename(sys.argv[0]))
    printf("\t\t-d or --device\t\tSerial device to read from (default /dev/ttyUSB0\n")
    printf("\t\t-s or --sql\t\tConfig file with SQL details (when none given output goes to stdout)\n")
    printf("\n")

##############################################################################
# Serial read
##############################################################################

# Default config
ser = serial.Serial()
ser.baudrate = 115200
ser.bytesize=serial.EIGHTBITS
ser.parity=serial.PARITY_NONE
ser.stopbits=serial.STOPBITS_ONE
ser.xonxoff=0
ser.rtscts=0
ser.timeout=20
ser.port="/dev/ttyUSB0"

def serial_open():
    # Open COM port
    try:
        ser.open()
    except:
        sys.exit ("Cannot open serial device:" % ser.name)      

def serial_read():
    try:
        raw = ser.readline()
    except:
        sys.exit ("Cannot read serial device:" % ser.name )      
    line = str(raw)
    return line.strip()

##############################################################################
# Parse serial line to P1 data
##############################################################################

def parse_line(line):
   # Example data: b'1-0:62.7.0(00.000*kW)\r\n'

   # strip unwanted part
   line=line.replace("b'","")
   line=line.replace(")\\r\\n'","")

   # Split line obi from data #TODO regexp in perl were so much easier ;'(
   a=line.split("(")
   obi = a[0]
   if len(a) > 1:
       a = a[1].split("*")
       val = a[0]
  
   # check if obi is recognized and update the object with data
   for item in P1D:
       if item.iden == obi:
           if item.form == "flo":
               item.floval = float(val)
           if item.form == "int":
               item.floval = int(val)
           if item.form == "datetime":
               item.strval = val           # TODO convert to databse time format
           if item.form == "str":
               item.strval = val

##############################################################################
# Send to database
##############################################################################
dbhost = "localhost"
dbname = "p1monitor"
dbuser = "kp"
dbpass = "kameel"

def p1todb():

    print("todo")

##############################################################################
# Print to stdout
##############################################################################

def p1tostdout():
   clear()
   printf("%-20s%-15s%-10s%-80s\n\n", "P1 Monitor", "P1 Standard:", standard_version, standard_source)
   printf("%-20s%-15s%-10s%-80s\n", "=====","======","=====","============")
   printf("%-20s%-15s%-10s%-80s\n", "Item", "Value", "Unit", "Description")
   printf("%-20s%-15s%-10s%-80s\n", "=====","======","=====","============")
   for item in P1D:
       if item.todb:
           val = item.strval
           if item.form == "flo":
               val = str(item.floval)
           if item.form == "int":
               val = str(item.intval)
           if item.form == "datetime":
               val = item.strval
  
           printf("%-20s%-15s%-10s%-80s\n", item.dbname, item.floval, item.unit, item.desc)

##############################################################################
# Main
##############################################################################

def main():
    # Get options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:s:", ["help", "device=", "sql="])
    except getopt.GetoptError as err:
        print(err) 
        usage()
        sys.exit(2)

    # Parse options
    sqlcfg = "" 
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-d", "--device"):
            ser.port = a
        elif o in ("-s", "--sql"):
            sqlcfg = a
        else:
            assert False, "unhandled option"

    # Get data
    serial_open()
    true=1
    while true:
        # read one full telegram
        while 1:
            line = serial_read()
            if len(line) > 2 and line[2] == "!":
                break
            else:
                parse_line(line)
        # output gathered data
        if sqlcfg == "":
            p1tostdout()
        else:
            p1todb()

if __name__ == "__main__":
    main()

#Close port and show status
try:
    ser.close()
except:
    sys.exit ("Oops %s. Aborted. Could not close serial port !!" % ser.name )      

exit()
