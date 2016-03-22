# Useful link:
http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
http://pycoder.net/bospy/presentation.html

# To install flask:
sudo aptitude install python-flask


# An example Tap query to dbserv (if running locally)
  curl -d 'query=SELECT+ra,decl,filterName+FROM+DC_W13_Stripe82.Science_Ccd_Exposure+WHERE+scienceCcdExposureId=125230127' http://localhost:5000/db/v0/sync
