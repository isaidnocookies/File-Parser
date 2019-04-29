import argparse
import json
import sys
import os


def getFileTypes(dir):
	filetypes = []
	try:
		for path, subdirs, files in os.walk(dir):
			for name in files:
				try:
					fullFile = (os.path.join(path, name))
					if "." in fullFile:
						fullFileSplit = fullFile.split(".")
						fileType = fullFileSplit[-1]
					else:
						fileType = "None"

					filetypes.append(fileType)
				except:
					continue
		return filetypes

	except:
		return []



def getCommandLineArguements():
	parser = argparse.ArgumentParser(description='Parse files within directory')
	parser.add_argument('-d', '--directory', help='Directory to index and parse')
	parser.add_argument('-o', '--output', default='./', help='Outfile file with indexing overview and data')

	return (parser.parse_args())


def getSupportedFileTypes():
	try:
		with open('./configuration.json') as configFile:
			config = json.load(configFile)

		return json.dumps(config["supported_file_types"])
	except:
		return []


def main():
	print "..."
	args = getCommandLineArguements()
	directoryToParse = args.output
	print getFileTypes(directoryToParse)

	# print args

if __name__ == "__main__":
	main()