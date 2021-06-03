# Data Engineering Task

## Introduction

This is a data engineering task to extract the 10 latest prices for the cryptocurrency Ethereum, from CoinGecko's public API. I will be using the Python wrapper for CoinGecko's API, provided on their [GitHub page](https://github.com/man-c/pycoingecko).

## Setting up the Environment

The first thing I did was to create a new folder in my local machine (Linux OS), and initialize a Git repository using `git init`. After that, I checked my Python version using `python3 --version`. It wasn't the latest version (it was 3.8.5), so I installed the latest version following the instructions from this [website](https://linuxize.com/post/how-to-install-python-3-9-on-ubuntu-20-04/), and then set up a virtual environment using `python3.9 -m venv data-eng-env`. I was already inside the repo that I created, so before doing anything, I activated the venv using `source data-eng-env/bin/activate`. Next, I created a README.md file using `touch README.md` and wrote the title of this project there. To ensure that I am inside the venv, I can use `env | grep VIRTUAL_ENV`, by piping grep with env, and checking that I am in the correct virtual environment.

Now, I want to track all the changes I made since the initialization. I stage all the changes using `git add .` and make a commit by writing `git commit -m "First commit; created venv and README"`. But before pushing my changes, I will need a GitHub repo first. I am using VS Code with the source control extension, so I simply create a new repository with the name "Data-Engineering-Task" from the "Branches" tab (after signing in with my GitHub account). Once created, it automatically pushes the changes to the new repo. Finally, I install CoinGecko's Python wrapper and create a new Python script using `touch ethprice.py`. I write these steps in the README file and push the new changes to my repo using `git push origin main` (I already configured my GitHub to use `main` instead of `master` as the default branch).

!['Branches' tab in VS Code](images/push_to_main.png "'Branches' tab in VS Code")

I am ready to start writing the Python script.

## Extracting Data from CoinGecko

First, I try to understand the APIs given in the [CoinGecko API page](https://www.coingecko.com/api/documentations/v3), pinging the API server to test it out. It works when it gives a 200 status code, which it does. Also, I was going to use the Python wrapper, then I realized it might be better to just use `requests` where I can specify the parameters more easily.

Next, I want to test out the `simple/price` request since it provides the current price of a crypto in terms of other currencies/cryptos while also including the 24h change and last update time. However, I don't know what the ID for Ethereum is, so I will need to look at the `coins/list` request to see the specific ID for Ethereum. To do this, I wrote a couple of functions to print out the data and put it into a Pandas dataframe. The ID for Ethereum turned out to be `ethereum` and there are over 7600 coins listed on CoinGecko.

Before going any further with data collection, I want to write the `coins_df` list of coins dataframe as a CSV file into my system, create a `requirements.txt` and Dockerize the script so that anyone can run it on their own local machine. However, this proved to be more complicated than I expected.

### Minor Bug

In my Ubuntu laptop, I created the `requirements.txt` file using `pip freeze > requirements.txt` because surprisingly, in contradiction to the info given [here](https://stackoverflow.com/questions/31684375/automatically-create-requirements-txt), using `pipreqs` resulted in generating over 100 dependencies but `pip freeze` generated much less. I also created a Dockerfile according to the [instructions](https://www.freecodecamp.org/news/docker-101-fundamentals-and-practice-edb047b71a51/), using a Python 3.9.5 image, telling Docker to install the dependencies from `requirements.txt` and running the Python script.

However there was a [bug](https://stackoverflow.com/questions/39577984/what-is-pkg-resources-0-0-0-in-output-of-pip-freeze-command) that occurs within Python virtual envs created in Ubuntu.

![Bug when building Dockerfile in Windows](images/bug_pkgresources.png "Bug when building Dockerfile in Windows")

I only found out about this after building the Docker file in my Windows laptop, to test if my script works on Windows.

![Just exclude pkg-resources from pip freeze](images/resolving_bug.png "Just exclude pkg-resources from pip freeze")

In this case, I fixed the bug by excluding the line containing `pkg-resources` from `pip freeze`, following the accepted answer in Stackoverflow:

    pip freeze | grep -v "pkg-resources" > requirements.txt

The `grep` command with the `-v` flag excludes the line containing `pkg-resources` from appearing in the `requirements.txt` file, so it will no longer be installed as a dependency.

### Building the Dockerfile and Running the Container

After fixing this bug, I went back to my Windows machine, cloned the latest repo and successfully built the Dockerfile using `docker build -t trailtask`.

![Docker image created. Why is it so large?](images/why_so_large.png "Docker image created. Why is it so large?")

However, just using `docker run trialtask` did not produce the CSV output that I expected. It took me some digging around to find out that I needed to mount a file drive, so that the CSV that is produced by running the container is also outputted into my local machine. According to a post from [here](https://phoenixnap.com/kb/docker-run-command-with-examples), Docker containers remove all the data they produce after they stop running. The solution is to mount a volume from your local host and write the CSV file into a separate folder `/data` that won't get destroyed after the container stops running. In my case, instead of running `docker run trialtask`, I needed to run

    docker run -v C:\Users\DELL\Desktop\Stuff\Data-Engineering-Task:/app/data detask

I also modified the Dockerfile to create a `/data` directory for this purpose. Running the above command successfully outputted the CSV file that I wanted into my local machine (and it was deleted afterwards).

![CSV file successfully written to local host](images/csv_file_created.png "CSV file successfully written to local host")

## Getting More Data
