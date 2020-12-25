import bs4
import clipboard
import infi.systray
import re
import requests
import system_hotkey
import win10toast
import os
import pkg_resources


class App:
    def __init__(self):
        self.hk = system_hotkey.SystemHotkey()
        self.title = "Markdown URL to Title"
        self.normal_icon = "resources\\icon\\normal.ico"
        self.running_icon = "resources\\icon\\running.ico"
        self.options = ()
        self.systray = infi.systray.SysTrayIcon(
            self.normal_icon, self.title, self.options, on_quit=self.on_quit)
        self.parse_hotkey = ('control', 'shift', 'q')
        self.cache = {}

    def start(self):
        self.systray.start()
        self.hk.register(self.parse_hotkey, callback=self.do_convert)
        print("Hotkey {} registed".format(self.parse_hotkey))
        print("Copy markdown content and press {} to update url title".format(
            "+".join(self.parse_hotkey)))

    def set_icon_normal(self):
        self.systray.update(icon=self.normal_icon)

    def set_icon_running(self):
        self.systray.update(icon=self.running_icon)

    def on_quit(self, sysTrayIcon):
        self.hk.unregister(self.parse_hotkey)

    def parse(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers)
        try:
            title = bs4.BeautifulSoup(
                response.content, "html.parser").title.string.strip()
        except Exception as e:
            print(repr(e))
            title = url
        return title

    def toast(self, text):
        toaster = win10toast.ToastNotifier()
        toaster.show_toast(
            self.title,
            text,
            duration=2,
        )

    def do_convert(self, sysTrayIcon):
        self.set_icon_running()
        data = clipboard.paste()
        pattern = r'https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]'
        urls = re.findall(pattern, data)
        if len(urls) > 0:
            ignored = 0
            origin_content = []
            left = data
            result = []
            for url in urls:
                origin_content.append(left.split(url)[0])
                left = left[left.index(url) + len(url):]
            origin_content.append(left)
            assert len(origin_content) == len(urls) + 1

            # parse url title using threading pool
            for url in urls:
                # check cache existance
                if url not in self.cache.keys():
                    self.cache[url] = self.parse(url)

            # wait for all jobs finished, which means that all urls have been parsed
            for i, url in enumerate(urls):
                part = origin_content[i]
                next_part = origin_content[i+1]
                markdown = "[{}]({})".format(self.cache[url], url)
                print("[{} / {}] {}".format(i + 1, len(urls), markdown), end="")
                if part.strip().endswith("](") and next_part.strip().startswith(")"):
                    print("[IGNORED]")
                    ignored += 1
                    continue
                print()
                result.append(part)
                result.append(markdown)
            result.append(left)
            clipboard.copy("".join(result))
            if ignored == 0:
                self.toast(
                    "{}/{} url has been parsed.".format(len(urls) - ignored, len(urls)))
            else:
                self.toast(
                    "{}/{} url has been parsed, {} ignored".format(len(urls) - ignored, len(urls), ignored))
        else:
            print("No url found in clipboard")
        self.set_icon_normal()


def init():
    distribution = pkg_resources.get_distribution('u2t')
    os.chdir(distribution.location)
    os.chdir(distribution.project_name)


def main():
    init()
    app = App()
    app.start()


if __name__ == "__main__":
    main()
