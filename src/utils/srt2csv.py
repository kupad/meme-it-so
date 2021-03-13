import srt
import csv

def td2ms(td):
    return int(td.total_seconds()*1000)

def srt2csv(srtfilepath, csvfilepath):

    with open(srtfilepath, 'r') as srtfile, open(csvfilepath, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        subs = srt.parse(srtfile)
        
        csvwriter.writerow(['srtidx','start(ms)','end(ms)','content'])
        for sub in subs:
             csvwriter.writerow([sub.index,td2ms(sub.start),td2ms(sub.end),sub.content])

def main():
    srtfilepath = './data/inputs/subs.srt'
    csvfilepath = './data/outputs/srt/subs.csv'
    srt2csv(srtfilepath, csvfilepath)

main()
