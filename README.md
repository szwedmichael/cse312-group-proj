# Its M&M

Group project for UB's CSE 312 class

## IMPORTANT NOTE TO THE GRADER

If you are on Windows 10 running docker desktop 4.27 for some reason unknown to God himself it will not build for you (it does on MacOS though :D). Please either upgrade to 4.28 or downgrade to 4.26

## Domain name

https://vacationhub.live/

## WS Feature

The likes are updated by web sockets

## Extra Feature Testing Procedure - Randomize Posts

1. Navigate to https://vacationhub.live/
2. Sign up and log in to two different account on two different windows/browsers.
3. Take note of the order of posts
    a. If there are no posts, quickly make at least 3 posts, at least one from each user
4. Click the Randomize Posts button on the first window. Verify the posts were randomized
5. Refresh the page on the second window. Verify the posts are not randomized, and are still in the same order as before.
6. Click the Randomize Posts button again on the first window. Verify the posts are randomized differently than before. Keep clicking this randomize and ensure that no pattern appears between the display of various posts (easier to prove the more posts there are)
7. Randomize the posts on the second window
8. Create a new post on the second window (a file upload is not required)
9. Verify the new post appears at the top of the page on the second window not randomized
10. Click the randomize posts button on the first window without refreshing, and ensure that the new post from the second window appears somewhere in the list (could happen to be at the top, but ensure the posts still appear randomized)
11. Refresh both browsers, and ensure the original order is displayed with the addition of the new post during the testing at the top
12. Give Group an AO