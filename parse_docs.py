import argparse
import ast
import glob
import importlib
import os
import re
import shutil
import json

import yaml

from collections import OrderedDict


def create_doc_structure(doc_path, output_path, doc_parent_dir):
    d = {}
    if os.path.isdir(doc_path):
        os.makedirs(output_path, exist_ok=True)
        init_filepath = os.path.join(doc_path, '__init__.py')
        if not os.path.exists(init_filepath):
            open(init_filepath, 'w').close()
        dirname = os.path.basename(output_path)
        dirname = output_path.split(os.sep)[2:]
        dirname.insert(0, 'fe')
        dirname = '.'.join(dirname)
        if dirname == 'fe':
            dirname = 'API'
        d[dirname] = []
        if dirname == 'API':
            d[dirname].append({'fe': [{'estimator': os.path.join('fastestimator', 'estimator.md')},
                                    {'network': os.path.join('fastestimator', 'network.md')},
                                    {'pipeline': os.path.join('fastestimator', 'pipeline.md')}]})
        for x in os.listdir(doc_path):
            doc_struct = create_doc_structure(os.path.join(doc_path, x), os.path.join(output_path, x), doc_parent_dir)
            if x in ['estimator.py', 'network.py', 'pipeline.py']:
                continue
            if doc_struct:
                d[dirname].append(doc_struct)
        if not d[dirname]:
            del d[dirname]
    else:
        filename = os.path.basename(doc_path)
        if filename != '__init__.py' and filename.endswith('.py'):
            filename = filename.split('.')[0]
            md_filename = filename + '.md'
            md_filepath = os.path.join(os.path.dirname(output_path), md_filename)
            docs_identifier = doc_path.split('.')[0].replace('/', '.').replace('\\', '.')
            md_content = f'::: {docs_identifier}'
            with open(md_filepath, 'w', encoding="utf8") as f:
                f.write(md_content)
            md_filepath = os.path.relpath(md_filepath, doc_parent_dir)
            d[filename] = os.path.join(md_filepath)
    return d


