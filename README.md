# tripad_python
> **Goal**: To create a specific web scraper for trip advisor. We want to collect data about trip advisor recommendation for restaurants, hotels, trip advices and vacation rentals. We want to collect the name, the number of comment, the comments themselves, the rating, the rank and the localization of each recommendation.

## Current situation

The code is running (take at most 3 minutes) and collect the following informations:

1. Name
2. Rating
3. Number of Review
4. Address
5. Number of comment

**Issues**: 

- The scraper collect information from place regardless of the geographic situation (it simply searches all the place in the world with the name we give at the beginning)
- The final csv file is not clean, especially for addresses which are sometimes unusable



Steps:

- [ ] Refactoring the old code
  - [ ] Create a map of the functions
  - [ ] Group functions into specific modules
  - [ ] Test the new modules on the new pages
  - [ ] Bring the useful one to the new folder
- [ ] Create a scrapper specifically for "Palermo"
  - [ ] Create a new map for the functions
  - [ ] Start with
    - [ ] Trip advices
    - [ ] Hôtels
    - [ ] Vacation rentals
  - [ ] Add a timer to see how long it would take
  - [ ] Do some test with limited figure or small places
- [ ] Add features to collect comments
  - [ ] Create the first test
  - [ ] Estimate the time it would take for the whole project
- [ ] Add feature to collect data from restaurant
  - [ ] Try to grab the API if it exist
  - [ ] Else try to automate mouse move/clic and scrolling
  - [ ] Estimate the time it would take
