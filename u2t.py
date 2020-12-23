import system_hotkey
import clipboard
import requests
import bs4
import re
import infi.systray
import win10toast

class App:
    def __init__(self):
        self.hk = system_hotkey.SystemHotkey()
        self.title = "Markdown URL to Title"
        self.normal_icon = "resources\\icon\\normal.ico"
        self.running_icon = "resources\\icon\\running.ico"
        self.options = ()
        self.systray = infi.systray.SysTrayIcon(self.normal_icon, self.title, self.options, on_quit=self.on_quit)
        self.hotkey = ('control', 'shift', 'q')

    def start(self):
        print("Starting...")
        self.systray.start()
        self.hk.register(self.hotkey, callback=self.convert)
        print("Hotkey {} registed".format(self.hotkey))
        print("Copy markdown content and press {} to update url title".format("+".join(self.hotkey)))

    def set_icon_normal(self):
        self.systray.update(icon=self.normal_icon)

    def set_icon_running(self):
        self.systray.update(icon=self.running_icon)

    def on_quit(self, sysTrayIcon):
        self.hk.unregister(self.hotkey)

    def parse(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers)
        try:
            title = bs4.BeautifulSoup(response.content, "html.parser").title.string
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

    def convert(self, sysTrayIcon):
        self.set_icon_running()
        print("Reading clipboard...")
        data = clipboard.paste()
        print("Clipboard: {}".format(repr(data)))
        pattern = r'https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]'
        urls = re.findall(pattern, data)
        if len(urls) > 0:
            print("Found {} urls in clipboard".format(len(urls)))
            ignored = 0
            origin_content = []
            origin_urls = []
            left = data
            result = []
            for url in urls:
                origin_content.append(left.split(url)[0])
                origin_urls.append(url)
                left = left[left.index(url) + len(url):]
            for i, url in enumerate(urls):
                print("-" * 0x20)
                print("Parsing: {}".format(url))
                if data[:data.index(url)].strip().endswith("](") and data[data.index(url) + len(url):].strip().startswith(")"):
                    print("This url is already surrounded in markdown style")
                    ignored += 1
                    continue
                title = self.parse(url)
                print("Found title: {}".format(title))
                print("Generating markdown...")
                markdown = "[{}]({})".format(title, url)
                result.append(origin_content[i])
                result.append(markdown)
            result.append(left)
            print("-" * 0x20)
            clipboard.copy("".join(result))
            self.toast("{}/{} url has been parsed.".format(len(urls) - ignored, len(urls)))
        else:
            print("No url found in clipboard")
        self.set_icon_normal()

def main():
    app = App()
    app.start()

if __name__ == "__main__":
    main()