from CommandBuilders.ShCommandBuilder import ShCommandBuilder


class StepsRunner:
	def __init__(self):
		self.shCommandBuilder = ShCommandBuilder()

	def run(self, content):
		assert content is not None

		lines = content.splitlines()
		for line in lines:
			stripped = line.strip(' \t\n\r')

			if len(stripped) == 0:
				continue
			if stripped.startswith("#"):
				continue

			self.processLine(stripped)

	def processLine(self, line):
		if self.shCommandBuilder.isShCommand(line):
			cmd = self.shCommandBuilder.getCommandFor(line)
			cmd.execute()
		else:
			raise Exception('unrecognised step')