def update_apphub_readme(readme_path):
    with open(readme_path, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if line.rstrip() == '## Table of Contents:':
                file.truncate(file.tell())
                break
            file.write(line)


def extract_installation_content(readme_path, output_path):
    with open(readme_path, 'r') as file:
        lines = file.readlines()
        startidx = 0
        endidx = len(lines) - 1
        for line in lines:
            if '## Installation' in line:
                startidx = lines.index(line)
            elif '## Useful Links' in line:
                endidx = lines.index(line)

    web_install_content = lines[startidx+1:endidx - 1]
    install_output_path = os.path.join(output_path, 'installation.md')
    with open(install_output_path, 'w') as f:
        f.write(''.join(web_install_content).rstrip())


def get_apphub_titles(readme_path):
    pattern = r'\* \*\*([a-zA-Z0-9 ()-]+)[\*\*]*:[\*\*]*.*\[\[notebook]\((.*)\)\]'
    titles_dict = {}
    with open(readme_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('###'):
                category_title = line.split('###')[-1]
            result = re.search(pattern, line)
            if result:
                title = result.group(1)
                print(title)
                notebook = result.group(2)
                notebook_name = notebook.split('/')[-1]
                titles_dict[notebook_name] = {
                    'title': title,
                    'category': category_title.strip()
                }
    return titles_dict


def extract_title_from_notebook(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_content = json.load(f)
    title_pattern = re.compile(r'#\s*([a-zA-z]* Tutorial) (\d+): (.*)')
    for cell in notebook_content['cells']:
        if cell['cell_type'] == 'markdown':
            source_text = ''.join(cell['source'])
            match = title_pattern.search(source_text)
            if match:
                return f"{match.group(1).strip()} {match.group(2)}: {match.group(3)}"
    return None


def sort_tutorials(tutorial_list):
    desired_order = ['Beginner Tutorials', 'Advanced Tutorials', 'XAI Tutorials']
    order_map = {category: idx for idx, category in enumerate(desired_order)}
    sorted_list = sorted(tutorial_list, key=lambda x: order_map[next(iter(x))])
    def get_numeric_prefix(title):
        import re
        match = re.search(r'\d+', title)
        return int(match.group()) if match else float('inf')
    for item in sorted_list:
        category = next(iter(item))
        tutorials = item[category]
        tutorials.sort(key=lambda tutorial: get_numeric_prefix(next(iter(tutorial))))
    return sorted_list


def convert_apphub(apphub_path, output_path):
    output_path = os.path.join(output_path, 'apphub')
    readme_path = os.path.join(apphub_path, 'README.md')
    os.makedirs(output_path, exist_ok=True)
    readme_output_path = os.path.join(output_path, 'README.md')
    shutil.copy(readme_path, output_path)
    update_apphub_readme(readme_output_path)
    titles_dict = get_apphub_titles(readme_path)
    apphubs = [{'Overview': os.path.join('apphub', 'README.md')}]
    # apphubs_dict = {}
    # apphubs_dict['Overview'] = os.path.join('apphub', 'README.md')
    categories = []
    for file in glob.glob(f"{apphub_path}/**/*.ipynb", recursive=True):

        file_elem = file.split(os.sep)
        filedir = os.path.join(*file_elem[2:-1])
        # category = file_elem[2]
        filename = file_elem[-1]
        title = titles_dict[filename]['title']
        category = titles_dict[filename]['category']
        # key = filename.split('.')[0]
        if category not in categories:
            if 'apphub_dict' in locals() and len(apphub_dict) != 0:
                apphubs.append(apphub_dict)
            apphub_dict = {}
            apphub_paths = []
            categories.append(category)
        
        filename = os.path.join(filedir, filename)
        apphub_paths.append({title: os.path.join('apphub', filename)})
        apphub_dict[category] = apphub_paths
        apphub_output_path = os.path.join(output_path, filedir)
        os.makedirs(apphub_output_path, exist_ok=True)
        shutil.copy(file, apphub_output_path)
    apphubs.append(apphub_dict)
    return apphubs


def convert_tutorials(tutorial_path, output_path):
    output_path = os.path.join(output_path, 'tutorial')
    os.makedirs(output_path, exist_ok=True)
    tutorials = []
    categories = []
    for file in glob.glob(f"{tutorial_path}/**/*.ipynb", recursive=True):
        file_elem = file.split(os.sep)
        category = file_elem[-2]
        if category == 'advanced':
            category_title = 'Advanced Tutorials'
        elif category == 'beginner':
            category_title = 'Beginner Tutorials'
        elif category == 'xai':
            category_title = 'XAI Tutorials'
        if category_title not in categories:
            if 'tutorial_dict' in locals() and len(tutorial_dict) != 0:
                tutorials.append(tutorial_dict)
            tutorial_dict = {}
            tutorial_dict[category_title] = []
            categories.append(category_title)
        category_output_path = os.path.join(output_path, category)
        os.makedirs(category_output_path, exist_ok=True)
        shutil.copy(file, category_output_path)
        filepath = os.path.join('tutorial', category, file_elem[-1])
        tutorial_title = extract_title_from_notebook(os.path.join('fastestimator', filepath))
        filename = file_elem[-1].split('.')[0]
        tutorial_dict[category_title].append({tutorial_title: filepath})

        # tutorial_dict[filename] = filepath
    tutorials.append(tutorial_dict)
    tutorials.insert(0, tutorials.pop(1))
    resources_dir = os.path.join(tutorial_path, 'resources')
    resources_output_dir = os.path.join(output_path, 'resources')
    os.makedirs(resources_output_dir, exist_ok=True)
    shutil.copytree(resources_dir, resources_output_dir, dirs_exist_ok=True)
    # copy cli tutorials
    cli_tutorial = os.path.join(tutorial_path, 'beginner', 't10_cli.md')
    if os.path.exists(cli_tutorial):
        cli_tutorial_docs = os.path.join(output_path, 'beginner')
        shutil.copy(cli_tutorial, cli_tutorial_docs)
        tutorials[-1]['Beginner Tutorials'].insert(9, {'Tutorial 10: How to use CLI': os.path.join('tutorial', 'beginner', 't10_cli.md')})
    tutorials = sort_tutorials(tutorials)
    return tutorials


def update_mkdocs_yaml(nav):
    with open('mkdocs.yml', 'r') as file:
        config = yaml.load(file, Loader=yaml.Loader)
    config['nav'] = nav
    with open('mkdocs.yml', 'w') as file:
        yaml.dump(config, file, sort_keys=False)


if __name__ == '__main__':
    repo_path = 'fastestimator'
    repo_subdirs = ['fastestimator']
    output_path = 'docs'
    output_folder = 'fastestimator'
    nav = []
    os.makedirs(output_path, exist_ok=True)
    extract_installation_content(os.path.join(repo_path, 'README.md'), output_path)
    nav.append({'Home': 'index.md'})
    nav.append({'Install': 'installation.md'})
    os.makedirs(output_path, exist_ok=True)
    apphubs_dict = convert_apphub(os.path.join(repo_path, 'apphub'), output_path)
    tutorial_dict = convert_tutorials(os.path.join(repo_path, 'tutorial'), output_path)
    nav.append({'Apphubs': apphubs_dict})
    nav.append({'Tutorials': tutorial_dict})
    for subdir in repo_subdirs:
        repo_subdir = os.path.join(repo_path, subdir)
        doc_output_path = os.path.join(output_path, subdir)
        d = create_doc_structure(repo_subdir, doc_output_path, output_path)
        nav.append(d)
        update_mkdocs_yaml(nav)
