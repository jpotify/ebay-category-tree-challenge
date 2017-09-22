import os
import sqlite3
import json
import template

class RenderCategories:
	def __init__(self):
		self.__db_file = 'data/categories.db'

	# Get categories from database
	def __get_categories(self, root_id):	
		try:
			if not os.path.isfile(self.__db_file):
				raise Exception('Database file "' + self.__db_file + '" doesn\'t exist')

			# Create connection to database
			conn = sqlite3.connect(self.__db_file)
			c = conn.cursor()

			c.execute(''' 
				WITH RECURSIVE my_expression AS (
					-- start with the "anchor", i.e. all of the nodes 
					-- whose parent_id is this one:
					SELECT id, parent_id, name, boe, name AS path, name AS tree, 0 as level
					FROM category
					WHERE id = ?
					
					UNION ALL
					
					-- then the recursive part:
					SELECT 
						current.id AS id,
						current.parent_id AS parent_id,
						current.name AS name,
						current.boe AS boe,
						previous.path || ' > ' || current.name AS path,
						substr('>>>>>>>>', 1, previous.level + 1) || current.name AS tree,
						previous.level + 1 AS level
					FROM category current
					JOIN my_expression AS previous ON current.parent_id = previous.id
				)
				SELECT id,parent_id,name,level,boe FROM my_expression ORDER BY path
			''', (root_id,))
			data = c.fetchall()

			if len(data) == 0:
				raise Exception('No category with ID: ' + root_id)

			categories = []
			for row in data:
				categories.append((row[0], row[1], row[2], row[3], row[4]))

			return categories
		except Exception as e:
			raise e

	# jsTree data format
	def __format_data_for_jstree(self, data):
		core = []

		for ctg_info in data:
			parent_id = '#' if ctg_info[1] is None else ctg_info[1]
			boe = 'Yes' if ctg_info[4] is 1 else 'No'
			text = ctg_info[2] + \
				' (' + ctg_info[0] + ') - ' + \
				' Level ' + str(ctg_info[3]) + \
				'. Best offer?: ' + boe
			
			core.append({'id': ctg_info[0], \
				'parent': parent_id, \
				'text':  text})

		return json.dumps(core)

	# Generate HTML file
	def __generate_html(self, root_id, data):
		target = open(root_id + '.html', 'w')
		target.truncate()

		content = template.body.format('Category ' + root_id, \
			'Display of category ' + root_id, data)

		target.write(content)
		target.close()

	#
	# Main method
	#
	def render(self, root_id):
		try:
			foo = self.__get_categories(root_id)
			bar = self.__format_data_for_jstree(foo)
			self.__generate_html(root_id, bar)
		except Exception as e:
			print(e)
#	End of file