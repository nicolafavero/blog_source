
Title: Run a blog with pelican
Date: 2018-07-12 09:00:00 +0100
Category: Projects
Tags: Python, Python2, Python3, pelican
Authors: Leonardo Giordani
Slug: run-a-pelican-blog
Summary: 

One of the main advice TODO I give to novice programmers is: write a blog.

Writing, and in general teaching, is a perfect way to understand concepts. Some say that you cannot claim you understood something until you can explain it properly. This unfortunately doesn't take into account that not everyone is a good communicator, and writing (also technical writing) is an art, not just a set of checkboxes to tick.

Nevertheless, explaining a concept forces you to try to organise your thought, to write them down in a sequential way, to explore corners that you take for granted while the concepts involved are all but simple.

So my advice is once again: write a blog. Share your experience as a programmer, mathematician, physicist, data scientist (and thousands of other interesting jobs that I can't mention here). Don't worry if you don't have a revolutionary discovery to share with others. We are sitting on the shoulders of giants TODO, and every little piece helps.

One of my most successful posts on this blog is something I wrote after fighting for 3 hours with a trivial Python syntax mistake. I was already a senior programmer, I did a novice mistake. I shared the solution and now that post has 800 visits a day TODO, which hopefully means at least 40 people that found a useful solution every day. Maybe these people will one day write the new Google or the new AWS, and I'm glad I helped them today.

# Pelican 

I run this blog since 2013. I wanted to use a static website generator because I liked the simplicity of the concept, and since GitHub was providing free hosting on GitHub Pages TODO LINK I considered it a viable option.

I started with Jekyll TODO LINK, a very well-known static website generator written in Ruby, because it was the system used by the vast majority of technical bloggers out there at the time. Unfortunately I'm not a Ruby programmer, so every issue I had with the build system that ended in a crash was a mystery to me. I also wanted to add functionalities to the system, and the language once again was a barrier. Jekyll is surely a very good system but it didn't suit my needs.

Since I didn't have the time to study Ruby at that point, I tried to find a good static site generator written in Python, a language that I know, and I found it in pelican TODO LINK. Arguably, the pelican website is not graphically amazing, and this worried me a bit, but I quickly discovered that the whole system is pretty good.

In 5 years I developed a wonderfully simple blogging workflow based on Git, so I decided to share my pelican setup with a Cookiecutter template TODO LINK. Recently I refurbished the template to update it with the latest changes that I made to my personal setup and I realised that, despite the documentation, setting up a blog based on pelican might still be difficult for some.

This post will hopefully help those who want to start a static blog with pelican. I will show you how to create your blog from scratch using pelican. You don't need to know Python to use pelican, even though, as it happened to me with Jekyll, it might help if you want to get involved in the development of the project.

# Prerequisites

You need to have Python 3 and Git installed in your system. Git Flow is optional, so if you don't want to use it you can avoid installing it.

# GitHub

You need to create two repositories in your GitHub account. The first one will host the source files of your blog (source repository), while the second one will host the actual static site files (deploy repository).

Call the first repository `blog_source` and the second one `<your_user_name>.github.io`. This latter is enforced by [GitHub pages](https://pages.github.com/), which uses by default that repository to publish the website at the address with that name.

# Install the template

Create a directory that will host your blog, get into it and create a Python virtual environment

``` sh
mkdir mysite
cd mysite
python3 -m venv venv3
```

Activate the virtual environment and install `cookiecutter`

``` sh
source venv3/bin/activate
pip install cookiecutter
```

Then run `cookiecutter` on the template I prepared

``` sh
$ cookiecutter https://github.com/lgiordani/cookiecutter-pelicanblog.git
```

Now, you will be asked some questions, let's look at them in detail. Remember that you can always start from scratch of fix the values you entered manually later.

* `github_username [yourusername]` - Well, this should be self-explanatory
* `blog_source_repo [blog_source]` - This is just the name of the source repository that you created on GitHub
* `deploy_repository [yourusername.github.com]` - This is the name of the deploy repository, i.e. the one that contains the actual static website. The default value is already filled with your GitHub username, so if you are setting up a GitHub Pages blog you can just accept it
* `deploy_directory [deploy]` - The directory where the deploy repository is cloned and that will be updated by the deployment process
* `use_versioning [y]` - Say `y` if you want to have a release process for your website with a version number and associated Git tags.

# Set up the environment

Now enter the directory that was created by the template, it has the name of the source repository

``` sh
cd <blog_source_repo>
```

(e.g. `cd blog_source`), and run the `setup.sh` script.

``` sh
./setup.sh
```

This script performs the following actions

    * It initializes git in the local repository, adding the source repository as a remote with the name `origin`
    * If you are using the versioning and you decided to use Git Flow, it initializes this last one, creating the `develop` branch.
    * Clones the https://github.com/getpelican/pelican-plugins repository
    * Clones the https://github.com/getpelican/pelican-themes repository
    * Creates the deploy directory which is a local clone one of the deploy repository
    * Creates some scripts to simplify your workflow

# Configure Pelican

Now everything is ready to run the `pelican-quickstart` script.

``` sh
pelican-quickstart
```

This script asks the following questions. I marked with a **!!** the answers that are not up to you but depend on the current setup

* `Where do you want to create your new web site? [.]` - **!!** Answer `pelican` so everything will be installed in that directory inside the current one, keeping the installation tidy.
* `What will be the title of this web site?` - This is up to you
* `Who will be the author of this web site?` - This is up to you
* `What will be the default language of this web site? [en]` - This is up to you
* `Do you want to specify a URL prefix? e.g., http://example.com   (Y/n)` **!!** Answer `Y`
* `What is your URL prefix? (see above example; no trailing slash)` **!!** This is `http://<username>.github.io`
* `Do you want to enable article pagination? (Y/n)` - This is up to you
* `How many articles per page do you want? [10]` - This is up to you
* `What is your time zone? [Europe/Paris]` - This is up to you
* `Do you want to generate a Fabfile/Makefile to automate generation and publishing? (Y/n)` - **!!** Answer `n`
* `Do you want an auto-reload & simpleHTTP script to assist with theme and site development? (Y/n)` - **!!** Answer `y`

If you have questions on this part you can read the [Pelican documentation}(http://docs.getpelican.com/en/latest/install.html).

