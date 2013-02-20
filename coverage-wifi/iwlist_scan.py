import os

def main():
    os.system('sudo iwlist eth1 scan | grep -e Quality -e ESSID > scan.dat')
    f = open('scan.dat', 'r')

    lines = f.readlines()

    for n in range(0, len(lines), 2):
        lines[n] = lines[n].replace(' ', '')
        quality, quality_data, signal_data = lines[n].split('=')
        quality_data = quality_data[:5]
        signal_data = signal_data[:3]

        lines[n+1] = lines[n+1].replace(' ', '')
        essid = lines[n+1].replace('ESSID:"', '')
        essid = essid[:-1]

        print 'ESSID: %s \tQUALITY: %s \tSIGNAL: %s' % (essid, quality_data, signal_data)

if __name__ == '__main__':
    main()

