import os
scriptFilePath = os.path.abspath(__file__)

scriptDir = os.path.dirname(scriptFilePath)
baseDir = os.path.join(scriptDir, os.pardir)

os.chdir(baseDir)

from SettingsProvider.FromFileSettingsProvider import FromFileSettingsProvider
from StepRunner.StepsRunner import StepsRunner
from utils.configs.BuildConfigProvider import BuildConfigProvider

class TaskRunner:
	def run(self):
		settingsProvider = FromFileSettingsProvider()
		settings = settingsProvider.fetchSettings()

		configsProvider = BuildConfigProvider()
		buildReadyConfigs = configsProvider.getConfigs(settings)

		for bc in buildReadyConfigs:
			self.runConfig(bc)

	def runConfig(self, config):
		content = self.getStepsContent(config)

		stepsRunner = StepsRunner(config)
		stepsRunner.run(content)

	def getStepsContent(self, config):
		pathToSteps = config['steps']
		stepsFile = open(pathToSteps)

		content = stepsFile.read()
		return content

runner = TaskRunner()
runner.run()
