import argparse
import json
import sys
import os
import webbrowser

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
			try:
				output.write('<p>{}<a href="file:///{}">{}</a></p>'.format(subindent, fullFilePath, f))
			except:
				print("Error outputing: " + str(fullFilePath))
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
						fileSplit = fullFile.split(".")
						fileType = str(fileSplit[-1])
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

def outputFilesByType(dir, outputFile):
	fileTypes = dict()

	output = open(outputFile, "w")
	output.write("<!doctype html>\n<body>\n")

	try:
		for path, subdirs, files in os.walk(dir):
			for name in files:
				try:
					fullFile = (os.path.join(path, name))
					fileType = ""

					try:
						if (name.index(".") >= 0):
							nameSplit = name.split(".")
							fileType = nameSplit[-1]
						else:
							fileType = "None"
					except:
						fileType = "None"

					if fileType in fileTypes.keys():
						fileTypes[fileType].append(name)
					else:
						fileTypes[fileType] = []
						fileTypes[fileType].append(name)
				except:
					print ("Unexpected error:", sys.exc_info())
					continue
		# return (fileTypes)
	except:
		print ("Experienced Error while outputing files by type")
		# return {}

	for theFileType in fileTypes.keys():
		output.write('<h1><strong>.{}</strong></h1>'.format(theFileType))
		output.write("\n")
		output.write("<p>")
		files = fileTypes[theFileType]
		for file in files:
			try:
				output.write(str(file))
			except:
				print ("Error writing output: " + str(file))
			output.write("<br>")
		output.write("<p>")

	output.write("</body></html>\n")
	output.close()

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
	outputFilesByType(directoryToParse, "filesByType.html")

	cwd = os.getcwd()
	webbrowser.open("file:///" + str(cwd) + "/treeOutput.html",new=2)

if __name__ == "__main__":
	main()