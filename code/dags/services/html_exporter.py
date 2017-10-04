import math
import jsonlines
from jinja2 import Template


HTML = """
<!doctype html>
<html class="no-js" lang="">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <title>The Daily Argus</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            col { float: left; width: 49.5%; }
            article { overflow: hidden; }
            article img { float: left; }
            article .article-body { float: left; }
        </style>
    </head>
    <body>
        <!--[if lte IE 9]>
            <p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
        <![endif]-->
        <h1>The Daily Argus</h1>
        <section>
        {% for articles in columns %}
            <div class="col">
                {% for article in articles %}
                    {% if article.new_headline %}
                    <article>
                        <img src="images/{{ article.id }}.jpg" />
                        <div class="article-body">
                            <h3>{{ article.new_headline }}</h3>
                            <p><a href="http://www.theargus.co.uk{{ article.url }}">View</a></p>
                        </div>
                    </article>
                    {% endif %}
                {% endfor %}
            </div>
        {% endfor %}
        </section>
    </body>
</html>
"""


def chunks(iterable, size):
    """Yield successive chunks of size from iterable."""
    chunksize = int(math.ceil(len(iterable) / size))
    return (iterable[i * chunksize:i * chunksize + chunksize] for i in range(size))


def render_headlines_to_html(headlines_file_path, output_file):
    """
    Generates a .html file from the given headlines
    """

    with jsonlines.open(headlines_file_path) as reader:
        with open(output_file, 'w') as writer:
            template = Template(HTML)
            writer.write(template.render(columns=chunks(list(reader), 2)))
