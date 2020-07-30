import praw
import pdb
import re
import os
import time

start = time.time()

# The bot config to use from praw.ini
reddit = praw.Reddit('bot1')
# The subreddits to scan
# if multiple, text would be all one stringg with each subreddit separated by + eg: "all+test"
subreddit = reddit.subreddit("ShadowWesley77")
# Put the name of the bot here!
ignore = str(reddit.redditor('ShadowWesley77'))
# The text we are looking for and the regex to find the ID
searchtext = "https://cdn.modulargrid.net/img/racks/modulargrid_"
regexfindid = 'https:\/\/cdn\.modulargrid\.net\/img\/racks\/modulargrid_([0-9]+)\.jpg'

# The two parts of the comment
botcomment = """You posted a link to your ModularGrid rack image. The link to the actual rack is more helpful in
                    providing advice as it allows users to see a module's function without having seen it before.
                    \n\nHere's the link to the actual rack: https://www.modulargrid.net/e/racks/view/"""

botcommentpart2 = """
    \n\nI'm a bot. If I've made a mistake, click [here.]
                    (https://www.reddit.com/message/compose?to=shadowwesley77)
"""

# Open our comments/posts replied to text files or create them if they don't exist
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
       posts_replied_to = f.read()
       posts_replied_to = posts_replied_to.split("\n")
       posts_replied_to = list(filter(None, posts_replied_to))

if not os.path.isfile("comments_replied_to.txt"):
    comments_replied_to = []
else:
    with open("comments_replied_to.txt", "r") as t:
       comments_replied_to = t.read()
       comments_replied_to = comments_replied_to.split("\n")
       comments_replied_to = list(filter(None, comments_replied_to))

# some vars to help report and switch behavior
checked = 0
replied = 0
switch = False
sticky = False

# Our main loop!
should_restart = True
while should_restart:
    should_restart = False
    # Switch between the hot, new, and stickied posts to scan
    if switch == True:
        posts = subreddit.new(limit=100)
        switch = False
    else:
        if sticky == True:
            posts = (subreddit.sticky(1), subreddit.sticky(2))
            sticky = False
        else:
            posts = subreddit.hot(limit=100)
            switch = True
            sticky = True

    # Check the submission text and each comment for the links
    for submission in posts:
        checked = checked + 1
        print ("Checked ", checked ," posts. ", submission.title)
        if checked % 3500 == 0:
           replied = 0
        if checked % 100 == 0:
           should_restart = True
           break
        #Check submission text
        if re.search(searchtext, submission.selftext, re.IGNORECASE) and submission.id not in posts_replied_to:
                mgid = re.search(regexfindid, submission.selftext)
                submission.reply(botcomment + mgid.group(1) + botcommentpart2)
                replied = replied + 1
                print("Bot replied to: ", submission.title)
                posts_replied_to.append(submission.id)
                with open("posts_replied_to.txt", "w") as f:
                    for post_id in posts_replied_to:
                        f.write(post_id + "\n")
        #Check comments of post
        submission.comments.replace_more(limit=0)
        comments = submission.comments[:]
        while comments:
           comment = comments.pop(0)
           if comment.id not in comments_replied_to and str.lower(str(comment.author)) != ignore:
               if re.search(searchtext, comment.body, re.IGNORECASE):
                   mgid = re.search(regexfindid, comment.body)
                   comment.reply(botcomment + mgid.group(1) + botcommentpart2)
                   replied = replied + 1
                   print("Bot replied to comment under: ", submission.title)
                   comments_replied_to.append(comment.id)
                   with open("comments_replied_to.txt", "w") as t:
                       for post_id in comments_replied_to:
                           t.write(post_id + "\n")
               comments.extend(comment.replies)
    should_restart = True
