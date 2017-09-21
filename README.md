eBay Category Tree Renderer
===========================

This **eBay Category Tree Renderer** is an engineering challenge of a company that I applied for a couple of years ago. The purpose of this challenge is to demonstrate the programming skills of the candidate in the context of a "real world" problem.

Description
-----------

The challenge consisted in two parts:

1. Using the [GetCategories API](http://developer.ebay.com/DevZone/XML/docs/reference/ebay/GetCategories.html) from eBay to download the entire eBay category tree and store it in a local SQLite database. The schema design is up to the developer.
2. Get the data from the SQLite database to render category trees in HTML. It needs to be valid markup that loads in a browser and clearly reflects the structure of the tree. Any fron-end library/framework can be used to display the tree.

The solution must be runnable from the command-line and must respond to a couple of tasks:

- Given the command-line argument `--rebuild` it uses the eBay GetCategories API to download the category tree and
   store it in a SQLite database. If the database already exists it should first be deleted.

- When given the command-line argument `--render <category_id>` it should output a file named <category_id>.html that contains a simple web page displaying the category tree rooted at the given ID. The tree should be rendered from the data in your SQLite database. GetCategories API should not be call in this task. if the database does not exist or no any category with the given ID could be found the program should exit with an error.

The way category trees are displayed in HTML should use nesting to make the structure clearly visible in a web browser. For example, nested tables or lists could be used. Each node of the tree should display 
the category ID, name, level and best offer. Beyond these requirements, creativity and imagination in the presentation are the limit.

A simple, self-contained program using as few external dependencies as possible is preferred.

SQLite
------

SQLite is a SQL database that lives in a single file. It is a very popular library, and most programming languages contain bindings to it. Part of the challenge consisted in design a SQL schema to store the category tree. For each category the following attributes must be stored:

- CategoryID
- CategoryName
- CategoryLevel
- BestOfferEnabled

Usage
-----

To get the whole category tree from the eBay API execute the python script with the `--rebuild` argument:

```
$ python3 categories.py --rebuild
```

By executing the command-line argument `--rebuild <category_id>` an html file called `<category_id>.html` is created:

```
$ python3 categories.py --render 179281
$ ls
179281.html
```

If no category ID can not be found, the scripts exits with an error:

```
$ python3 categories.py --render 7777777
No category with ID: 7777777
```

Technology stack
----------------

- Python 3.4.3
- jQuery 3.0
- [jsTree 3.3.1](https://www.jstree.com/)
- Twitter Bootstrap
- SQLite
- [DB Browser for SQLite](http://sqlitebrowser.org/) as graphical tool to inspect the local database.
