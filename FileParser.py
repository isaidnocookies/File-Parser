import argparse
import json
import sys
import os

def saveTreeToFile(dir, outputFile):
	output = open(outputFile, "w")
	output.write("<!doctype html>\n<body>\n")

	for path, subdirs, files in os.walk(dir):
		level = path.replace(dir, '').count(os.sep)
		indent = '&nbsp' * 4 * (level)
		# print('{}{}/'.format(indent, os.path.basename(path)))
		output.write('<p><strong>{}{}/</strong></p>'.format(indent, os.path.basename(path)))
		output.write("\n")
		subindent = '&nbsp' * 4 * (level + 1)
		for f in files:
			# print('{}{}'.format(subindent, f))
			fullFilePath = (os.path.join(path, f))
			output.write('<p>{}<a href="file:///{}">{}</a></p>'.format(subindent, fullFilePath, f))
			# <a href="file:///C:\Videos\lecture.mp4">Link 2</a>
			output.write("\n")

	output.write("</body></html>\n")
	output.close()

def getFileTypes(dir):
	fileTypes = dict()
	try:
		for path, subdirs, files in os.walk(dir):
			for name in files:
				try:
					fullFile = (os.path.join(path, name))
					fileType = ""

					if "." in name:
						fullFileSplit = fullFile.split(".")
						fileType = str(fullFileSplit[-1])
						if (fullFileSplit.index(".") < fullFileSplit.index("/")):
							print ("Hidden File")
					else:
						fileType = "None"

					if (fileType in fileTypes.keys()):
						fileTypes[fileType] = fileTypes[fileType] + 1
					else:
						fileTypes[fileType] = 1
				except:
					print ("Unexpected error:", sys.exc_info()[0])
					continue
		return fileTypes
	except:
		return {}

def saveFilesByType(dir):
	fileTypes = dict()
	try:
		for path, subdirs, files in os.walk(dir):
			for name in files:
				try:
					fullFile = (os.path.join(path, name))
					fileType = ""

					if (name.index(".") >= 0):
						nameSplit = name.split(".")
						fileType = nameSplit[-1]
					else:
						fileType = "None"

					if (fileType in fileTypes.keys()):
						fileTypes[fileType].append(name)
					else:
						fileTypes[fileType] = []
						fileTypes[fileType].append(name)
				except:
					print ("Unexpected error:", sys.exc_info())
					continue

		print (fileTypes)
		return (fileTypes)
	except:
		return {}

def getCommandLineArguements():
	parser = argparse.ArgumentParser(description='Parse files within directory')
	parser.add_argument('-d', '--directory', help='Directory to index and parse')
	# parser.add_argument('-o', '--output_directory', default='./', help='Outfile file with indexing overview and data')

	return (parser.parse_args())

def getSupportedFileTypes():
	try:
		with open('./configuration.json') as configFile:
			config = json.load(configFile)
		return json.dumps(config["supported_file_types"])
	except:
		return []

def getIgnoredFileTypes():
	try:
		with open('./configuration.json') as configFile:
			config = json.load(configFile)
		return json.dumps(config["ignored_file_types"])
	except:
		return []

def main():
	args = getCommandLineArguements()
	directoryToParse = args.directory
	saveTreeToFile(directoryToParse, "treeOutput.html")
	# saveFilesByType(directoryToParse)

if __name__ == "__main__":
	main()