# Strava-Visualization
A script to create visualizations of strava rides

# Fun with the Strava API

![image](https://github.com/brad90four/Strava-Visualization/blob/main/strava_vis_6426581509.gif)

## Steps to work with the stand alone `strava.py`
1. Create a Strava Application

    -  You will need your Client ID and Client Secret

2. Copy the url

   `http://www.strava.com/oauth/authorize?client_id=[REPLACE_WITH_YOUR_CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read_all,activity:read_all`

   into your browser and place your Client ID in the placeholder.
3. Approve the application on the prompt and wait for the redirect url to appear.
4. When the redirect url is shown in your browser, copy the Authorization Code shown in it.

    `localhost/exchange_token?stat=&code=[VERY_LONG_CODE_HERE]&scope=read,activity:read_all,read_all`

5. Run the ``curl`` request with your Client ID, Client Secret and the Authorization Code from above in your terminal.

   ``curl -X POST https://www.strava.com/oauth/token -F client_id=YOURCLIENTID -F client_secret=YOURCLIENTSECRET -F code=AUTHORIZATIONCODE -F grant_type=authorization_code``

6. Create a ``.env`` file with the following information:
    ```
    REFRESH_TOKEN=<token that is given in the curl response>
    ACCESS_CODE=<token that is given in the curl response>
    CLIENT_ID=<ID given to your Strava application>
    CLIENT_SECRET=<secret given to your Strava application>
    ```

7. Use the ``access_token`` and ``refresh_token`` provided in the response in the ``.env`` file.

8. From the command line, run ``python strava.py``.
9. When the access token expires, run ``auth.py`` from the commandline
