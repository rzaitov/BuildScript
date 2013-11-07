from commands.RemoveProjectCommand import RemoveProjectCommand
from parsers.InsideParser.InsideRemoveParser import InsideRemoveParser


class RemoveProjectCommandBuilder:
	def __init__(self):
		pass

	def isRemoveProject(self, line):
		assert line is not None

		parser = InsideRemoveParser('sln')
		isValid = parser.isValidLine(line)

		return isValid

	def getCommandFor(self, line):
		assert line is not None

		parser = InsideRemoveParser('sln')
		result = parser.parseLine(line)

		slnPath = result[0]
		projectName = result[1]

		command = RemoveProjectCommand(slnPath, projectName)
		return command