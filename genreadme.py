"""
Generate readme table using info from json
"""
import argparse
import os
import json


def longest_str_len(items, key):
    values = [len(item.get(key, '')) for item in items] + [len(key)]
    return max(*values)


def table_row(info, col_name=20, col_status=20, col_description=60, col_authors=60):
    tmpl = f"| {{name:{col_name}}} | {{status:{col_status}}} | {{description:{col_description}}} | {{authors:{col_authors}}} |"

    return tmpl.format(
        name=info.get('name', ''),
        status=info.get('status', ''),
        description=info.get('description', ''),
        authors=info.get('authors', '')
    )


def main(args):
    infos = []

    for root, folders, files in os.walk(args.folder):
        for folder in folders:
            info_path = os.path.join(root, folder, "info.json")
            if not os.path.exists(info_path):
                continue

            with open(info_path) as f:
                data = json.load(f)

            description = "<details><summary>{short}</summary>{long}</details>".format(
                short=data.get('short'),
                long=data.get('description'),
            )

            info = dict(
                name=folder,
                status="",
                description=description,
                authors=', '.join(data.get('author', []))
            )

            infos.append(info)

    infos = sorted(infos, key=lambda x: x.get('name', '').lower())
    col_name = longest_str_len(infos, 'name')
    col_status = 20
    col_description = longest_str_len(infos, 'description')
    col_authors = longest_str_len(infos, 'authors')

    table_head = table_row(
        dict(
            name="Name",
            status="Status",
            description="Description",
            authors="Author(s)",
        ),
        col_name=col_name,
        col_status=col_status,
        col_description=col_description,
        col_authors=col_authors
    )

    table_div = f"| {'-' * (col_name)} | {'-' * (col_status)} | {'-' * (col_description)} | {'-' * (col_authors)} |"

    rows = [
        table_row(
            info,
            col_name=col_name,
            col_status=col_status,
            col_description=col_description,
            col_authors=col_authors
        ) for info in infos
    ]

    print(table_head)
    print(table_div)
    print('\n'.join(rows))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate Readme table for Red Disocrd Bot cogs")

    parser.add_argument('folder', help="location of the repo")

    args = parser.parse_args()
    main(args)
