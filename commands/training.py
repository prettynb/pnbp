import click

from pnbp.models import Notebook, Note
from pnbp.wrappers import pass_nb

from pnbp.training import AnaerobicTraining, AnaerobicTrainingParser, Exercise, create_trainee, loads_trainee
from pnbp.training import categories as c


@pass_nb
def _create_trainee(nb=None):
	"""
	"""
	return create_trainee(nb=nb)


@pass_nb
@click.option('-t', '--trainee-name', help="The name of an existing trainee.")
def _loads_trainee(trainee_name:str ,nb=None):
	"""
	"""
	trainee = loads_trainee(trainee_name, nb=nb)
	print(trainee)
	return trainee


@pass_nb
def _collect_all_training(nb=None):
	""" """
	ns = "".join([f"[[{n.name}]]\n" for n in nb.notes.values() if n.is_tagged('#training')])
	ns = "\nall #training :\n\n --- \n\n " + ns

	nb.generate_note('all training', ns, overwrite=True)


@pass_nb
def _parse_training(nb=None):
	""" """
	# training = AnaerobicTrainingParser


def main():

	pass

	# client = load_client('curtis_brunelle')
	# df = pd.read_csv('clients/fletch_brunelle/2019-01-22_hypr_fletch_brunelle.csv')
	# df = pd.read_csv('clients/curtis_brunelle/asverbose/2019-01-15_hypr_curtis_brunelle_V.csv')
	# cowboy_method = 'testdata/inputs/cowboy_template.txt'

	# # TRAININGRES: ##
	# df = exercisere('clients/curtis_brunelle/astxt/2019-01-15_hypr_curtis_brunelle.txt', 'curtis brunelle')

	# exercisere('clients/fletch_brunelle/astxt/2019-01-22_hypr_fletch_brunelle.txt', 'fletch brunelle')
	# exercisere('testdata/outputs/filledtemplate.txt', 'curtis_brunelle')

	# exercisere('testdata/inputs/examplebwt.txt', 'curtis brunelle')
	# exercisere('testdata/inputs/exampledual.txt', 'curtis brunelle')

	# metconre('testdata/cleanmetcon.txt')

	# df = from_template(cowboy_method, 'curtis_brunelle',
	# 					start='5/6', days=['Mon', 'Wed', 'Fri'],
	# 					goal1RMs={'Bench Press':275, 'Back Squat':405, 'Front Squat':350},
	# 					exportfile='testdata/outputs/filledtemplate.txt')
	
	# df = df[[col for col in df.columns if col not in ['x']]]
	# df.to_csv('testdata/outputs/filledtemplate.csv', index=False)

	# df = pd.read_csv('testdata/outputs/filledtemplateexreed.csv')
	

	## RECOVERRES: ##
	# sleepre('testdata/inputs/cleansleep.txt')
	# physiore('testdata/inputs/cleanrecovery.txt')
	# fluidre('testdata/inputs/cleanfluids.txt', 'curtis brunelle')
	# supplementre('testdata/inputs/cleansupps.txt')



	## CLIENTSTUFF: ##
	# all_df = collect_all_ex_df(exclude=['johnny_noname'], asverbose=True)
	# all_df.to_csv('testdata/outputs/allclientprogs.csv')
	# print(all_df.to_string())

	# meal_planning('curtis_brunelle')

	# predict_recomp(client, weeks=12)



	## EXFRAMES: ##
	## Determine volume % by category:
	# mydict = category_volume(df, client=client)
	# print(mydict)
	# print(mydict['horizPush'] / mydict['total_vol'])

	## Capturing volume done per muscle, per day, and plotting:
	# vol_df = vbm_to_df(df, client='curtis_brunelle', plot=False)
	# print(vol_df.to_string())
	# vol_df.to_csv('testdata/outputs/volbydaily.csv')

	## View weekly breakdown in reach/surpass of adaptive volumes:
	# mv_df = watch_m_v(df, client)
	# print(mv_df)

	## Pretty print a program to xlsx:
	# df = pd.read_csv('testdata/outputs/filledtemplate.csv')
	# df_to_xlsx(df, 'testdata/outputs/printedexcel2.xlsx', pprint=False)



	## EXERCISE: ##
	## Fixing adaptive_peak:
	# ex = Exercise('Pull Ups', 4, 10, 55, 'curtis_brunelle')
	# ex.make_assignments()
	# print(ex.muscles)
	# print(ex.joints)
	# print(ex.ratios)
	# print(ex.vol)

	# print(ex.adapt_peak)



	## DATABASING: ##
	## Update the exnotes database:
	# file = open('clients/curtis_brunelle/archive/2019-01-15_hypr_curtis_brunelle.txt').read()
	# exnotes = get_notes(file)
	# update_notes(exnotes)



if __name__ == '__main__':
	main()

