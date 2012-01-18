#!/usr/bin/env python
#coding: utf8

def label(input, output):
    i = open(input, "r")
    o = open(output, "w")
    try:
        for line in i:
            print line
            flag = raw_input()
            if flag == "1":
                o.write(line.rstrip("\n"))
                o.write("____" + flag + "\n")
                o.flush()
            else:
                o.write(line.rstrip("\n"))
                o.write("____0\n")
                o.flush()
    except:
        pass
    finally:
        i.close()
        o.close()

def count(input):
    i = open(input, "r")
    count = 0
    n = 0
    try:
        for line in i:
            if line.rstrip("\n").split("____")[1] == "1":
                count += 1
            n += 1
        print "count: %s, n: %s" % (count, n)
    except:
        pass
    finally:
        i.close()

def count_http(input):
    i = open(input, "r")
    count = 0
    n = 0
    try:
        for line in i:
            if not "http" in line:
                continue
            if line.rstrip("\n").split("____")[1] == "1":
                count += 1
            n += 1
        print "count: %s, n: %s" % (count, n)
    except:
        pass
    finally:
        i.close()
    
if __name__ == '__main__':
    import sys
    input, output = sys.argv[1:3]
    label(input, output)
    count(output)