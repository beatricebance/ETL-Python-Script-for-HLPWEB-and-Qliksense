# ETL-Python-Script-for-HLPWEB-and-Qliksense
Script python to download , rename, move data to Azure Blob from HLPWEB and QlikSense Hub
You only have to do this once

Change the link to your Database extraction web path (The link here is for HLP Web Alstom)then 

Download edge driver from https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ and move it to :
driver_path = r'C:\Program Files\edgedriver_win64\msedgedriver.exe'

You can use Jupyter StandAlone module or Jupyter in Vs Code(Vs code is faster since you just need to add Jupyter as an extension)

Either way it work

You can use your wsl if you have it already on your computer for python venv

\\wsl$\NomDeVotreDistribution 

If you don't have a python venv nor python on your computer install it

Upgrade your pip with Python pip install --upgrade or  python.exe -m pip install --upgrade pip

If you want create a virtual environnement or use directly the python install on your computer:
pip install virtualenv
virtualenv venv
.venv/Scripts/activate

Now intall the requirements:
pip install -r requirements.txt
pip install ipykernel -U --force-reinstall
pip freeze > requirements.txt "to add extensions to requirements files when you have install more"

Create an environnement path on your computer so you don't have to change the path (PS :better use environnement variable path on your computer )
DATA_PATH =  (Write the correct path from your computer)
source_folder =  (Write the correct path from your computer)
PASSWORD_ALSTOM = Your PASSWORD_ALSTOM
USERNAME = Your alstom username
destination_folder_QUALITY_PORTAL = Write the correct path from your computer)
