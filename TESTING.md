# FreeFrom - Testing #

## Contents ##
- [Automated Testing](#automated-testing)
    - [HTML](#html)
    - [Custom CSS Styling](#custom-css-styling)
    - [JavaScript Code Testing](#javascript-code-testing)
    - [Python Code Testing](#python-code-testing)
    - [Automated Performance And Quality Testing](#automated-performance-and-quality-testing)
- [User Stories Testing](#user-stories-testing)
- [Additional UX Testing](#additional-ux-testing)
- [Manual Testing](#manual-testing)
    - [Responsive Design](#responsive-design)
    - [Browser Compatibility Testing](#browser-compatibility-testing)
- [Bugs Fixed During Testing](#bugs-fixed-during-testing)
- [Bugs Remaining](#bugs-remaining)

## Automated Testing ##

### HTML ###
All **HTML** code was validated using the [W3C Markup Validation Service](https://validator.w3.org/) 
regularly during the development process. **The HTML Source Code** was regularly viewed for each page 
using **Google Chrome** (right click, *View page source*) and passed through the 
[W3C Markup Validation Service](https://validator.w3.org/). 

The following error was found during the final **HTML** validation check:
* A stray closing *i* tag was found in the **Product View** template. This was removed, the HTML was revalidated and passed.

All HTML code now passes validation with no error or warnings. See [HTML Validation Reports](/static/testing/validation/html)

### Custom CSS Styling ###
[Custom CSS styling](./assets/css/style.css) was validated using the [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/).  
No errors were generated. 10 "unknown vendor extension" warnings were generated. See [CSS Validation Report](/static/testing/validation/css/css-validation.pdf).  
The warnings are related to the 10 global variables declared at the top of the [Custom CSS](/static/css/style.css). 
The warnings are generated because the [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/) 
does not currently support CSS global variable declaration are are not considered to be an issue. 
See [Github Link](https://github.com/w3c/css-validator/pull/173).

### JavaScript Code Testing ##
The [JavaScript Event Handler Module](/static/js/events.js) was validated using the 
[JSHint](https://jshint.com/about/) static code analysis tool, and passed without errors or warnings.
See [JavaScript Event Handler Module Validation](/static/testing/js/events-jshint-validation.pdf). 
Due to the lack of complexity of **JavaScript** code implemented on the project, **Automated Unit Testing** 
of the **JavaScript** code was considered unecessary. All **JavaScript** event handlers in the event 
handler module have been thoroughly manually tested as part of the [Manual Testing](#manual-testing) process.

### Python Code Testing ##
All **Python Code** was thoroughly tested at the command line during the development process, and has been validated 
using [Flake 8](https://pypi.org/project/flake8/).  

One F401 error was generated on the [Application Python module](/app.py) file concerning the *env* module being 
imported but not used. This is not considered to be a problem as *env* is only being imported in the testing 
environment to initialise the environmental variables, and is not imported in the production version of 
the site. See [Python Code Flake8 Validation](/static/testing/validation/python/python-flake8-validation.png).

### Automated Performance And Quality Testing ###
Performance and Quality was tested with the [Lighthouse](https://chrome.google.com/webstore/detail/lighthouse/blipmdconlkpinefehnmjammfjpmpbjk?hl=en) 
extension for [Google Chrome](https://www.google.com/intl/en_uk/chrome/). 

Initial [Lighthouse](https://chrome.google.com/webstore/detail/lighthouse/blipmdconlkpinefehnmjammfjpmpbjk?hl=en) scores were:
* **Performance** 84%
* **Accessibility** 90%
* **Best Practices** 93%
* **SEO** 94%  
See [Initial Lighthouse Report](/static/testing/validation/performance/lighthouse-report-1.pdf).

To improve **Accesibility**, the *name* and *aria-label* atttributes were added to the **Search** and **Add** 
buttons as required on the **Home** page.

To improve **Best Practices** and **Performance**, the [FreeFrom logo](/static/testing/logo.png) was re-sized to 
94px x 100px and compressed using the [GIMP](https://www.gimp.org/) and [RIOT](https://riot-optimizer.com/) 
image manipulation and optimisation tools.

Final [Lighthouse](https://chrome.google.com/webstore/detail/lighthouse/blipmdconlkpinefehnmjammfjpmpbjk?hl=en) scores were:
* **Performance** 86%
* **Accessibility** 98%
* **Best Practices** 100%
* **SEO** 94%  
See [Final Lighthouse Report](/static/testing/validation/performance/lighthouse-report-2.pdf).

## User Stories Testing ###
* ***As a User, I would like to be able to register on the site.***  
The user is able to **Register** on the site using the **Register** form, which can be accessed from **Home Page Alert Links** 
or from the **Sign In** form. Once the **Register** form has been populated and the **Form Validation** and checking has been 
passed, the user is registered on the database, redirected back to the **Home** page, and notified with a message 
at the top of the screen. The **Home Page Alert** is updated to remove the **Sign In** and **Register** links and shows the 
**User Name** of the signed in user. The **Navigation Menu** shows a link to **Sign Out**:  

<img src="/static/testing/user-stories/home-signedout.png" width="600px" style="margin: 5px; border=1px solid black">

<img src="/static/testing/user-stories/register.png" width="400px" style="margin: 5px; border=1px solid black">  

<img src="/static/testing/user-stories/home-signedin.png" width="600px" style="margin: 5px; border=1px solid black">  

* ***As a User, I would like to be able to sign in to the site.***  
The user is able to **Sign In** to the site using the **Sign In** form which can be accessed from **Home Page Alert Links** 
or from the **Sign In** link on the **Navigation Menu**. The **Sign In** form also has a link to the **Register** form. 
Once the **Sign In** form has been populated and the **Form Validation** and checking has been passed, the user is signed in, 
redirected back to the **Home** page, and notified with a message at the top of the screen. 
The **Home Page Alert** is updated to remove the **Sign In** and **Register** links and shows the 
**User Name** of the signed in user. The **Navigation Menu** shows a link to **Sign Out**:  
<img src="/static/testing/user-stories/home-signedout.png" width="600px" style="margin: 5px;">  
<img src="/static/testing/user-stories/signin.png" width="400px" style="margin: 5px;">  
<img src="/static/testing/user-stories/home-signedin.png" width="600px" style="margin: 5px;">  

* ***As a User, I would like to be able to sign out of the site.***  
If the user is **Signed In**, the **Navigation Menu** shows a link to **Sign Out**. If the link is clicked, the user 
is redirected back to the **Home** page and notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/navigation-menu-signedout.png" width="600px" style="margin: 5px;">  
<img src="/static/testing/user-stories/signout-success.png" width="150px" style="margin: 5px;">  

* ***As a User, I am searching for a product which is free from one or more allergens.***  
The user is able to optionally type part or all of a **Product** name into the **Search** input and 
may also optionally select the **Category** and **Allergens** to **Search** based on. Products are 
returned into the product list below. Each product can be viewed in more detail by clicking on 
the **Product Name Link** in the **Product Results Table**.
The **Search** also works if no details are input (all products are returned into the product list). 
Screen prints showing the results of various typical product searches are shown below:  
<img src="/static/testing/user-stories/product-search-1.png" width="600px" style="margin: 5px;">  
<img src="/static/testing/user-stories/product-search-2.png" width="600px" style="margin: 5px;">  
<img src="/static/testing/user-stories/product-search-3.png" width="600px" style="margin: 5px;">  
<img src="/static/testing/user-stories/product-search-4.png" width="600px" style="margin: 5px;">  
<img src="/static/testing/user-stories/product-search-5.png" width="600px" style="margin: 5px;">  
<img src="/static/testing/user-stories/product-search-6.png" width="600px" style="margin: 5px;">  
<img src="/static/testing/user-stories/product-search-7.png" width="600px" style="margin: 5px;">  
<img src="/static/testing/user-stories/product-search-8.png" width="600px" style="margin: 5px;">  

* ***As a User, I have found a product which is free from one or more allergens, and I want to add it to the database.***  
If the user is **Signed In**, they may add a product to the database using the **Add** button on the **Home** page. 
Once the **Form Validation** and checking has been passed, the new **Product** is added to the database and the user is redirected 
to the **Product View** page, and notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/product-add.png" width="400px" style="margin: 5px;">  
<img src="/static/testing/user-stories/product-add-success.png" width="400px" style="margin: 5px;">  

* ***As a User, I have tried a product and would like to rate it.***  
* ***As a User, I have tried a product and would like to review it.***  
If the user is **Signed In**, they may rate and review products on the **Product View** page. 
Once the **Form Validation** and checking has been passed and the review and rating has been 
succesfully added, the user is notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/product-rate-review.png" width="400px" style="margin: 5px;">  
<img src="/static/testing/user-stories/product-rate-review-success.png" width="400px" style="margin: 5px;">  

* ***As a User, I would like to edit an existing product.***
If the user is **Signed In**, they may **Edit** a product by clicking the **Edit Product** button from the **Product View** 
page. The **Product Edit** form is presented, and once the **Form Validation** and checking has been passed and the product has been 
successfully updated, the user is redirected to the **Product View** page for the updated **Product**, 
and is notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/product-edit.png" width="400px" style="margin: 5px;">   
<img src="/static/testing/user-stories/product-edit-success.png" width="400px" style="margin: 5px;">  

* ***As a User, I would like to delete an existing product.***
If the user is **Signed In**, they may **Delete** a product that they have added. If the user is **Signed In** with **Admin** 
privileges, they may **Delete** any product from the database. The **Product Delete** feature is accessed from the **Product Edit** form, 
using the **Delete** button. If the **Delete** button is clicked, the user is asked to confirm that they want to **Delete** the **Product**. 
If the user clicks **Cancel**, they are redirected back to the **Product Edit** form. If the user clicks **Delete**, the product is 
deleted from the database and the user is redirected to the **Home** page and notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/product-delete.png" width="400px" style="margin: 5px;">  
<img src="/static/testing/user-stories/product-delete-confirm.png" width="400px" style="margin: 5px;">  
<img src="/static/testing/user-stories/product-delete-success.png" width="200px" style="margin: 5px;">  

* ***As a User, I would like to add a new product category.***
If the user is **Signed In** and has **Admin** privileges, the **Categories** menu is shown in the **Navigation Menu**. 
The user can pick **Add Category** from the **Categories Menu** and populate the new **Category** name in the form input. 
Once the form has passed **Form Validation** and checking and the new **Category** has been succesfully added, 
the user is redirected to the **Home** page and is notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/category-add.png" width="300px" style="margin: 5px;">  
<img src="/static/testing/user-stories/category-add-success.png" width="200px" style="margin: 5px;">  

* ***As a User, I would like to edit an existing product category.***
If the user is **Signed In** and has **Admin** privileges, the **Categories** menu is shown in the **Navigation Menu**. 
The user can pick **Edit Category** from the **Categories Menu**, pick the **Category** to edit from the **Category Selector**
and populate the new **Category** name in the form input. 
Once the form has passed **Form Validation** and checking and the **Category** has been succesfully edited, 
the user is redirected to the **Home** page and is notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/category-edit.png" width="300px" style="margin: 5px;">  
<img src="/static/testing/user-stories/category-edit-success.png" width="200px" style="margin: 5px;">  

* ***As a User, I would like to delete an existing product category.***
If the user is **Signed In** and has **Admin** privileges, the **Categories** menu is shown in the **Navigation Menu**. 
The user can pick **Delete Category** from the **Categories Menu**, and pick the **Category** name to delete from the 
**Category Selector**. If the **Delete** button is clicked, the user is asked to confirm that they want to **Delete** the **Category**. 
If the user clicks **Cancel**, they are redirected back to the **Category Delete** form. If the user clicks **Delete**, the **Category** is 
deleted from the database, the user is redirected to the **Home** page and is notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/category-delete.png" width="400px" style="margin: 5px;">  
<img src="/static/testing/user-stories/category-delete-confirm.png" width="400px" style="margin: 5px;">  
<img src="/static/testing/user-stories/category-delete-success.png" width="200px" style="margin: 5px;">  

* ***As a User, I would like to add a new allergen.***  
If the user is **Signed In** and has **Admin** privileges, the **Allergens** menu is shown in the **Navigation Menu**. 
The user can pick **Add Allergen** from the **Allergens Menu** and populate the new **Allergen** name in the form input. 
Once the form has passed **Form Validation** and checking and the new **Allergen** has been added, the user is redirected to the 
**Home** page and is notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/allergen-add.png" width="300px" style="margin: 5px;">  
<img src="/static/testing/user-stories/allergen-add-success.png" width="200px" style="margin: 5px;">  

* ***As a User, I would like to edit an existing allergen.***
If the user is **Signed In** and has **Admin** privileges, the **Allergens** menu is shown in the **Navigation Menu**. 
The user can pick **Edit Allergen** from the **Allergen Menu**, pick the **Allergen** to edit from the **Allergen Seelctor**  
and populate the new **Allergen** name in the form input. 
Once the form has passed **Form Validation** and checking and the **Allergen** has been succesfully edited, the user is notified with a message 
at the top of the screen:  
<img src="/static/testing/user-stories/allergen-edit.png" width="300px" style="margin: 5px;">  
<img src="/static/testing/user-stories/allergen-edit-success.png" width="200px" style="margin: 5px;">  

* ***As a User, I would like to delete an existing allergen.***
If the user is **Signed In** and has **Admin** privileges, the **Allergens** menu is shown in the **Navigation Menu**. 
The user can pick **Delete Allergen** from the **Allergens Menu**, and pick the **Allergen** name to delete from the 
**Allergen Selector**. If the **Delete** button is clicked, the user is asked to confirm that they want to **Delete** the **Allergen**. 
If the user clicks **Cancel**, they are redirected back to the **Allergen Delete** form. If the user clicks **Delete**, the **Allergen** is 
deleted from the database and the user is notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/allergen-delete.png" width="400px" style="margin: 5px;">  
<img src="/static/testing/user-stories/allergen-delete-confirm.png" width="400px" style="margin: 5px;">  
<img src="/static/testing/user-stories/allergen-delete-success.png" width="200px" style="margin: 5px;">  

* ***As a User, I would like to be able to contact the developer.***   
The user may access the **Contact Form** from the **Footer Link**. If the user is **Signed In**, their email address is populated 
automatically. Once the user has populated the **Contact Form** and the form has passed **Form Validation** and checking and has 
been succesfully submitted, a message is displayed at the top of the screen:  
<img src="/static/testing/user-stories/contact-developer.png" width="300px" style="margin: 5px;">  
<img src="/static/testing/user-stories/contact-developer-success.png" width="200px" style="margin: 5px;">  
<img src="/static/testing/user-stories/contact-developer-email.png" width="300px" style="margin: 5px;">  

