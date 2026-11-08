def main():
    with open("ds.csv", 'r') as f1, open("ds.tsv", 'w') as f2:
        for line1 in f1:
            flag = False
            i = 0
            line2 = ""
            lens = len(line1)
            while i < lens:
                if line1[i] == '"' and flag == False:
                    flag = True
                    line2 += line1[i]
                elif line1[i] == '"' and flag == True:
                    flag = False
                    line2 += line1[i]
                elif line1[i] == "," and flag:
                    line2 += line1[i]
                elif line1[i] == "," and flag == False:
                    line2 += "\t"
                else:
                    line2 += line1[i]
                i+=1
            f2.write(line2)
if __name__ == '__main__':
    main()