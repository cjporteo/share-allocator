# Share Allocator

I created this utility to speed up and automate a common investing task.

Consider the following scenario:

 - you have $10000 of capital to inject into your portfolio
 - you want to invest into AAPL, AMZN, MSFT and JPM with weights 10, 15, 8, 5, respectively
 - you want to invest as much of that $10000 as possible

How many shares of each stock do you need to purchase? 

When fractional share purchasing is not an option, this becomes a tedious endeavour. Fairly quickly into my investing career I grew tired of manually computing share purchases like this and decided to build this utility.

There's a decent chance something like this already exists somewhere, but I wasn't able to find anything in 10 minutes of Googling so decided to just do it myself. I thought it would be a fun academic exercise, anyway.

## Required Packages

 - `yahoo_fin` to get live stock prices, scraping from Yahoo Finance
 - `pandas`

## Usage

Currently, this utility is far from user-friendly. You need to enter your stock symbols and weights directly into the script. 

![Input](https://i.imgur.com/YyALuqC.png)

The algorithm will then evaluate several different investment allocations in an attempt to align with the desired weighting. The potential allocations are sorted according to proportion of the injected capital that is actually invested. The choices with the lowest amount of leftover cash are displayed first.

![Output](https://i.imgur.com/LUfJTUN.png)

## Vague Algorithm Explanation

For this explanation, I'm going to continue with the example stocks and weights I've been using so far in this readme.

We have $10000 of capital to inject, and we wish to allocate ~26.3158% of that capital into AAPL.

`10/(10+15+8+5) = 0.263158`

At time of writing this, one share of AAPL trades for $260.14 USD, and we want to invest $2631.58 into the stock. So, if fractional share purchases were allowed (which is becoming more and more common nowadays), we would purchase 10.116 shares.

`2631.58/260.14 = 10.116`

However, a lot of brokerages only support share purchases in integer amounts, so our ideal purchase of 10.116 shares isn't going to fly. We can either buy 10 (**under-allocated**) or 11 (**over-allocated**) shares of AAPL.

For each stock, unless we are incredibly lucky we will never be able to purchase an amount of shares that exactly mirrors our desired allocation, so we must either go **slightly below** or **slightly above**. This repeated choice of either under-allocating or over-allocating each stock in our portfolio forms the basis of the algorithm.

For every stock in the portfolio, we have two choices (go **down** or go **up**), so this naturally forms a binary tree structure. We navigate this tree using textbook DFS and prune as we go.

## Coming Soon

I intend to host this utility online using Flask in the near future. I'll use SQLAlchemy to handle CRUD operations for the user inputted tabular data.

One feature I'd like to add is to take into account existing shares in the user's portfolio, so that the use case of tweaking and rebalancing an existing portfolio can be supported.
