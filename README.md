artisan [![Build Status](https://travis-ci.org/firstopinion/artisan.png)](https://travis-ci.org/firstopinion/artisan)
=======

CLI build tool to help ease the pain of developing emails.

![Artisan](http://i.cloudup.com/9oBp4FQSRO.jpg)



Installation
------------

`pip install email-artisan`



Setup
-----

Artisan uses a specific directory structure in order to build. Make sure your working directory matches

	- (Working Directory)
	  - src
	    - masters
	      - [master name]
	        - index.html
	        - images
	    - messages
	      - [message name]
	        - index.html
	        - images



Usage
-----

### Develop:

`artisan craft`

#### Options

| Name   | Description                                            | Short | Default     |
| ------ | ------------------------------------------------------ | ----- | ----------- |
| --cwd  | Dir script is executed from                            | -d    | os.getcwd() |
| --port | Port files are served.                                 | -p    | 8080        |
| --src  | Src dir that will be built (relative to cwd)           | -s    | src         |
| --out  | Output dir that src will be built to (relative to cwd) | -o    | dev         |

### Publish:

`artisan ship`

Add an artisan.json file to your working directory:

{

}



Tests
-----

Navigate to dir. Must be run from project root

`python -m unittest artisan.tests.artisan_test`



Contributing
------------



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