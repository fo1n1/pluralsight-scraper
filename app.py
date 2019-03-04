import time

from course import Course
from driver import DriverUtils
from login import Login

LOAD_DIR = r'F:\+pluralsight_dir'
COURSE_PAGE_URL = '<COURSE_URL>'
LOGIN = '<LOGIN>'
PASSWORD = '<PASSWORD>'


def download_course():
    course = open_course_as_authorized_user()
    course.download_episodes(LOAD_DIR)


def open_course_as_authorized_user():
    login_page = Login()
    login_page.login(LOGIN, PASSWORD)
    DriverUtils.get_driver().get(COURSE_PAGE_URL)
    time.sleep(10)
    return Course()


if __name__ == '__main__':
    download_course()
