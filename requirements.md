## Functional Requirements
1. Sign Up (Thy)
2. Edit User Profile (Anthony)
3. Delete Account (Charles)
4. Login (CJ)
5. Logout (CJ)
6. Reset password(Charles)
7. Ability to Customize font sizes and text style (italic,underline,etc.) font color and highlight (Anthony)
8. Create a Note / Folder(Anthony)
9. Move notes into different categories/folders (Anthony)
10. Add a password protected folder (Charles)
11. Advance search items with regular expressions or filters by categories (Thy)
12. Favorite and unfavorite notes(Charles)
13. Save notes as, pdf, etc (Thy)
14. Delete notes  (CJ)


<using the syntax [](images/ui1.png) add images in a folder called images/ and place sketches of your webpages>

## Non-functional Requirements
1. Multilingual support
2. Only expected to work on Google Chrome

## Use Cases 
1. Use Case Name (Should match functional requirement name)
- **Pre-condition:** <can be a list or short description>
- **Trigger:** <can be a list or short description>
- **Primary Sequence:**
1. Ut enim ad minim veniam, quis nostrum e
2. Et sequi incidunt
3. Quis aute iure reprehenderit
4. ...
5. ...
6. ...
7. ...
8. ...
9. ...
10. <Try to stick to a max of 12 steps>
- **Primary Postconditions:** <can be a list or short description>
- **Alternate Sequence:** <you can have more than one alternate sequence to
describe multiple issues that may arise and their outcomes>
1. Ut enim ad minim veniam, quis nostrum e
2. Ut enim ad minim veniam, quis nostrum e
3. ...
- **Alternate Sequence <optional>:** <you can have more than one alternate sequence to describe multiple issues that may arise>

1. Sign Up (Thy)
- **Pre-condition:** The user is on the webpage
- **Trigger:** The user hit the sign up button
- **Primary Sequence:**
1. The system prompts the user to enter email address, username, password, and re-enter their password.
2. The user enters the email address, username, password, and validating password.
3. The system checks if the user entered the prompts correctly and sends a validation email.
4. The user checks their email for a validation code and enters the code.
5. The system validates the code and stores the account information on the database.
6. The system takes the user to the profile customization page. 
7. The system prompts the user to upload a profile picture, and enter their biography.
8. The user uploads their profile picture, enters their biography and then clicks the save button.
9. The system saves the profile to the database 
10. The system take the user to their homepage
- **Primary Postconditions:**
1. The user account is created and stored in the database
2. The user can log in this account anytime after the account is created
Alternate Sequence:
2. The user enter an invalid email address, missing any field or the passwords don’t match
- a. Display an error message
- b. Prompt the user to enter the information again
4. The user enter an incorrect validation code
- a. Display an error message
- b. Prompt the user to enter the information again 
	8. The user didn’t upload a profile picture or/ and enter their biography.
- a. The system uses the default profile picture and leaves the biography blank. The system save the profile to the database

2. Edit User Profile (Anthony)
- **Pre-condition:** The user is logged in
- **Trigger:** The user clicks the “edit profile” button in the profile page
- **Primary Sequence:**
1. The user makes changes to their biography or uploads a new profile
2. The user clicks the “Save Changes” button.
3. The system prompts the user with an “Are you sure?” message.
4. The user clicks confirm. 
- **Primary Postconditions:**
- The user’s profile is updated or it stays the same. 
- **Alternate Sequence:**
1. The user does not make any changes to their profile and clicks “Save Changes”
- a.The System displays a “No changes were made” message

7. Ability to Customize font sizes and text style (italic,underline,etc.) font color and highlight  (Anthony)
- **Pre-condition:** THe user is on one of their note pages
- **Trigger:** The user clicks the text size number, any of the text style buttons (bold, italic, underline), the text color button, or the text highlight button.
- **Primary Sequence:**
1. The user types in a different font size or adjusts the font style, color, or highlight.
2. The System adjusts the font size/style/color/highlight for the following text.
- **Primary Postconditions:**
- Any text typed from that point is the correct size, style, color, and has the correct highlight
- **Alternate Sequence:**
1. The user has highlighted a section of text and adjusts the font size/style/color/highlight after
- a. The font size/style/color/highlight applies to the section of text and to the text typed after that section.

8. Create a Note / Folder (Anthony)
- **Pre-condition:** The user is on their homepage.
- **Trigger:** The user clicks the new Note/Folder button.
- **Primary Sequence:**
1. The user clicks the new Note/Folder button.
2. The system prompts the user to enter a name.
3. The user enters a name and clicks the create button.
4. The system creates a new Note/Folder and displays it on the homepage
- **Primary Postconditions:**
-  A new Note/Folder is created with the name the user specified and is available to the user on the homepage. 
- **Alternate Sequence:**
3. The user does not enter a name and clicks the create button
- a. The Note/Folder is still created, but has the name "untitled"

9. Ability to move notes into different folder (Anthony)
- **Pre-condition:** The user is on their homepage
- **Trigger:** The user right clicks one of their notes and selects the “Move to folder” option.
- **Primary Sequence:**
1. The system prompts the user to select which folder they want to move the note to.
2. The user selects the folder.
3. The user clicks the “move” button
4. The system moves the note to the corresponding folder
- **Primary Postconditions:**
- The folder is in the correct location and the user is brought to the default homepage.
- **Alternate Sequence:**
1. The user clicks the exit button at any point in the process.
- a. The user is brought back to the hompage




