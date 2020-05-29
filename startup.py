import yaml
import settings

def load_list(filepath):
	list_ = open(filepath)
	list_ = yaml.safe_load(list_)
	return list_

def index_list(listvar):
	index = {}
	cnt = 0
	for item in listvar:
		index[item['name']] = cnt
		cnt += 1
	return index

def load_table(filepath, separator=','):
	with open(filepath) as f:
		content = f.readlines()

	content = [x.strip() for x in content]
	table = ([c.split(separator) for c in content])
	return table

def load_text(filepath):
	with open(filepath) as f:
		content = f.read()

	return content

def main_startup():
	banes = load_list(settings.BANES_YAML)
	boons = load_list(settings.BOONS_YAML)
	feats = load_list(settings.FEATS_YAML)
	return {
		'banes': banes,
		'banes_index':index_list(banes),
		'boons':boons,
		'boons_index':index_list(boons),
		'feats':feats,
		'feats_index':index_list(feats),
		'np_attack_range':load_table(settings.NON_PHYSICAL_ATTACK_RANGE),
		'multi_target':load_table(settings.MULTI_TARGET_SUMMARY),
		'boon_cr':load_table(settings.BOON_CR),
		'wealth_overview':load_table(settings.WEALTH_OVERVIEW),
		'help':load_text(settings.HELP)
	}