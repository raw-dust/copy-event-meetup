# copy-event-meetup
This copies an event in Meetup.com from one group to other groups.

Steps:
* You will need an API KEY from https://secure.meetup.com/meetup_api/oauth_consumers/ and place it in the *YOUR_CLIENT_ID* .
* Change *http://YOUR_WEBSITE* to any website. 
* Put the access token url in a web browser. Meetup will ask to authorize your app and then redirect you to the redirect location with an access token in the URL like http://YOUR_WEBSITE?token=YOUR_TOKEN .
* Put the token in *TOKEN_FROM_OAUTH_STEP*.
* Change *GROUP-NAME* to the name of the group as shown in the URL that you are copying from.
* Change *fromevent* to the event number you are copying from.
* Change *togroups* to a list of the groups as shown in the URL that you are copying to.
* Set *announce* true if you want to announce it in that group.
