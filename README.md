# Background  
The web application I chose for my final project is a customer communication hub. This is a light weight clone from FrontApp (https://front.com). Front is a recent start-up company to successfully introduce a Customer Communication solution to the markets. I was inspired from its innovation. The application differentiated from the email clients and ticketing CRM systems. The former was built for one-to-one communication between individuals, and limited to one channel. The latter was built for transactions, not building relationships with customers.  
  
# Introduction  
This is a light weight customer communication hub web application, called "FrontPage". It was designed for a team to use to build customer relationships with every conversation in a human way. The application was implemented to synchronize with a real Gmail Account which acts like an actual company primary contact email address (such as [sales@company.com](mailto:sales@company.com) or [customerservice@company.com](mailto:customerservice@company.com)). All team members are the Users of the application. The application is the "frontpage" for all team members to manage the conversations with the customers. Each incoming email will be transformed as a Task in the application.  
  
# Application Features  
The two main functionalities of the application are the accountability and collaboration capability. I implemented below functions to achieve the goal:  
- Assignment  
-- Each task can easily be assigned to any team members (Users), or unassigned from previous assigned members  
- Drafted email  
-- Each member can draft a response email to a Task and save it. Other members can see the drafted email, edit it or save it afterwards.  
- Comment  
-- Members can comment (discuss) within each Task and its Draft in the same page before sending out the actual response to customer.  
   
# Distinctiveness  
- This application is a customer communication tool which is fundamentally different from all previous projects we implemented such as the e-commerce site, social network or old Pizza ordering project.  
- I specifiedly used both Class-based and function-based views to implement views as Python objects instead of functions. Which is significantly different from all my previous projects in which I purely used function-based views.  
- The primary content source was came from outside of the application. I noticed that the content sources from all previous projects were relied on users' created content, through Forms to capture user inputs for example. Which is easier than capturing (fetching) content from outside. This application was implemented to communicate with a real-world application (Gmail) through the APIs Google provided.  
- related_name argument is filled properly for OneToOne relationship between two tables.  
  
# Complexity  
- The application was implemented to use Gmail APIs to access the emails from a Gmail account ([customerservice.democompany@gmail.com](mailto:customerservice.democompany@gmail.com)). It largely increased the complexity of the application compared with to all previous projects. I achieved this task inside the backend of the application. I implemented a Python function to access those APIs, get and decode those data and present back to to Django views to save them into the database and present them to html template.  
- In order to achieve the better user experience, the application was implemented like a single page application. All the functionalities were achieved within one single page. There is actually only one html template (task_list.html), but to be reused multiple times.  
- In order to reuse the same html template and reduce duplicated codes, Class-based views inheritance was implemented.  
- Pagination was implemented.  
- The application was implemented the full cycle of a Task. From being received, to be assigned to a member, drafted reply, discussed and finally sent out as an email to the original requester. The email sending functionality was achieved by using Gmail APIs.  
  
# Lifecycle of a Task  
1. A task was created from an incoming email  
2. The task was showed in the left hand side's task list  
3. The task can be viewed, assigned to (or unassigned from) an individual member  
4. A draft reply will be created along with its own task  
5. All members can discuss/comment within a single page of the task and its draft  
6. The task's draft can be saved, viewed and edited by all the members  
7. The draft can be sent out as a reply to the original incoming email  
8. The task will be marked done once reply was sent  
  
# Files  
In addition to the standard static files like **javascript.js** for javascript codes, **styles.css** for CSS and standard Django files like **views**, **urls**, **models**, **forms** and **templates**, there is a **gmail.py** file to manage the connection to Google APIs for receiving and sending emails. **credentials.json** is the Google specified authentication credential file for accessing your own Gmail from this application. The credential.json can be generated under the Credentials Tab inside the Google Cloud API portal:  
[https://console.cloud.google.com/apis/](https://console.cloud.google.com/apis/?authuser=0)  
A new project has to be created for creating credential and accessing the APIs.  
**requirements.txt** was created for all the dependences  
  
# How to run the application  
1. Create a new Gmail account  
2. Create a new Project under ([https://console.cloud.google.com/](https://console.cloud.google.com/?authuser=0))  
3. Create credentials.json inside the created Project (under OAuth 2.0 Client IDs)  
4. Replace the frontpage/credentials.json with your own credentials.json file  
5. Delete the token.json file (in highest level of the project) (Once you run the application, your own token.json file will be created)  
6. Inside frontpage/gmail.py edit this variable with your own email address  
COMPANY_EMAIL = '[customerservice.democompany@gmail.com](mailto:customerservice.democompany@gmail.com)'  
7. Download all the dependences through frontpage/requirements.txt in your virtual environment  
8. Run the application under project folder (python manage.py runserver)
