'''
Created on April 9, 2018
@author: Moayad Almohaishi
'''
import argparse
import os.path
import re
import os
import sys

class GcodeCleaner():
    def __init__(self, fileName = None, outputfile = None, readFirst = True):
        if(fileName is None):
            raise ValueError("GcodeCleaner.Constructor: No file is provided.")
        if(type(fileName) is not str):
            raise ValueError("GcodeCleaner.Constructor: fileName must be a string.")
        if(len(fileName) <4):
            raise ValueError("GcodeCleaner.Constructor: Input file name is too short.")
        self.fileName = fileName
        self.outputfile = outputfile
        self.content = ''
        if(readFirst):self.read()
        # put all files in txtData folder
    def read(self):
        if(self.fileName is None):
            raise ValueError("GcodeCleaner.read: fileName is not setup yet.")

        if(os.path.isfile(self.fileName)):
            file = open(self.fileName,'r')
        else:
            raise ValueError("GcodeCleaner.read: File is not found:" + self.fileName)
        try:
            self.setContent(file.read())
        except:
            pass
        finally:
            file.close()

    def setContent(self,content):
        if(type(content) is not str):
            raise ValueError("GcodeCleaner.setContent: content must be a string.")
        if(len(content) < 1):
            raise ValueError("GcodeCleaner.setContent: content is empty.")
        self.content = content

    def removeComments(self):
        if( len(self.content) > 0):
            self.content = re.sub(r'\([^()]*\)', '', self.content)
        self.save()

    def save(self):
        if(self.outputfile is None):
            raise ValueError("GcodeCleaner.save: No file is provided.")
        if(type(self.outputfile) is not str):
            raise ValueError("GcodeCleaner.save: fileName must be a string.")
        if(len(self.outputfile) <4):
            raise ValueError("GcodeCleaner.save: Input file name is too short.")
        if(self.content is None):
            raise ValueError("GcodeCleaner.save: No content is provided.")
        if(type(self.content) is not str):
            raise ValueError("GcodeCleaner.save: content must be a string.")
        if(len(self.content) <1):
            raise ValueError("GcodeCleaner.save: content is empty.")
        try:
            file = open(self.outputfile, 'w')
            try:
                 file.write(self.content)
            except:
                 raise ValueError("GcodeCleaner.save: cannot write the file")
            finally:
                file.close()
        except IOError:
            pass

def main(argv=sys.argv):
    inFile = (FLAGS.input_file if FLAGS.input_file else
        'input.gcode')
    outFile = (FLAGS.output_file if FLAGS.output_file else
        'output.gcode')

    cleaner = GcodeCleaner(fileName=inFile, outputfile=outFile)
    cleaner.read()
    cleaner.removeComments()
    #cleaner.save()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--input_file',
      type=str,
      default='',
      help='Absolute path to the input gcode file.'
  )
  parser.add_argument(
      '--output_file',
      type=str,
      default='',
      help='Absolute path to the output gcode file.'
  )
  FLAGS, unparsed = parser.parse_known_args()
  main(argv=[sys.argv[0]] + unparsed)
