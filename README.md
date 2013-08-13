artisan [![Build Status](https://travis-ci.org/firstopinion/artisan.png)](https://travis-ci.org/firstopinion/artisan)
=======

CLI build tool to help ease the pain of developing emails.

![Artisan](http://i.cloudup.com/9oBp4FQSRO.jpg)



Installation
------------

Installing from source (from root):

`python setup.py install`



Setup
-----

Artisan uses a specific directory structure in order to build. Make sure your working directory matches

	- (Working Directory)
	  - artisan.json
	  - src
	    - masters
	      - [master name]
	        - index.html
	        - images
	    - messages
	      - [message name]
	        - index.html
	        - images
	  - build (created when artisan ship)
	  - preview (created when running artisan craft)

Add an artisan.json file to your working directory:

	{
		"port": 8080,
		"aws": {
			"aws_access_key_id": "ACCESS_KEY",
			"aws_secret_access_key": "SECRET_KEY"
		}
	}



Usage
-----

### Develop:

`artisan craft`

#### Options

| Name   | Short |  Description                                           | Default     |
| ------ | ----- | ------------------------------------------------------ | ----------- |
| --cwd  | -d    | Dir script is executed from                            | os.getcwd() |
| --port | -p    | Port files are served.                                 | 8080        |

### Publish:

`artisan ship`



Tests
-----

From root:

`python setup.py test`



Developing
----------

From root:

`python setup.py develop`



Todos
-----

1. Add to pip
2. Write tests for S3 sync using fake-s3: https://github.com/jubos/fake-s3
3. Update ship to only push modified images



License
-------
The MIT License (MIT)
Copyright (c) 2013 Jarid Margolin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.