# tumblr2yaki

Downloads post content and metadata using the Tumblr API. Then takes the json output and converts video and text blocks to individual index.txt pages with the correct directory structure and the text/html content type.

# Usage

```
python tumblrbackup.py > backup.json
python convert2yaki.py
```

# Output

``` javascript
[
    {
        "body": "<p>Text body.</p>",
        "id": 11309083598,
        "tags": [],
        "timestamp": 1318313280,
        "title": "Text post",
        "type": "text"
    },
    {
        "id": 11084927889,
        "source": "Quote Author",
        "source_title": "quotesource.com",
        "source_url": "http://www.quotesource.com/",
        "tags": [
            "tag1",
            "tag2"
        ],
        "text": "Quote body.",
        "timestamp": 1317865857,
        "type": "quote"
    },
    ...
]
```

# Configuration

``` javascript
{
    "url": "my.tumblr.com",
    "api_key": "myApiKey",
    "strip_metadata": ["format", "note_count", "post_url", "reblog_key", "date", "blog_name"],
    "backup_file": "backup.json",
    "yaki_root": "Yaki/pages/main/blog"
}
```

# Tests

```
cd test
python -m unittest discover
```
