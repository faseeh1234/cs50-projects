Final Project // Muhammad Faseeh Jawed, Natalia Siwek & Abdullah Shahid Sial


This file serves as a documentation of our entire project, in the form of a user manual. While we've aimed to answer most questions regarding this project's functionality, if you have any other pertaining questions, feel free to reach out to any of the developers.


// Premise //

The whole premise of the webpage is to allow users to log in their exercises and track their performance over multiple weeks. This implementation ensures that users can register, input personal information and then implement their own style of exercises whilst tracking how their performance changes over a period of time. The webpage has some pre-developed features, such as typical exercises a user may enter as well as the muscle target groups they wanna enter, but they have an option to add new ones as well using the other option.


// How to run //

Download the zip file called final.zip provided. Run your personal codespace (either online or on your desktop) and drag and drop the final zip file on your codespace's explorer section. Once done, Then execute:

unzip final.zip

to create a folder called finance. You no longer need the ZIP file, so you can execute

rm final.zip

and respond with “y” followed by Enter at the prompt to remove the ZIP file you downloaded. Now type

cd final

followed by Enter to move yourself into (i.e., open) that directory. Your prompt should now resemble the below.

final/ $

Execute ls by itself, and you should see a few files and folders. If you run into any trouble, follow these same steps again and see if you can determine where you went wrong!

To run our program, type out flask run in the terminal and press enter. It should like something like below:

final/ $ flask run


Now, Command + click on the https link that shows up in your terminal window, amongst other things. This will open up a new tab that should load to present a landing page to our website.

// Website breakdown


On the upper left section, you will see two options: Log in & Register. As a first time user, click on Register. You will be prompted to type out your username and password, and then re-enter the password again. Please make sure that your password must contain an upperletter, a digit, and a special character and have at least 8 characters. The program will prompt an error page and remind you of this if you do not.

Once registered, you will be prompted to a personal info page. Here, please type in your gender, current height (best estimation) and weight in the fields provided. Then press the blue enter button. This completes the registration stage.

 This will prompt you to the original log in page, where you can type in your registered username and password to gain access to the website. Now, you will have the opportunity to enter your desired split. Don't worry, you can change this later too. Here, please type in the number of exercises you intend to do in your split for each muscle group. Make sure you are cognizant of any error messages that may pop up.

 After pressing enter, the new page (index) should have a list of the muscle groups as well as a dynamic progress percentage of your exercises. As and when you log in your work out exercises, this percentage bar will change depending on the exercises you enter. Click on any of the muscles, select an exercise of that muscle group, type in the maximum weight lifted as well as the iterations done. Then click add to update your records. If an exercise you performed is not on the list, you can also add an exercise below. Keep updating for every exercise you performed in a day and see your split progress through the percentages on the index page.

 On the index page, along the top left, you will find some additional links. The first is the tracker, which actually just takes you back to the index page from any other page. The history page logs all of your entered exercises and their data alongside the time stamp when you entered them. The update health info page also allows you to edit the weight you entered initially, when you registered. Finally, the See the Progress page allows you to see the graphical progress you've made for each exercise you performed logged with date on the x axis and weight used on the y axis. Please note that for the graph to give you effective information, you need to consistently log in your exercises over multiple days, since the website functionality is designed to accomodate for long-term progress, not short-term artifical one.

 Finally, the log out button on the far top-right allows you to log out! (lol)


 I absolutely love the GYM TRACKER WOOHOO, and you should too. Love you



Some Important Points:

1. The website tracks time with real-time data, not with any form of user entry.
2. The graphs are adaptive, and work very successfully over long periods of testing.
3. The tracker percentage ensures it accounts for exercise entered and reps listed for each muscle group.




