# Project 1

http://rond.ir is a website for finding round sim cards. There are too many items there and we want to find the best
 out of them, a.k.a. the phone number which its roundness worths its price. 

## Step 1) Cloning project:
I have implemented an incomplete solution. It has a function named 
`request_phone_numbers(prefix, page_number)` which visits rond.ir website (a "hamrahe avval" page like 
[this](https://www.rond.ir/SearchSim/Mci/910/Permanent?page=1&StateId=0&CityId=0&SimOrderBy=Update&ItemPerPage=120))
 and fetches its phone numbers and prices. Read its 
 [docstring](https://docs.python.org/3/tutorial/controlflow.html#tut-docstrings)
 in file `round-sim.py`.
 
 After 
 [Cloning project](https://help.github.com/articles/cloning-a-repository/#platform-mac), go to directory `project-1` and 
 run command `pip install -r requirements.txt` to install requirements. Then make sure you are connected to internet and
 run `python round-sim.py`. It should print something like:
  
  `[{'price': '270000', 'phone_number': '09102626228'}, {'price': '270000', 'phone_number': '09102626229'}, ...`
  
## Step 2) Making a database of phone numbres:
In order to find the best phone number, we have to first create a database of phone numbers and prices. So that we 
fetch them once from the internet, store them in a file and after that, we work with the file instead of internet.

Fetch at least
250 phone numbers for each prefix in range 0910 to 0919 using `request_phone_numbers(prefix, page_number)`. You do not
need to understand how I have implemented this function. Just use it as a 
[Black Box](https://en.wikipedia.org/wiki/Black_box). 

In order to fetch phone numbers, you have to call 
`request_phone_numbers` multiple times. Each call, visits rond.ir website once. Usually websites block users who visit 
them with very high frequency in order to prevent attacks. So 
[search](https://www.google.com/#q=site:stackoverflow.com+wait+python) 
for a way to wait a second between each call of `request_phone_numbers`.

Store the whole results (including price for each phone number) in a file named `database.txt` using
[json](https://docs.python.org/3/tutorial/inputoutput.html?highlight=json#saving-structured-data-with-json)
format.

## Step 3) Find the best phone number:
We have stored all phone numbers in `database.txt`. So we do not need to call `request_phone_numbers` anymore.
Write a function named `main()` that reads phone numbers from `database.txt` and prints the bests of them with their prices.

The best phone number is a phone number which is round enough, but is not too expensive. Design a meter to evaluate
 the trade-of balance and score each (phone-number, price) based on your meter. Print the top 5 best phone numbers.
 
## Step 4) Make a pull request:
This is an open-source project and you have made it more smart in steps 2 and 3. So why not contributing?
Create a pull request described 
[here](https://www.digitalocean.com/community/tutorials/contributing-to-open-source-getting-started-with-git#tutorial_series_61).
