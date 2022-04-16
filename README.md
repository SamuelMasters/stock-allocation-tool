# Stock Allocation Tool

## By Samuel Masters

#### This project was developed to act as my thidd portfolio project, based on Python Essentials, as part of my Diploma in Software Development with Code Institute.

### [Click here to view the deployed application.](https://stock-allocation-tool-ci.herokuapp.com/)

### [Click here to view the public repository.](https://github.com/SamuelMasters/stock-allocation-tool)

---

# Table of Contents:

1. [The Why](#the-why)
2. [User Experience(UX)](#user-experience-UX)
   1. [Target Audience](#target-audience)
   2. [Strategy](#strategy)
   3. [Scope](#scope)
   4. [Structure](#structure)
   5. [Skeleton](#skeleton)
      1. [Wireframes](#wireframes)
   6. [Surface](#surface)
      1. [Colours](#colours)
      2. [Typography](#typography)
      3. [Images & Icons](#images-&-icons)
3. [Features](#features)
   1. [Current Features](#current-features)
   2. [Future Features](#future-features)
4. [Technologies](#technologies)
5. [Testing](#testing)
   1. [Tests](#tests)
   2. [Bugs & Fixes](#bugs-&-fixes)
6. [Deployment](#deployment)
   1. [GitHub Pages](#github-pages)
7. [Credits](#credits)

# Project Objective & Purpose

The purpose of this Python application is to serve a business need, that is, recommending stock to be sent to each market for a variety of different SKUs.

The objective is to further my own education and knowledge of the Python language, as well as to serve as a proof of concept of what a larger project of a similar purpose could start with. 

# User Experience (UX)

## Target Audience

- Small businesses selling products in multiple markets. 
- Retail or eCommerce businesses looking to maintain optimal stock levels.

## Strategy

To create an simple application that accesses inventory and sales data, and uses it to quickly and easily calculate recommendations for outgoing quantities for each SKU, in each market, with the business aim being to maintain stock levels. Additionally, the application should let users customise the parameters used in those calculations, and let them read the data points that are contributing to the calculation.

### Project Goals

- To provide quick and easy restock recommendations.
- To allow users to read the specific datapoints from the connected dataset. 
- To allow users to customise the parameters used in the key restock calculation.

## Scope:

The scope of the Stock Allocation Tool application at the time of submission is as set out by the features below:

- Connection to and caching of an external dataset located in Google Sheets. 
- Instructions accessible from the main menu which inform the user about the use of the application, and what each option on the main menu does. 
- Calculation of recommended replenishment for each SKU in the connected dataset. 
- A query data function which allows users to view specific data points for each SKU, as well as calculate basic mathematical operations on numerical dataset columns. 

If this project were to be revisited in the future, the following features would be considered:

- Adding a fully-fledged graphic user interface (GUI) to the application, rather than having the application run solely with a command line interface (CLI). A dedicated GUI would allow for simultaneous display of different data points and an improved user experience. 
- The ability to export the results of the restock calculations to a .csv or .txt file on the users' local system, as well as to let them define the file path for where this file would be exported to. 

## Structure

The application's structure is set within a command line interface. It starts with a simple welcome screen, and messages printed to the console which inform the user about the application's initial caching of external data. The main menu then provides the user with various options on how to proceed. 

Sub-menus are housed within the Adjust Variables and Query Data top-menu options. These sub-menus allow the user to choose what variable they wish to change or what type of data they want to examine, respectively. 

- Main Menu
  - Instructions
  - Capture New Snapshot
  - Export Replenishment
  - Adjust Variables
    - Overstock
    - Days of Supply Target
    - Return to Main Menu
  - Query Data
    - Specific SKU Data
    - SUM, AVERAGE or RANGE of entire numerical column
    - All values from one row
    - Return to Main Menu
  - Exit


## Skeleton

### Wireframes

At the project outset, [Lucidchart](https://www.lucidchart.com/pages/) was used to create an inital foundation of the idea. It included information on inital thoughts on how the user might interact with the application, what Python libraries or modules may be required, what sort of variables may need to be involved, whether those variables should be static or dynamic (user-configurable), and what functions may need to be created to handle different operations within the application. 

The below images show how the wireframing process formed. 

- [Conceptualisation](assets/images/wireframes/Lucidchart_1.png)
- [Functions](assets/images/wireframes/Lucidchart_2.png)


## Surface

### Colours, Typography, Imagery

The entire application sits and works within a command line interface, therefore design considerations were generally minimal within the scope of this project. Instead, the user experience received more focus, resulting in considerations like how the user may navigate the menus, how they might understand the information presented to them, and keeping the terminal clear to help maintain high readability. 

---

# Features

## Current Features

- Connection to a mutable external dataset containing relevant inventory data. 
- In-app calculation and output of recommended units to restock for each SKU in the external dataset. 
- The ability to query specific datapoints from the dataset, from within the app itself (as opposed to having to view the dataset itself separately).
- Calculation and output of basic mathematical operations conducted on numerical columns from the external dataset.  

## Future Features

- A migration from the command-line interface to a fully fledged graphical user interface instead, allowing for more user-friendly presentation of data and output. 
- The ability to generate an external document containing the results of the restock calculations, and for the user to choose where this file should be saved. 


# Technologies

## Languages

- [Python](https://www.python.org/)

## Other Technologies, Frameworks & Libraries

- [GSpread](https://docs.gspread.org/en/latest/#)
  - API for Google Sheets which allowed for reading of the sole external dataset.
- [Google Auth](https://google-auth.readthedocs.io/en/master/)
  - Used in conjunction with GSpread, this allowed the application to gain permission and access to the external dataset. 

# Testing

## Tests

### Flake8, Pylint

The Code Institute Python template was used to c

### [W3 HTML Validation](https://validator.w3.org/)

The single HTML document in this project passed with no errors. 
- [Index](https://validator.w3.org/nu/?doc=https%3A%2F%2Fsamuelmasters.github.io%2Fblackjack%2F)

![Project URL passing through W3C HTML validator.](assets/testing/html-validator.png)

### [Jigsaw CSS Validation](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fsamuelmasters.github.io%2Fblackjack%2F&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en)

![Project URL passing through Jigsaw CSS validator.](assets/testing/css-validator.png)

## Bugs & Fixes

1. Fixed -- W3 HTML Validator Errors
   - During the first round of validation, an error was returned which indicated that paragraph tags were being used incorrectly, as they contained other block-level elements within them. I resolved this error by replacing the parent elements with a section element instead of the paragraph element. 
2. Fixed -- Looping functions
   - The debugging process showed that functions were being called at the end of each round of the game when they were not supposed to, which meant at one point the game was looping itself endlessly. The was fixed by changing the order in which functions were called in the code, and refactoring some of the functions themselves to reduce multiple calls to the same function.

# Deployment

## Gitpod
GitPod was used as the IDE for this project. It can be setup via the following steps:
1. Install the Gitpod browser extension [here](https://chrome.google.com/webstore/detail/gitpod-always-ready-to-co/dodmmooeoklaejobgleioelladacbeki).
2. Navigate to your GitHub account and log in. 
3. Navigate to your own repository. 
4. Click the green 'Gitpod' button near the top of the page. 

## Heroku

Heroku was used to deploy this project. 

It was achieved via the following steps: 

1. Navigate to your GitHub repository. 
2. Click on 'Settings'. 
3. On the left-hand navbar, click on 'Pages'. 
4. Under 'Source', click on the dropdown menu, and select "main". 
5. Click 'Save'. Wait a few minutes, refresh the page, and a link will be provided at the top of the page with a URL to your website. 

## Cloning the repository

If you wish to clone the repository to make a dynamic copy of this project, you may do so via the following steps: 

1. Navigate to your GitHub account and log in. 
2. Navigate to the [repository](https://github.com/SamuelMasters/blackjack). 
3. Click 'Code', and on the dropdown menu, click the copy icon alongside the provided URL. 
4. Open Gitpod in your own repository, and open a terminal. 
5. Type 'git clone ' followed by the URL you copied in the previous steps.
6. Press Enter to finish cloning of the repository.  

## Forking the repository

If you wish to fork the repository to make a static, independent copy of this project, you may do so via the following steps: 

1. Navigate to your GitHub account and log in. 
2. Navigate to the [repository](https://github.com/SamuelMasters/blackjack). 
3. In the top-right corner, click 'Fork'. 
4. You should now have a copy of the original repository amongst your other repositories. 

Copying a repository in this way allows you to make changes to the code without affecting the original project, and can be useful for experimentation. 

---

# Credits

1. [Code Institute](https://codeinstitute.net/)
   - For providing me with the knowledge and skills to develop this project, and for supporting my learning journey. 
2. [W3Schools](https://www.w3schools.com/)
   - This website provided a handy, quick reference for checking syntax of the JavaScript included in this project. 
3. [Chris Quinn](https://github.com/10xOXR)
   - A big thank you to Chris, who's advice has been invaluable whilst working on this project.   
4. [Favicon.io](https://favicon.io/)
   - The site's favicon was found on the website [favicon.io](https://favicon.io/) and was used in this project under the [Creative Commons 4.0 license](https://creativecommons.org/licenses/by/4.0/legalcode). The icon was available as part of the open source [Twemoji](https://github.com/twitter/twemoji/blob/master/assets/svg/1f9fc.svg) project. 
4. [Tutorial Republic](https://www.tutorialrepublic.com/faq/how-to-find-the-sum-of-an-array-of-numbers-in-javascript.php)
   - This page helped me to understand how to find the sum of an numerical array, and their code example was adapted for use in my own work (comments annotate this code in the script.js file). 