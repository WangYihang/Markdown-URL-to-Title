import bs4
import clipboard
import infi.systray
import os
import pkg_resources
import queue
import re
import requests
import sys
import system_hotkey
import termcolor
import threading
import win10toast


def print_success(x): return termcolor.cprint(x, 'green')
def print_error(x): return termcolor.cprint(x, 'red')
def print_warning(x): return termcolor.cprint(x, 'yellow')
def print_info(x): return termcolor.cprint(x)


class App:
    def __init__(self):
        self.title = "Markdown URL to Title"
        self.normal_icon = "resources\\icon\\normal.ico"
        self.running_icon = "resources\\icon\\running.ico"
        self.options = ()
        self.threads_number = 0x10
        self.request_timeout = 0x04
        self.cache = {}

        sys.stdout.write("Starting {}...".format(
            termcolor.colored(self.title, "green"))) and sys.stdout.flush()
        self.systray = infi.systray.SysTrayIcon(
            self.normal_icon, self.title, self.options, on_quit=self.on_quit)
        self.hk = system_hotkey.SystemHotkey()
        self.parse_hotkey = ('control', 'shift', 'q')
        self.q = queue.Queue()
        self.start_workers()

    def start_workers(self):
        for _ in range(self.threads_number):
            threading.Thread(target=self.worker, daemon=True).start()
        self.toast("{} started with {} threads".format(
            self.title, self.threads_number))

    def start(self):
        self.systray.start()
        self.hk.register(self.parse_hotkey, callback=self.do_convert)
        print_success(" [DONE]")
        print("Usage: ")
        print("1. Copy markdown content")
        print("2. press {} to update url title".format(
            " + ".join([termcolor.colored(single_key.upper(), "cyan") for single_key in self.parse_hotkey])))

    def set_icon_normal(self):
        self.systray.update(icon=self.normal_icon)

    def set_icon_running(self):
        self.systray.update(icon=self.running_icon)

    def on_quit(self, sysTrayIcon):
        self.hk.unregister(self.parse_hotkey)

    def parse(self, url, index, total):
        print_info("Processing: {}".format(url))
        # check cache existance
        if url not in self.cache.keys():
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
            }

            try:
                response = requests.get(
                    url, headers=headers, timeout=self.request_timeout)
                title = bs4.BeautifulSoup(
                    response.content, "html.parser").title.string.strip()
                markdown = "[{}]({})".format(title, url)
                print("[{} / {}] {}".format(index + 1, total,
                                            termcolor.colored(markdown, "green")))
                self.cache[url] = markdown
            except Exception as e:
                print("[{} / {}] {} - {}".format(index + 1, total,
                                                 termcolor.colored(url, "red"), termcolor.colored(repr(e), "red")))

    def worker(self):
        while True:
            task = self.q.get()
            url = task["url"]
            index = task["index"]
            total = task["total"]
            self.parse(url, index, total)
            self.q.task_done()

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
        print_success("Found {} urls in the clipboard".format(len(urls)))
        tasks = []
        if len(urls) == 0:
            print_warning("No url found in clipboard")
        else:
            origin = []
            remaining = data
            result = []

            # Split origin content by all urls
            for url in urls:
                origin.append(remaining[:remaining.index(url)])
                remaining = remaining[remaining.index(url) + len(url):]
            origin.append(remaining)
            assert len(origin) == len(urls) + 1

            # Find urls need to be processed, which is not in the format `[title](url)`
            for i, url in enumerate(urls):
                before_url = origin[i]
                after_url = origin[i+1]
                if not (before_url.strip().endswith("](") and after_url.strip().startswith(")")):
                    tasks.append(url)

            if len(tasks) == 0:
                print_warning(
                    "No urls need to be processed".format(len(tasks)))
                message = "No url has been parsed.".format(
                    len(tasks), len(urls))
            else:
                print_success(
                    "Found {} urls need to be processed".format(len(tasks)))
                # parse url title using threading pool
                for i, url in enumerate(tasks):
                    self.q.put({"url": url, "index": i, "total": len(tasks)})

                # wait for all jobs finished, which means that all urls have been parsed
                self.q.join()

                # construct result
                for i, url in enumerate(urls):
                    before_url = origin[i]
                    after_url = origin[i + 1]
                    result.append(before_url)

                    # Check if the format is already satisfied
                    if not (before_url.strip().endswith("](") and after_url.strip().startswith(")")):
                        # Not satisfied
                        if url in self.cache.keys():
                            result.append(self.cache[url])
                        else:
                            result.append(url)
                    else:
                        # Satisfied
                        result.append(url)

                result.append(remaining)
                clipboard.copy("".join(result))

                message = "[{} / {}] urls has been parsed.".format(
                    len(tasks), len(urls))
                print_success(message)

            self.toast(message)
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
