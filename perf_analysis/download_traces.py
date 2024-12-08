import gdown

# Provide the Google Drive file ID
url = 'https://drive.google.com/uc?id=1wCbo_ymEiEWtN9b97_xJzQp-stQor5Bo'

# Download the file
gdown.download(url, 'cputraces.tar.gz', quiet=False)
