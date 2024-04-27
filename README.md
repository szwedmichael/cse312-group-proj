# Its M&M

Group project for UB's CSE 312 class

## IMPORTANT NOTE TO THE GRADER

If you are on Windows 10 running docker desktop 4.27 for some reason unknown to God himself it will not build for you (it does on MacOS though :D). Please either upgrade to 4.28 or downgrade to 4.26

## Domain name

https://vacationhub.live/

## WS Feature

The likes are updated by web sockets

## Extra Feature Testing Procedure

1. Navigate to https://vacationhub.live/
2. Sign up and log in to two different account on two different windows/browsers
3. Take note of the order of posts
    a. If there are no posts, quickly make at least 3 posts from either user
4. Click the Randomize Posts button on the first window. Verify the posts were randomized
5. Refresh the page on the second window. Verify the posts are not randomized, and are still in the same order as before.
6. Click the Randomize Posts button again on the first window. Verify the posts are no longer randomized and back to how they were originally.
7. Randomize the posts on the second window
8. Create a new post on the first window.
   a. Refresh both browsers
    b. Ensure that the post appeared in the second window but in a random order
    c. Ensure that the post appeared in the first window at the top (in the normal order)
