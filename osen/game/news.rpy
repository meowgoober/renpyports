init offset = -100







define NEWS_URL = "https://raw.githubusercontent.com/npckc/renpy-news/main/news.json"

define NEWS_MOBILE_URL = "https://raw.githubusercontent.com/npckc/renpy-news/main/news_mobile.json"



define NEWS_CHECK_INTERVAL = 1.0

















translate ja strings:

    old "News (!){#news}"
    new "{font=tl/None/npckc.ttf}News (!){/font}"

    old "News{#news}"
    new "{font=tl/None/npckc.ttf}News{/font}"

    old "NEWS (!){#news}"
    new "{font=tl/None/npckc.ttf}NEWS (!){/font}"

    old "NEWS{#news}"
    new "{font=tl/None/npckc.ttf}NEWS{/font}"

translate de strings:

    old "News (!){#news}"
    new "Info (!)"

    old "News{#news}"
    new "Info"

    old "NEWS (!){#news}"
    new "INFO (!)"

    old "NEWS{#news}"
    new "INFO"

translate el strings:

    old "News (!){#news}"
    new "Νέα (!)"

    old "News{#news}"
    new "Νέα"

    old "NEWS (!){#news}"
    new "ΝΈΑ (!)"

    old "NEWS{#news}"
    new "ΝΈΑ"

translate es strings:

    old "News (!){#news}"
    new "Info (!)"

    old "News{#news}"
    new "Info"

    old "NEWS (!){#news}"
    new "INFO (!)"

    old "NEWS{#news}"
    new "INFO"

translate esla strings:

    old "News (!){#news}"
    new "Info (!)"

    old "News{#news}"
    new "Info"

    old "NEWS (!){#news}"
    new "INFO (!)"

    old "NEWS{#news}"
    new "INFO"

translate fr strings:

    old "News (!){#news}"
    new "Info (!)"

    old "News{#news}"
    new "Info"

    old "NEWS (!){#news}"
    new "INFO (!)"

    old "NEWS{#news}"
    new "INFO"

translate id strings:

    old "News (!){#news}"
    new "Berita (!)"

    old "News{#news}"
    new "Berita"

    old "NEWS (!){#news}"
    new "BERITA (!)"

    old "NEWS{#news}"
    new "BERITA"

translate it strings:

    old "News (!){#news}"
    new "Info (!)"

    old "News{#news}"
    new "Info"

    old "NEWS (!){#news}"
    new "INFO (!)"

    old "NEWS{#news}"
    new "INFO"

translate ko strings:

    old "News (!){#news}"
    new "뉴스 (!)"

    old "News{#news}"
    new "뉴스"

    old "NEWS (!){#news}"
    new "뉴스 (!)"

    old "NEWS{#news}"
    new "뉴스"

translate pl strings:

    old "News (!){#news}"
    new "Info (!)"

    old "News{#news}"
    new "Info"

    old "NEWS (!){#news}"
    new "INFO (!)"

    old "NEWS{#news}"
    new "INFO"

translate pt strings:

    old "News (!){#news}"
    new "Info (!)"

    old "News{#news}"
    new "Info"

    old "NEWS (!){#news}"
    new "INFO (!)"

    old "NEWS{#news}"
    new "INFO"

translate ptbr strings:

    old "News (!){#news}"
    new "Info (!)"

    old "News{#news}"
    new "Info"

    old "NEWS (!){#news}"
    new "INFO (!)"

    old "NEWS{#news}"
    new "INFO"

translate ru strings:

    old "News (!){#news}"
    new "Весть (!)"

    old "News{#news}"
    new "Весть"

    old "NEWS (!){#news}"
    new "ВЕСТЬ (!)"

    old "NEWS{#news}"
    new "ВЕСТЬ"

translate th strings:

    old "News (!){#news}"
    new "ข่าว (!)"

    old "News{#news}"
    new "ข่าว"

    old "NEWS (!){#news}"
    new "ข่าว (!)"

    old "NEWS{#news}"
    new "ข่าว"

translate vi strings:

    old "News (!){#news}"
    new "Tin tức (!)"

    old "News{#news}"
    new "Tin tức"

    old "NEWS (!){#news}"
    new "TIN TỨC (!)"

    old "NEWS{#news}"
    new "TIN TỨC"

translate zh strings:

    old "News (!){#news}"
    new "信息 (!)"

    old "News{#news}"
    new "信息"

    old "NEWS (!){#news}"
    new "信息 (!)"

    old "NEWS{#news}"
    new "信息"

translate zhs strings:

    old "News (!){#news}"
    new "信息 (!)"

    old "News{#news}"
    new "信息"

    old "NEWS (!){#news}"
    new "信息 (!)"

    old "NEWS{#news}"
    new "信息"



screen news(news):

    zorder 100
    modal True

    add "#000000c0"

    frame:
        xalign 0.5
        yalign 0.5

        padding (40,40)

        has vbox
        spacing 10

        imagebutton:
            idle NewsImage()
            action OpenURL(news["link"])

        null height 4

        text news["text"] xalign 0.5

        textbutton "{font=DejaVuSans.ttf}✖{/font}":
            xalign 0.5
            action Hide("news")






default persistent.news_last_checked = 0


default persistent.seen_news = 0

init python:


    import time
    import requests
    import certifi



    def news_thread():
        
        print("Checking the news.")
        
        
        
        
        ca_file = os.path.join(config.gamedir, certifi.where())
        
        if not os.path.exists(ca_file):
            ca_file = os.path.join(config.savedir, "cacert.pem")
            
            with open(ca_file, "wb") as f:
                f.write(renpy.file("python-packages/certifi/cacert.pem").read())
        
        
        now = time.time()
        
        if not config.developer:
            if now < persistent.news_last_checked + (NEWS_CHECK_INTERVAL * 86400):
                return
        
        persistent.news_last_checked = now
        
        
        if persistent.news:
            old_version = persistent.news["version"]
        else:
            old_version = 0
        
        
        if renpy.variant("mobile"):
            news = requests.get(NEWS_MOBILE_URL, verify=ca_file).json()
        else:
            news = requests.get(NEWS_URL, verify=ca_file).json()
        
        
        if news["version"] == old_version:
            return
        
        
        news["image_data"] = requests.get(news["image"], verify=ca_file).content
        
        
        persistent.news = news
        
        return

    def run_news_thread():
        """
        Try to run the news thread. If something fails, print an exception
        that Ren'Py will log to its console and log.txt.
        """
        
        try:
            news_thread()
        except:
            import traceback
            traceback.print_exc()


    @renpy.pure
    class ShowNews(Action):
        """
        This is an action that shows the news.
        """
        
        def __call__(self):
            if not persistent.news:
                return
            
            persistent.seen_news = persistent.news["version"]
            
            renpy.show_screen("news", persistent.news)
            renpy.restart_interaction()
        
        def get_sensitive(self):
            return persistent.news is not None

    def HasUnseenNews():
        """
        This function returns True if there is new news to present to the
        player, and False otherwise.
        """
        
        if persistent.news is None:
            return False
        
        return persistent.news["version"] > persistent.seen_news

    def NewsImage():
        """
        Returns a displayable giving the image corresponding to the news
        blast.
        """
        
        if persistent.news is None:
            return Null()
        
        return im.Data(persistent.news["image_data"], persistent.news["image"])

init 100 python:


    if not persistent.updated:
        persistent.news = None
        persistent.news_last_checked = 0
        persistent.seen_news = 0
        persistent.updated = True

    renpy.invoke_in_thread(news_thread)
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
