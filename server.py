from stepik import Stepik
from werkzeug.contrib.cache import SimpleCache
from flask import Flask, request, jsonify
import requests

cache = SimpleCache()
app = Flask(__name__)
st = Stepik()

@app.route('/lessons')
def lessons():
    lesson_id = request.args.get('lesson', '')
    # Check if id is int
    try:
        lesson_id = int(lesson_id)
    except Exception as e:
        response = jsonify(message="Invalid Lesson ID: "+lesson_id)
        response.status_code = 404
        return response
    # Check if lesson exists and get update date
    try:
        date = st.get_lesson_date(lesson_id)
    except requests.exceptions.HTTPError as e:
        response = jsonify(message="Lesson not found: "+str(lesson_id))
        response.status_code = 404
        return response

    cached = cache.get(str(lesson_id))
    # cached[0] is a cached date, cached[0] is a cached data
    if not cached or cached[0] != date:
        # Get steps from stepic, if lesson not in cache or updated
        steps = st.get_text_steps(lesson_id)
        cache.set(str(lesson_id), (date, steps))
    else:
        steps = cached[1]
    return jsonify({lesson_id: steps})

def main():
    app.run(threaded=True)

if __name__ == '__main__':
    main()