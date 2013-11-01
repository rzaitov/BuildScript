from CommandBuilders.CleanBuildCommandBuilder import CleanBuildCommandBuilder
from CommandBuilders.CreateBackupCommandBuilder import CreateBackupCommandBuilder
from CommandBuilders.MakeDirsCommandBuilder import MakeDirsCommandBuilder
from CommandBuilders.PatchCsprojCommandBuilder import PatchCsprojCommandBuilder
from CommandBuilders.PatchInfoplistCommandBuilder import PatchInfoplistCommandBuilder
from CommandBuilders.RemoveProjectCommandBuilder import RemoveProjectCommandBuilder
from CommandBuilders.ShCommandBuilder import ShCommandBuilder
from commands.ValueProvider import ValueProvider


class StepsRunner:
	def __init__(self, config):
		assert config is not None

		self.valueProvider = ValueProvider(config)

		self.shCommandBuilder = ShCommandBuilder()
		self.removeProjectBuilder = RemoveProjectCommandBuilder()
		self.createBackupBuilder = CreateBackupCommandBuilder()
		self.createDirs = MakeDirsCommandBuilder()
		self.patchCsproj = PatchCsprojCommandBuilder(config, self.valueProvider)
		self.patchInfoPlist = PatchInfoplistCommandBuilder(self.valueProvider)

		buildUtilPath = config['build_tool']
		self.cleanBuilder = CleanBuildCommandBuilder(buildUtilPath, 'clean')
		self.buildBuilder = CleanBuildCommandBuilder(buildUtilPath, 'build')

	def run(self, content):
		assert content is not None

		lines = content.splitlines()
		for line in lines:
			stripped = line.strip(' \t\n\r')

			if len(stripped) == 0:
				continue
			if stripped.startswith("#"):
				continue
			else:
				self.processLine(stripped)

	def processLine(self, line):
		if self.shCommandBuilder.isShCommand(line):
			cmd = self.shCommandBuilder.getCommandFor(line)
			cmd.execute()
		elif self.removeProjectBuilder.isRemoveProject(line):
			cmd = self.removeProjectBuilder.getCommandFor(line)
			cmd.execute()
		elif self.cleanBuilder.isCleanBuild(line):
			cmd = self.cleanBuilder.getCommandFor(line)
			cmd.execute()
		elif self.buildBuilder.isCleanBuild(line):
			cmd = self.buildBuilder.getCommandFor(line)
			cmd.execute()
		elif self.createBackupBuilder.isCreateBackup(line):
			cmd = self.createBackupBuilder.getCommandFor(line)
			cmd.execute()
		elif self.createDirs.isMakeDirsCommand(line):
			cmd = self.createDirs.getCommandFor(line)
			cmd.execute()
		elif self.patchCsproj.isPatchCsproj(line):
			cmd = self.patchCsproj.getCommandFor(line)
			cmd.execute()
		elif self.patchInfoPlist.isPatchInfoPlist(line):
			cmd = self.patchInfoPlist.getCommandFor(line)
			cmd.execute()
		else:
			msg = "unrecognised step. Line: '{0}'".format(line)
			raise Exception(msg)