from skills import flaskapp
import platform

print("Running on {0}".format('Linux' if platform.system() == 'Linux' else 'Windows'))

# Run 
if __name__ == "__main__":
    flaskapp.run(debug=True, port='5000', host='0.0.0.0')