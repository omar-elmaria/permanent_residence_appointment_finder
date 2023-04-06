# vhs_appointment_finder
This repo contains a Selenium script that automatically checks for Consultation appointments on the Volkshochschule Berlin Mitte Website (https://vhsmitte.flexappoint.de/#/). This website is used to book appointments for the "Leben in Deutschland" test, which is a prerequisite for obtaining the permanent residence or citizenship in Germany 

# How it works?
The script runs every 15 minutes on VM hosted on Google Cloud. It checks for appointments in the **current month** and **six months in the future**. If it finds an appointment as shown in the screenshot below,
it sends an E-mail notification. I created this script because I was fed up with checking the website every day to get an appointment and wanted to automate this process.

![image](https://user-images.githubusercontent.com/98691360/230377124-363ae693-4a53-4702-830f-cf49c8caf117.png)

This is how the E-mail notification looks like...

![image](https://user-images.githubusercontent.com/98691360/230377260-c24212c2-db63-4d22-8c3d-76783620a382.png)
