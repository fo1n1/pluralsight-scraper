import os, time
import requests

from clint.textui import progress
from driver import DriverUtils
from page import Page
from selenium.webdriver.common.keys import Keys

MODULES = "//section[@class='module open']"
MODULE_EPISODES = './/li'
VIDEO = '//video'
MODULE_TITLE = ".//header//h2"
EPISODE_TITLE = './/h3'


class Course(Page):

    def get_modules(self):
        return self.find_all(MODULES)

    @staticmethod
    def get_module_episodes(module):
        return [episode for episode in module.find_elements_by_xpath(MODULE_EPISODES)]

    def get_video_link(self):
        video_elt = self.find_by(VIDEO)
        link = video_elt.get_attribute("src")
        return link

    def pause_video(self):
        body = self.find_by("//body")
        body.send_keys(Keys.SPACE)

    def download_episodes(self, dir):
        course_path = self.create_course_directory(dir)
        modules = self.get_modules()
        module_count = 1
        for module in modules:
            module_path, module_title = self.create_module_directory(course_path, module, module_count)
            episodes = self.get_module_episodes(module)
            episode_count = 1
            for episode in episodes:
                Course.open_episode(episode)
                self.pause_video()
                episode_title = self.generate_episode_title(episode, episode_count)
                self.download_video(episode_title, module_path)
                episode_count = episode_count + 1
                self.wait_a_bit(10)
            module_count = module_count + 1

    def download_video(self, episode_title, module_path):
        episode_file_path = os.path.join(module_path, episode_title)
        Course.download(self.get_video_link(), episode_file_path)

    def create_course_directory(self, dir):
        course_path = os.path.join(dir, self.get_course_title())
        Course.create_directory(course_path)
        return course_path

    def generate_episode_title(self, episode, episode_count):
        return str(episode_count) + "_" + self.get_episode_title(episode)

    @staticmethod
    def open_episode(episode):
        episode.click()
        time.sleep(5)

    def create_module_directory(self, course_path, module, module_count):
        module_title = str(module_count) + '_' + self.get_module_title(module)
        module_path = os.path.join(course_path, module_title)
        Course.create_directory(module_path)
        return module_path, module_title

    @staticmethod
    def get_module_title(module):
        return module.find_element_by_xpath(MODULE_TITLE).text.replace(':', '')

    @staticmethod
    def get_course_title():
        return DriverUtils.get_driver().title.replace(':', '')

    @staticmethod
    def get_episode_title(episode):
        return episode.find_element_by_xpath(EPISODE_TITLE).text.replace('.', '') + ".mp4"

    @staticmethod
    def create_directory(directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    @staticmethod
    def download(url, path):
        r = requests.get(url, stream=True)
        with open(path, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()
