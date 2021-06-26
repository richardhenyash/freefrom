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
All **Python Code** has been validated using [Flake 8](https://pypi.org/project/flake8/). 
One F401 error is generated on the [Application Python module](/app.py) file concerning the env module being 
imported but not used. This is not considered to be a problem as env is only being imported in the testing 
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
buttons as required on the **Home** page, and the **Alert Link** colour was changed to white and the links underlined.

To improve **Best Practices** and **Performance**, the [FreeFrom logo](/static/testing/logo.png) was re-sized to 
94px x 100px and compressed using the [GIMP](https://www.gimp.org/) and [RIOT](https://riot-optimizer.com/) 
image manipulation and optimisation tools.

Final [Lighthouse](https://chrome.google.com/webstore/detail/lighthouse/blipmdconlkpinefehnmjammfjpmpbjk?hl=en) scores are:
* **Performance** 86%
* **Accessibility** 98%
* **Best Practices** 100%
* **SEO** 94%
See [Final Lighthouse Report](/static/testing/validation/performance/lighthouse-report-2.pdf).