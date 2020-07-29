import praw
import pdb
import re
import os
import time

start = time.time()

reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit("magictcg+mtgjudge+mtgaltered+MTGO+mtgcube+mtgfinance+lrcast+CompetitiveEDH")
ignore = str(reddit.redditor('mtgcardfetcher'))

lmsrcomment = """>Queen Marchesa (long may she reign)\n
                    \nPlease address the Queen with respect. I'm a bot. If I've made a mistake, click [here.]
                    (https://www.reddit.com/message/compose?to=shadowwesley77)
                    """
        
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

checked = 0
replied = 0
switch = False

#Check submission titles
should_restart = True
while should_restart:
    should_restart = False
    if switch == True:
        posts = subreddit.new(limit=100)
        switch = False
    else:
        posts = subreddit.hot(limit=100)
        switch = True
    for submission in posts:
        if submission.id not in posts_replied_to:
            checked = checked + 1
            print ("Checked ", checked ," posts. ", submission.title)
            if checked % 3500 == 0:
                msg = "Uptime: " + str("{:.2f}".format((time.time()-start)/3600)) + " hours.\n\n Checked " + str(checked) + " posts.\n\nReplied to " + str(replied) + " posts."
                reddit.redditor('shadowwesley77').message("Bot Status", msg,)
                replied = 0
            if checked % 100 == 0:
                should_restart = True
                break
            if re.search("Queen Marchesa", submission.title, re.IGNORECASE) and not re.search("long may she reign", submission.title, re.IGNORECASE):
                submission.reply(lmsrcomment)
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
                    if re.search("Queen Marchesa", comment.body, re.IGNORECASE) and not re.search("long may she reign", comment.body, re.IGNORECASE):
                        comment.reply(lmsrcomment)
                        replied = replied + 1
                        print("Bot replied to comment under: ", submission.title)
                        comments_replied_to.append(comment.id)
                        with open("comments_replied_to.txt", "w") as t:
                            for post_id in comments_replied_to:
                                t.write(post_id + "\n")
                    comments.extend(comment.replies)
        else:
            #Check comments of post
            submission.comments.replace_more(limit=0)
            comments = submission.comments[:]
            while comments:
                comment = comments.pop(0)
                if comment.id not in comments_replied_to and str.lower(str(comment.author)) != ignore:
                    if re.search("Queen Marchesa", comment.body, re.IGNORECASE) and not re.search("long may she reign", comment.body, re.IGNORECASE):
                        comment.reply(lmsrcomment)
                        replied = replied + 1
                        print("Bot replied to comment under: ", submission.title)
                        comments_replied_to.append(comment.id)
                        with open("comments_replied_to.txt", "w") as t:
                            for post_id in comments_replied_to:
                                t.write(post_id + "\n")
                    comments.extend(comment.replies)
    should_restart = True




            
            
