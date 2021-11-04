from skills import flaskapp, in_linux, gpio

# Run 
if __name__ == "__main__":
    flaskapp.run(debug=True, port='5000', host='0.0.0.0')
    # except KeyboardInterrupt:
    #     gpio.cleanup()
    #     print("GPIO cleanup")
    #     print("Exit")