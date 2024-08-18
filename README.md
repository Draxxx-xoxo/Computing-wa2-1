ACTIVITY HUB

- Inspiration
  
My inspiration for this project stemmed from my experiences with my CCA, Stageoworks. Over the months of involvement, I observed a significant challenge: information was dispersed across various platforms. For instance, reminders were communicated through WhatsApp, while schedules were maintained on Google Sheets, among other scattered locations. This fragmentation proved to be a considerable inconvenience, requiring members to navigate multiple sources to access necessary information and locate relevant links. Additionally, WhatsApp reminders were frequently overlooked or lost amidst a deluge of messages, leading to missed notifications and a general sense of disorganization.

Recognizing these issues, I conceived the idea of developing a centralized web portal designed to consolidate all essential resources and communications for CCA members. By integrating announcements, schedules, and other crucial information into a single, accessible platform, the portal aims to streamline processes, enhance efficiency, and ensure that no critical updates are overlooked. This solution not only addresses the current inefficiencies but also enhances overall coordination within the CCA, ultimately fostering a more organized and productive environment.

Furthermore, incorporating an admin page into the web portal significantly enhances its functionality and user experience. This dedicated administrative interface will allow both teachers and CCA EXCO leaders to manage and update all relevant content from a single, unified location. The ability to make real-time changes to schedules, reminders, and other critical information without the need to navigate multiple platforms streamlines the management process and reduces the risk of errors or outdated information.

The admin page also facilitates more efficient control over access and permissions. By utilizing a system of manageable and shareable passwords, administrators can easily grant or restrict access as needed. This centralized control ensures that only authorized individuals can make alterations, thereby maintaining the integrity and accuracy of the information. This approach not only simplifies the process of updating and sharing information but also enhances security and accountability, making it easier to coordinate and oversee the various aspects of the CCA's activities.

Additionally, I was motivated by a desire to build a more connected and supportive community within my CCA. I envisioned a platform where members could share encouraging and motivating messages with each other. By including this feature, I aimed to boost morale and enhance team spirit. 

In summary, I undertook this project to improve organization and communication within ASRJC and Stageworks, aiming to streamline information management, uplift CCA morale and enhance overall efficiency, to make a positive impact on the ASRJC community!

- What it does

Activity Hub is a comprehensive web application designed to enhance communication and streamline administrative tasks within CCAs, in this instance, Stageworks. Built with Flask, this application offers a user-friendly interface and a range of features to support effective management and engagement.

Key Features:
Home Page:

Message Board: A space where members can post and view motivational and encouraging messages. This helps foster a positive community spirit and keeps everyone connected.

Announcements:
View Announcements: Display important announcements categorized into homework, events, and reminders. This feature helps members stay informed about key updates and deadlines.

Attendance Management:
Track Attendance: View and manage attendance records, including the ability to mark students as present, absent, or on leave. The interface provides a clear view of attendance data and allows for easy updates.

Schedule Management:
View and Update Schedule: Access the current schedule with details on term, week, date, day, session, start and end times, and remarks. This feature helps in organizing and keeping track of scheduled activities.

Admin Dashboard:
Secure Login: Admins can log in using a secure password to access control features.
Manage Announcements: Add, edit, or delete announcements as needed.Their announcements are sorted into homeworks, reminders and events to their desire.
Student Management: Add or remove students from the attendance list.
Update Attendance Records: Add new dates to the attendance records and update student attendance statuses.
Manage Schedule: Add or remove schedule entries.
Change Password: Update the admin password to maintain security.
Clear Messages: Option to clear all messages from the message board for a fresh start.

Technical Aspects:
Password Management: Passwords are securely hashed using bcrypt and stored in a JSON file, ensuring robust security for administrative access.
Database Integration: Utilizes SQLite for efficient data storage and management, handling various aspects such as announcements, attendance, and schedules.
Dynamic Content: The app dynamically updates content based on user interactions, ensuring real-time reflection of changes and data.

- How it's built
  
Framework and Libraries:

