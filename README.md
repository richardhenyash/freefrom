# FreeFrom #
[FreeFrom Live Site](https://freefrom.herokuapp.com/)  

<img src="/static/testing/responsive/freefrom-responsive.png" width="100%" style="margin: 15px;">

## Contents ##
- [Background](#background)
- [Project Goals](#project-goals)
- [Site Owner Goals](#site-owner-goals)
- [User Goals](#user-goals)
- [UX](#ux)
    - [Project Strategy](#project-strategy)
        - [Opportunities Matrix](#opportunities-matrix)
    - [Project Scope](#project-scope)
        - [User Demographics](#user-demographics)
        - [User Requirements](#user-requirements)
        - [User Stories](#user-stories)
        - [Contraints](#constraints)
        - [Functional Requirements](#functional-requirements)
        - [Business Rules](#business-rules)
        - [Key Features](#key-features)
    - [Site Map](#site-map)
    - [Wireframes](#wireframes)
    - [Design Choices](#design-choices)
        - [Fonts](#fonts)
        - [Colours](#colours)
- [Technologies](#technologies)
    - [Integrated Development Environment](#Integrated-Development-Environment])
    - [Database](#database)
    - [Deployment](#deployment)
    - [Languages](#languages)
    - [Frameworks Libraries and Tools](#frameworks-libraries-and-tools)
    - [Browser Support](#browser-support)
- [Structure](#structure)
    - [Information Architecture](#information-architecture)
    - [Features Implemented](#features-implemented)
        - [Features Implemented in Phase 1](#features-implemented-in-phase-1)
        - [Features To Be Implemented In Future Development Phases](#features-to-be-implemented-in-future-development-phases)
        - [Design Changes During The Phase 1 Development](#design-changes-during-the-phase-1-development)
    - [Responsive Styling](#responsive-styling)
    - [Python Code Logic](#python-code-logic)
        - [Products](#products)
        - [Categories](#categories)
        - [Allergens](#allergens)
        - [User Authentication](#user-authentication)
        - [Mail](#mail)
    - [Python Code Refactoring](#python-code-refactoring)
    - [Form Validation](#form-validation)
    - [JavaScript Code Logic](#javascript-code-logic)
- [Testing](#testing)
- [Deployment](#deployment)
- [Credits](#credits)
- [Acknowledgements](#acknowledgements)

## Background ##
EU law mandates that 14 major food allergens are listed in food product ingredients.
It is currently quite difficult when shopping to identify products which are suitable for different allergies and intolerances - 
generally requiring the consumer to read the ingredients on individual product packaging, which can be quite time consuming.
Additionally, since the COVID-19 pandemic, consumers are less comfortable picking up products in a supermarket, reading the ingredients
and then putting the product back on the shelf.

## Project Goals ##
To provide an online, open source, interactive information resource that enables consumers to identify 
products which are free from common allergens, and therefore suitable for food allergies and intolerances. 
The site could also be expanded in the future to include for example products suitable for vegans, 
products which are free from palm oil, and products which are ethically sourced.

## Site Owner Goals ##
Developing the site will serve as a learning experience for the developer. The finished website will act as a showcase for the
developer's skills and will also help to raise the developer's profile. If the site becomes very popular, it may be
possible to generate advertising revenue in the future.

## User Goals ##
To find products which are free from allergens and therefore suitable for food intolerances and allergies, 
and to add intolerance and allergy safe food products to the information resource.

## UX ##

### Project Strategy ###

#### Opportunities Matrix ####
The following opportunities were identified and ranked using a score of 1 - 5 for importance and viability:

Opportunity|Description|Importance|Viability|Opportunity ID
-----------|-----------|----------|---------|--------------
Create database| Create an online, searchable database that enables consumers to identify products which are suitable for food allergies and intolerances|5|3|Op-1
Enable User contribution|Enable users to contribute to the database|5|3|Op-2
Showcase developer's skills|The site will serve as a showcase for the developer's skills, and increase the developer's standing within the tech community|4|3|Op-3

<img src="/static/wireframes/strategy-matrix.png" width="400px" style="margin: 15px;">

### Project Scope ###
#### User Demographics ####
* The primary users of the site will be consumers with food allergies and intolerances, 
and consumers with children or relatives who have food allergies and intolerances.
* A simple, well layed out site with the key information being easy to find and easy 
to contribute to would suit this demographic.

#### User Requirements ####
* Simple and well layed out.
* Easy to find key information.
* Easy to contribute to.
* Responsive design is required as users may be viewing the site on Mobile, Tablet or Desktop.

#### User Stories ####
* ***As a User, I am searching for a product which is free from one or more allergens.***
* ***As a User, I have found a product which is free from one or more allergens, and I want to add it to the database.***
* ***As a User, I have tried a product and would like to rate it.***
* ***As a User, I have tried a product and would like to review it.***
* ***As a User, I would like to add a new product category.***
* ***As a User, I would like to add a new allergen.***
* ***As a User, I would like to be able to contact the developer.***

#### Constraints #####
* Developer skill set - the Developer is currently learning Python, Flask and MongoDB. 
This may impact on which features can be succesfully implemented during the phase 1 development.
* Developer's available time - the developer is working full time whilst studying.
This coupled with the developer's current skills constraints may impact which features 
can be succesfully implemented during the phase 1 development.

#### Functional Requirements ####
* The User needs to be able to register.
* The User needs to be able to login and logout.
* The User needs to be able to search for products which are free from one or more allergens.
* The User needs to be able to add products.
* The User needs to be able to rate products.
* The User needs to be able to review products.
* The User needs to be able to edit products.
* The User needs to be able to delete products (this should be restricted to users with the correct privelages).
* The User needs to be able to add product categories (this should be restricted to users with the correct privelages).
* The User needs to be able to edit product categories (this should be restricted to users with the correct privelages).
* The User needs to be able to delete product categories (this should be restricted to users with the correct privelages).
* The User needs to be able to add allergens (this should be restricted to users with the correct privelages).
* The User needs to be able to edit allergens (this should be restricted to users with the correct privelages).
* The User needs to be able to delete allergens (this should be restricted to users with the correct privelages).
* The User needs to be able to contact the developer.

#### Business Rules ####
* It is not envisaged that the site will generate profits. It is intended to be used as an independent source of 
information for consumers. If the site becomes very popular, it may be possible to generate advertising revenue in the future.

#### Key Features ####
The following key features have been identified and scored from 1 - 5 for importance and viability. 
Each feature is mapped back to the [Opportunities Matrix](#opportunities-matrix). 
The proposed development phase has also been indicated:

Feature|Description|Importance|Viability|Opportunity ID|Development Phase
-------|-----------|----------|---------|--------------|-----------------
Registration Form|User registration form|5|3|Op-2|1
Login/Logout|User login/logout form|5|3|Op-2|1
Search|Enables users to search the database based on one or more allergies or intolerances|5|3|Op-1|1
Add Product|Enables users to add a product to the database|3|3|Op-2|1
Add Category|Enables users with required privelages to add product categories to the database|3|3|Op-1, Op-2|1
Edit Category|Enables users with required privelages to edit product categories in the database|3|3|Op-1, Op-2|1
Delete Category|Enables users with required privelages to delete product categories from the database|3|3|Op-1, Op-2|1
Add Allergen|Enables users with the required privelages to add allergens to the database|3|3|Op-1, Op-2|1
Edit Allergen|Enables users with the required privelages to edit allergens in the database|3|3|Op-1, Op-2|1
Delete Allergen|Enables users with the required privelages to deelte allergens in the database|3|3|Op-1, Op-2|1
Rate Product|Enables users to give a star rating to a product|2|2|Op-2|1
Review Product|Enables users to review a product|2|2|Op-2|1
Contact Form|Form to contact developer|4|5|Op-3|1
GitHub Link|Link to developer github page|4|5|Op-3|1
Upload Pictures|Enables users to add pictures of products and ingredients|1|2|Op-2|2
Barcode Scanner|Enables users to automatically add products by scanning a product barcode with their device camera|1|1|Op-2|2

<img src="/static/wireframes/scope-matrix.png" width="600px" style="margin: 15px;">

### Site Map ###
An initial [Site Map](/static/wireframes/site-map.png) was produced, and is shown below:  
<img src="/static/wireframes/site-map.png" width="400px" style="margin: 15px;">

### Wireframes ### 
[Initial Wireframes](/static/wireframes/rev0) were produced showing the Home, Sign In, Register, View Product, 
Edit Product, Add Product, Add Category, Edit Category, Delete Category, Add Allergen, Edit Allergen, Delete Allergen and 
Contact Developer page layouts. The Home page is shown below:  

<img src="/static/wireframes/rev0/home.png" width="600px" style="margin: 15px;">

[Responsive design wireframes](/static/wireframes/rev1) were then produced showing the Home page layout on Table and Phone. 
The [Responsive design wireframes](/static/wireframes/rev1) are shown below:  

<img src="/static/wireframes/rev1/home-tablet.png" width="300px" align="left" style="margin: 15px;">
<img src="/static/wireframes/rev1/home-phone.png" width="300px" style="margin: 15px;">

### Design Choices ###

#### Fonts ####
[Architect's Daughter](https://fonts.google.com/specimen/Architects+Daughter) has been chosen as the logo font for the [FreeFrom logo](/static/testing/logo.png). 
The font has a hand drawn appearence, looks very attractive with the dove logo and fits well with the overall site theme.  
* font-family: "Architects Daughter", sans-serif;

[Montserrat](https://fonts.google.com/specimen/Montserrat) has been chosen as the title font and is used for the 
navigation menu, controls, forms and footer links. [Montserrat](https://fonts.google.com/specimen/Montserrat) has 
a simple, clean, rounded look and is available in a good selection of weights.
* font-family: "Montserrat", sans-serif;

[Open Sans](https://fonts.google.com/specimen/Montserrat) has been chosen as the body font and is used for the search results and review tables. 
[Open Sans](https://fonts.google.com/specimen/Montserrat) is complimentary to [Montserrat](https://fonts.google.com/specimen/Montserrat) and has 
a similar clean look and feel but is not quite as wide, which will allow for more information to be displayed in the search results and review tables. 
[Open Sans](https://fonts.google.com/specimen/Montserrat) is also available in a good selection of weights.
* font-family: "Open Sans", sans-serif;


[Architect's Daughter](https://fonts.google.com/specimen/Architects+Daughter) and [Montserrat](https://fonts.google.com/specimen/Montserrat) 
are available from [Google Fonts](https://fonts.google.com/) and are licensed under the [Open Font License](https://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&id=OFL).  
[Open Sans](https://fonts.google.com/specimen/Montserrat) is available from [Google Fonts](https://fonts.google.com/) and is licensed under the 
[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.html).

#### Colours ####
White was chosen as the background colour to enable a smple and clear design to be implemented.  
Bright foreground colours were chosen to contrast with the white background. Colour ideas were generated 
using the [ColorSpace](https://mycolor.space/) colour palette generator. The final colour palette selected 
is shown below: 

<img src="/static/wireframes/colour-palette.png" width="800px" style="margin: 15px;">  

* #FFFFFF - "White" - used for the background.
* #009EA3 - "Vividian Green" - used for results and review table links.
* #E97C72 - "Salmon" - used for form control borders and results and review table next and previous buttons.
* #E35B4F - "Fire Opal" - used for navbar backgorund, buttons, results table header backround, inputs and footer links.
* #C22C1E - "Venetian Red" - used as a higlighting colour for items coloured with "Fire Opal".
* #F5B800 - "Orange Yellow" - used for alerts, buttons, results and review table row borders and stars.
* #CC9900 - "Lemon Curry" - used as a higlighting colour for items coloured with "Orange Yellow".

## Technologies ##

### Integrated Development Environment ##
* [GitHub](https://github.com/)

### Database ###
* [Mongo DB](https://www.mongodb.com/)

### Deployment ###
* [Heroku](https://dashboard.heroku.com/)

### Languages ###
* [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
* [CSS](https://www.w3.org/Style/CSS/Overview.en.html)
* [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
* [Python](https://www.python.org/)

### Frameworks Libraries and Tools ###
* [Bootstrap](https://getbootstrap.com/docs/5.0/getting-started/introduction/), to assist with responsive design.
* [Font Awesome](https://fontawesome.com/), for icons.
* [Google Fonts](https://fonts.google.com/), for fonts.
* [jQuery](https://jquery.com/), to assist with JavaScript coding and DOM manipulation.
* [PyMongo](https://pypi.org/project/pymongo/), to enable interaction with [Mongo DB](https://www.mongodb.com/).
* [Flask](https://flask.palletsprojects.com/en/2.0.x/), to render and display web pages.
* [DataTables](https://datatables.net/), to enable easy display of data tables.
* [WTForms](https://wtforms.readthedocs.io/en/2.3.x/), for form validation.
* [wftorms-validators](https://pypi.org/project/wtforms-validators/), for additional form validators.
* [Jinja](https://jinja.palletsprojects.com/en/3.0.x/), to enable easy display of database information using templating.
* [Werkzeug](https://werkzeug.palletsprojects.com/en/2.0.x/), to enable generation and checking of secure password hashes.
* [SMTPLib](https://docs.python.org/3/library/smtplib.html), to enable contact email to be sent.

### Browser Support ###
The following browsers are all supported by **FreeFrom**.
* [Google Chrome](https://www.google.com/intl/en_uk/chrome/)
* [Microsoft Edge](https://www.microsoft.com/en-us/edge)
* [Safari](https://www.apple.com/uk/safari/)
* [Firefox](https://www.mozilla.org/en-GB/firefox/new/)
* [Opera](https://www.opera.com/)

For further information please see  the **Browser Compatibility** section in [TESTING.md](TESTING.md).  

## Structure ##

### Information Architecture ###
[Mongo DB](https://www.mongodb.com/) has been selected to host the back end database for [FreeFrom](https://freefrom.herokuapp.com/). 
[Mongo DB](https://www.mongodb.com/) is a non relational [NoSQL](https://www.mongodb.com/nosql-explained) database hosting platform, 
which provides an easily scalable platform to base the [FreeFrom](https://freefrom.herokuapp.com/) site on.  

The project data schema 
was modelled using [Moon Modeller](https://www.datensen.com/data-modeling/moon-modeler-for-databases.html) and is shown below:  

<img src="/static/wireframes/schema.png" width="800px" style="margin: 15px;"> 

As shown in the schema diagram, there are four collections, **Users**, **Products**, **Categories** and **Allergens**.  

Please note that the field **allergens_suitability** in the **Products** collection was renamed to **free_from_allergens**. 
This change was not picked up in the note below the "products" collection in the schema diagram shown above 
and unfortunately the free 14 day trial for the software ended. 

[FreeFrom](https://freefrom.herokuapp.com/) is deployed using [Heroku](https://dashboard.heroku.com/). 
For further information see [Deployment](#deployment).

### Features Implemented ###

#### Features Implemented in Phase 1 ####
* **Home Page**, enables users to search for products which are free from one or more allergens:  
<img src="/static/testing/home.png" width="800px" style="margin: 5px;"> 

* **FreeFrom** logo, links to home page if selected:  
<img src="/static/testing/logo.png" width="300px" style="margin: 5px;"> 

* **Home Page Alert**, explains the purpose of the site, shows user name if signed in:  
<img src="/static/testing/home-alert.png" width="700px" style="margin: 5px;"> 

* **Search Input**, allows user to optionally input product search criteria to filter search results:  
<img src="/static/testing/search.png" width="500px" style="margin: 5px;">  

* **Category Selector**, allows user to optionally select category to filter search results:  
<img src="/static/testing/category.png" width="500px" style="margin: 5px;">  

* **Search Button**, searches the database and returns matched products in the **Product Results Table**. 
Resizes if user is not signed in and add button is not displayed:  
<img src="/static/testing/search-button.png" width="100px" style="margin: 5px;">  

* **Add Button**, links to the **Product Add** form. Only shown if user is signed in:  
<img src="/static/testing/add-button.png" width="100px" style="margin: 5px;">  

* **Allergen Selector**, allows user to optionally select allergens to filter search results:  
<img src="/static/testing/allergen-selector.png" width="80%" style="margin: 5px;">  

* **Product Results Table**, displays product search results. Product name links to **Product View** page:
<img src="/static/testing/results-table.png" width="80%" style="margin: 5px;"> 

* **Sign In**, displays form allowing user to sign in. Includes link to **Register**:  
<img src="/static/testing/signin.png" width="500px" style="margin: 5px;"> 

* **Register**, displays form allowing user to register:  
<img src="/static/testing/register.png" width="500px" style="margin: 5px;"> 

* **Product View**, displays product details. If user is signed in, allows review and rating to 
be added or updated.   
**Add** button enables user to review and rate product.  
**Add** button text is changed to **Update** if the user has already reviewed the product.  
**Update** button updates review and rating if product has already been reviewed by the user.  
**Product Edit** button links to **Product Edit** page.  
User reviews are shown below in the user reviews table:  
<img src="/static/testing/product-view-add-review.png" width="500px" style="margin: 5px;">  
<img src="/static/testing/product-view-update-review.png" width="500px%" style="margin: 5px;">  

* **Product Edit**, displays form allowing product to be edited:  
<img src="/static/testing/product-edit.png" width="500px" style="margin: 5px;">  

* **Product Add**, displays form allowing product to be added:  
<img src="/static/testing/product-add.png" width="500px" style="margin: 5px;">  

* **Allergen Add**, displays form allowing Allergen to be added:  
<img src="/static/testing/allergen-add.png" width="500px" style="margin: 5px;">  

* **Allergen Edit**, displays form allowing Allergen to be edited:  
<img src="/static/testing/allergen-edit.png" width="500px" style="margin: 5px;">  

* **Allergen Delete**, displays form allowing Allergen to be deleted:  
<img src="/static/testing/allergen-delete.png" width="500px" style="margin: 5px;">  

* **Allergen Delete Confirm**, displays form confirming Allergen sohuld be deleted:  
<img src="/static/testing/allergen-delete-confirm.png" width="800px" style="margin: 5px;">  

* **Category Add**, displays form allowing Category to be added:  
<img src="/static/testing/category-add.png" width="500px" style="margin: 5px;">  

* **Category Edit**, displays form allowing Category to be edited:  
<img src="/static/testing/category-edit.png" width="500px" style="margin: 5px;">  

* **Category Delete**, displays form allowing Category to be deleted:  
<img src="/static/testing/category-delete.png" width="500px" style="margin: 5px;">  

* **Category Delete Confirm**, displays form confirming Category should be deleted:  
<img src="/static/testing/category-delete-confirm.png" width="800px" style="margin: 5px;">  

* **Footer Contact Developer Link**, links to **Contact Developer** form:  
<img src="/static/testing/contact-link.png" width="150px" style="margin: 5px;">  

* **Footer GitHub Link**, links to developer page on [GitHub](https://github.com/richardhenyash):  
<img src="/static/testing/github-link.png" width="40px" style="margin: 5px;">  

* **Contact Developer**, enables developer to be contacted by email:  
<img src="/static/testing/contact.png" width="300px" style="margin: 5px;">  

#### Features To Be Implemented In Future Development Phases ####
* Currently, when the user navigates back to the **Home** page from the **Product View** page, 
the previous search results are not displayed. Adding this functionality was investigated and
is likely to involve significant restructuring and re-testing of the python code. This feature 
is recommended to be implemented in a future development phase.

#### Design Changes During The Phase 1 Development ####
The following design changes were implemented following initial user feedback:
* The **Home** page alert was updated to include links to **Sign In** and **Register** 
if the user is not signed in:  
<img src="/static/testing/home-alert-new.png" width="700px" style="margin: 5px;">

* The **Home** page search button was updated to take up the space of the search and add buttons 
if the user is not signed in:  
<img src="/static/testing/search-new.png" width="700px" style="margin: 5px;">  
<img src="/static/testing/search-new-signedin.png" width="700px" style="margin: 5px;">

* The **Register** form was updated to include a link to **Sign In**:  
<img src="/static/testing/register-new.png" width="500px" style="margin: 5px;">  

* The **Product Add** route was updated to redirect to the **Product View** of the 
successfully added product.  

* The **Product View** form was updated to include an **Add Product** button:  
<img src="/static/testing/product-view-update-review-new.png" width="500px" style="margin: 5px;"> 

* The form validation for the **Product** form was updated to allow special characters 
(e.g. "&", "-" etc) in product names.

* Selection higlighting was turned off on the **Product View** form fields.

* Font sizes were increased slightly.

* Additional error checking was implemented.


### Responsive Styling ###
* The **Navigation Menu** is collapsible, and collapses to an icon on small devices less than 768 pixels wide. 
This is implemented using the [Bootstrap Navbar](https://getbootstrap.com/docs/5.0/components/navbar/) component.  
* The **Search Input**, **Category Selector**, **Search Button** and **Add Button** are responsively styled, 
and stack on small devices less than 768 pixels wide.  

See **Responsive Design** section in [TESTING.md](TESTING.md) for further information and [Responsive Testing](/static/testing/responsive) screen prints.

### Python Code Logic ###
The **Python Code** for the project has been split into the following modules, using the 
[Flask Blueprint](https://flask.palletsprojects.com/en/2.0.x/blueprints/) function:

* [Application](/app.py) - Flask routes and functions related to the **Flask Application** and **Error Handling**.
* [Allergens](/allergens.py) - Flask routes and functions related to **Allergens**.
* [Categories](/categories.py) - Flask routes and functions related to **Categories**.
* [Database](/database.py) - Functions related to the **Mongo Database**.
* [Environment](/database.py) - Environmental variables, imported when working locally in debug mode.
* [Forms](/forms.py) - [WTForms](https://wtforms.readthedocs.io/en/2.3.x/) form class definitions.
* [Mail](/mail.py) - Flask routes and functions related to sending an email via the **Contact Developer** form.
* [User Authentication](userauth.py) - Flask routes and functions related to **User Authentication**.

The high level code logic is explained in the [UML Diagrams](/static/wireframes/uml/) below: 

#### [Products](/static/wireframes/uml/products-logic.png) ####
<img src="/static/wireframes/uml/products-logic.png" width="800px" style="margin: 5px;">  

#### [Categories](/static/wireframes/uml/categories-logic.png) ####
<img src="/static/wireframes/uml/categories-logic.png" width="700px" style="margin: 5px;">  

#### [Allergens](/static/wireframes/uml/allergens-logic.png) ####
<img src="/static/wireframes/uml/allergens-logic.png" width="700px" style="margin: 5px;">  

#### [User Authentication](/static/wireframes/uml/userauth-logic.png) ####
<img src="/static/wireframes/uml/userauth-logic.png" width="700px" style="margin: 5px;">  

#### [Mail](/static/wireframes/uml/mail-logic.png) ####
<img src="/static/wireframes/uml/mail-logic.png" width="400px" style="margin: 5px;"> 

### Python Code Refactoring ###
After attending an online [Code Institute](https://codeinstitute.net/) seminar on [Python Classes](https://www.w3schools.com/python/python_classes.asp) 
given by [Ben Kavanagh](https://github.com/BAK2K3), consideration was given to re-factoring the code using an object orientated approach. 
A new [Class](https://github.com/richardhenyash/freefrom/tree/class) branch was created on in the 
[Project Code Repository Location](https://github.com/richardhenyash/freefrom). Classes and class methods were created in the 
**products**, **allergens**, **categories** and **userauth** python code modules. The class orientated approach was succesfully 
implemented as a test on the **Product View** route, which resulted in a significant simplification of the code. Unfortunately, 
due to time constaints, it was not possible to implement the object orientated approach across the project, but this should 
definitely be considered for a future project development phase, and as a better method of working for future
projects.

### Form Validation ###
Form validation is achieved in [Python](https://www.python.org/) using [WTForms](https://wtforms.readthedocs.io/en/2.3.x/). 
Custom **Form Classes** are defined within the [Forms](/forms.py) module for each required form. 
Additional custom validators have been imported from [wftorms-validators](https://pypi.org/project/wtforms-validators/) and implemented.
See below table for form validation implemented using WTForms:  

Form|Field|WTForms Field Type|Required|Minimum Length|Maximum Length|Notes
----|-----|------------------|--------|--------------|--------------|-----
Sign In|User Name|StringField|Yes|5|25|May only contain letters or numbers
Sign In|Password|PasswordField|Yes|5|25|
Register|User Name|StringField|Yes|5|25|Inherits field from Sign In form class
Register|Password|PasswordField|Yes|5|25|Inherits field from Sign In form class
Register|Email|PasswordField|Yes|5|None|Inherits field from Sign In form class
Register|Confirm Password|PasswordField|Yes|None|None|Must match Password
Contact|Name|StringField|Yes|3|100|May only contain letters or spaces
Contact|Email|StringField|Yes|5|None|
Contact|Message|TextAreaField|Yes|10|500|
Product Add|Name|StringField|Yes|3|50|
Product Add|Manufacturer|StringField|Yes|3|50|
Product Add|FreeFrom|StringField|No|None|None|Automatically populated from check boxes
Product Add|Review|TextAreaField|Yes|5|50|
Product Add|Rating|StringField|No|1|1|Automatically populated using JavaScript event handlers
Product View|Name|StringField|No|None|None|Read Only
Product View|Manufacturer|StringField|No|None|None|Read Only
Product View|FreeFrom|StringField|No|None|None|Read Only
Product View|Review|TextAreaField|Yes|5|250|
Product View|Rating|StringField|No|1|1|Automatically populated using JavaScript event handlers
Product Edit|Name|StringField|Yes|3|50|
Product Edit|Manufacturer|StringField|Yes|3|50|
Product Edit|FreeFrom|StringField|No|None|None|Automatically populated from check boxes
Allergen Add|Name|StringField|Yes|3|20|May only contain letters or spaces
Allergen Edit|Name|StringField|Yes|3|20|May only contain letters or spaces
Category Add|Name|StringField|Yes|3|30|May only contain letters or spaces
Category Edit|Name|StringField|Yes|3|30|May only contain letters or spaces

### JavaScript Code Logic ###
[JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) has been used to implement the following features:  

* Initialisation of [DataTables](https://datatables.net/), which are used to display the **Product** search results on the **Home** 
page and the **Reviews** on the **Product View** page in a searchable, sortable, paginated data table format using a plug in.

* Clickable **Rating** stars on the **Product View** and **Product Add** forms. When the star icons are clicked on the 
**Product View** and **Product Add** forms, a hidden form input with the id of "Rating" is updated to the correct "star" rating 
between 1 and 5 using the **JavaScript** on click event handlers defined in the [Events](/static/js/events.js) module.

* When the **Product View** form is ready, the hidden form input with id "Rating" is read and the **Rating** star icons 
are updated to reflect the correct rating value.

See [UML Diagram](/static/wireframes/uml/) below:  
<img src="/static/wireframes/uml/events-logic.png" width="300px" style="margin: 5px;">  

## Testing ##

Further testing information and screen prints can be found in [TESTING.md](TESTING.md).

## Deployment ##
The project has been developed using [Gitpod](https://www.Gitpod.io/) and [GitHub](https://github.com/). 
The project was regularly commited to [GitHub](https://github.com/) during the initial development phase.
The website resides as a repository in [GitHub](https://github.com/).and has been been deployed 
using [Heroku](https://dashboard.heroku.com/).

In order to make a fork or clone of the project, a [GitHub](https://www.Gitpod.io/) account is required. 
The [Gitpod Browser Extension](https://www.Gitpod.io/docs/browser-extension/) is also recommended.  

The project may be forked by following these steps:
* Go to the [Project Code Repository Location](https://github.com/richardhenyash/freefrom) on [GitHub](https://github.com/).
* In the top-right corner of the page, click "Fork".  

For further information on forking a [GitHub](https://github.com/) repository, 
see the [GitHub Documentation](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo).

The project may be cloned by following these steps:
* Go to the [Project Code Repository Location](https://github.com/richardhenyash/freefrom) on [GitHub](https://github.com/).
* Select the "Code" dropdown and choose "GitHub CLI" under "Clone". This will give you a URL that may be copied into the clipboard. 
* Open the Git Bash command line interface in [Gitpod](https://www.Gitpod.io/).
* Change the current working directory to the location where you would like the cloned directory to reside.
* Type git clone, and then paste the URL copied earlier, eg:  
$ git clone https://github.com/richardhenyash/balloon-pop-maths
* Press Enter to create the local clone.

The code may also be downloaded to a local computer by following these steps:
* Go to the [Project Code Repository Location](https://github.com/richardhenyash/freefrom) on [GitHub](https://github.com/).
* Select the "Code" dropdown and choose the "Download ZIP" option.
* This will download a copy of the entire project locally as a .zip file.  

For further information on cloning a [GitHub](https://github.com/) repository, see the [GitHub Documentation](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository).

The steps required to deploy the website to [Heroku](https://dashboard.heroku.com/) are as follows:
* Create a `requirements.txt` file using the terminal command `pip freeze > requirements.txt`.
* Create a `Procfile` with the terminal command `echo web: python app.py > Procfile`.
* git add and git commit the new `requirements.txt` and `Procfile` and then git push the project to GitHub.
* Create a new app on the Heroku website by clicking the "New" button in your dashboard. Give it a name and set the region to Europe.
* From the heroku dashboard of your newly created application, click on "Deploy" > "Deployment method" and select GitHub.
* Confirm the linking of the heroku app to the correct GitHub repository.
* In the heroku dashboard for the application, click on "Settings" > "Reveal Config Vars".
* Set the following config vars:
* To get your MONGO_URI read the MongoDB Atlas documentation here
* In the heroku dashboard, click "Deploy".
* In the "Manual Deployment" section of this page, made sure the master branch is selected and then click "Deploy Branch".
* The site is now successfully deployed.

## Credits ##

* [Vector Stock](https://www.vectorstock.com/) for the attractive dove logo.
* [DataTables](https://datatables.net/) for the brilliant tables plug in.
* [WTForms](https://wtforms.readthedocs.io/en/2.3.x/) for the excellent form validation library and 
[Crash Course](https://wtforms.readthedocs.io/en/2.3.x/crash_course/) which I followed to implement the **Form Validation**.
* [wftorms-validators](https://pypi.org/project/wtforms-validators/) for the awesome additional form validation library.
* My mentor [Reuben Ferrante](https://github.com/arex18) for the examples which helped me implement the **Form Validation** 
and [Flask Blueprints](https://flask.palletsprojects.com/en/2.0.x/blueprints/).
* [Google Fonts](https://fonts.google.com/) for the attractive fonts used on the site, which enabled me to get started quickly.
* [hex 2 rgba](http://hex2rgba.devoth.com/) for the hex to RGBA conversion tool.
* The excellent [Code Institute](https://codeinstitute.net/) course material which enabled me to succefully implement the project.
* [ColorSpace](https://mycolor.space/) for the colour ideas generated using the colour pallete generator.

## Acknowledgements ##

Many thanks to the following for help and inspiration during this project:
* My mentor [Reuben Ferrante](https://github.com/arex18) for helping to get me started off on the right footing and for the insightful
review and comments on the site.
* [Neringa Bickmore](https://github.com/neringabickmore) for your encouragement with my project idea.
* [Ben Kavanagh](https://github.com/BAK2K3) for the very helpful comments on the site and general 
 encouragement, and for the excellent online seminar on **Python Classes**.
* The [Code Institute](https://codeinstitute.net/) [slack](https://slack.com/intl/en-gb/) community, for all your encouragement and help.
