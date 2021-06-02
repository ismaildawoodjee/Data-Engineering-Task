# Data Engineering Task

## Introduction

This is a data engineering task to extract the 10 latest prices for the cryptocurrency Ethereum, from CoinGecko's public API. I will be using the Python wrapper for CoinGecko's API, provided on their [GitHub page](https://github.com/man-c/pycoingecko).

## Setting up the Environment

The first thing I did was to create a new folder in my local machine (Linux OS), and initialize a Git repository using `git init`. After that, I checked my Python version using `python3 --version`. It wasn't the latest version (it was 3.8.5), so I installed the latest version following the instructions from this [website](https://linuxize.com/post/how-to-install-python-3-9-on-ubuntu-20-04/), and then set up a virtual environment using `python3.9 -m venv data-eng-env`. I was already inside the repo that I created, so before doing anything, I activated the venv using `source data-eng-env/bin/activate`. Next, I created a README.md file using `touch README.md` and wrote the title of this project there. To ensure that I am inside the venv, I can use `env | grep VIRTUAL_ENV`, by piping grep with env, and checking that I am in the correct virtual environment.

Now, I want to track all the changes I made since the initialization. I stage all the changes using `git add .` and make a commit by writing `git commit -m "First commit; created venv and README"`. But before pushing my changes, I will need a GitHub repo first. I am using VS Code with the source control extension, so I simply create a new repository with the name "Data-Engineering-Task" from the "Branches" tab (after signing in with my GitHub account). Once created, it automatically pushes the changes to the new repo. Finally, I install CoinGecko's Python wrapper and create a new Python script using `touch ethprice.py`. I write these steps in the README file and push the new changes to my repo using `git push origin main` (I already configured my GitHub to use `main` instead of `master` as the default branch).

I am ready to start writing the Python script.

## Extracting Data from CoinGecko

First, I try to understand the APIs given in the [CoinGecko API page](https://www.coingecko.com/api/documentations/v3), pinging the API server to test it out. It works when it gives a 200 status code, which it does. Also, I was going to use the Python wrapper, then I realized it might be better to just use `requests` where I can specify the parameters more easily.

Next, I want to test out the `simple/price` request since it provides the current price of a crypto in terms of other currencies/cryptos while also including the 24h change and last update time. However, I don't know what the ID for Ethereum is, so I will need to look at the `coins/list` request to see the specific ID for Ethereum. To do this, I wrote a couple of functions to print out the data and put it into a Pandas dataframe. The ID for Ethereum turned out to be `ethereum`.