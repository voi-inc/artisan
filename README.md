artisan [![Build Status](https://travis-ci.org/firstopinion/artisan.png)](https://travis-ci.org/firstopinion/artisan)
=======

CLI build tool to help ease the pain of developing emails.

![Artisan](http://i.cloudup.com/9oBp4FQSRO.jpg)



Why? What?
----------
Developing, testing, and publishing handcrafted emails is a pain. Lets look at the following example:

![Example Usage](https://i.cloudup.com/yPloOPZ189.png)

We have 3 email messages that all use a similiar shell, but have varying interior content. Artisan uses jinja2 templating to allow reuse of this outer shell.

![Example Usage Explained](https://i.cloudup.com/J2zFfpnLmj.png)

### Craft

The `artisan craft` method offers a live development environment that watches for file changes and builds your email messages on the fly. Artisan also utilizes the opensource premailer package, which takes external styles, and moves them inline. For example:

**src**

	<style>
		.table-zero {
			margin-top: 0;
			margin-right: 0;
			margin-bottom: 0;
			margin-left: 0;
			padding-top: 0;
			padding-right: 0;
			padding-bottom: 0;
			padding-left: 0;
		}
	</style>
	
	<table class="table-zero"></table>
	
**build**

	<table style="margin-top: 0; margin-right: 0; margin-bottom: 0; margin-left: 0; padding-top: 0; padding-right: 0; padding-bottom: 0; padding-left: 0;"></table>


### Ship

The `artisan ship` method is used to sync your media to a cloud provider (right now there is only support for Amazon S3). It will also create a `build` directory wich holds your html with your updated img paths.

**src**

	<img src="/masters/01/images/logo.png" alt="Logo">

**build**

	<img src="https://s3.amazonaws.com/bucketname/masters/01/images/logo.png" alt="Logo">



Requirements
------------
- `python-dev`
- `libxml2-dev`
- `libxslt-dev`


Installation
------------

Installing from source:

1. `git clone https://github.com/firstopinion/artisan.git`
2. `cd artisan`
3. `python setup.py install`


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
		"storage": {
			"type": "aws",
			"aws_access_key_id": "I_AM_A_SECRET",
			"aws_secret_access_key": "I_AM_A_KEY",
			"bucket": "I_AM_A_BUCKET"
		}
	}



Usage
-----

`artisan craft`

or

`artisan ship`



Tests
-----

`python setup.py test`



Developing
----------

`python setup.py develop`



Todos
-----

1. Fix README issue with pip long description
2. Write tests for S3 sync using fake-s3: https://github.com/jubos/fake-s3
3. Update ship to only push modified images
4. Create firstopinion.github.io/artisan

Known Issues
------------

1. Ship does not remove images when deleted in source.



License
-------
The MIT License (MIT)
Copyright (c) 2013 First Opinion

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