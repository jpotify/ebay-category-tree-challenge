import re
import requests
import sqlite3
import os
import xml.etree.ElementTree as ET

class RebuildCategories:
	def __init__(self):
		self.__prefix = '{urn:ebay:apis:eBLBaseComponents}'
		self.__db_file = 'data/categories.db'

		# Creates 'data' dir if not exists
		if not os.path.exists('data'):
			os.makedirs('data')

	# Get categories from eBay API
	def __get_categories_from_api(self):
		url = 'https://api.sandbox.ebay.com/ws/api.dll'
		headers = {'X-EBAY-API-CALL-NAME': 'GetCategories', \
			'X-EBAY-API-APP-NAME': 'EchoBay62-5538-466c-b43b-662768d6841',\
			'X-EBAY-API-CERT-NAME': '00dd08ab-2082-4e3c-9518-5f4298f296db',\
			'X-EBAY-API-DEV-NAME': '16a26b1b-26cf-442d-906d-597b60c41c19',\
			'X-EBAY-API-SITEID': '0',\
			'X-EBAY-API-COMPATIBILITY-LEVEL': '861'}
		data = '<?xml version="1.0" encoding="utf-8"?>\
	<GetCategoriesRequest xmlns="urn:ebay:apis:eBLBaseComponents">\
	  <RequesterCredentials>\
	    <eBayAuthToken>AgAAAA**AQAAAA**aAAAAA**PMIhVg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GhCpaCpQWdj6x9nY+seQ**L0MCAA**AAMAAA**IahulXaONmBwi/Pzhx0hMqjHhVAz9/qrFLIkfGH5wFH8Fjwj8+H5FN4NvzHaDPFf0qQtPMFUaOXHpJ8M7c2OFDJ7LBK2+JVlTi5gh0r+g4I0wpNYLtXnq0zgeS8N6KPl8SQiGLr05e9TgLRdxpxkFVS/VTVxejPkXVMs/LCN/Jr1BXrOUmVkT/4Euuo6slGyjaUtoqYMQnmBcRsK4xLiBBDtiow6YHReCJ0u8oxBeVZo3S2jABoDDO9DHLt7cS73vPQyIbdm2nP4w4BvtFsFVuaq6uMJAbFBP4F/v/U5JBZUPMElLrkXLMlkQFAB3aPvqZvpGw7S8SgL7d2s0GxnhVSbh4QAqQrQA0guK7OSqNoV+vl+N0mO24Aw8whOFxQXapTSRcy8wI8IZJynn6vaMpBl5cOuwPgdLMnnE+JvmFtQFrxa+k/9PRoVFm+13iGoue4bMY67Zcbcx65PXDXktoM3V+sSzSGhg5M+R6MXhxlN3xYfwq8vhBQfRlbIq+SU2FhicEmTRHrpaMCk4Gtn8CKNGpEr1GiNlVtbfjQn0LXPp7aYGgh0A/b8ayE1LUMKne02JBQgancNgMGjByCIemi8Dd1oU1NkgICFDbHapDhATTzgKpulY02BToW7kkrt3y6BoESruIGxTjzSVnSAbGk1vfYsQRwjtF6BNbr5Goi52M510DizujC+s+lSpK4P0+RF9AwtrUpVVu2PP8taB6FEpe39h8RWTM+aRDnDny/v7wA/GkkvfGhiioCN0z48</eBayAuthToken>\
	  </RequesterCredentials>\
	  <[1>\
	  </GetCategoriesRequest>'

		top_lvl_ctg = self.__get_top_level_categories(url, headers, data)

		# Parse XML info and get CategoryArray section from XML
		tree = ET.fromstring(top_lvl_ctg)
		top_lvl_ctg_list = tree.find(self.__prefix + 'CategoryArray')
		
		all_categories_list = []
		for ctg_id in top_lvl_ctg_list:
			current_id = ctg_id.findtext(self.__prefix + 'CategoryID')
			
#			if current_id is not None and current_id != '1':
			if current_id is not None:
				print('Root ID: ', current_id)
				child_ctg = self.__get_child_categories_tree(url, headers, \
					data, current_id)
				bar = self.__parse_to_list(child_ctg)
				all_categories_list += bar
		
		return all_categories_list
		
	# Get top-level categories
	def __get_top_level_categories(self, url, headers, data):
		top_level_args = '<DetailLevel>ReturnAll</DetailLevel>\
		  <OutputSelector>CategoryID</OutputSelector>\
		  <LevelLimit>1</LevelLimit>'
		top_level_args = re.sub(r"</?\[\d+>", top_level_args, data)
		
		r = requests.post(url, headers=headers, data=top_level_args)

		return r.content
		
	# Get child category tree
	def __get_child_categories_tree(self, url, headers, data, parent_id):
		child_ctg_args = '<CategoryParent>' + parent_id + '</CategoryParent>\
		  <DetailLevel>ReturnAll</DetailLevel>\
		  <LevelLimit>6</LevelLimit>'
		child_ctg_args = re.sub(r"</?\[\d+>", child_ctg_args, data)
		
		r = requests.post(url, headers=headers, data=child_ctg_args, \
			timeout=None)

		return r.content
		

	# Parse XML data from eBay API to a list
	def __parse_to_list(self, info_from_api):
		# Parse XML info
		tree = ET.fromstring(info_from_api)
		
		# Get CategoryArray section from XML
		category_list = tree.find(self.__prefix + 'CategoryArray')
		
		ctg_tuples = []
		if category_list is not None:
			for child in category_list:
				ctg_id = child.findtext(self.__prefix + 'CategoryID')
				ctg_name = child.findtext(self.__prefix + 'CategoryName')
				ctg_level = child.findtext(self.__prefix + 'CategoryLevel')
				ctg_parent_id = child.findtext(self.__prefix + 'CategoryParentID')
				ctg_boe = child.findtext(self.__prefix + 'BestOfferEnabled')
				ctg_boe = 'false' if ctg_boe is None else ctg_boe
				
				# All this attributes must be present but category is disscarded
				if ctg_id is not None and ctg_name is not None and \
					ctg_level is not None and ctg_parent_id is not None:
					p_id = None if ctg_parent_id == ctg_id else ctg_parent_id
					ctg_tuples.append((ctg_id, ctg_name, int(ctg_level), \
						p_id, ctg_boe == 'true'))

		return ctg_tuples

	# Store category list in a SQLite database
	# http://charlesleifer.com/blog/querying-tree-structures-in-sqlite-using-python-and-the-transitive-closure-extension/
	# https://www.sqlite.org/lang_with.html
	def __store_in_db(self, categories):
		# Remove previous database file
		if os.path.isfile(self.__db_file):
			os.remove(self.__db_file)

		try:
			# Create connection to database
			conn = sqlite3.connect(self.__db_file)
			c = conn.cursor()

			# Main table creation:
			# The order of columns must match the order of values in tuples list
			# created at __parse_to_list function
			c.execute('''CREATE TABLE category (
				id TEXT PRIMARY KEY,
				name TEXT NOT NULL,
				lvl INTEGER NOT NULL,
				parent_id TEXT NULL REFERENCES category(id),
				boe INTEGER NOT NULL
				) WITHOUT ROWID''')

			c.executemany('''INSERT INTO category VALUES (?,?,?,?,?)''', categories)

			conn.commit()
		except Exception as e:
			conn.rollback()
			raise e
		finally:
			conn.close()

	#
	# Main method
	#
	def rebuild(self):
		ctg_from_ebay = self.__get_categories_from_api()
		self.__store_in_db(ctg_from_ebay)

#	End of file
