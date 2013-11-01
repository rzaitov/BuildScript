import re

from parser.CopyParser.CopyArguments import CopyArguments
from parser.LineParser import LineParser


class CopyLineParser(LineParser):
	def __init__(self):
		self.__copyArguments = CopyArguments()

	def parseLine(self, line):
		assert line is not None

		srcFileNameRegexp = r"'(?P<src>[^']+)'"
		dstFileNameRegexp = r"'(?P<dst>[^']+)'$"

		regexpSource = self.startsWithKeywordToken('copy') + srcFileNameRegexp + self.keywordToken('to') + dstFileNameRegexp
		regexp = re.compile(regexpSource, re.UNICODE)

		match = regexp.match(line)
		self._guardMatch(match, line, regexpSource)

		src = match.group('src')
		dst = match.group('dst')

		self.__copyArguments.setArguments(src, dst)
		return self.__copyArguments

	def isValidLine(self, line):
		assert line is not None

		isValid = line.startswith("copy");
		return isValid