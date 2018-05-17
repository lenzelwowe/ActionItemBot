def main():
    oglist = "Action Items for Wednesday, 05/16/18\n\n*-One* by Wenzel L\n*-Two* by Wenzel L\n*-Three* by Wenzel L\n*-Four* by Wenzel L"
    front = oglist.split('\n',2)
    firstpart = ''.join(front[0:2])
    print('a')
    numItems = 3
    indToDel = 2

    name = 'Wenzel L'
    strnow = "8888"

    secondlist = front[2].split('\n')
    finishedTask = secondlist.pop(indToDel - 1)
    newEnd = "\n".join(secondlist)
    finalText = newEnd.split('-----------------')[0] + "\n"
    if(len(oglist.split('-----------------'))>1):
        finishedList = "\n" + (oglist.split('-----------------')[-1]) + "\n"
    else:
        finishedList = "\n"
    
    new_text = firstpart + "\n\n" + finalText + '-----------------' + finishedList + finishedTask + '\nDone! ' + name + ' at ' + strnow
    print(new_text)

if __name__ == '__main__':
    main()