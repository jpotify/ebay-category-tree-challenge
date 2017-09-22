import argparse
import rebuild_categories as rbldc_ctg
import render_categories as rndr_ctg

# Definition of arguments program
parser = argparse.ArgumentParser(description='An eBay category tree displayer')
parser.add_argument('--rebuild', action='store_true', default=False, \
	help='Downloads a category tree from eBay and store it locally.')
parser.add_argument('--render', nargs=1, action='store', \
	help='Renders a category tree view.')
args = parser.parse_args()

if args.rebuild:
	from_api = rbldc_ctg.RebuildCategories()
	from_api.rebuild()

if args.render:
	display = rndr_ctg.RenderCategories()
	display.render(args.render[0])
