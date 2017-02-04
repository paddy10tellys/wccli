import click
import logging
import os
from binaryornot.check import is_binary
#  from collections import Counter


@click.command()
@click.argument('sourcefile', type=click.Path(exists=True))
def cli(sourcefile):
    """ This script counts words in a text file """
    logger = logging.getLogger(__name__)  #  _name_ refs current module
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='wc.log', level=logging.INFO, format=log_fmt)

    ext = os.path.splitext(sourcefile)[1][1:]
    basename = os.path.splitext(sourcefile)[0]
    outputfilename = basename + "-count." + ext

    try:
        if (is_binary(sourcefile)):
            raise ValueError("you tried to load a binary file!")
    except ValueError as e:
        logging.error(str(e))
        exit(str(e))

    try:
        if ext != 'txt':
            click.echo('must be a text file ending in .txt')
            raise ValueError('file extension was not .txt!')
    except ValueError as e:
        logging.error(str(e))
        exit()

    try:
        with open(sourcefile) as sourcefile:  # open sourcefile
            data = sourcefile.read()
    except IOError as e:
        logging.error(str(e))
        click.echo('Cannot read the target file for some reason')

    data = data.lower()  # make everything lower case
    for ch in '"''!@#$%^&*()-_=+,<.>/?;:[{]}~`\|':
        data = data.replace(ch, " ")  # replace punctuation with whitespace

#  do something with the data eg count & list words in freq order

    wordDict = {}  # create empty dictionary

    for word in data.split():
        if word not in wordDict:
            wordDict[word] = 1  # add the word
        else:
            wordDict[word] = wordDict[word] + 1  # increment count

# sort items in x by the word count (value in x[1]) rather than the actual
# words in x[0] Sort alphabetically on x[0] when counts are equal
    commonest = sorted(wordDict.items(), key=lambda x: (x[1], x[0]))

    for word, freq in commonest:
        print("%-13s %d" % (word, freq))

    largestWord = ""
    for word, freq in commonest:
        if len(largestWord) < len(word):
            largestWord = word

    used = 0
    for word, freq in commonest:
        if used < int(freq):
            used = int(freq)
            most_no = freq

    mylist = []
    for word, freq in commonest:
        if freq == most_no:
            mylist.append(word)
    print('Commonest word(s) {} used {} times'.format(mylist, most_no))

    # c = Counter()
    # for word, freq in c.most_common():
    #     c.update(commonest)
    # print('%s : %d' % (word, freq))

    # t = sorted(commonest, key=lambda x: -x[1])[:1]
    # for x in t:
    #     print('{0}: {1}'.format(*x))
# write results

    click.echo('Analysis saved in {}'.format(outputfilename))

    with open(outputfilename, "w") as outputfile:
        args = (("Total words: ", len(data.split()), " Unique words: ",
            len(commonest), "\nLongest word: ", largestWord))
        summary = ("{} {} {} {} {} {}".format(*args))
        click.echo(summary)
        outputfile.write(summary)
        for word, freq in commonest:
            outputfile.write("\n\n%-13s %d \n" % (word, freq))

if __name__ == '__main__':
    cli()


