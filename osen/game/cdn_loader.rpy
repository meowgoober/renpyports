init python:
    import renpy.loader as loader
    import urllib.request
    import io

    old_load = loader.load

    def cdn_load(fn, *args, **kwargs):
        # Only intercept files inside 'osen/' folder
        if fn.startswith("osen/"):
            # Keep the folder structure for JSDelivr
            path_in_repo = fn[len("osen/"):]  # remove leading "osen/"
            url = f"https://cdn.jsdelivr.net/gh/meowgoober/renpyports@main/osen/{path_in_repo}"
            try:
                with urllib.request.urlopen(url) as response:
                    data = response.read()
                    return io.BytesIO(data)
            except Exception as e:
                print(f"Failed to load {url}: {e}")
        return old_load(fn, *args, **kwargs)

    loader.load = cdn_load
