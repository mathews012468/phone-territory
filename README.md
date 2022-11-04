# Phone Territory Central Database
When a phone number is not in service multiple times in a row;
When the person who owns the number doesn't speak Spanish;
When the person who owns the number doesn't live in our territory;

We take the number away from the territory.

However, when we go out and look for new phone numbers on websites like whitepages, truepeoplesearch, etc., often we end up adding back those same numbers that we removed for perfectly valid reasons.

To avoid this, we can't completely remove those "bad" numbers from the territory. We need to "remember" them so that we don't run into the situation described above.

The solution, that this project aims to provide, is to store the history of every phone number that has ever been in a territory of ours. Then, when it's time to use one of these territories, this database can retrieve all of the phone numbers in that territory satisfying any number of conditions, such as:

1. NOT Last three outcomes are all not in service (it doesn't have to be three)
2. NOT Someone left a message or spoke to the owner of the phone number
3. Address is in territory boundaries

and so on. As the territory is being used, it can be updated to reflect the call outcomes (whether it's No en casa, No en servicio, Ocupado, etc.) and any census (on whitepages and other websites) that the group conductor or the territory servant decides to do.

## Technical details
I'm storing each phone number in its own folder, where the name of the folder is the phone number itself. Each phone number folder will have three files, titled 'names', 'addresses', and 'call-outcomes', each of which will have a separate record on each line of the file. Each record will consist of two pieces of information, separated by a period (.). The first will be the main data, whether it's the name, address, or call outcome, and the second will be a timestamp representing when that record was entered.

As an example, suppose we're entering the phone number (123) 456-7890 (no need to worry about the + before the phone number, since we will only be dealing with American numbers) with the address 100 Main Street and the name of the current owner is John Doe. Let's say we're entering this information for the first time on November 4th, 2022 at 10:46am. Then the folder would look like:

```
1234567890
| names
| addresses
| call-outcomes
```

The 'names' file would look like:

```
John Doe.11-04-2022 10:46
```

The 'addresses' file would look like:

```
100 Main Street.11-04-2022 10:46
```

And the call outcomes file would be empty. If the phone number were later updated with the name Jane Doe on December 5th, 2022 at 6:13pm, then the 'names' file would look like:

```
Jane Doe.12-05-2022 18:13
John Doe.11-04-2022 10:46
```

To avoid storing too much information, I am going to store the last ten records for each name, address, and call outcome at most. If there are already ten records and we go to add another, the oldest one will get deleted.

## Other notes
I have to think more deeply about how I'm storing the time and location, but for now I'm just going to stick to:

Time: MM-DD-YYYY HH:SS (where the HH ranges from 00 to 23)  
Location: STREET ADDRESS, CITY, STATE ZIPCODE