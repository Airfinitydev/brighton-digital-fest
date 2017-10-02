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
        {% for article in articles %}
            <article>
                <img src="images/{{ article.id }}.jpg" />
                <div class="article-body">
                    <h3>{{ article.new_headline|default(article.headline) }}</h3>
                    <p><a href="http://www.theargus.co.uk{{ article.url }}">View</a></p>
                </div>
            </article>
        {% endfor %}
        </section>
    </body>
</html>
"""


def render_headlines_to_html(headlines_file_path, output_file):
    """
    Generates a .html file from the given headlines
    """

    with jsonlines.open(headlines_file_path) as reader:
        with open(output_file, 'w') as writer:
            template = Template(HTML)
            writer.write(template.render(articles=reader))
