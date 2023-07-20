import re
import json

import mkdocs.plugins
from mkdocs.config.defaults import MkDocsConfig


def clean_search(config: MkDocsConfig):
    """Clean the search index.

    Remove unnecessary plotly and css blocks (from mkdocs-jupyter) to
    keep the search index small.

    Parameters
    ----------
    config: MkdocsConfig
        Object containing the search index.

    """
    with open(f"{config.data['site_dir']}/search/search_index.json", 'r') as f:
        search = json.load(f)

    for elem in search["docs"]:
        # Remove plotly graphs
        elem["text"] = re.sub(r"window\.PLOTLYENV.*?\)\s*?}\s*?", "", elem["text"], flags=re.S)

        # Remove mkdocs-jupyter css
        elem["text"] = re.sub(r"\(function \(global, factory.*?(?=Example:)", "", elem["text"], flags=re.S)

    with open(f"{config.data['site_dir']}/search/search_index.json", 'w') as f:
        json.dump(search, f)


def update_source_url(html):
    pattern = r'(<a\s*href="https:\/\/github\.com\/fastestimator\/fastestimator\/)(raw)(\/\S+.)(md)"'
    html = re.sub(pattern, fr'\1blob\3py"', html)

    html = re.sub(r'<div class="jp-RenderedHTMLCommon jp-RenderedHTML jp-OutputArea-output " data-mime-type="text\/html">\s*?<script type="text\/javascript">.*?<\/script>\s*?<\/div>', "", html, flags=re.S)

    # Fix plots in jupyter notebook
    html = re.sub(r'(?<=<script type="text\/javascript">)\s*?require\(\["plotly"\], function\(Plotly\) {\s*?(?=window\.PLOTLYENV)', "", html)
    html = re.sub(r'\).then\(function\(\){.*?(?=<\/script>)', ')}', html, flags=re.S)
    html = re.sub(r'<a href="installation\.html" class="md-nav__link md-nav__link(--active)?">\s*Install\s*</a>', fr'', html)
    #html = re.sub(r'\.\.\/\.\.\/apphub\/(.+)\/(.+)\.ipynb', fr'http://127.0.0.1:8000/apphub/\2.html', html)
    html = re.sub(r'(\.[a-zA-Z0-9\/\._]+)\.ipynb', fr'\1.html', html)
    # # Correct sizes of the plot to adjust to frame
    # html = re.sub(r'(?<=style="height:1000px; width:)\d+?px(?=;")', "100%", html)
    # html = re.sub(r'(?<="showlegend":\w+?),"width":\d+?,"height":\d+?(?=[},])', "", html)
    return html


# def on_page_content(html, page, config, files):
#     print(page.title)
#     html = update_plotly(html)
#     html = update_source_url(html)
#     return html

def on_post_page(output, page, config):
    output = update_source_url(output)
    return output

def on_post_build(config: MkDocsConfig):
    clean_search(config=config)


# if __name__ == '__main__':
#     with open('../site/apphub/rand_augment.html') as f:
#         html = f.read()
#     import pdb; pdb.set_trace()
#     html = convert_plotly(html)