Flask: The core web framework used to build the application, providing the infrastructure for handling web requests and rendering templates.
bcrypt: A library used for secure password hashing, ensuring that sensitive credentials are protected.
SQLite: Database Management

Purpose: SQLite is employed as the lightweight, serverless database system for managing the application's data. It provides an efficient way to store, query, and manipulate data without the need for a separate database server.
Schema and Tables:
Announcements: Stores announcements categorized by type (homework, event, reminder) with fields for unique IDs and announcement content.
Attendance: Tracks student attendance records, including fields for student IDs, names, classes, and dynamic date columns for recording attendance status.
Schedule: Contains scheduling information with details such as term, week, date, day, session, start and end times, and remarks.
Database Operations:
Query Execution: Functions like opendb are used to execute SELECT queries and retrieve data from the database.
Data Modification: Functions like editdb handle INSERT, UPDATE, and DELETE operations to modify records.
Schema Changes: Functions like addcolumn allow for the addition of new columns to tables as needed, such as adding new dates to the attendance table.
Row Deletion: The delete_rows_by_ids function manages the removal of specific records from tables based on given IDs.
Integration: SQLite is integrated seamlessly with Flask, allowing for real-time data management and updates directly through the application interface.
Core Functionalities:

Password Management: Implements secure password handling with bcrypt for hashing and verifying passwords, ensuring that credentials are protected.
Dynamic Content Management: Admins can manage announcements, attendance records, and schedules through an intuitive interface, with functionalities for adding, editing, or deleting data.
Token-Based Authentication:

Secure Access: Utilizes token-based authentication for managing admin access. A unique token is generated upon successful login and used to authenticate further administrative actions.
Token Management: Tokens are stored and validated to ensure only authorized users can access the admin functionalities. Tokens can be invalidated upon logout.
User Interface:

HTML Templates: Jinja2 templating is used to render dynamic content on web pages, including announcements, attendance records, and schedules.
Message Board: Features a public message board where users can post and view motivational messages to enhance community spirit.
Routes and Views:

Home Route (/): Displays the message board for users to post and view messages.
Announcements Route (/announcements): Shows categorized announcements retrieved from the database.
Attendance Route (/attendance): Manages and displays attendance records, with functionality for updating student statuses.
Schedule Route (/schedule): Presents the schedule data from the database.
Admin Route (/admin): Provides a secure login interface for administrators, with access controlled via token-based authentication.
Admin Dashboard (/admin/control): A comprehensive control panel for admins to manage announcements, students, attendance, and schedules.
Security Measures:

Authentication: Token-based authentication ensures secure access to administrative functions.
Password Protection: Admin passwords are securely hashed and stored to prevent unauthorized access.
File Management:

JSON Files: Used for storing hashed passwords and configuration settings.
Text Files: Used for storing and retrieving messages on the message board.

- Challenges encountered
  
Since I was pretty new to Flask and many of the technologies involved, I ran into several challenges while building the Activity Hub web app.

Here’s a rundown of what I encountered and how I tackled each issue!

Getting the Hang of Flask:

Challenge: I had never worked with Flask before, so setting up routes, handling requests, and rendering templates was all new to me. It felt a bit like trying to read a foreign language at first.
Solution: I practised for a long time and tried my upmost best to debug all my problems. The CS50 duck was rlly useful! There were many times where my webapp was not showing up properly. This was usually due to small  typo errors or wrong variable names. Even though these errors were minor, i had realised what a serious impact it could have on my webapp. I strived to be more careful and look clearly when i type.

Working with SQLite:
Challenge: I had no prior experience with databases or SQL, so creating tables, writing queries, and managing data was a bit confusing.
Solution: I was completely lost with SQL at first. It seemed far fetched for me to actually successfully use the SQL datebase. I comtemplated just sticking to my comfort zone like txt and csv files. However, diving deeper into the benifits of using an SQL database, i had realised that more pain equates to more gain. I had watched Youtube tutorials and also asked my helpful friends who were more knowledgable in SQL. Using SQL really improved the effeciency of of my information accessing and storing, definately integrating the data more seemlessly into my webapp.

