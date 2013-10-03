import commands.build_command as bcmd
import utils.PathConverter.path_converter as pc
import utils.infoplist.patcher as plist


class PatchInfoPlist(bcmd.BuildCommand):
	_command_prefix = 'info_plist_'
	_cmd_prefix_len = len(_command_prefix)

	def __init__(self, config):
		self._config = config
		self._info_plist_rel_path = None
		self._plist_dict = {}

		self.ParseConfig()

	def ParseConfig(self):
		self.FetchInfoPlistPath()
		self.FetchAllParams()

	def FetchInfoPlistPath(self):
		self._info_plist_rel_path = self._config['info_plist_rel_path']

	def FetchAllParams(self):
		all_conf_keys = self.FetchAllConfigKeys()

		for k in all_conf_keys:
			self.AddValueFor(k)

	def FetchAllConfigKeys(self):
		all_keys = []
		for k in self._config.keys():
			if k.startswith(PatchInfoPlist._command_prefix) and not k.endswith('rel_path'):
				all_keys.append(k)

		return all_keys

	def AddValueFor(self, conf_key):
		value_token = self._config[conf_key]
		value = self.ParseValueToken(value_token)

		k = self.ParsePlistKeyFrom(conf_key)
		self._plist_dict[k] = value

	def ParseValueToken(self, value_token):
		value = value_token

		if value_token.startswith('@'):
			key = value_token[1:]
			value = self._config[key]

		return value

	def ParsePlistKeyFrom(self, config_key):
		return config_key[PatchInfoPlist._cmd_prefix_len:]

	def Execute(self):
		sln_path = self._config['sln_path']
		pConverter = pc.PathConverter(sln_path)

		info_plist_abs_path = pConverter.Convert(self._info_plist_rel_path)
		patcher = plist.Patcher(info_plist_abs_path)

		patcher.AddOrReplace(self._plist_dict)
