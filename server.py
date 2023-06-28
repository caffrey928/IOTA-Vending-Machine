from flask import Flask, request
from utils import lcd, pusher, detect_button, get_balance
import time
import multiprocessing


app = Flask(__name__)
balance = 0

@app.route('/')
def hello():
    return 'Hello, World!'
    
@app.route('/payment', methods=['POST'])
def payment():
    global balance
    if request.method == 'POST':
        # Crawl payment data
        lcd("Wait for 3 seconds...")
        time.sleep(3)
        
        new_balance = get_balance()
        print("Balance: ", new_balance)

        payment = 0
        if(new_balance == -1):
            payment = 0
        else:
            payment = new_balance - balance
            balance = new_balance
        
        # Check the payment
        if(payment <= 0):
            lcd("Failed Payment!")
        elif(payment < 5000000):
            lcd("No enough money!")
        else:
            lcd("Success Payment!")
            pusher()
        
        time.sleep(3)

        lcd("Pay 5Mi to buy!")
        
        # Return the response
        return "Finish Payment!"

# run "python3 server.py" to start development server
# run "gunicorn server:app" to start production depployment server
if __name__ == '__main__':
    lcd("Pay 5Mi to buy!")
    balance = get_balance()
    print("Balance: ", balance)
    p = multiprocessing.Process(target=detect_button, args=())
    p.start()
    app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=False)
    p.join()