Implementing Password Hashing with bcrypt:
Challenge: Password hashing was a completely new concept for me, and I wasn’t sure how to securely handle user passwords.
Solution: I checked out the bcrypt documentation and followed tutorials to learn how to hash and verify passwords. I practiced with basic examples to see how it all fit together.

Setting Up Token-Based Authentication:
Challenge:I wanted to make sure that only users that type in the correct password was allowed access to the site. However, I was unfamiliar with how token-based authentication worked, especially how to generate and manage tokens securely.
Solution: I looked up resources on tokens and JSON Web Tokens and used Python’s uuid library to generate tokens. I tested how to validate and manage these tokens within Flask.

Managing Dynamic Content:
Challenge: Handling dynamic content like announcements and attendance records was tricky, especially with updating and querying the database.
Solution: I learned how to handle form data and database interactions through Flask’s documentation. I created test cases to make sure that the data was being handled correctly. I also made sure that i had the correct format for my data, like using columns for my attendance dates and making sure column names were not similiar as it would cause it to crash.

Making It Visually appealing and user-friendly:
Challenge: With just basic HTML and CSS skills, making sure the app looked good and was easy to navigate was daunting
Solution: I used responsive design techniques. I had experimented with different input types as well as the styling options for each of them. I also planned a colour scheme and tried my best to stick to it. By making the insturctions and navigation pop, i ensured that the user experience would be an memorable one, and also prevent any errors.

Debugging and Testing:
Challenge: Debugging the app and making sure everything worked correctly was tough, especially since I was still learning.
Solution: I used Flask’s debugging tools and set the app to run in debug mode. Testing thoroughly and using browser developer tools helped me spot and fix issues.

Some key issues were:
1. Making sure that the list from the checkbox was equal to the id of the row i wanted to delete or add. I had to do alot of debugging and experimenting with values.
2. Making sure the token was usable and that the admin page was not accessible by users who just change the link of the page.
3. My rows were not showing up properly. The data was either wrong or at the wrong place. I had to edit my SQL queries and troubleshooted until the result was accurate.
4. For the attendance, column names had could not repeat and had a specific format. They did not allow "-" which was the format in the input type date. I had to debug this issues and change the format according and also revert it back when displaying it on the site.
   
- Accomplishments that I'm proud of

As someone new to web development, I’m really proud of pulling off a web app that I’m actually happy with. It wasn’t a walk in the park—creating this took a ton of time, late nights, hard work, and effort. There were definitely moments when I was tempted to give up and implement something less demanding. But I stuck with it and kept pushing through, even when it felt like I was hitting a wall.
I kept going and didn’t let myself back down, consulting my friends and the CS50 duck. Seeing the finished app made all that hard work feel worth it. I felt a huge sense of accomplishment, something I’ve never felt before. It was amazing to see that my efforts paid off and that I managed to step out of my comfort zone to achieve something meaningful. This experience not only enhanced my skills but also boosted my confidence in tackling unfamiliar projects.
  
- What I learned

Resilience: Sticking with the project through tough times taught me to keep going even when things got difficult.

Patience: I learned that good things take time and that it’s important to take things one step at a time.

Confidence: Completing the project boosted my self-esteem and showed me that I can learn new things and succeed.

Problem-Solving: Overcoming obstacles improved my ability to figure things out and trust my instincts.

Satisfaction of Achievement: Seeing the project come together gave me a deep sense of pride and accomplishment.

Enjoying the Journey: Despite the challenges, I learned to appreciate the process and find joy in reaching my goals.

- What's next for Activity Hub!

Even though Activity Hub now enables centralised information viewing, there are still lots of features that could be added.
For instance, for stageworks there could be
1. Script storing
2. Blocking generator
3. Member profiles
4. Skill practising
5. Set manager
6. Set planner
7. Prop tracker

In the future, if this project goes any further i would like to implement these for Stageoworks!
For these features i hope to gather opinions from teachers and CCA mates on their preference and adjust it to their liking:)
For now, Acitivity Hub is pretty usable for all CCAs which i think is a plus in terms of flexibility:)
