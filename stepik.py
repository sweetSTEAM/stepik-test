import requests
import datetime

class Stepik():
    """Class-wrapper for Stepik API"""
    def __init__(self):
        self.STEPS_API = "https://stepik.org:443/api/steps"
        self.LESSON_API = "https://stepik.org:443/api/lessons/"

    def _request(self, url, payload=None):
        """Getting json from Stepik"""
        r = requests.get(url, params=payload)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        return r.json()

    def get_lesson_date(self, lesson_id):
        lesson_url = self.LESSON_API + str(lesson_id)
        data = self._request(lesson_url)
        return data['lessons'][0]['update_date']

    def get_text_steps(self, lesson_id):
        do = True
        out = []
        page = 1
        # Iterate over pages w/ steps
        while do:
            # Getiing page
            payload = {'lesson': lesson_id, 'page': page}
            data = self._request(self.STEPS_API, payload)
            # Checking types of all steps on page
            for step in data['steps']:
                if step['block']['name'] == 'text':
                    out.append(step['id'])
            # Move to the next page, if exists
            # Haven't seen cases w/ more then 1 page though
            do = data['meta']['has_next']
            page += 1
        return out

    def str_to_time(self, time_str):
        return datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')

def main():
    # For tests
    print("Input lesson id:")
    lesson = int(input())
    st = Stepik()
    try:
        print(st.str_to_time(st.get_lesson_date(lesson)),
            st.get_text_steps(lesson))
    except requests.exceptions.HTTPError as e:
        print("Lesson not found")
        
if __name__ == '__main__':
    main()