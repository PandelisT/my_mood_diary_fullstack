# My Mood Diary Full Stack Application

The purpose of this application is to track the thoughts, problem areas and skills for clients who see a psychologist for various issues. The range of issues can include mental health, drug and alcohol addictions, food disorders etc. This application will allow the users (clients) to journal their thoughts and track their problem areas and skills in conjunction with a psychologist who will assist in the implementation of the app for their clients.

Behavioural activation is engaging in positive activities to boost mood. This is a therapeutic strategy for treating depression. Part of this strategy needs you to monitor your daily activities and systematically schedule in activities throughout your day. For more information: https://www.psychologytools.com/self-help/behavioral-activation/

Thoughts, emotions and behaviours are all intertwined whereby negative thoughts can trigger negative behaviours. A more holistic approach is usually implemented by tracking these three areas i.e. negative thoughts, general mood ratings and problem behaviours.

Tracking mood, thoughts and behaviours has been shown to increase insight, motivation and willingness to change. Skills are designed at the individual level to replace the negative moods, thoughts and behaviours. 

The journal entries are for clients to track mood, thoughts and behaviours. A psychologist with the client then analyses these entries, identifies problem areas and then creates skills to combat these problem areas. A more complete example can be found in the user stories and personas.

**\- Functionality / features**

User authentication
Mood tracking through journal entries (CRUD resources for adding/updating/deleting/reading journal entries)
Problem area tracking  (CRUD resources for adding/updating/deleting/reading problem areas)
Skills tracking (CRUD resources for adding/updating/deleting/reading skills)
Adding psychologist details

**\- Target audience**

The target audience is clients who see a psychologist for any issue from addiction to mental health issues. It can also be used as a too for psychologists to help treat their clients more effectively.

**\- Tech stack**

My tech stack includes:

PostgreSQL database in AWS RDS
Python Flask with Jinja2 templates
HTML/CSS in Jinja2 templates
AWS ECS and ECR for deployment
Docker to create images of Flask App