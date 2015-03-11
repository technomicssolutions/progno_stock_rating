progno_stock_rating Technical documentation
===================


Technologies

1. Django 1.5:
	A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
2. psycopg2:
	Psycopg is the most popular PostgreSQL adapter for the Python programming language. At its core it fully implements the Python DB API 2.0 specifications
3. South 0.7.4:
	South is a tool to provide consistent, easy-to-use and database-agnostic migrations for Django applications.
4. simplejson 3.5.3:
	simplejson is a simple, fast, complete, correct and extensible JSON encoder and decoder for Python 2.5+ and Python 3.3+. It is pure Python code with no dependencies, but includes an optional C extension for a serious speed boost.

5. xlrd 0.9.3:
	Library for developers to extract data from Microsoft Excel (tm) spreadsheet files
6. django-jsonfield 0.9.13:
	django-jsonfield is a reusable Django field that allows you to store validated JSON in your model.
	
7. django-recaptcha:
	django-recaptcha uses a modified version of the Python reCAPTCHA client which is included in the package as client.py.

8. django-social-auth 0.7.28:
	Django Social Auth is an easy way to setup social authentication/authorization
mechanism for Django projects.
9. lxml 3.3.6:
	Powerful and Pythonic XML processing library combining libxml2/libxslt with the ElementTree API.


Modules

1. public 
2. web 


PUBLIC
	This module is for public user functionalities.
1.models

PublicUser : Table keeps the information about public users including facebook details

WatchList :  Information about companies which is added to watchlist by users

Compare list : Information about companies which is added to comparelist by users

Company price value : keeps the record of BSE and NSE price values of each company

Help : Queries of users are stored in this table

Token : Model for token verification of user signup

2.views
Home : this view performs user authentication.It checks whether the user is a public user or admin user. If it is a public user redirect into home page of public user else redirect into admin's home page.

Login: Authentication view

ActivateAccount :  For activate the account.checks  whether the activation link send as email is valid or not.if it is a valid link then activate the user account else give a message “activation link is invalid”

VerifyRecaptcha : verify the recaptcha provided in the signup form.

Signup : Signup view

Logout: Logut view

StarRating : Starrating calculation view

StarRatingReport : Starrating display view

AddToWatchlist: add companies to watchlist.

ViewWatchList : list companies which is added ino watchlist

AddToComparelist : add companies to compare list.user can add maximum 4 stocks in compare list

ChangeCompareList : change the companies in the compare list 

ViewCompareList : list companies which is added to compare list

DeleteFromCompareList :delete company from compare list

SearchCompany : search companies by name and ISIN

SearchResult : list the result of search

HelpView : submit help form to database and send an alert message to admin about the help request from the user.

Disclaimer: Disclaimer document display

PrivacyPolicy: Privacy Policy document display

TermsOfUse : Terms of use document display

ForgotPassword: Forgot password view

ResetPassword: Reset password view

WEB
      this module is for progno admin functionalities
      
1.database models

Date: common model for date.

UserPermission: inherited from Date model.it contains the informations about user permissions

AnalyticalHead :inherited from Date model.it contains informations about analytical heads

DataField : inherited from Date model.It contains the datafields defined by admin

DataFile : inherited from Data model. Keeps the record of files which is uploaded by admin

FieldMap : contains data field and file field.this is for mapping the data field and file field.

Operator : contains various operators.

Formula : contains various formulas created using operators.

Function : contains various functions.functions are parameters of analytical heads.

ContinuityFunction : inherited from Function model.

ConsistencyFunction : inherited from Function model.

Industry : contains the details of industries

CompanyFile :keeps record of company files uploaded by admin

Company :contains informations about companies

ParameterLimit : Strong point,weak point like parameter features of functions are stored here.

StarRating : keeps star rating informations

CompanyFunctionScore : contains function score and functions of companies.

CompanyModelFunctionPoint : contains function point details

CompanyModelScore : contains modelscore and star ratinginformations of companies.

CompanyStockData : stores stockdata of companies.

NSEPrice : contains the NSE price value of companies

BSEPrice : contains the BSE price value of companies

2.views

Dashboard: Progno admin dashboard view

Administration: Administartion settings view

FieldsWithMapping: Returns fieldMap objects which are already mapped with DataField object.

FieldSettings : Returns informations in the Datafield Model and add new data to the DataField model.

FunctionSettings: Returns informations in the Function Model and add new data to the Function model.

Companies: list all informations in CompanyFile model and add new data to it.

DataUpload: List all datafiles and save and process the datafile object while uploading new file

FieldMapping: perform mapping between Datafield and FileField objects and save the results

Model : Rating model creation and display view

Login: Authentication view

Logout: logout view

Users : List all users

IndustryDetails : list the informations of industries saved in database

SaveUser : save user informations in database.

GeneralFunctions : returns general function details

ContinuityFunctions : returns continuity function details

ConsistencyFunctions : returns consistency function details

DeleteField : Delete DataField object

DeleteHead : Delete AnalyticalHead object

DeleteModel : Delete AnalysisModel object

DeleteUser : Delete  User.

DeleteParameter : Delete ParameterLimit object and its corresponding CompanyModelFunctionPoint object also deleted.

DeleteRating : delete StarRating object

ResetPassword: Reset password view

OperatorsView : List all operators in the database

DeleteFunction: Deleting Function

DeleteDataFile : Delete DataFile object

CompanyModelStarRating: Calculate star rating of companies.

SaveModelStarRating: save star rating to database.

RatingXML: export star rating report to an xml file.


