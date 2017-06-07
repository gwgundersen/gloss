"""Dev deployment script.
"""

from gloss import app


app.run(debug=True, port=8080, host='0.0.0.0')
