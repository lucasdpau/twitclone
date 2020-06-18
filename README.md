# Twitclone
This is a Twitter clone I built for practice and learning, using Django, Javascript, and SQL.

Twitclone is hosted at http://lp-twitclone.herokuapp.com 

If you don't want to register, just login with the test account:
username: test password: test

### Functionality:
* Create a customized profile for yourself, including biography, location and a selection of profile pictures.
* Write, delete, like and 'retweet' posts.
* Add hashtags to your posts, and browse other posts based on their hashtags.
* View posts of other users that you have followed.


### Development:
Creating this Twitter clone was quite the journey, especially because I had never used Twitter before. I eventually made a Twitter account to do some research, but in the beginning I didn't even know what a retweet was. I did know that people made small posts iwth a 140 character limit though, so I started there.

The beginning took a while because I was coming from Flask and I had to get used to how Django did things. One thing I quickly appreciated was the way Django handles databases with their Models system. Having Django migrate changes to the database was a lot easier than making the changes manually in Flask. I would later be even more thankful as this made it easy for me to switch from using SQLite to Postgres when deploying to Heroku. 

After I implemented the ability to post Tweets, I decided to add the ability to delete them. I realized that I needed a layer of authentication here, because I didn't want the wrong user to be able to delete another user's post just by visiting the correct URL.

I eventually ran into a large roadblock, where I was unable to 'attach' extra data, such as biography or a follow list, to Django's built-in User model. I wanted to keep using the built in model as it already had authentication among other features included, and I wasn't sure how to append another custom model to this. After taking a few weeks away from the project I eventually stumbled upon a solution that allowed the program to update both the User and the added "profile" information together.

Once I got profiles working I decided to add profile pictures. However, I did not want to deal with the headache that is content moderation, so I did not allow users to uppload their own pictures. I instead provided simple geometric shapes that the user could choose from, so I could prove that I could implement this feature if I truly wanted to. 
