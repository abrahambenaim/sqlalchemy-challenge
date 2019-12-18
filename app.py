app = Flask(__trip__)

@app.route('/')
def home():
    return 'Welcome to my homepage'

@app.route('/api/v1.0/precipitation')

