# Introduction
## The main idea for this project was that each user can maintain his diet diary so as to analyze his/her diet. On the main page via an API all the food items that are present on the company's website will be displayed as shown below:


## Logging In
![Admin Page](./assets/admin_page.png)  

On clicking the “Admin Login” button, admin_page() function is called and it renders the admin_login.html file; redirects to Admin Login page.

![Admin Login](./assets/admin_login.png)  

On clicking the “Login” button, admin_login() function is called. If the Admin Id or Password is wrong, an error message is shown: “Invalid Admin or Password”; if the data is correct, it renders the fm_table.html file.

---
## Data Manipulation
![Food master table](./assets/food_master_table.png)  

After successful login to admin page, the food master table appears which contains data fetched from MySQL central database.

#### Adding
![Adding](./assets/adding.png)  

When “Add New Food” is clicked on Food Master Table, this webpage is shown. Several input fields are shown.  

#### Batch Upload
![CSV Batch Upload](./assets/csv_batch_upload.png)  

When “Add New CSV File” is clicked on Food Master Table, this webpage is shown. Several input fields are shown.

#### Updating
![Updating](./assets/updating.png)  

When “Edit” is clicked on Food Master Table, this webpage is shown by rendering update_form.html. Several input fields are shown.
All the fields which are allowed to modify can be modified from here.

---
## Analysis
![Analysis](./assets/analysis.png)  

Redirects to the User Food Log Charts.
The webpage has date inputs which shows calories consumption from dates recorded in database.

![Interval Analysis 1](./assets/interval_analysis_1.png)
![Interval Analysis 2](./assets/interval_analysis_2.png)  
_Interval Anlaysis_  

![Daily Analysis](./assets/daily_analysis.png)  
_Daily Analysis_  

#### Datewise

![Datewise Analysis](./assets/datewise_analysis.png)  

Userfoodlogchart() accepts input from “Select From Date”, “Select To Date” and “Select Meal Type”; when “Submit” button is pressed, a line graph is shown representing the calories consumption between the selected date range and selected meal type. Comparison with average calorie consumption for men and women is also shown.

---
## Comparing
#### Consumption
![Consume Comparison](./assets/consume_comparison.png)  
_Accessing_  
![Consume Comparison Charts](./assets/consume_comparison_charts.png)  
_Charts_  

Redirects to the Consume Comparison page.
This page shows 2 analysis graphs. First graph is a pie-chart which shows distribution of quantities of nutrients consumed in present day. Second graph is a line chart which shows various line graphs.

#### Purchase
![Purchase Comparison](purchase_comparison.png)  
_Accessing_  
![Purchase Comparison Charts 1](./assets/purchase_comparison_charts_1.png)  
![Purchase Comparison Charts 2](./assets/purchase_comparison_charts_2.png)  
_Charts_  

When Purchase Comparison is clicked, it calls the purchaseComparison() function which renders the purchaseComparison.html file and redirects to Purchase Comparison page. This page has 3 graphs:
1. Pie-chart that shows nutrient wise distribution of food items purchased today.
2. Pie-chart that shows nutrient based distribution of food items purchased in last 7 recorded days.
3. A bar graph that shows comparison b/w User Intake, Overall Intake and Average Intake of nutrients for that particular day. 
---
## Pancare
#### Adding manually
![Adding Manually Pancare](./assets/adding_manually_pancare.png)  

On filling the above fields. And clicking the Submit button, function Adds individual food to Pan-care

#### Batch upload
![Batch Upload Pancare](./assets/batch_upload_pancare.png)  

On clicking the Submit button, function batch uploads food to Pan-care

---
## Purchases
![Purchases Table](./assets/purchases_table.png)  
_Purchases Table_  

#### Adding
![Adding to Purchases Table](./assets/adding_to_purchases_table.png)  
Redirects to a form to add food to purchase table.  
![Updating Purchases Table](./assets/updating_purchases_table.png)  
Redirects to a form to update food items in purchase table,
